# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import re
import networkx as nx
from yaml.nodes import ScalarNode

from ne_lint.yamllint_ext import LintProblem
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.constants import UNUSED_IMPORT_CTX
from ne_lint.yamllint_ext.utils import (
    recurse_get_readable_object,
    process_relevant_tokens,
    find_values_by_key,
    context as ctx,
    INTRINSIC_FNS,
)
from ne_lint.yamllint_ext.rules.constants import (
    GCP_TYPES,
    AWS_TYPES,
    AZURE_TYPES,
    AWS_VALID_KEY,
    AZURE_VALID_KEY,
    TERRAFORM_TYPES,
    firewall_rule_gcp,
    AWS_TYPE_WITH_TAGS,
    deprecated_node_types,
    REQUIRED_RELATIONSHIPS,
    TFLINT_SUPPORTED_CONFIGS,
    TERRATAG_SUPPORTED_FLAGS,
    security_group_validation_aws,
    security_group_validation_azure,
    security_group_validation_openstack,
)

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
PROPERTY_TYPES = (
    'integer',
    'string',
    'boolean',
    'dict',
    'list',
    'float',
    'regex'
)
PROPERTY_TYPES_Z = (
    int,
    str,
    bool,
    dict,
    list,
    float,
    None
)


@process_relevant_tokens(NENode, 'node_templates')
def check(token=None, context=None, node_types=None, **_):
    if not ctx['start_lines']['node_templates']:
        ctx['start_lines']['node_templates'] = token.node.start_mark.line
    line_index = {}
    edges = []
    for node_template in token.node.value:
        if not len(node_template) == 2:
            continue
        parsed_node_template = parse_node_template(
            node_template[1], context.get(node_template[0].value))
        edges, line_index = prepre_cyclic_inputs(
            node_template, edges, line_index,
            parsed_node_template.line or token.line)
        remove_node_type_from_context(parsed_node_template.node_type)
        yield from check_deprecated_node_type(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_intrinsic_functions(
            parsed_node_template.dict,
            parsed_node_template.line or token.line)
        yield from check_dependent_types(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_interfaces(
            parsed_node_template,
            parsed_node_template.line or token.line)
        yield from check_relationships(
            parsed_node_template,
            parsed_node_template.line or token.line)
        if parse_node_template.properties:
            yield from check_client_config(
                parsed_node_template,
                parsed_node_template.line or token.line)
            yield from check_security_group(
                parsed_node_template,
                parsed_node_template.line or token.line)
            yield from check_properties(
                parsed_node_template,
                parsed_node_template.line or token.line)
            yield from check_external_resource(
                parsed_node_template,
                parsed_node_template.line or token.line)
            yield from check_get_attribute(
                parsed_node_template,
                parsed_node_template.line or token.line)
            yield from check_supports_tagging(
                parsed_node_template,
                parsed_node_template.line or token.line)
        if parse_node_template.node_type:
            yield from check_node_type_imported(
                node_types,
                parsed_node_template,
                parsed_node_template.line or token.line)
            if parse_node_template.properties:
                yield from check_terraform(
                    parsed_node_template,
                    parsed_node_template.line or token.line)
    yield from check_cyclic_node_dependency(edges, line_index)


def parse_node_template(node_template_mapping, node_template_model):
    node_template_model.set_values(
        recurse_get_readable_object(node_template_mapping))
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
    if model.node_type.startswith('cloudify.') and \
            model.node_type not in deprecated_node_types:
        yield LintProblem(
            line,
            None,
            "deprecated node type. "
            f"Replace usage of {model.node_type} with "
            f"{model.node_type.replace('cloudify', 'nativeedge')}."
        )
    elif model.node_type in deprecated_node_types:
        yield LintProblem(
            line,
            None,
            "deprecated node type. "
            "Replace usage of {} with {}.".format(
                model.node_type,
                deprecated_node_types[model.node_type]),
            fixable=True)


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
                value[0] not in ctx.get('imported_node_templates', {}) \
                and value[0] not in ['SELF', 'TARGET', 'SOURCE']:
            yield LintProblem(
                line,
                None,
                "{} references undefined target {}".format(key, value[0])
            )


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
            'please use "client_config".'.format(model.name),
            fixable=True
        )
    elif 'client_config' not in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name)
        )


