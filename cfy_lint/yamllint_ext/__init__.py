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

import re
import yaml

from yamllint import parser
from yamllint.parser import (
    Token,
    line_generator,
    comments_between_tokens)

from .constants import (BLUEPRINT_MODEL, NODE_TEMPLATE_MODEL)

PROBLEM_LEVELS = {
    0: None,
    1: 'warning',
    2: 'error',
    None: 0,
    'warning': 1,
    'error': 2,
}

context = {}


class LintProblem(object):
    """Represents a linting problem found by yamllint."""
    def __init__(self, line, column, desc='<no description>', rule=None):
        #: Line on which the problem was found (starting at 1)
        self.line = line
        #: Column on which the problem was found (starting at 1)
        self.column = column
        #: Human-readable description of the problem
        self.desc = desc
        #: Identifier of the rule that detected the problem
        self.rule = rule
        self.level = None

    @property
    def message(self):
        if self.rule is not None:
            return '({}): {}'.format(self.rule, self.desc)
        return self.desc

    def __eq__(self, other):
        return (self.line == other.line and
                self.column == other.column and
                self.rule == other.rule)

    def __lt__(self, other):
        return (self.line < other.line or
                (self.line == other.line and self.column < other.column))

    def __repr__(self):
        return '%d:%d: %s' % (self.line, self.column, self.message)


def get_cosmetic_problems(buffer, conf, filepath):
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
        if isinstance(elem, CfyToken):
            # elem = CfyToken.from_token(token=elem)
            update_model(elem)
            for rule in token_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                context[rule.ID]['node_template_level'] = context.get(
                    'node_template_level')
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf,
                                          elem.curr,
                                          elem.prev,
                                          elem.after,
                                          elem.nextnext,
                                          context[rule.ID]):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    build_string_from_stack(elem.stack, elem.prev, elem.curr)
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


def get_syntax_error(buffer):
    try:
        list(yaml.parse(buffer, Loader=yaml.BaseLoader))
    except yaml.error.MarkedYAMLError as e:
        problem = LintProblem(e.problem_mark.line + 1,
                              e.problem_mark.column + 1,
                              'syntax error: ' + e.problem + ' (syntax)')
        problem.level = 'error'
        return problem


def _run(buffer, conf, filepath):
    assert hasattr(buffer, '__getitem__'), \
        '_run() argument must be a buffer, not a stream'

    first_line = next(parser.line_generator(buffer)).content
    if re.match(r'^#\s*yamllint disable-file\s*$', first_line):
        return

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    for problem in get_cosmetic_problems(buffer, conf, filepath):
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

    if isinstance(input, (bytes, str)):
        return _run(input, conf, filepath)
    elif hasattr(input, 'read'):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _run(content, conf, filepath)
    else:
        raise TypeError('input should be a string or a stream')


def assign_current_top_level(elem):
    if isinstance(elem.curr, yaml.tokens.ScalarToken) and \
            elem.curr.value in BLUEPRINT_MODEL and \
            isinstance(elem.nextnext,
                       yaml.tokens.BlockMappingStartToken):
        return elem.curr.value
    elif isinstance(elem.curr, yaml.tokens.BlockEndToken) and \
            isinstance(elem.nextnext, yaml.tokens.ScalarToken) and \
            elem.nextnext.value in BLUEPRINT_MODEL:
        return ''


def assign_nested_node_template_level(elem):
    if not isinstance(elem.curr, yaml.tokens.ScalarToken):
        return
    if elem.curr.value not in NODE_TEMPLATE_MODEL:
        return
    if isinstance(elem.nextnext, (yaml.tokens.BlockMappingStartToken,
                                  yaml.tokens.BlockEntryToken)):
        return elem.curr.value


def update_model(_elem):
    """Tracking a Cloudify Model inside YAMLLINT context.

    :param _elem:
    :return:
    """
    if stop_document(_elem):
        # The document is finished.
        return
    # We are in the middle of the document.
    top_level = assign_current_top_level(_elem)
    node_template(_elem)
    if skip_inputs_in_node_templates(_elem):
        return
    elif isinstance(top_level, str):
        context['current_top_level'] = top_level  # noqa


def stop_document(_elem):
    if isinstance(_elem.curr, yaml.tokens.StreamStartToken):
        # This is the start of the YAML document.
        context['model'] = BLUEPRINT_MODEL
        context['current_top_level'] = None  # noqa
    elif isinstance(_elem.curr, yaml.tokens.StreamEndToken):
        # This is the end of the YAML document.
        del context['model']
        return True
    return False


def node_template(_elem):
    if context.get('current_top_level') == 'node_templates':
        # When we are looking at Node Templates, we may
        nt = assign_nested_node_template_level(_elem)
        if isinstance(nt, str):
            context['node_template_level'] = nt
    else:
        context['node_template_level'] = None


def skip_inputs_in_node_templates(top_level):
    return context.get('current_top_level') == 'node_templates' and \
           top_level == 'inputs'


