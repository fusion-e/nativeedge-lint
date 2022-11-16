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

from contextlib import contextmanager

TRUE_PATTERN = 'TRUE'
FALSE_PATTERN = 'FALSE'
TRUE_REPLACEMENT = 'true'
FALSE_REPLACEMENT = 'false'


@contextmanager
def filelines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    yield lines
    with open(filename, 'w') as file:
        file.writelines(lines)


def fix_problem(problem):
    if problem.file or problem.line:
        fix_truthy(problem)


def fix_truthy(problem):
    if problem.rule == 'truthy':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            line = replace_words(line, TRUE_PATTERN, TRUE_REPLACEMENT)
            line = replace_words(line, FALSE_PATTERN, FALSE_REPLACEMENT)
            lines[problem.line - 1] = line


def replace_words(line, pattern, replacement):
    words = line.split(' ')
    new_words = []
    for word in words:
        if word.upper().strip() == pattern:
            if word.endswith('\n'):
                word = word.lstrip()
                print('Replacing {} with {}.'.format(
                    word.strip(), replacement))
                word = word.upper().replace(pattern, replacement)
            else:
                print('Replacing {} with {}.'.format(word, replacement))
                word = word.upper().replace(pattern, replacement)
        new_words.append(word)
    return ' '.join(new_words)
