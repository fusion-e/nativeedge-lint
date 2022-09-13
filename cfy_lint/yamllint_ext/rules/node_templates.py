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

import re
import yaml

from .. import LintProblem
from ..generators import CfyNode
from ..utils import process_relevant_tokens, INTRINSIC_FNS, context as ctx
from .constants import (GCP_TYPES,
                        AWS_TYPES,
                        AZURE_TYPES,
                        TERRAFORM_TYPES,
                        AWS_VALID_KEY,
                        AZURE_VALID_KEY,
                        TFLINT_SUPPORTED_CONFIGS,
                        TERRATAG_SUPPORTED_FLAGS,
                        deprecated_node_types,
                        REQUIRED_RELATIONSHIPS,
                        firewall_rule_gcp,
                        security_group_validation_aws,
                        security_group_validation_azure,
                        security_group_validation_openstack)

VALUES = []

ID = 'node_templates'
TYPE = 'token'
CONF = {
    'allowed-values': list(VALUES),
    'check-keys': bool,
    'check-node-types': bool
}
DEFAULT = {
    'allowed-values': ['true', 'false'],
    'check-keys': True,
    'check-node-types': True
}


@process_relevant_tokens(CfyNode, 'node_templates')
def check(token=None, context=None, node_types=None, **_):
    for node_template in token.node.value:
        if not len(node_template) == 2:
            continue
        parsed_node_template = parse_node_template(
            node_template[1], context.get(node_template[0].value))
        yield from check_deprecated_node_type(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_intrinsic_functions(
            parsed_node_template.dict,
            parsed_node_template.line or token.line)
        yield from check_client_config(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_dependent_types(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_security_group(
              parsed_node_template,
              parsed_node_template.line or token.line)
        yield from check_node_type_imported(
            node_types,
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_terraform(
            parsed_node_template,
            parsed_node_template.line or token.line)


def parse_node_template(node_template_mapping, node_template_model):
    node_template_model.set_values(
        recurse_node_template(node_template_mapping))
    node_template_model.line = node_template_mapping.start_mark.line + 1
    return node_template_model


def check_node_type_imported(node_types, model, line):
    node_types = node_types or {}
    if model.node_type not in node_types:
        yield LintProblem(
            line,
            None,
            "unimported node type: {}".format(model.node_type))


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
        if isinstance(value, list):
            if value[0] not in ctx.get('inputs', {}):
                yield LintProblem(
                    line,
                    None,
                    "get_input references undefined input: {}".format(value[0])
                )
        elif value not in ctx.get('inputs', {}):
            yield LintProblem(
                line,
                None,
                "get_input references undefined input: {}".format(value)
            )
    elif key in ['get_attribute', 'get_property']:
        if value[0] not in ctx.get('node_templates', {}) and \
                value[0] not in ctx.get('imported_node_templates', {}):
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


def check_client_config(model, line):
    if model.node_type in GCP_TYPES:
        yield from check_gcp_config(model, line)
    if model.node_type in AZURE_TYPES:
        yield from check_azure_config(model, line)
    if model.node_type in AWS_TYPES:
        yield from check_aws_config(model, line)


def check_gcp_config(model, line):
    if 'gcp_config' in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" has deprecated property "gcp_config". '
            'please use "client_config".'.format(model.name)
        )
    elif 'client_config' not in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name)
        )
    elif not all(x in ['auth', 'zone']
                 for x in model.properties['client_config']):
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required client config values '
            '["auth", "zone"].'.format(
                model.name)
        )


def check_azure_config(model, line):
    if 'client_config' not in model.properties or \
            'azure_config' in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name))
    client_config = model.properties.get('client_config', {})
    if not all(x in AZURE_VALID_KEY for x in client_config.keys()):
        if 'get_input' not in model.properties['client_config'] or \
                'get_secret' not in model.properties['client_config']:
            yield LintProblem(line,
                              None,
                              'Invalid parameters provided for client config. '
                              'Valid parameters are {}'.format(
                                  AZURE_VALID_KEY))


def check_aws_config(model, line):
    if 'client_config' not in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name))
    client_config = model.properties.get('client_config')
    if not all(x in AWS_VALID_KEY for x in client_config.keys()):
        if 'get_input' not in model.properties['client_config'] or \
                'get_secret' not in model.properties['client_config']:
            yield LintProblem(line,
                              None,
                              'Invalid parameters provided for client config. '
                              'Valid parameters are {}'.format(AWS_VALID_KEY))


def check_dependent_types(model, line):
    required_relationship_types = REQUIRED_RELATIONSHIPS.get(
        model.node_type, {})
    model.required_relationships = required_relationship_types
    if model.required_relationships_not_met(ctx['node_templates'],
                                            ctx.get('imported_node_templates',
                                                    {})):
        yield LintProblem(
            line,
            None,
            model.required_relationships_message
        )


def check_security_group(model, line):
    if model.node_type in security_group_validation_aws:
        yield from check_security_group_validation_aws(model, line)
    if model.node_type in security_group_validation_azure:
        yield from check_security_group_validation_azure(model, line)
    if model.node_type in security_group_validation_openstack:
        yield from check_security_group_validation_openstack(model, line)
    if model.node_type in firewall_rule_gcp:
        yield from check_firewall_rule_gcp(model, line)


