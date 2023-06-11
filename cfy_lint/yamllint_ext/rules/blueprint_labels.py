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

from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    recurse_get_readable_object
    )

VALUES = []

ID = 'blueprint_labels'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['blueprint_labels', 'blueprint-labels'])
def check(token=None, **_):
    if token.prev.node.value == 'blueprint-labels':
        yield LintProblem(
                token.prev.line,
                None,
                'The blueprint_labels key should be written '
                'with an underscore not a dash.')
    for item in token.node.value:
        d = recurse_get_readable_object(item)
        if not isinstance(d, dict):
            yield LintProblem(
                token.line,
                None,
                'blueprint_labels contains nested dictionaries')
        for key, value in d.items():
            if not isinstance(value, dict):
                yield LintProblem(
                    token.line,
                    None,
                    'Every label should be a dictionary')
            else:
                for key, value in value.items():
                    if key != 'values':
                        yield LintProblem(
                            token.line,
                            None,
                            'The name of the key should be "values"')
                    if not isinstance(value, list):
                        yield LintProblem(
                            token.line,
                            None,
                            'The value of the "values" is should be a list')
