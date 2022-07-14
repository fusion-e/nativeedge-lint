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

from .. import LintProblem

from ..generators import CfyNode
from ..utils import process_relevant_tokens

VALUES = []

ID = 'node_types'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, 'node_types')
def check(token=None, **_):
    for node_type in token.node.value:
        yield from node_type_follows_naming_conventions(
            node_type[0].value, token.line)


def node_type_follows_naming_conventions(value, line):
    split_node_type = value.split('.')
    last_key = split_node_type.pop()
    if not {'cloudify', 'nodes'} <= set(split_node_type):
        yield LintProblem(
            line,
            None,
            "node types should following naming convention cloudify.nodes.*: "
            "{}".format(value))
    if not good_camel_case(last_key, split_node_type):
        new_value = '.'.join(
            [k.lower() for k in split_node_type]) + '.{}'.format(last_key)
        yield LintProblem(
            line,
            None,
            "incorrect camel case {}. Suggested: {} ".format(value, new_value))


def good_camel_case(last_key, split_node_type):
    if not last_key[0].isupper():
        return False
    for key in split_node_type:
        if key[0].isupper():
            return False
    return True
