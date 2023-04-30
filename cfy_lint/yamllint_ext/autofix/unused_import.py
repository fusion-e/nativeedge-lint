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

TYP = 'imports'
MSG = r' unused import item'


def fix_unused_import(problems):
    for problem in reversed(problems):
        if problem.rule == TYP and re.search(MSG, problem.message):
            with filelines(problem.file) as lines:
                lines.pop(problem.line - 1)
