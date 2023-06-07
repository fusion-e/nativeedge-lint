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

from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.utils import process_relevant_tokens

VALUES = []

ID = 'blueprint_labels'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['blueprint_labels', 'blueprint-labels'])
def check(token=None, **_):
    if token.prev.node.value == 'blueprint-labels':
        yield LintProblem(
                token.line,
                None,
                'Should be written in this form blueprint_labels')
    for item in token.node.value:
        d = recurse_node_type(item)
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


def recurse_node_type(mapping):
    if isinstance(mapping, yaml.nodes.ScalarNode):
        return mapping.value
    if isinstance(mapping, yaml.nodes.MappingNode):
        mapping_list = []
        for item in mapping.value:
            mapping_list.append(recurse_node_type(item))
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
                mapping[0].value: recurse_node_type(mapping[1])
            }
        else:
            new_list = []
            for item in mapping:
                new_list.append(recurse_node_type(item))
            return new_list
    elif isinstance(mapping, yaml.nodes.SequenceNode):
        new_list = []
        for item in mapping.value:
            new_list.append(recurse_node_type(item))
        return new_list
