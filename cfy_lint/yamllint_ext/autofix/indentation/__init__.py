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

import sys

from cfy_lint.yamllint_ext.autofix.utils import filelines
from cfy_lint.yamllint_ext.autofix.indentation.utils import (
    get_yaml_dict,
    get_file_content,
    filter_corrections,
    get_compare_file_content,
    indentify_indentation_corrections
)


def fix_indentation(problem):
    if problem.rule == 'indentation':
        with filelines(problem.file) as lines:
            original = get_file_content(problem.file)
            compare = get_compare_file_content(get_yaml_dict(problem.file))
            corrections = filter_corrections(
                indentify_indentation_corrections(original, compare),
                problem.line)
            for line, correction in sorted(corrections.items()):
                if line == -1:
                    print('Unable to autofix indentation for line {}. '
                          'Unsupported YAML.'.format(problem.line))
                    sys.exit(1)
                lines[line - 1] = correction['new']
            problem.fixed = True
