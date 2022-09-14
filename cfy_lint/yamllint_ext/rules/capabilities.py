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
from ..utils import process_relevant_tokens, recurse_mapping, context as ctx

VALUES = []

ID = 'capabilities'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['outputs', 'capabilities'])
def check(token=None, **_):
    for item in token.node.value:
        if token.prev.node.value == 'outputs':
            output_obj = CfyOutput(item)
            if not output_obj.name and not output_obj.mapping:
                continue
        elif token.prev.node.value == 'capabilities':
            output_obj = CfyCapability(item)
        if output_obj.not_output():
            continue
        if isinstance(output_obj, CfyOutput):
            ctx['outputs'].update(output_obj.__dict__())
        else:
            ctx['capabilities'].update(output_obj.__dict__())
        desig = 'output' if token.prev.node.value == 'outputs' \
            else 'capability'
        if not output_obj.value:
            yield LintProblem(
                token.line, None,
                '{} {} does not provide a value.'.format(
                    desig, output_obj.name)
            )
        if not output_obj.description:
            yield LintProblem(
                token.line, None,
                '{} {} does not provide a description.'.format(
                    desig, output_obj.name)
            )


class CfyOutput(object):
    def __init__(self, nodes):
        self.name, self.mapping = self.get_name_mapping(nodes)
        if self.name and self.mapping:
            for key in list(self.mapping.keys()):
                if key not in ['description', 'value']:
                    del self.mapping[key]
            self.value = self.mapping.get('value')
            self.description = self.mapping.get('description')

    def get_name_mapping(self, nodes):
        return get_output(nodes)

    def not_output(self):
        return all([not k for k in self.mapping.values()])

    def __dict__(self):
        return {
            self.name: self.mapping
        }


class CfyCapability(CfyOutput):

    def get_name_mapping(self, nodes):
        return get_capability(nodes)

    def not_capability(self):
        return all([not k for k in self.mapping.values()])


def get_capability(nodes):
    if len(nodes) != 2:
        name = None
        mapping = None
    else:
        name = get_node_name(nodes[0])
        mapping = get_capability_mapping(nodes[1])
    return name, mapping


def get_output(nodes):
    if len(nodes) != 2:
        name = None
        mapping = None
    else:
        name = get_node_name(nodes[0])
        mapping = get_capability_mapping(nodes[1])
    return name, mapping


def get_node_name(node):
    if isinstance(node, yaml.nodes.ScalarNode):
        return node.value


def get_capability_mapping(node):
    mapping = {
        'description': None,
        'value': None,
    }
    if isinstance(node, yaml.nodes.MappingNode):
        for tup in node.value:
            if not len(tup) == 2:
                continue
            mapping_name = tup[0].value
            mapping_value = get_mapping_value(mapping_name, tup[1].value)
            mapping[mapping_name] = mapping_value
    return mapping


def get_mapping_value(name, value):
    if name not in ['value']:
        return value
    else:
        return recurse_mapping(value)
