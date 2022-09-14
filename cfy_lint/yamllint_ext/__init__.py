########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

from yamllint import parser
from .generators import (
    CfyNode,
    CfyToken,
    token_or_comment_or_line_generator,
)
from .overrides import (
    LintProblem,
    spaces_after,
    spaces_before,
    get_syntax_error
)
from .utils import (
    context,
    setup_types,
    update_model,
    setup_node_templates,
)

PROBLEM_LEVELS = {
    0: None,
    1: 'warning',
    2: 'error',
    None: 0,
    'warning': 1,
    'error': 2,
}


def get_cosmetic_problems(buffer, conf, filepath, base_path=None):

    setup_types(buffer, base_path=base_path)

    rules = conf.enabled_rules(filepath)

    # Split token rules from line rules
    token_rules = [r for r in rules if r.TYPE == 'token']
    comment_rules = [r for r in rules if r.TYPE == 'comment']
    line_rules = [r for r in rules if r.TYPE == 'line']

    for rule in token_rules:
        context[rule.ID] = {}

    class DisableDirective:
        def __init__(self):
            self.rules = set()
            self.all_rules = {r.ID for r in rules}

        def process_comment(self, comment):
            try:
                comment = str(comment)
            except UnicodeError:
                return  # this certainly wasn't a yamllint directive comment

            if re.match(r'^# yamllint disable( rule:\S+)*\s*$', comment):
                items = comment[18:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

            elif re.match(r'^# yamllint enable( rule:\S+)*\s*$', comment):
                items = comment[17:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules.clear()
                else:
                    for id in rules:
                        self.rules.discard(id)

        def is_disabled_by_directive(self, problem):
            return problem.rule in self.rules

    class DisableLineDirective(DisableDirective):
        def process_comment(self, comment):
            try:
                comment = str(comment)
            except UnicodeError:
                return  # this certainly wasn't a yamllint directive comment

            if re.match(r'^# yamllint disable-line( rule:\S+)*\s*$', comment):
                items = comment[23:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

    # Use a cache to store problems and flush it only when a end of line is
    # found. This allows the use of yamllint directive to disable some rules on
    # some lines.
    cache = []
    disabled = DisableDirective()
    disabled_for_line = DisableLineDirective()
    disabled_for_next_line = DisableLineDirective()

    for elem in token_or_comment_or_line_generator(buffer):

        if isinstance(elem, CfyNode):
            setup_node_templates(elem)
            for rule in token_rules:
                rule_conf = conf.rules[rule.ID]
                try:
                    problems = rule.check(
                        conf=rule_conf,
                        token=elem,
                        context=context[rule.ID],
                        node_types=context.get('imported_node_types', {}))
                except TypeError:
                    continue
                else:
                    for problem in problems:
                        problem.rule = rule.ID
                        problem.level = rule_conf['level']
                        cache.append(problem)

        elif isinstance(elem, CfyToken):
            update_model(elem)
            for rule in token_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                problems = rule.check(rule_conf,
                                      elem.curr,
                                      elem.prev,
                                      elem.after,
                                      elem.nextnext,
                                      context[rule.ID])
                for problem in problems:
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

        elif isinstance(elem, parser.Comment):
            for rule in comment_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

            disabled.process_comment(elem)
            if elem.is_inline():
                disabled_for_line.process_comment(elem)
            else:
                disabled_for_next_line.process_comment(elem)

        elif isinstance(elem, parser.Line):
            for rule in line_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

        # This is the last token/comment/line of this line, let's flush the
        # problems found (but filter them according to the directives)
        for problem in cache:
            if not (disabled_for_line.is_disabled_by_directive(problem) or
                    disabled.is_disabled_by_directive(problem)):
                yield problem

        disabled_for_line = disabled_for_next_line
        disabled_for_next_line = DisableLineDirective()
        cache = []


def _run(buffer, conf, filepath, base_path=None):
    assert hasattr(buffer, '__getitem__'), \
        '_run() argument must be a buffer, not a stream'

    first_line = next(parser.line_generator(buffer)).content
    if re.match(r'^#\s*yamllint disable-file\s*$', first_line):
        return

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    problems = list(get_cosmetic_problems(buffer, conf, filepath, base_path))

    for problem in sorted(problems, key=lambda x: x.line):
        # Insert the syntax error (if any) at the right place...
        if (syntax_error and syntax_error.line <= problem.line and
                syntax_error.column <= problem.column):
            yield syntax_error

            # If there is already a yamllint error at the same place, discard
            # it as it is probably redundant (and maybe it's just a 'warning',
            # in which case the script won't even exit with a failure status).
            if (syntax_error.line == problem.line and
                    syntax_error.column == problem.column):
                syntax_error = None
                continue

            syntax_error = None

        yield problem

    if syntax_error:
        yield syntax_error


def run(input, conf, filepath=None):
    """Lints a YAML source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: yamllint configuration object
    """
    if conf.is_file_ignored(filepath):
        return ()

    base_path = os.path.dirname(os.path.abspath(input.name))

    if isinstance(input, (bytes, str)):
        base_path = os.path.dirname(os.path.abspath(input.name))
        return _run(input, conf, filepath, base_path=base_path)
    elif hasattr(input, 'read'):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _run(content, conf, filepath, base_path=base_path)
    else:
        raise TypeError('input should be a string or a stream')
