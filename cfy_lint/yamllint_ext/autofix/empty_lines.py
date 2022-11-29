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

from cfy_lint.yamllint_ext.autofix.utils import filelines


def fix_empty_lines(problem):
    with filelines(problem.file) as lines:
        successive_blank_lines = 0
        index = 0
        pattern = "^ *\n"
        while re.match(pattern, lines[0]):
            lines.pop(0)

        while index < (len(lines)):
            line = lines.pop(index)
            if re.match(pattern, line):
                successive_blank_lines += 1
                if successive_blank_lines >= 2:
                    continue
            else:
                successive_blank_lines = 0
            lines.insert(index, line)
            index += 1

        while re.match(pattern, lines[-1]):
            lines.pop(-1)
