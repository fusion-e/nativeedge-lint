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

from pprint import pprint
from yaml import Node
from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    recurse_get_readable_object,
    context as ctx
    )

VALUES = []

ID = 'blueprint_labels'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['blueprint_labels', 'blueprint-labels'])
def check(token=None, **_):
    dsl = ctx.get("dsl_version")
    if dsl == 'cloudify_dsl_1_3':
        yield LintProblem(
            token.prev.line,
            None,
            'cloudify_dsl_1_3 does not support Blueprint Labels')
    if token.prev.node.value == 'blueprint-labels':
        yield LintProblem(
                token.prev.line,
                None,
                'The blueprint_labels key should be written '
                'with an underscore not a dash.')
        
    for item in token.node.value:
        print('------------------')
        dictionary = recurse_get_readable_object(item)
        print('dictionary: {}'.format(dictionary))
        if not isinstance(dictionary, dict):
            yield LintProblem(
                token.line,
                None,
                desc='Every label should be a dictionary')

        for k, v in dictionary.items():
            print('nested_value: {}  dictionary? {}'.format(v, type(v)))
            if not isinstance(v, dict):
                yield LintProblem(
                    token.line,
                    None,
                    desc='blueprint_labels contains nested dictionaries')
            
            nested_key = list(v.keys())
            nested_value = list(v.values())
            print('nested_value: {}'.format(nested_value))

            print('nested_key: values == {}'.format(nested_key[0]))
            if nested_key[0] != 'values':
                yield LintProblem(
                    token.line,
                    None,
                    desc='The name of the key should be "values"')
                
            print('nested_value:{} type is {} == list'.format(nested_value[0], type(nested_value[0])))
            if not isinstance(nested_value[0], list):
                yield LintProblem(
                    token.line,
                    None,
                    desc='The value of the "values" is should be a list')
