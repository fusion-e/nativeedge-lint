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


def fix_empty_lines(problem):
    # The dictionary context['fix_error_empty_line']
    # indicated which lines were deleted

    if problem.fix_all or problem.fix_new_lines:
        with filelines(problem.file) as lines:
            blank_lines = 0
            deleted_lines = 0
            index = 0
            pattern = "^ *\n"
            while re.match(pattern, lines[0]):
                lines.pop(0)

            while index < (len(lines)):
                line = lines.pop(index)
                if re.match(pattern, line):
                    blank_lines += 1
                    if blank_lines >= 2:
                        continue
                else:
                    if blank_lines > 1:
                        if context['fix_error_empty_line']:
                            deleted_lines += blank_lines - 1
                        i = index + blank_lines + deleted_lines
                        context['fix_error_empty_line'][i] = blank_lines - 1
                    blank_lines = 0

                lines.insert(index, line)
                index += 1

            while re.match(pattern, lines[-1]):
                lines.pop(-1)
