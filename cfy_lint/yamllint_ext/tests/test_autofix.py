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
from tempfile import NamedTemporaryFile

from cfy_lint.yamllint_ext import autofix
from cfy_lint.yamllint_ext.autofix import utils
from cfy_lint.yamllint_ext.autofix import indentation
from cfy_lint.yamllint_ext.overrides import LintProblem
from cfy_lint.yamllint_ext.autofix import trailing_spaces


def test_get_space_diff():
    messages = [
        "wrong indentation: expected 10 but found 12",
        "wrong indentation: expected 6 but found 7",
    ]

    assert indentation.get_space_diff(messages[0]) == (10 * ' ', 12 * ' ')
    assert indentation.get_space_diff(messages[1]) == (6 * ' ', 7 * ' ')


def test_get_indented_regex():
    lines = [
        '    - foo',
        '      bar'
    ]
    assert utils.get_indented_regex(
        lines[0], 4) == re.compile(r'^\s{4}[\-\s{1}A-Za-z]')
    assert utils.get_indented_regex(
        lines[1], 4) == re.compile(r'^\s{4}[A-Za-z]')


def get_file(lines):
    fix_truthy_file = NamedTemporaryFile(delete=False)
    f = open(fix_truthy_file.name, 'w')
    f.writelines(lines)
    f.close()
    return f


def test_fix_indentation():
    lines = [
        'foobar:\n',
        '      - foo\n',
        '      - bar\n',
    ]
    expected = [
        'foobar:\n',
        '  - foo\n',
        '  - bar\n',
    ]
    fix_indentation_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='wrong indentation: expected 2 but found 6',
                rule='indentation',
                file=fix_indentation_file.name
            )
            indentation.fix_indentation(problem)
    finally:
        f = open(fix_indentation_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_indentation_file.name)
    assert expected == result_lines


def test_trailing_spaces():
    lines = [
        'They wanna get my      \n',
        'They wanna get my gold on the ceiling      \n',
        "I ain't blind, just a matter of time     \n",
        'Before you steal it         \n',
        "Its all right, ain't no guarding my high      \n"
    ]
    expected_lines = [
        'They wanna get my\n',
        'They wanna get my gold on the ceiling\n',
        "I ain't blind, just a matter of time\n",
        'Before you steal it\n',
        "Its all right, ain't no guarding my high\n"
    ]
    fix_trailing_spaces_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='foo',
                rule='trailing-spaces',
                file=fix_trailing_spaces_file.name
            )
            trailing_spaces.fix_trailing_spaces(problem)
    finally:
        f = open(fix_trailing_spaces_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_trailing_spaces_file.name)
    assert result_lines == expected_lines


def test_fix_truthy():
    lines = [
        '\n',
        'True, not everything is tRue.\n'
        'And if I say TRUE to you!\n',
        'true TruE TRue TrUE truE\n',
        'False falSe FalsE FALSE false,\n',
        '     "False"      "falsE"\n',
        '\n',
    ]
    expected_lines = [
        '\n',
        'True, not everything is tRue.\n',
        'And if I say true to you!\n',
        'true true true true true\n',
        'false false false false false,\n',
        '     "False"      "falsE"\n',
        '\n'
    ]
    fix_truthy_file = get_file(lines)
    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i + 1,
                column=0,
                desc='foo',
                rule='truthy',
                file=fix_truthy_file.name
            )
            autofix.fix_truthy(problem)
    finally:
        f = open(fix_truthy_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_truthy_file.name)
    assert result_lines == expected_lines
