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

from cfy_lint.yamllint_ext.autofix.utils import filelines


def fix_add_label(problems):
    counter = 0
    for problem in problems:
        if problem.rule == 'inputs' and ' is missing a display_label.' in \
                problem.message:
            with filelines(problem.file) as lines:
                line = lines[problem.line - 1 + counter]
                line = line.rstrip()
                line = line.rstrip(':')
                line = line.lstrip()
                line = line.replace('_', ' ')
                line = line.title()
                line = "    display_label: '{}'\n".format(line)
                lines.insert(problem.line + counter, line)
                counter += 1
