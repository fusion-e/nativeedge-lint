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
                               next.start_mark.column,
                               max_desc,
                               fixable=True)
        elif min != - 1 and spaces < min:
            return LintProblem(token.start_mark.line + 1,
                               next.start_mark.column + 1,
                               min_desc,
                               fixable=True)


def spaces_before(token, prev, next, min=-1, max=-1,
                  min_desc=None, max_desc=None):
    if (prev is not None and prev.end_mark.line == token.start_mark.line and
            # Discard tokens (only scalars?) that end at the start of next line
            (prev.end_mark.pointer == 0 or
             prev.end_mark.buffer[prev.end_mark.pointer - 1] != '\n')):
        spaces = token.start_mark.pointer - prev.end_mark.pointer
        if max != - 1 and spaces > max:
            return LintProblem(token.start_mark.line + 1,
                               token.start_mark.column,
                               max_desc,
                               fixable=True)
        elif min != - 1 and spaces < min:
            return LintProblem(token.start_mark.line + 1,
                               token.start_mark.column + 1,
                               min_desc,
                               fixable=True)


class LintProblem(object):
    """Represents a linting problem found by yamllint."""
    def __init__(self,
                 line,
                 column,
                 desc='<no description>',
                 rule=None,
                 file=None,
                 token=None,
                 start_mark=None,
                 end_mark=None,
                 next=None,
                 prev=None,
                 nextnext=None,
                 fixable=None):
        #: Line on which the problem was found (starting at 1)
        self._line = line
        #: Column on which the problem was found (starting at 1)
        self.column = column or 0
        #: Human-readable description of the problem
        self._desc = desc
        #: Identifier of the rule that detected the problem
        self.rule = rule
        self.level = None
        self._file = file
        self._token = token
        self._start_mark = start_mark
        self._end_mark = end_mark
        self._next = next
        self._prev = prev
        self._nextnext = nextnext
        self._fixed = False
        self._fixes = []
        self._fix = False
        self._fixable = fixable
        self._update_line = None

    @property
    def line(self):
        if self.update_line:
            return self.update_line
        if self.start_mark and self.end_mark:
            return self.start_mark + 1
        else:
            return self._line

    @line.setter
    def line(self, value):
        self._line = value

    @property
    def update_line(self):
        return self._update_line

    @update_line.setter
    def update_line(self, value):
        self._update_line = value

    @property
    def desc(self):
        if self.fixable:
            return self._desc + " (auto-fix available)"
        else:
            return self._desc + " (auto-fix unavailable)"

    @property
    def fixable(self):
        return self._fixable

    @fixable.setter
    def fixable(self, value):
        self._fixable = value

    @property
    def fixes(self):
        return self._fixes

    @fixes.setter
    def fixes(self, value):
        self._fixes = value

    @property
    def fix_all(self):
        for fix in self.fixes:
            if fix.line == -1 and fix.rule == 'all':
                return True
        return False

    @property
    def fix(self):
        for fix in self.fixes:
            if fix.line == -1 and fix.rule == 'all':
                return True
            elif fix.line == self.line and fix.rule == self.rule:
                return True
        return False

    @property
    def fix_new_lines(self):
        for fix in self.fixes:
            if fix.rule == 'empty-lines':
                return True
        return False

    @property
    def fixed(self):
        return self._fixed

    @fixed.setter
    def fixed(self, value):
        self._fixed = value

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

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    @property
    def start_mark(self):
        return self._start_mark

    @start_mark.setter
    def start_mark(self, value):
        self._start_mark = value

    @property
    def end_mark(self):
        return self._end_mark

    @end_mark.setter
    def end_mark(self, value):
        self._end_mark = value

    @property
    def nextnext(self):
        return self._nextnext

    @nextnext.setter
    def nextnext(self, value):
        self._nextnext = value

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, value):
        self._prev = value


def get_syntax_error(buffer):
    try:
        list(yaml.parse(buffer, Loader=yaml.BaseLoader))
    except yaml.error.MarkedYAMLError as e:
        problem = LintProblem(e.problem_mark.line + 1,
                              e.problem_mark.column + 1,
                              'syntax error: ' + e.problem + ' (syntax)')
        problem.level = 'error'
        return problem