def check_security_group_validation_aws(model, line):
    resource_config = model.properties.get('resource_config', {})
    ip_permissions = resource_config.get('IpPermissions', {})
    for item in ip_permissions:
        from_port = item.get('FromPort', {})
        to_port = item.get('ToPort', {})
        if from_port == '-1' or to_port == '-1':
            yield LintProblem(
                line,
                None,
                "Security group rule too open. {}".format(item))
        if int(to_port) - int(from_port) < 0:
            yield LintProblem(
                line,
                None,
                "Security group The port is invalid. {}".format(item))


def check_security_group_validation_azure(model, line):
    resource_config = model.properties.get('resource_config', {})
    security_rules = resource_config.get('securityRules', {})
    for item in security_rules:
        destination_port_range = item['properties'].get(
            'destinationPortRange', {})
        if destination_port_range == '*':
            yield LintProblem(
                line,
                None,
                "Security group rule too open. {}".format(item))


def check_security_group_validation_openstack(model, line):
    security_group_rules = model.properties.get('security_group_rules', {})
    for item in security_group_rules:
        protocol = item.get('protocol', {})
        port_range_min = item.get('port_range_min', {})
        port_range_max = item.get('port_range_max', {})
        if port_range_max == 'null' or port_range_min == 'null':
            if protocol != 'icmp':
                yield LintProblem(
                    line,
                    None,
                    "Security group rule Invalid. {}".format(item))
        elif port_range_max == '65535' or port_range_min == '1':
            yield LintProblem(
                line,
                None,
                "Security group rule too open. {}".format(item))
        elif int(port_range_max) - int(port_range_min) < 0:
            yield LintProblem(
                line,
                None,
                "Security group The port range is invalid. {}".format(item))


def check_firewall_rule_gcp(model, line):
    allowed = model.properties.get('allowed', {})
    for item in allowed['tcp']:
        if '-' in str(item):  # 12345-12349
            ports = re.split('-', item)
            if int(ports[0]) > int(ports[1]):
                yield LintProblem(
                    line,
                    None,
                    "Security group The port range is invalid.{}".format(item))


def check_terraform(model, line):
    if model.node_type in TERRAFORM_TYPES:
        tflint_config = model.properties.get('tflint_config', {})
        tfsec_config = model.properties.get('tfsec_config', {})
        terratag_config = model.properties.get('terratag_config', {})
        if tflint_config:
            yield from check_tflint(model, line)
        if tfsec_config:
            yield from check_tfsec(model, line)
        if terratag_config:
            yield from check_terratag(model, line)


def check_tfsec(model, line):
    tfsec_config = model.properties.get('tfsec_config', {})
    enable = tfsec_config.get('enable', {})
    if enable and enable == 'false':
        yield LintProblem(
            line,
            None,
            'tfsec_config will have no effect if "enable: false".')
    config = tfsec_config.get('config', {})
    include = config.get('include', None)
    exclude = config.get('exclude', None)
    if exclude and not isinstance(exclude, list) or \
            include and not isinstance(include, list):
        yield LintProblem(
            line,
            None,
            'tfsec_config.config '
            'parameters "include" and "exclude" should be a list')
    flags_override = tfsec_config.get('flags_override', {})
    for flag in flags_override:
        if 'color' == flag:
            yield LintProblem(
                line,
                None,
                'Color flag cannot be used in flags_override')


def check_tflint(model, line):
    tflint_config = model.properties.get('tflint_config', {})
    enable = tflint_config.get('enable', {})
    if enable and enable == 'false':
        yield LintProblem(
            line,
            None,
            'tflint_config will have no effect if "enable: false".')
    config = tflint_config.get('config', {})
    for item in config:
        type_name = item.get('type_name', {})
        if type_name not in TFLINT_SUPPORTED_CONFIGS:
            yield LintProblem(
                line,
                None,
                'unsupported key {} in tflint_config.'
                .format(TFLINT_SUPPORTED_CONFIGS))
        option_name = item.get('option_name', {})
        if type_name == 'plugin' and not option_name:
            yield LintProblem(
                line,
                None,
                'tflint_config "type_name" key must also provide '
                '"option_name", which is the plugin name.')
        elif type_name == 'config':
            option_value = item.get('option_value', {})
            if not option_value:
                yield LintProblem(
                    line,
                    None,
                    'To use tflint with type_name: config, it is necessary to '
                    'write option_value ')
    flags_override = tflint_config.get('flags_override', {})
    for flag in flags_override:
        if 'color' == flag:
            yield LintProblem(
                line,
                None,
                'color flag is not supported in flags_override')


def check_terratag(model, line):
    terratag_config = model.properties.get('terratag_config', {})
    enable = terratag_config.get('enable', {})
    if enable and enable == 'false':
        yield LintProblem(
            line,
            None,
            'terratag_config will have no effect if "enable: false".')
    tags = terratag_config.get('tags', {})
    if not tags or not isinstance(tags, dict):
        yield LintProblem(
            line,
            None,
            'tags should be a dict')
    flags_override = terratag_config.get('flags_override', {})
    if not isinstance(flags_override, list):
        yield LintProblem(
            line,
            None,
            'flags_override should be a list')
    for flag in flags_override:
        if not isinstance(flag, dict):
            yield LintProblem(
                line,
                None,
                'The flags inside flags_override should be a dict')
        key = flag.keys()
        for key in key:
            if '-' in key:
                yield LintProblem(
                    line,
                    None,
                    'The flags should be without a "-" sign, {}'.format(key))
            if key not in TERRATAG_SUPPORTED_FLAGS:
                yield LintProblem(
                    line,
                    None,
                    'unsupported flag, {}'.format(TERRATAG_SUPPORTED_FLAGS))