def check_azure_config(model, line):
    if 'azure_config' in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" has deprecated property "azure_config". '
            'please use "client_config".'.format(model.name),
            fixable=True
        )
    elif 'client_config' not in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name))
    # client_config = model.properties.get('client_config', {})
    elif not all(x in AZURE_VALID_KEY for x in
                 model.properties.get('client_config', {}).keys()):
        if 'get_input' not in model.properties['client_config'] and \
                'get_secret' not in model.properties['client_config']:
            yield LintProblem(line,
                              None,
                              'Invalid parameters provided for client config. '
                              'Valid parameters are {}'.format(
                                  AZURE_VALID_KEY))


def check_aws_config(model, line):
    if 'aws_config' in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" has deprecated property "aws_config". '
            'please use "client_config".'.format(model.name),
            fixable=True
        )
    elif 'client_config' not in model.properties:
        yield LintProblem(
            line,
            None,
            'The node template "{}" '
            'does not provide required property "client_config".'.format(
                model.name))
    # client_config = model.properties.get('client_config')
    elif not all(x in AWS_VALID_KEY for x in
                 model.properties.get('client_config').keys()):
        if 'get_input' not in model.properties['client_config'] and \
                'get_secret' not in model.properties['client_config']:
            yield LintProblem(line,
                              None,
                              'Invalid parameters provided for client config. '
                              'Valid parameters are {}'.format(AWS_VALID_KEY))


def check_dependent_types(model, line):
    required_relationship_types = REQUIRED_RELATIONSHIPS.get(
        model.node_type, {})
    model.required_relationships = required_relationship_types
    if model.required_relationships_not_met(
            ctx['node_templates'],
            ctx.get('imported_node_templates', {})):
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
        if terratag_config:
            yield from check_terratag(model, line)
        if not any([tflint_config, tfsec_config]):
            # TODO: Update node type.
            yield LintProblem(
                line,
                None,
                'nativeedge.nodes.terraform.Module type should be used '
                'with some policy validation product, such as TF Sec, '
                'or TF Lint.',
                severity=2
            )
        else:
            if tflint_config:
                yield from check_tflint(model, line)
            if tfsec_config:
                yield from check_tfsec(model, line)


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


def check_external_resource(model, line):
    if model.is_external and 'resource_config' in model.properties:
        yield LintProblem(
            line,
            None,
            'resource_config is not required, '
            'when use_external_resource is true.')


def remove_node_type_from_context(node_type):
    if UNUSED_IMPORT_CTX in ctx:
        for import_item in list(ctx[UNUSED_IMPORT_CTX].keys()):
            if node_type in ctx[UNUSED_IMPORT_CTX][import_item]:
                del ctx[UNUSED_IMPORT_CTX][import_item]


def remove_plugin_from_context(plugin_name):
    if UNUSED_IMPORT_CTX in ctx:
        for import_item in list(ctx[UNUSED_IMPORT_CTX].keys()):
            if plugin_name in import_item:
                del ctx[UNUSED_IMPORT_CTX][import_item]


def check_get_attribute(model, line):
    relationships = get_target_list_relationships(model, line)
    for item, value in model.properties.items():
        attribute = find_values_by_key(value, ['get_attribute'])
        for attr in attribute:
            if attr[0] not in relationships:
                yield LintProblem(
                    line,
                    None,
                    "The node template '{name}' uses an intrinsic function "
                    "with target node_template '{target}', but does not "
                    "provide a relationship. Add a relationship under '{name}'"
                    " with target '{target}'."
                    .format(name=model.name, target=attr[0]))


def get_target_list_relationships(model, line):
    if not model.relationships:
        return []
    target_list = []
    for rel in model.relationships:
        target_list.append(rel.get('target'))
    return target_list


def check_supports_tagging(model, line):
    if model.node_type in AWS_TYPE_WITH_TAGS:
        if 'Tags' not in model.properties:
            yield LintProblem(
                line,
                None,
                'The node template {node} with {type} does not provide Tags '
                'parameter in properties. A best practice is to provide Tags.'
                'For example: https://tinyurl.com/yveu36xs'
                .format(node=model.name, type=model.node_type))


def prepre_cyclic_inputs(node_template, edges, line_index, line_number):
    node_name = node_template[0].value
    for item in node_template[1].value:
        if item[0].value == "relationships":
            for subitem in item[1].value:
                relationship_node_name = subitem.value[1][1].value
                edges.append((node_name, relationship_node_name))
    line_index[node_name] = line_number
    return edges, line_index


def check_cyclic_node_dependency(edges, lines_index):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    cycles = nx.simple_cycles(graph)
    for cycle in cycles:
        lines = []
        for node in cycle:
            lines.append(lines_index[node])

        yield LintProblem(
            sorted(lines)[-1],
            None,
            "A dependency loop consistent of {} was identified".format(cycle)
        )


