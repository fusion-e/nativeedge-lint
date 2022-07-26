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


def mapping_is_two_length_intrinsic_function(mapping):
    if len(mapping) == 2 and not isinstance(mapping[0], tuple):
        try:
            if mapping[0].value in INTRINSIC_FNS:
                return True
        except AttributeError:
            return False


def mapping_is_one_length_intrinsic_function_tuple(mapping):
    if len(mapping) == 1 and isinstance(mapping[0], tuple):
        if len(mapping[0]) == 2 and mapping[0][0].value in INTRINSIC_FNS:
            return True


def mapping_is_one_length_intrisic_function_mapping_node(mapping):
    if len(mapping) == 1 and isinstance(mapping[0],
                                        yaml.nodes.MappingNode):
        try:
            if len(mapping[0].value) == 2 and \
                   mapping[0].value[0].value in INTRINSIC_FNS:
                return True
        except AttributeError:
            return False


def recurse_mapping(mapping):
    if isinstance(mapping, dict):
        new_dict = {}
        for k, v in mapping.items():
            new_dict[k] = recurse_mapping(v)
        return new_dict
    elif isinstance(mapping, (list, tuple)):
        new_list = []
        if mapping_is_two_length_intrinsic_function(mapping):
            return recurse_mapping({mapping[0].value: mapping[1].value})
        if mapping_is_one_length_intrinsic_function_tuple(mapping):
            return recurse_mapping(
                {
                    mapping[0][0].value: mapping[0][1].value
                }
            )
        if mapping_is_one_length_intrisic_function_mapping_node(mapping):
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
