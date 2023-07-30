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
import os
import re
import sys
import json
import time
import yaml
import pathlib
import urllib.request
from urllib.parse import urlparse
from packaging.version import parse as version_parse

from yamllint.config import YamlLintConfigError

from cfy_lint.yamllint_ext.cloudify.models import NodeTemplate
from cfy_lint.yamllint_ext.constants import (
    UNUSED_IMPORT,
    UNUSED_INPUTS,
    DEFAULT_TYPES,
    BLUEPRINT_MODEL,
    UNUSED_IMPORT_CTX,
    LATEST_PLUGIN_YAMLS,
    NODE_TEMPLATE_MODEL)

INTRINSIC_FNS = [
    'merge',
    'concat',
    'get_sys',
    'get_input',
    'get_label',
    'get_secret',
    'string_find',
    'string_split',
    'string_lower',
    'string_upper',
    'get_property',
    'get_attribute',
    'string_replace',
    'get_capability',
    'get_environment_capability',
]

context = {
    'imports': [],
    'dsl_version': None,
    'inputs': {},
    'imported_node_types': [],
    UNUSED_INPUTS: {},
    UNUSED_IMPORT_CTX: {},
    'node_templates': {},
    'node_types': {},
    'capabilities': {},
    'outputs': {},
    'current_tokens_line': 0,
    'add_label': [],
    'line_diff': {},
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


def get_json_from_marketplace(url):
    try:
        resp = urllib.request.urlopen(url)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        if isinstance(e, urllib.error.URLError):
            raise urllib.error.URLError("Connection Error")
        return {}
    body = resp.read()
    return json.loads(body)


def get_plugin_id_from_marketplace(plugin_name):
    url_plugin_id = 'https://marketplace.cloudify.co/plugins?name={}'.format(
        plugin_name)
    json_resp = get_json_from_marketplace(url_plugin_id)
    if 'items' in json_resp:
        if len(json_resp['items']) == 1:
            return json_resp['items'][0]['id']


def get_plugin_versions_from_marketplace(plugin_id):
    url_plugin_version = 'https://marketplace.cloudify.co/' \
                         'plugins/{}/versions?'.format(plugin_id)
    json_resp = get_json_from_marketplace(url_plugin_version)
    if 'items' in json_resp:
        versions = [item['version'] for item in json_resp['items']]
        return sorted(versions, key=lambda x: version_parse(x))
    return []


def get_plugin_release_spec_from_marketplace(plugin_id, plugin_version):
    release_url = 'https://marketplace.cloudify.co/plugins/{}/{}'.format(
        plugin_id, plugin_version)
    return get_json_from_marketplace(release_url)


def validate_versions(versions, validations):
    for neq in validations['!=']:
        if neq in versions:
            versions.remove(neq)
    for gteq in validations['>=']:
        parsed_gteq = version_parse(gteq)
        versions = [v for v in versions if version_parse(v) >= parsed_gteq]
    for lteq in validations['<=']:
        parsed_lteq = version_parse(lteq)
        versions = [v for v in versions if version_parse(v) <= parsed_lteq]
    for gt in validations['>']:
        parsed_gt = version_parse(gt)
        versions = [v for v in versions if version_parse(v) > parsed_gt]
    for lt in validations['<=']:
        parsed_lt = version_parse(lt)
        versions = [v for v in versions if version_parse(v) < parsed_lt]
    return versions


def get_validations(version_constraints):
    validations = {
        '==': [],
        '!=': [],
        '>=': [],
        '<=': [],
        '>': [],
        '<': [],
    }
    # Organize the version constraints so we get a dict like this:
    # {
    #    '==': [],
    #    '!=': ['1.0'],
    #    '>=': ['0.8', 0.9'],
    #    '<=': ['1.1'],
    # }
    try:
        for version_constraint in version_constraints:
            sign = re.match('[\\<\\>\\=\\!]+', version_constraint).group(0)
            plugin_version = re.findall(
                '(\\d+.\\d+.\\d+)', version_constraint)[0]
            validations[sign].append(plugin_version)
    except Exception as e:
        raise YamlLintConfigError('invalid version: %s' % e)
    return validations


def get_version_constraints(plugin_name, plugin_version_string):
    version_constraints = list(
        # Get rid of irrelevant stringy stuff.
        filter(
            lambda item: item, re.split(
                'plugin:| |{}|,'.format(plugin_name),
                plugin_version_string)
        )
    )
    # re.split is afraid of this one.
    if '?version' in version_constraints:
        version_constraints.remove('?version')
    if 'version=' in version_constraints:
        version_constraints.remove('version=')
    return version_constraints


def get_plugin_spec(plugin_version_string, plugin_name):

    version_constraints = get_version_constraints(
        plugin_name, plugin_version_string)

    validations = get_validations(version_constraints)

    plugin_id = get_plugin_id_from_marketplace(plugin_name)
    versions = get_plugin_versions_from_marketplace(plugin_id)

    if len(validations['==']) == 1 and validations['=='][0] in versions:
        return get_plugin_release_spec_from_marketplace(
            plugin_id, validations['=='][0])

    versions = validate_versions(versions, validations)

    if len(versions):
        return get_plugin_release_spec_from_marketplace(
            plugin_id, versions[-1])


def get_plugin_yaml_url(plugin_import):
    plugin_name, plugin_spec = _get_plugin_spec(plugin_import)
    if not plugin_spec:
        return LATEST_PLUGIN_YAMLS.get(plugin_name)
    elif len(plugin_spec.get('yaml_urls', [])):
        return plugin_spec['yaml_urls'][0]['url']


def _get_plugin_spec(plugin_import):
    parsed_import_item = urlparse(plugin_import)
    plugin_name = parsed_import_item.path
    return plugin_name, get_plugin_spec(parsed_import_item.query, plugin_name)


def get_node_types_for_plugin_import(plugin_import):
    plugin_name, plugin_spec = _get_plugin_spec(plugin_import)
    plugin_version = None
    if plugin_spec:
        plugin_version = plugin_spec['version']
    return get_node_types_for_plugin_version(plugin_name, plugin_version)


def get_node_types_for_plugin_version(plugin_name, plugin_version):

    node_types = {}
    offset = 0
    url = 'https://marketplace.cloudify.co/node-types?' \
          '&plugin_name={}' \
          '&plugin_version={}' \
          '&offset={}'.format(plugin_name, plugin_version, offset)

    while True:
        result = get_json_from_marketplace(url)
        if 'items' in result:
            for item in result['items']:
                if item['type'] not in node_types:
                    node_types[item['type']] = item
            # Stop paginating results when the offset has been incrimented
            # Beyond the amount of total reported results.
            if result['pagination']['total'] <= offset:
                break
            offset += 100
            url = re.sub(r'offset=\d+', 'offset={}'.format(offset), url)

    return node_types


def import_cloudify_yaml(import_item, base_path=None, cache_ttl=None):
    cache_ttl = cache_ttl or 86400
    cache_item = re.sub('[^0-9a-zA-Z]+', '_', import_item)
    current_dir = pathlib.Path(__file__).parent.resolve()
    cache_dir = pathlib.Path(os.path.join(
        current_dir,
        'cloudify/__cfylint_runtime_cache')).resolve()
    cache_dir
    if not cache_dir.exists():
        os.makedirs(cache_dir.absolute())
    cache_item_path = pathlib.Path(
        os.path.join(cache_dir.absolute(), cache_item))
    if cache_item_path.exists():
        # Check if the file has been stale for a while
        if cache_item_path.stat().st_ctime + cache_ttl < time.time():
            os.remove(cache_item_path)

    result = {}
    parsed_import_item = urlparse(import_item)
    if parsed_import_item.scheme == 'plugin':
        if cache_item_path.exists():
            with open(cache_item_path.absolute(), 'r') as jsonfile:
                result['node_types'] = json.load(jsonfile)
        else:
            node_types = get_node_types_for_plugin_import(
                import_item)
            result['node_types'] = node_types
            with open(cache_item_path.absolute(), 'w') as jsonfile:
                json.dump(node_types, jsonfile)
        # This is kind of wasteful, but
        # what this does is it stores the node types also
        # per plugin import line.
        # this enables us to analyze
        # if a plugin is being used.
        result[UNUSED_IMPORT] = {
            import_item: list(result['node_types'].keys())
        }
    if parsed_import_item.scheme in ['http', 'https']:
        if cache_item_path.exists():
            with open(cache_item_path.absolute(), 'r') as jsonfile:
                result = json.load(jsonfile)
        else:
            page = urllib.request.Request(
                import_item,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            try:
                infile = urllib.request.urlopen(page).read()
            except urllib.error.HTTPError:
                print('Error: Unable to reach URL: {}'.format(import_item))
                sys.exit(1)
            result = yaml.safe_load(infile)
            with open(cache_item_path.absolute(), 'w') as jsonfile:
                json.dump(result, jsonfile)
    elif import_item == 'cloudify/types/types.yaml':
        result = DEFAULT_TYPES
    elif base_path and os.path.exists(os.path.join(base_path, import_item)):
        with open(os.path.join(base_path, import_item), 'r') as stream:
            result = yaml.safe_load(stream)
            node_types_used = make_list_types(result)
            delete_imports_from_unused_ctx(node_types_used)
            add_to_imported_node_types(node_types_used)

    elif os.path.exists(import_item):
        with open(import_item, 'r') as stream:
            result = yaml.safe_load(stream)
        result = result or {}

    for k in result.keys():
        left = 'imported_{}'.format(k)
        if left not in context:
            if isinstance(result[k], dict) and left in ['imported_node_types']:
                context[left] = list(result[k].keys())
            else:
                context[left] = result[k]
        elif isinstance(context[left], list):
            if k in ["tosca_definitions_version"]:
                context[left].append(result[k])
            else:
                context[left].extend(result[k])
        elif isinstance(context[left], str):
            if context[left] != result[k] and \
                    k in ["tosca_definitions_version"]:
                if not isinstance(context[left], list):
                    tmp = [context[left]]
                    context[left] = tmp
                context[left].append(result[k])
            elif context[left] != result[k]:
                raise Exception(
                    'There is no match between '
                    '{result} and {context}'.format(
                        context=context[left],
                        result=result[k]))
        else:
            context[left].update(result[k])


def delete_imports_from_unused_ctx(node_types_used):
    need_to_del = []
    unused_import = context[UNUSED_IMPORT_CTX].keys()
    for type in node_types_used:
        for k in unused_import:
            if type in context[UNUSED_IMPORT_CTX][k]:
                need_to_del.append(k)

    for d in need_to_del:
        del context[UNUSED_IMPORT_CTX][d]

    if 'plugin:cloudify-fabric-plugin' in context[UNUSED_IMPORT_CTX].keys():
        del context[UNUSED_IMPORT_CTX]['plugin:cloudify-fabric-plugin']


def make_list_types(content_file):
    values = []
    keys = ['type', 'derived_from']
    for k, v in content_file.items():
        if 'node_templates' == k:
            values.extend(find_values_by_key(v, keys))
        if 'node_types' == k:
            values.extend(v.keys())
            values.extend(find_values_by_key(v, ['derived_from']))
    return values


def find_values_by_key(yaml_data, keys):
    """
    Find all values associated with a given key in YAML data.
    :param yaml_data: YAML data to search through.
    :param keys: List of keys to look for in the YAML data.
    :return: List of all values associated with the given key.
    """
    values = []
    if isinstance(yaml_data, dict):
        for k, v in yaml_data.items():
            if k in keys:
                values.append(v)
            elif isinstance(v, (dict, list)):
                nested_values = find_values_by_key(v, keys)
                if nested_values:
                    values.extend(nested_values)
    elif isinstance(yaml_data, list):
        for i in yaml_data:
            if isinstance(i, (dict, list)):
                nested_values = find_values_by_key(i, keys)
                if nested_values:
                    values.extend(nested_values)
            elif i in keys:
                values.append(i)
    return values


def setup_types(buffer=None, data=None, base_path=None):
    try:
        data = data or yaml.safe_load(buffer)
    except yaml.parser.ParserError:
        return
    if not data:
        return
    for imported in data.get('imports', {}):
        import_cloudify_yaml(imported, base_path=base_path)
    add_to_node_types(data.get('node_types', {}))


def add_to_imported_node_types(node_types_used):
    if isinstance(node_types_used, list):
        for item in node_types_used:
            if item not in context['imported_node_types']:
                context['imported_node_types'].append(item)
    elif node_types_used not in context['imported_node_types']:
        context['imported_node_types'].append(node_types_used)


def add_to_node_types(node_types):
    context['imported_node_types'].extend(node_types.keys())


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
        if 'bool' in mapping.tag:
            return bool(mapping.value.lower() == "true")
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


def check_node_imported(node_name):
    for keys in context['imported_node_types_by_plugin']:
        if node_name in context['imported_node_types_by_plugin'][keys]:
            return True
    return False


def recurse_get_readable_object(mapping):
    if isinstance(mapping, yaml.nodes.ScalarNode):
        return mapping.value
    if isinstance(mapping, yaml.nodes.MappingNode):
        mapping_list = []
        for item in mapping.value:
            mapping_list.append(recurse_get_readable_object(item))
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
                mapping[0].value: recurse_get_readable_object(mapping[1])
            }
        else:
            new_list = []
            for item in mapping:
                new_list.append(recurse_get_readable_object(item))
            return new_list
    elif isinstance(mapping, yaml.nodes.SequenceNode):
        new_list = []
        for item in mapping.value:
            new_list.append(recurse_get_readable_object(item))
        return new_list
