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
from ..utils import recurse_mapping, INTRINSIC_FNS, context as ctx
from .constants import deprecated_node_types

VALUES = []

ID = 'node_templates'
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
        if not token.prev or not token.prev.node.value == 'node_templates':
            return
        for node_template in token.node.value:
            line = token.node.start_mark.line + 1
            if not len(node_template) == 2:
                continue
            parsed_node_template = parse_node_template(
                node_template[1], context.get(node_template[0].value))
            yield from check_deprecated_node_type(
                parsed_node_template,
                parsed_node_template.line or line)
            yield from check_intrinsic_functions(
                parsed_node_template.dict,
                parsed_node_template.line or line)


def parse_node_template(node_template_mapping, node_template_model):
    node_template_model.set_values(
        recurse_node_template(node_template_mapping))
    node_template_model.line = node_template_mapping.start_mark.line + 1
    return node_template_model


def check_deprecated_node_type(model, line):
    if model.node_type in deprecated_node_types:
        yield LintProblem(
            line,
            None,
            "deprecated node type. "
            "Replace usage of {} with {}.".format(
                model.node_type,
                deprecated_node_types[model.node_type]))


def check_intrinsic_functions(data, line):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in INTRINSIC_FNS:
                yield from validate_instrinsic_function(key, value, line)
            else:
                yield from check_intrinsic_functions(value, line)
    elif isinstance(data, list):
        for item in data:
            yield from check_intrinsic_functions(item, line)


def validate_instrinsic_function(key, value, line):
    if key == 'get_input':
        if value not in ctx.get('inputs', {}):
            yield LintProblem(
                line,
                None,
                "get_input references undefined input: {}".format(value)
            )
    elif key in ['get_attribute', 'get_property']:
        if value[0] not in ctx.get('node_templates', {}):
            yield LintProblem(
                line,
                None,
                "{} references undefined target {}".format(key, value[0])
            )


def recurse_node_template(mapping):
    if isinstance(mapping, yaml.nodes.ScalarNode):
        return mapping.value
    if isinstance(mapping, yaml.nodes.MappingNode):
        mapping_list = []
        for item in mapping.value:
            mapping_list.append(recurse_node_template(item))
        mapping_dict = {}
        for item in mapping_list:
            try:
                mapping_dict[item[0]] = item[1]
            except KeyError:
                mapping_dict.update(item)
        return mapping_dict
    elif isinstance(mapping, tuple):
        if len(mapping) == 2 and isinstance(mapping[0], yaml.nodes.ScalarNode):
            return {
                mapping[0].value: recurse_node_template(mapping[1])
            }
        else:
            new_list = []
            for item in mapping:
                new_list.append(recurse_node_template(item))
            return new_list
    elif isinstance(mapping, yaml.nodes.SequenceNode):
        new_list = []
        for item in mapping.value:
            new_list.append(recurse_node_template(item))
        return new_list
