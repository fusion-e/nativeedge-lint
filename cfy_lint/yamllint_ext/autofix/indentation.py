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
from cfy_lint.yamllint_ext.autofix.utils import (filelines, get_indented_regex)


def fix_indentation(problem):
    if problem.rule == 'indentation':
        with filelines(problem.file) as lines:
            expected, found = get_space_diff(problem.desc)
            indented_regex = get_indented_regex(
                lines[problem.line - 1], len(found))
            idx = problem.line - 1
            while True:
                if idx == len(lines) or not indented_regex.match(lines[idx]):
                    break
                lines[idx] = replace_spaces(expected, found, lines[idx])
                idx += 1
                continue


def replace_spaces(expected, found, line):
    sans_newline = line.rstrip()
    new_line = sans_newline.replace(found, expected)
    print('Old line {}.'.format(sans_newline))
    print('New line {}.'.format(new_line))
    if sans_newline != line:
        new_line += '\n'
    return new_line


def get_space_diff(message):
    """Get the indentation that exists, and what we want to replace it with.
    :param message: The string message that we have in problem.desc
    :return: (found, desired)
    """
    found_expect = re.findall(r'\d+', message)
    if isinstance(found_expect, list) and len(found_expect) == 2:
        return int(found_expect[0]) * ' ', int(found_expect[1]) * ' '
    return 0, 0
