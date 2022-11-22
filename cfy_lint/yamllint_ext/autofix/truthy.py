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

from cfy_lint.logger import logger
from cfy_lint.yamllint_ext.autofix.utils import filelines

TRUE_PATTERN = 'TRUE'
FALSE_PATTERN = 'FALSE'
TRUE_REPLACEMENT = 'true'
FALSE_REPLACEMENT = 'false'


def fix_truthy(problem):
    if problem.rule == 'truthy':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            line = replace_words(line, TRUE_PATTERN, TRUE_REPLACEMENT)
            line = replace_words(line, FALSE_PATTERN, FALSE_REPLACEMENT)
            lines[problem.line - 1] = line


def replace_words(line, pattern, replacement):
    clean_line = line.rstrip()
    new_words = []
    for word in clean_line.split(' '):
        if word.upper() == pattern:
            logger.debug('Replacing {} with {}.'.format(word, replacement))
            word = word.upper().replace(pattern, replacement)
        new_words.append(word)
    if clean_line != line:
        new_words[-1] += '\n'
    return ' '.join(new_words)
