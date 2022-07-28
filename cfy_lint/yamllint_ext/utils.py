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

import io
import yaml

from .cloudify.models import NodeTemplate
from .constants import (BLUEPRINT_MODEL, NODE_TEMPLATE_MODEL)

INTRINSIC_FNS = [
    'get_input', 'get_capability', 'get_attribute', 'get_property']

context = {
    'imports': [],
    'dsl_version': None,
    'inputs': {},
    'node_templates': {},
    'node_types': {},
    'capabilities': {},
    'outputs': {},
    'current_tokens_line': 0
}


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
    # print(vars(_elem))
    context['current_tokens_line'] = _elem.line_no
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
    if isinstance(token, (
            yaml.tokens.ValueToken,
            yaml.tokens.ScalarToken,
            yaml.tokens.FlowEntryToken,
            yaml.tokens.FlowMappingEndToken,
            yaml.tokens.FlowMappingEndToken,
            yaml.tokens.FlowMappingStartToken,
            yaml.tokens.BlockEntryToken)):
        return str(token)
    if isinstance(token, yaml.tokens.KeyToken):
        return '\n'
    elif isinstance(token, yaml.tokens.ValueToken):
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


def build_string_from_stack(stack):
    string = ''
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
    # print(string)


def recurse_tokens(stack, index=0, recurse_until=None):
    new_stack = []
    while True:

        try:
            token = stack[index]
            index += 1
        except IndexError:
            return new_stack, index

        if not isinstance(token, (yaml.tokens.FlowMappingStartToken,
                                  yaml.tokens.FlowMappingEndToken,
                                  yaml.tokens.BlockMappingStartToken,
                                  yaml.tokens.BlockSequenceStartToken,
                                  yaml.tokens.BlockEndToken)):
            new_stack.append(token)

        elif isinstance(token, yaml.tokens.BlockSequenceStartToken):
            # Seems to be indentation.
            inner_stack, index = recurse_tokens(
                stack, index, yaml.tokens.BlockEndToken)
            inner_stack.insert(0, token)
            new_stack.append(inner_stack)
            continue


        elif isinstance(token, yaml.tokens.BlockMappingStartToken):
            # Seems to be indentation.
            inner_stack, index = recurse_tokens(
                stack, index, yaml.tokens.BlockEndToken)
            inner_stack.insert(0, token)
            new_stack.append(inner_stack)
            continue

        elif isinstance(token, yaml.tokens.FlowMappingStartToken):
            # These get dicts.
            inner_stack, index = recurse_tokens(
                stack, index, yaml.tokens.FlowMappingEndToken)
            inner_stack.insert(0, token)
            new_stack.append(inner_stack)
            continue

        elif isinstance(token, yaml.tokens.FlowSequenceStartToken):
            # These get lists.
            inner_stack, index = recurse_tokens(
                stack, index, yaml.tokens.FlowSequenceEndToken)
            inner_stack.insert(0, token)
            new_stack.append(inner_stack)
            continue

        elif recurse_until and isinstance(token, recurse_until):
            return new_stack, index

    return new_stack, index


def recurse_nodes(node, line_no=0):
    ordered_nodes = []
    if not node:
        return
    elif isinstance(node, (list, tuple)):
        for sub in node:
            ordered_nodes.extend(recurse_nodes(sub, line_no))
    elif isinstance(node, yaml.nodes.Node):
        if node.start_mark.line <= line_no <= node.end_mark.line:
            ordered_nodes.append(node)
        if isinstance(node, yaml.nodes.CollectionNode):
            if node.start_mark.line <= line_no <= node.end_mark.line:
                ordered_nodes.append(node)
                ordered_nodes.extend(recurse_nodes(node.value, line_no))
    return list(dict.fromkeys(ordered_nodes))


def setup_node_templates(elem):
    if 'node_templates' not in context:
        context['node_templates'] = {}
    if elem.prev and elem.prev.node.value == 'node_templates':
        for item in elem.node.value:
            node_template = setup_node_template(item)
            if node_template.name not in context:
                context['node_templates'].update({
                    node_template.name: node_template
                })
    elem.node_templates = context['node_templates']


def setup_node_template(list_item):
    if len(list_item) == 2:
        if isinstance(list_item[0], yaml.nodes.ScalarNode) and \
                isinstance(list_item[1], yaml.nodes.MappingNode):
            node_template = NodeTemplate(list_item[0].value)
            node_template.node_type = setup_node_type(list_item[1].value)
            return node_template


def setup_node_type(value):
    return value[0][1].value


def recurse_mapping(mapping):
    if isinstance(mapping, dict):
        new_dict = {}
        for k, v in mapping.items():
            new_dict[k] = recurse_mapping(v)
        return new_dict
    elif isinstance(mapping, (list, tuple)):
        new_list = []
        if len(mapping) == 2 and not isinstance(mapping[0], tuple) and mapping[0].value in INTRINSIC_FNS:
            return recurse_mapping({mapping[0].value: mapping[1].value})
        if len(mapping) == 1 and isinstance(mapping[0], tuple):
            if len(mapping[0]) == 2 and mapping[0][0].value in INTRINSIC_FNS:
                return recurse_mapping(
                    {
                        mapping[0][0].value: mapping[0][1].value
                    }
                )
        if len(mapping) == 1 and isinstance(mapping[0],
                                            yaml.nodes.MappingNode):
            if len(mapping[0].value) == 2 and \
                    mapping[0].value[0].value in INTRINSIC_FNS:
                return recurse_mapping(
                    {
                        mapping[0].value[0].value: mapping[0].value[1].value
                    }
                )
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


def process_relevant_tokens(model, keyword):
    def wrapper_outer(function):
        def wrapper_inner(*args, **kwargs):
            token = kwargs.get('token')
            if isinstance(token, model):
                if isinstance(keyword, str):
                    if token.prev and token.prev.node.value == keyword:
                        yield from function(*args, **kwargs)
                if isinstance(keyword, list):
                    if token.prev and token.prev.node.value in keyword:
                        yield from function(*args, **kwargs)
        return wrapper_inner
    return wrapper_outer


def update_dict_values_recursive(default_dict, name_file_config):
    with io.open(name_file_config):
        f = open("config.yaml", "r")
        user_dict = f.read()

    default_dict = yaml.load(default_dict)
    user_dict = yaml.load(user_dict)

    if user_dict and default_dict:
        for key, value in user_dict.items():
            if value is dict:
                update_dict_values_recursive(default_dict[key], value)
            if value:
                default_dict[key] = value
    return default_dict
