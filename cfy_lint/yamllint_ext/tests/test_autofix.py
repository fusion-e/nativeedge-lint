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

import os
from tempfile import NamedTemporaryFile

from cfy_lint.yamllint_ext.autofix import fix_truthy
from cfy_lint.yamllint_ext.overrides import LintProblem


def test_fix_truthy():
    lines = [
        'True, not everything is tRue.\n'
        'And if I say TRUE to you!\n',
        'true TruE TRue TrUE truE\n',
        'False falSe FalsE FALSE false,\n',
        '     "False"      "falsE"\n'
    ]
    expected_lines = [
        'True, not everything is tRue.\n',
        'And if I say true to you!\n',
        'true true true true true\n',
        'false false false false false,\n',
        '     "False"      "falsE"\n'
    ]
    fix_truthy_file = NamedTemporaryFile()
    f = open(fix_truthy_file.name, 'w')
    f.writelines(lines)
    f.close()

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='foo',
                rule='truthy',
                file=fix_truthy_file.name
            )
            fix_truthy(problem)
    finally:
        f = open(fix_truthy_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_truthy_file.name)

    assert result_lines == expected_lines