def token_to_string(token):
    if isinstance(token, yaml.tokens.ValueToken):
        return ': '
    elif isinstance(token, yaml.tokens.ScalarToken):
        return token.value
    elif isinstance(token, yaml.tokens.FlowEntryToken):
        return ', '
    elif isinstance(token, yaml.tokens.FlowMappingEndToken):
        return '} '
    elif isinstance(token, yaml.tokens.FlowMappingStartToken):
        return ' {'
    # elif isinstance(token, yaml.tokens.BlockMappingStartToken):
    #     string = ' {' + string
    # elif isinstance(token, yaml.tokens.BlockSequenceStartToken):
    #     string = ' ' + string
    elif isinstance(token, yaml.tokens.BlockEntryToken):
        return '-'
    # elif isinstance(token, yaml.tokens.BlockEndToken):
    #     string = '] ' + string


def build_string_from_stack(stack, prev, curr):
    string = ''
    stack.insert(0, prev)
    stack.insert(0, curr)
    index = 0
    while True:
        if index > len(stack):
            break
        token = stack[index]
        if isinstance(token, yaml.tokens.KeyToken):
            inner_index = 0
            while True:
                inner_index += 1
                inner_token = stack[index + inner_index]
                if isinstance(inner_token, yaml.tokens.BlockEndToken):
                    break
            for skipping_index in range(index, index + inner_index):
                converted_token = token_to_string(stack[skipping_index])
                if converted_token:
                    string = converted_token + string
                else:
                    continue
            index = index + inner_index
            continue
        index += 1
        converted_token = token_to_string(token)
        if converted_token:
            string = converted_token + string
        else:
            break
    # print(string)


class CloudifyDSLObject(object):
    pass


class NodeTemplate(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def node_type(self):
        return self.data.get('type', {})

    def properties(self):
        return self.data.get('properties', {})

    def interfaces(self):
        return self.data.get('interfaces', {})

    def relationships(self):
        return self.data.get('relationships', [])


class CfyToken(Token):
    def __init__(self, line_no, curr, prev, after, nextnext, stack):
        super().__init__(line_no, curr, prev, after, nextnext)
        self.after = self.next
        self.stack = stack

    @staticmethod
    def from_token(token):
        return CfyToken(
            token.line_no, token.curr, token.prev, token.next, token.nextnext)


class SafeLineLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def token_or_comment_generator(buffer):
    yaml_loader = SafeLineLoader(buffer)
    # data = yaml_loader.get_data()
    # print(data)

    try:
        stack = []
        prev = None
        curr = yaml_loader.get_token()
        while curr is not None:
            next = yaml_loader.get_token()
            nextnext = (yaml_loader.peek_token()
                        if yaml_loader.check_token() else None)

            yield CfyToken(
                curr.start_mark.line + 1, curr, prev, next, nextnext, stack)

            for comment in comments_between_tokens(curr, next):
                yield comment

            stack.insert(0, prev)
            prev = curr
            curr = next

    except yaml.scanner.ScannerError:
        pass


def generate_node_templates(node_templates):
    for key, value in node_templates.items():
        yield NodeTemplate(key, value)


def cloudify_dsl_generator(buffer):
    yaml_loader = yaml.SafeLoader(buffer)
    data = yaml_loader.get_single_data()
    yield generate_node_templates(data.get('node_templates'))


def token_or_comment_or_line_generator(buffer):
    """Generator that mixes tokens and lines, ordering them by line number"""
    tok_or_com_gen = token_or_comment_generator(buffer)
    line_gen = line_generator(buffer)

    tok_or_com = next(tok_or_com_gen, None)
    line = next(line_gen, None)

    while tok_or_com is not None or line is not None:
        if tok_or_com is None or (line is not None and
                                  tok_or_com.line_no > line.line_no):
            yield line
            line = next(line_gen, None)
        else:
            yield tok_or_com
            tok_or_com = next(tok_or_com_gen, None)

    # yield cloudify_dsl_generator(buffer)


def spaces_after(token, prev, next, min=-1, max=-1,
                 min_desc=None, max_desc=None):
    if next is not None and token.end_mark.line == next.start_mark.line:
        spaces = next.start_mark.pointer - token.end_mark.pointer
        if max != - 1 and spaces > max:
            return LintProblem(token.start_mark.line + 1,
                               next.start_mark.column, max_desc)
        elif min != - 1 and spaces < min:
            return LintProblem(token.start_mark.line + 1,
                               next.start_mark.column + 1, min_desc)


def spaces_before(token, prev, next, min=-1, max=-1,
                  min_desc=None, max_desc=None):
    if (prev is not None and prev.end_mark.line == token.start_mark.line and
            # Discard tokens (only scalars?) that end at the start of next line
            (prev.end_mark.pointer == 0 or
             prev.end_mark.buffer[prev.end_mark.pointer - 1] != '\n')):
        spaces = token.start_mark.pointer - prev.end_mark.pointer
        if max != - 1 and spaces > max:
            return LintProblem(token.start_mark.line + 1,
                               token.start_mark.column, max_desc)
        elif min != - 1 and spaces < min:
            return LintProblem(token.start_mark.line + 1,
                               token.start_mark.column + 1, min_desc)