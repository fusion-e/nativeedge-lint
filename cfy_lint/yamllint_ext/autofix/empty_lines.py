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

from cfy_lint.yamllint_ext.utils import context
from cfy_lint.yamllint_ext.autofix.utils import filelines

PATTERN = "^ *\n"


def fix_empty_lines(problem):
    if problem.fix_all or problem.fix_new_lines:
        with filelines(problem.file) as lines:
            successive_blank_lines = 0
            deleted_lines = 0
            index = 0
            current_sum = 0
            keys = []
            context['line_diff'][0] = 0

            # remove blanklines from start of file
            while re.match(PATTERN, lines[0]):
                lines.pop(0)

            while index < (len(lines) - 1):
                line = lines.pop(index)

                if re.match(PATTERN, line):
                    successive_blank_lines -= 1
                    if successive_blank_lines <= -2:
                        continue
                else:
                    if successive_blank_lines < -1:
                        current_sum += successive_blank_lines + 1
                        context['line_diff'][index + deleted_lines] = \
                            current_sum
                        deleted_lines -= successive_blank_lines + 1
                        keys.append(index)
                    successive_blank_lines = 0

                lines.insert(index, line)
                index += 1

            # remove blanklines from end of file
            while re.match(PATTERN, lines[-1]):
                lines.pop(-1)