def check_interfaces(model, line):
    if model.interfaces:
        for iface_name, iface_value in model.interfaces.items():
            if isinstance(iface_value, dict):
                for op_name, op_value in iface_value.items():
                    if isinstance(op_value, dict):
                        keys = list(op_value.keys())
                        for k in keys:
                            if k not in ['implementation',
                                         'inputs',
                                         'executor']:
                                yield LintProblem(
                                    line,
                                    None,
                                    f'Operation key {k} '
                                    'is not in schema: '
                                    '[implementation, inputs, executor].'
                                )
                            elif k == 'implementation':
                                if isinstance(op_value[k], str):
                                    if 'fabric.fabric_plugin' in op_value[k]:
                                        remove_plugin_from_context(
                                            'nativeedge-fabric-plugin')
                                    elif 'ansible.ne_ansible' in op_value[k]:
                                        remove_plugin_from_context(
                                            'nativeedge-ansible-plugin')
            if iface_name.startswith('cloudify.'):
                yield LintProblem(
                    line,
                    None,
                    "deprecated interfaces. "
                    f"Replace usage of {iface_name} with "
                    f"{iface_name.replace('cloudify', 'nativeedge')}."
                )


def check_relationships(model, line):
    if model.relationships:
        for data in model.relationships:
            for key, value in data.items():
                if key not in ['target',
                               'type',
                               'source_interfaces',
                               'target_interfaces']:
                    yield LintProblem(
                        line,
                        None,
                        f'Interface key {key} '
                        'is not in schema: '
                        '[target, type, source_interfaces, '
                        'target_interfaces].'
                    )
                elif isinstance(value, str) and value.startswith('cloudify.'):
                    yield LintProblem(
                        line,
                        None,
                        "deprecated relationships. "
                        f"Replace usage of {value} with "
                        f"{value.replace('cloudify', 'nativeedge')}."
                    )


def transform_string(value):
    if isinstance(value, str):
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
    return value


