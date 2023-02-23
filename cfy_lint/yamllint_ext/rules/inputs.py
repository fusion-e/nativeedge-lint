########
# Copyright (c) 2014-2023 Cloudify Platform Ltd. All rights reserved
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

from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.constants import UNUSED_INPUTS
from cfy_lint.yamllint_ext.utils import (
    INTRINSIC_FNS,
    recurse_mapping,
    context as ctx, process_relevant_tokens)

VALUES = []

ID = 'inputs'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
ALLOWED_KEYS = [
    'type',
    'hidden',
    'default',
    'required',
    'constraints',
    'description',
    'display_label'
]
DSL_1_3 = [
    'list',
    'dict',
    'regex',
    'float',
    'string',
    'integer',
    'boolean',
    'textarea'
]
DSL_1_4 = [
    'node_id',
    'node_ids',
    'blueprint_id',
    'node_template',
    'deployment_id',
    'blueprint_ids',
    'deployment_ids',
    'capability_value',
    'node_instance_ids',
]
DSL_1_4.extend(DSL_1_3)
INPUTS_BY_DSL = {
    'cloudify_dsl_1_3': DSL_1_3,
    'cloudify_dsl_1_4': DSL_1_4
}


@process_relevant_tokens(CfyNode, ['inputs', 'get_input'])
def check(token=None, skip_suggestions=None, **_):
    if token.prev.node.value == 'inputs':
        for item in token.node.value:
            if isinstance(item, yaml.nodes.ScalarNode):
                yield LintProblem(
                    token.line,
                    None,
                    'Bad inputs format. '
                    'Input should be a key not a list item.')
            input_obj = CfyInput(item)
            if not input_obj.name and not input_obj.mapping:
                continue
            if input_obj.not_input():
                continue
            ctx['inputs'].update(input_obj.__dict__())
            if input_obj.name not in ctx[UNUSED_INPUTS]:
                ctx[UNUSED_INPUTS].update(
                    {
                        input_obj.name: LintProblem(
                            token.line,
                            None,
                            'input {} is unused.'.format(input_obj.name)
                        )
                    }
                )
            yield from validate_inputs(input_obj,
                                       input_obj.line or token.line,
                                       ctx.get("dsl_version"),
                                       skip_suggestions)

    if token.prev.node.value == 'get_input':
        if isinstance(token.node.value, list):
            if isinstance(token.node.value[0], yaml.nodes.ScalarNode):
                if token.node.value[0].value not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input {}'
                        .format(token.node.value[0].value))
                elif token.node.value[0].value in ctx[UNUSED_INPUTS]:
                    del ctx[UNUSED_INPUTS][token.node.value[0].value]
            if isinstance(token.node.value[0], tuple):
                if token.node.value[0][0] not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input "{}"'.format(token.node.value[0][0]))
                elif token.node.value[0][0] in ctx[UNUSED_INPUTS]:
                    del ctx[UNUSED_INPUTS][token.node.value[0][0]]
        else:
            if token.node.value not in ctx['inputs']:
                yield LintProblem(
                    token.line,
                    None,
                    'undefined input "{}"'.format(token.node.value))
            elif token.node.value in ctx[UNUSED_INPUTS]:
                del ctx[UNUSED_INPUTS][token.node.value]


def validate_inputs(input_obj, line, dsl, skip_suggestions=None):
    suggestions = 'inputs' in skip_suggestions
    if input_obj.invalid_keys:
        yield LintProblem(
            line,
            None,
            'the following keys are invalid for inputs: {}'.format(
                input_obj.invalid_keys))
    if not input_obj.input_type:
        message = 'input "{}" does not specify a type. '.format(input_obj.name)
        if input_obj.default:
            if isinstance(input_obj.default, dict):
                for key in input_obj.default.keys():
                    if key in INTRINSIC_FNS:
                        input_obj.default = None
                if isinstance(input_obj.default, dict) and not suggestions:
                    message += 'The correct type could be "dict".'
            if isinstance(input_obj.default, str) and not suggestions:
                message += 'The correct type could be "string".'
            if isinstance(input_obj.default, bool) and not suggestions:
                message += 'The correct type could be "boolean".'
            if isinstance(input_obj.default, list) and not suggestions:
                message += 'The correct type could be "list".'
        yield LintProblem(line, None, message)
    elif input_obj.input_type not in INPUTS_BY_DSL.get(dsl, []):
        yield LintProblem(
            line,
            None,
            'Input of type {} is not supported by DSL {}.'.format(
                input_obj.input_type, dsl
            )
        )
    elif not input_obj.display_label:
        yield LintProblem(
            line,
            None,
            'Input {} is missing a display_label.'.format(input_obj.name)
        )


class CfyInput(object):
    def __init__(self, nodes):
        self._line = None
        self.name, self.mapping = self.get_input(nodes)
        self.invalid_keys = []
        if self.name and self.mapping:
            for key in list(self.mapping.keys()):
                if key not in ALLOWED_KEYS:
                    self.invalid_keys.append(key)
                    del self.mapping[key]
            self.input_type = self.mapping.get('type')
            self.description = self.mapping.get('description')
            self._default = self.mapping.get('default')
            self.constraints = self.mapping.get('constraints')
            self.display_label = self.mapping.get('display_label')

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
        if not isinstance(nodes, tuple) or len(nodes) != 2:
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
            'display_label': None,
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
