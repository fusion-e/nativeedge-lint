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

from cfy_lint.yamllint_ext.autofix.truthy import fix_truthy
from cfy_lint.yamllint_ext.autofix.indentation import fix_indentation
from cfy_lint.yamllint_ext.autofix.trailing_spaces import fix_trailing_spaces
from cfy_lint.yamllint_ext.autofix.deprecated_node_types import \
    fix_deprecated_node_types
from cfy_lint.yamllint_ext.autofix.deprecated_relationships import \
    fix_deprecated_relationships


def fix_problem(problem):
    if problem.file or problem.line:
        fix_truthy(problem)
        fix_indentation(problem)
        fix_trailing_spaces(problem)
        fix_deprecated_node_types(problem)
        fix_deprecated_relationships(problem)