def check_if_properties_are_valid(model, prop_name, valid_props, line):
    # Check if the property is not expected.
    if prop_name not in valid_props:
        yield LintProblem(
            line,
            None,
            f'The node template "{model.name}" has '
            f'an invalid property "{prop_name}". '
            f'It must be one of '
            f'{", ".join(list(valid_props.keys()))}'
        )
    else:
        prop_data_type_name = valid_props[prop_name].get('type')
        # Check if the plugin defines the node template property type.
        prop_value = transform_string(model.properties[prop_name])

        if not prop_data_type_name:
            # No is does not.
            return
        if prop_data_type_name in PROPERTY_TYPES:
            if isinstance(prop_value, dict):
                prop_key, input_name, input_type = lint_dsl_fn(
                    prop_value,
                    prop_data_type_name)
                if all([prop_key, input_name, input_type]) and \
                        input_type != prop_data_type_name:
                    yield LintProblem(
                        line, None,
                        f'The node template "{model.name}" '
                        'has an invalid property '
                        f'"{prop_name}". The intrinsic '
                        f'function "{prop_key}" has the '
                        f'target input "{input_name}", which '
                        'declares a type '
                        f'"{input_type}" but '
                        'the node property is expected to be '
                        f'of the type "{prop_data_type_name}".'
                    )
                    return
                elif any([prop_key, input_name, input_type]):
                    return
            expected_prop_type_index = PROPERTY_TYPES.index(
                prop_data_type_name)
            expected_prop_type_obj = PROPERTY_TYPES_Z[expected_prop_type_index]
            prop_type = actual_prop_value_obj = type(prop_value)
            if actual_prop_value_obj in PROPERTY_TYPES_Z:
                actual_prop_type_index = PROPERTY_TYPES_Z.index(
                    actual_prop_value_obj)
                prop_type = PROPERTY_TYPES[actual_prop_type_index]
            if prop_data_type_name == 'integer' and \
                    isinstance(prop_value, str) and prop_value.isdigit():
                pass
            elif not isinstance(prop_value, expected_prop_type_obj):
                yield LintProblem(
                    line,
                    None,
                    f'The node template "{model.name}" has an invalid '
                    f'property "{prop_name}". The value '
                    f'"{prop_value}" is actually of type '
                    f'"{prop_type}". The expected type is '
                    f'"{prop_data_type_name}".'
                )
        else:
            # Check if the data type has a definition.
            data_type_properties = ctx['data_types'].get(
                prop_data_type_name, {})
            prop_value = transform_string(model.properties[prop_name])
            prop_type = type(prop_value)
            prop_type_index = PROPERTY_TYPES_Z.index(prop_type)
            prop_type_dsl_name = PROPERTY_TYPES[prop_type_index]
            if not isinstance(prop_value, dict):
                yield LintProblem(
                    line,
                    None,
                    f'The node template "{model.name}" has an invalid '
                    f'property "{prop_name}". The value '
                    f'"{prop_value}" is actually of type '
                    f'"{prop_type_dsl_name}". The expected type is a dict '
                    'representation of the custom data type '
                    f'"{prop_data_type_name}".'
                )
                return

            # The data type is not a basic data type.
            for sub_prop_name in prop_value.keys():
                prop_key, input_name, input_type = lint_dsl_fn(
                    prop_value,
                    prop_data_type_name)
                if all([prop_key, input_name, input_type]):
                    if input_type != 'dict':
                        yield LintProblem(
                            line,
                            None,
                            f'The node template "{model.name}" has '
                            f'an invalid property "{prop_name}". '
                            f'The intrinsic function "{prop_key}" '
                            f'has the target input "{input_name}", '
                            'which declares a type '
                            f'"{input_type}" but the '
                            'node property is expected to be a dict '
                            'representation of the custom data type '
                            f'"{prop_data_type_name}".'
                        )
                    continue
                if sub_prop_name not in data_type_properties:
                    yield LintProblem(
                        line, None,
                        f'The node template "{model.name}" has '
                        f'an invalid property "{prop_name}". '
                        f'The key "{sub_prop_name}" must be one of '
                        f'{", ".join(list(data_type_properties.keys()))}'
                    )
                else:
                    parameter_type = data_type_properties[sub_prop_name].get(
                        "type")
                    if parameter_type:
                        sub_prop_value = transform_string(
                            prop_value[sub_prop_name])
                        prop_type_index = PROPERTY_TYPES_Z.index(
                            type(sub_prop_value))
                        prop_type_value = PROPERTY_TYPES[prop_type_index]
                        if parameter_type == 'integer' and \
                                isinstance(sub_prop_value, str) and \
                                sub_prop_value.isdigit():
                            pass
                        elif parameter_type != prop_type_value and \
                                prop_type_value != 'dict':
                            yield LintProblem(
                                line,
                                None,
                                f'The node template "{model.name}" has an '
                                f'invalid property "{prop_name}". The key '
                                f'"{sub_prop_name}" is actually of type '
                                f'"{prop_type_value}". '
                                f'The expected type is {parameter_type}.'
                            )
                        elif prop_type_value == 'dict':
                            prop_key, input_name, input_type = lint_dsl_fn(
                                prop_value[sub_prop_name],
                                prop_type_value)
                            if all([prop_key, input_name, input_type]) and \
                                    parameter_type != input_type:
                                yield LintProblem(
                                    line, None,
                                    f'The node template "{model.name}" '
                                    'has an invalid property '
                                    f'"{prop_name}.{sub_prop_name}". The '
                                    f'intrinsic function "{prop_key}" has the '
                                    f'target input "{input_name}", which '
                                    'declares a type '
                                    f'"{input_type}" but '
                                    'the node property is expected to be '
                                    f'of the type "{parameter_type}".'
                                )


def check_properties(model, line):
    if not model.properties:
        return
    node_type_properties = ctx['node_types_props'].get(model.node_type, {})
    valid_properties = node_type_properties.get('properties', {})
    if valid_properties:
        for k in model.properties.keys():
            yield from check_if_properties_are_valid(
                model, k, valid_properties, line)


def lint_dsl_fn(prop_value, prop_data_type_name):
    prop_key = None
    input_name = None
    input_type = None
    for prop_key in prop_value.keys():
        if prop_key in INTRINSIC_FNS:
            if prop_key == 'get_input':
                input_name = prop_value.get(prop_key)
                if isinstance(input_name, str):
                    input_def = ctx['inputs'][input_name]
                    if input_def and 'type' in input_def:
                        if isinstance(input_def, dict) and \
                                input_def['type'] != prop_data_type_name:
                            input_type = input_def['type']
                        elif input_def["type"].value != prop_data_type_name:
                            input_type = input_def["type"].value
    if isinstance(input_type, ScalarNode):
        input_type = input_type.value
    return (prop_key, input_name, input_type)
