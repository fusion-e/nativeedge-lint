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

ID = 'inputs'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
INTRINSIC_FNS = [
    'get_input', 'get_capability', 'get_attribute', 'get_property']


def check(conf=None,
          token=None,
          prev=None,
          next=None,
          nextnext=None,
          context=None):
    if 'inputs' not in context:
        context['inputs'] = {}
    if isinstance(token, CfyNode):
        line = token.node.start_mark.line + 1
        if token.prev and token.prev.node.value == 'inputs':
            for item in token.node.value:
                input_obj = CfyInput(item)
                if input_obj.not_input():
                    continue
                context['inputs'].update(input_obj.__dict__())
                yield from validate_inputs(input_obj, line)
        if token.prev and token.prev.node.value == 'get_input':
            if token.node.value not in context['inputs']:
                yield LintProblem(
                    line,
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
        self.name, self.mapping = get_input(nodes)
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

    def not_input(self):
        return all([not k for k in self.mapping.values()])

    def __dict__(self):
        return {
            self.name: self.mapping
        }


def get_input(nodes):
    if len(nodes) != 2:
        name = None
        mapping = None
    else:
        name = get_input_name(nodes[0])
        mapping = get_input_mapping(nodes[1])
    return name, mapping


def get_input_name(node):
    if isinstance(node, yaml.nodes.ScalarNode):
        return node.value


def get_input_mapping(node):
    mapping = {
        'type': None,
        'default': None,
        'description': None,
        'constraints': None,
    }
    valid_keys = mapping.keys()
    if isinstance(node, yaml.nodes.MappingNode):
        for tup in node.value:
            if not len(tup) == 2:
                continue
            mapping_name = tup[0].value
            mapping_value = get_mapping_value(mapping_name, tup[1].value)
            mapping[mapping_name] = mapping_value
    return mapping


def get_mapping_value(name, value):
    if name not in ['default', 'constraints']:
        return value
    else:
        return recurse_mapping(value)


def recurse_mapping(mapping):
    if isinstance(mapping, dict):
        new_dict = {}
        for k, v in mapping.items():
            new_dict[k] = recurse_mapping(v)
        return new_dict
    elif isinstance(mapping, (list, tuple)):
        new_list = []
        if len(mapping) == 2 and mapping[0].value in INTRINSIC_FNS:
            return recurse_mapping({mapping[0].value: mapping[1].value})
        if len(mapping) == 1 and \
                len(mapping[0]) == 2 and \
                mapping[0][0].value in INTRINSIC_FNS:
            return recurse_mapping({mapping[0][0].value: mapping[0][1].value})
        for item in mapping:
            new_list.append(recurse_mapping(item))
        return new_list
    elif not isinstance(mapping, yaml.nodes.Node):
        return mapping
    elif isinstance(mapping, yaml.nodes.ScalarNode):
        return mapping.value
    elif isinstance(mapping, yaml.nodes.SequenceNode):
        new_list = []
        for item in mapping.value:
            new_list.append(recurse_mapping(item))
        return new_list
    elif isinstance(mapping, yaml.nodes.MappingNode):
        new_dict = {}
        new_list = []
        for item in mapping.value:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                key = item[0].value
                value = recurse_mapping(item[1].value)
                new_dict[key] = value
            else:
                new_list.append(item)
        if new_dict:
            return new_dict
        return new_list
