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


def fix_spaces_in_brackets(problem):
    if problem.rule in ['brackets', 'braces'] and \
            'too many spaces inside ' in problem.message:
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            if problem.rule == 'braces':
                new_line = re.sub(r'{\s+', '{ ', line)
                new_line = re.sub(r'\s+}', ' }', new_line)
                lines[problem.line - 1] = new_line
                problem.fixed = True
            elif problem.rule == 'brackets':
                new_line = re.sub(r'\[\s+', '[ ', line)
                new_line = re.sub(r'\s+\]', ' ]', new_line)
                lines[problem.line - 1] = new_line
                problem.fixed = True
