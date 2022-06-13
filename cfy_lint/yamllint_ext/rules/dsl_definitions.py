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

import yaml

from .. import LintProblem

from ..generators import CfyNode

VALUES = []

ID = 'dsl_definitions'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


def check(conf=None,
          token=None,
          prev=None,
          next=None,
          nextnext=None,
          context=None):
    if isinstance(token, CfyNode):
        line = token.node.start_mark.line + 1
        if not token.prev or not token.prev.node.value == 'dsl_definitions':
            return
        for dsl_definition in token.node.value:
            if not isinstance(dsl_definition[0].value, str) or \
                    dsl_definition[0].value.isdigit():
                yield LintProblem(
                    line,
                    None,
                    'dsl definition should be a string and '
                    'should not start with a numeric character: {}'
                    .format(dsl_definition[0].value)
                )
            if not isinstance(dsl_definition[1], yaml.nodes.MappingNode):
                yield LintProblem(
                    line,
                    None,
                    'dsl definition {} content must be a dict: {}'
                    .format(dsl_definition[0].value,
                            type(dsl_definition[1].value))
                )
