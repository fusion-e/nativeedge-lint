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
from ..utils import (
    INTRINSIC_FNS,
    recurse_mapping,
    context as ctx, process_relevant_tokens)

VALUES = []

ID = 'inputs'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['inputs', 'get_input'])
def check(token=None, **_):
    if token.prev.node.value == 'inputs':
        for item in token.node.value:
            input_obj = CfyInput(item)
            if input_obj.not_input():
                continue
            ctx['inputs'].update(input_obj.__dict__())
            yield from validate_inputs(input_obj, input_obj.line or token.line)

    if token.prev.node.value == 'get_input':
        if isinstance(token.node.value, list):
            if isinstance(token.node.value[0], yaml.nodes.ScalarNode):
                if token.node.value[0].value not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input {}'
                        .format(token.node.value[0].value))
            if isinstance(token.node.value[0], tuple):
                if token.node.value[0][0] not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input "{}"'.format(token.node.value[0][0]))
        else:
            if token.node.value not in ctx['inputs']:
                yield LintProblem(
                    token.line,
                    None,
                    'undefined input "{}"'.format(token.node.value))


def validate_inputs(input_obj, line):
    if not input_obj.input_type:
        message = 'input "{}" does not specify a type. '.format(input_obj.name)
        if input_obj.default:
            if isinstance(input_obj.default, dict):
                for key in input_obj.default.keys():
                    if key in INTRINSIC_FNS:
                        input_obj.default = None
                if isinstance(input_obj.default, dict):
                    message += 'The correct type could be "dict".'
            if isinstance(input_obj.default, str):
                message += 'The correct type could be "string".'
            if isinstance(input_obj.default, bool):
                message += 'The correct type could be "boolean".'
            if isinstance(input_obj.default, list):
                message += 'The correct type could be "list".'
        yield LintProblem(line, None, message)


class CfyInput(object):
    def __init__(self, nodes):
        self._line = None
        self.name, self.mapping = self.get_input(nodes)
        for key in list(self.mapping.keys()):
            if key not in ['type', 'default', 'description', 'constraints']:
                del self.mapping[key]
        self.input_type = self.mapping.get('type')
        self.description = self.mapping.get('description')
        self._default = self.mapping.get('default')
        self.constraints = self.mapping.get('constraints')

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def line(self):
        return self._line

    def not_input(self):
        return all([not k for k in self.mapping.values()])

    def __dict__(self):
        return {
            self.name: self.mapping
        }

    def get_input(self, nodes):
        if len(nodes) != 2:
            name = None
            mapping = None
        else:
            name = self.get_input_name(nodes[0])
            mapping = self.get_input_mapping(nodes[1])
        return name, mapping

    def get_input_name(self, node):
        if isinstance(node, yaml.nodes.ScalarNode):
            self._line = node.end_mark.line + 1
            return node.value

    def get_input_mapping(self, node):
        mapping = {
            'type': None,
            'default': None,
            'description': None,
            'constraints': None,
        }
        if isinstance(node, yaml.nodes.MappingNode):
            for tup in node.value:
                if not len(tup) == 2:
                    continue
                mapping_name = tup[0].value
                mapping_value = self.get_mapping_value(
                    mapping_name, tup[1].value)
                mapping[mapping_name] = mapping_value
        return mapping

    def get_mapping_value(self, name, value):
        if name not in ['default', 'constraints']:
            return value
        else:
            return recurse_mapping(value)
