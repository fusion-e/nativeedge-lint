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


def fix_deprecated_node_types(problem):
    if problem.rule == 'node_templates' and \
            'deprecated node type' in problem.message:
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            line = line.rstrip()
            print('line = {}'.format(line))

            split = problem.message.split()
            new_line = line.replace(split[-3], split[-1].rstrip('.'))
            print('line num = {}'.format(problem.line))
            print('message = {}'.format(problem.message))
            print('line = {}'.format(line))
            print('split = {}'.format(split))
            print('-3 = {}'.format(split[-3]))
            print('-1 = {}'.format(split[-1]))
            print('new_line = {}'.format(new_line))
            lines[problem.line - 1] = new_line + '\n'
