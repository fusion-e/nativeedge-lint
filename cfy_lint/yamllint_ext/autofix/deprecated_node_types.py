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

from cfy_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_deprecated_node_types(problem):
    if problem.rule != 'node_templates':
        return
    if 'deprecated node type' in problem.message:
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            line, eol = get_eol(line)
            split = problem.message.split()
            new_line = line.replace(split[-5], split[-3].rstrip('.'))
            lines[problem.line - 1] = new_line + eol
        problem.fixed = True
    if 'has deprecated property' in problem.message:
        words = problem.message.split()
        pattern = re.compile('(azure|aws|gcp)_config')
        target = words[-6].replace('"', '').replace('.', '') + ":"
        if not pattern.search(target):
            return
        line_number = problem.line - 1
        with filelines(problem.file) as lines:
            while target not in lines[line_number]:
                line_number += 1
            line = lines[line_number]
            line, eol = get_eol(line)
            new_line = re.sub(target, "client_config:", line)
            lines[line_number] = new_line + eol
        problem.fixed = True
