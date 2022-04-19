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

from .constants import (BLUEPRINT_MODEL, NODE_TEMPLATE_MODEL)

context = {}


def assign_current_top_level(elem):
    if isinstance(elem.curr, yaml.tokens.ScalarToken) and \
            elem.curr.value in BLUEPRINT_MODEL and \
            isinstance(elem.nextnext,
                       yaml.tokens.BlockMappingStartToken):
        return elem.curr.value
    elif isinstance(elem.curr, yaml.tokens.BlockEndToken) and \
            isinstance(elem.nextnext, yaml.tokens.ScalarToken) and \
            elem.nextnext.value in BLUEPRINT_MODEL:
        return ''


def assign_nested_node_template_level(elem):
    if not isinstance(elem.curr, yaml.tokens.ScalarToken):
        return
    if elem.curr.value not in NODE_TEMPLATE_MODEL:
        return
    if isinstance(elem.nextnext, (yaml.tokens.BlockMappingStartToken,
                                  yaml.tokens.BlockEntryToken)):
        return elem.curr.value


def update_model(_elem):
    """Tracking a Cloudify Model inside YAMLLINT context.

    :param _elem:
    :return:
    """
    if stop_document(_elem):
        # The document is finished.
        return
    # We are in the middle of the document.
    top_level = assign_current_top_level(_elem)
    node_template(_elem)
    if skip_inputs_in_node_templates(_elem):
        return
    elif isinstance(top_level, str):
        context['current_top_level'] = top_level  # noqa


def stop_document(_elem):
    if isinstance(_elem.curr, yaml.tokens.StreamStartToken):
        # This is the start of the YAML document.
        context['model'] = BLUEPRINT_MODEL
        context['current_top_level'] = None  # noqa
    elif isinstance(_elem.curr, yaml.tokens.StreamEndToken):
        # This is the end of the YAML document.
        del context['model']
        return True
    return False


def node_template(_elem):
    if context.get('current_top_level') == 'node_templates':
        # When we are looking at Node Templates, we may
        nt = assign_nested_node_template_level(_elem)
        if isinstance(nt, str):
            context['node_template_level'] = nt
    else:
        context['node_template_level'] = None


def skip_inputs_in_node_templates(top_level):
    return context.get('current_top_level') == 'node_templates' and \
           top_level == 'inputs'


def token_to_string(token):
    if isinstance(token, yaml.tokens.ValueToken):
        return ': '
    elif isinstance(token, yaml.tokens.ScalarToken):
        return token.value
    elif isinstance(token, yaml.tokens.FlowEntryToken):
        return ', '
    elif isinstance(token, yaml.tokens.FlowMappingEndToken):
        return '} '
    elif isinstance(token, yaml.tokens.FlowMappingStartToken):
        return ' {'
    # elif isinstance(token, yaml.tokens.BlockMappingStartToken):
    #     string = ' {' + string
    # elif isinstance(token, yaml.tokens.BlockSequenceStartToken):
    #     string = ' ' + string
    elif isinstance(token, yaml.tokens.BlockEntryToken):
        return '-'
    # elif isinstance(token, yaml.tokens.BlockEndToken):
    #     string = '] ' + string


def build_string_from_stack(stack, prev, curr):
    string = ''
    stack.insert(0, prev)
    stack.insert(0, curr)
    index = 0
    while True:
        if index > len(stack):
            break
        token = stack[index]
        if isinstance(token, yaml.tokens.KeyToken):
            inner_index = 0
            while True:
                inner_index += 1
                inner_token = stack[index + inner_index]
                if isinstance(inner_token, yaml.tokens.BlockEndToken):
                    break
            for skipping_index in range(index, index + inner_index):
                converted_token = token_to_string(stack[skipping_index])
                if converted_token:
                    string = converted_token + string
                else:
                    continue
            index = index + inner_index
            continue
        index += 1
        converted_token = token_to_string(token)
        if converted_token:
            string = converted_token + string
        else:
            break
    print(string)
