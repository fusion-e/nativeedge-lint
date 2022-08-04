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

import yaml


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


class LintProblem(object):
    """Represents a linting problem found by yamllint."""
    def __init__(self, line, column, desc='<no description>', rule=None):
        #: Line on which the problem was found (starting at 1)
        self.line = line
        #: Column on which the problem was found (starting at 1)
        self.column = column or 0
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


def get_syntax_error(buffer):
    try:
        list(yaml.parse(buffer, Loader=yaml.BaseLoader))
    except yaml.error.MarkedYAMLError as e:
        problem = LintProblem(e.problem_mark.line + 1,
                              e.problem_mark.column + 1,
                              'syntax error: ' + e.problem + ' (syntax)')
        problem.level = 'error'
        return problem
