# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml

from ne_lint.yamllint_ext import LintProblem
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    recurse_mapping,
    context as ctx
)

VALUES = []

ID = 'capabilities'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(NENode, ['outputs', 'capabilities'])
def check(token=None, **_):
    for item in token.node.value:
        if token.prev.node.value == 'outputs':
            output_obj = NEOutput(item)
            if not output_obj.name and not output_obj.mapping:
                continue
        elif token.prev.node.value == 'capabilities':
            output_obj = NECapability(item)
            if not output_obj.name and not output_obj.mapping:
                continue
        if output_obj.not_output():
            continue
        if isinstance(output_obj, NEOutput):
            ctx['outputs'].update(output_obj.__dict__())
        else:
            ctx['capabilities'].update(output_obj.__dict__())
        desig = 'output' if token.prev.node.value == 'outputs' \
            else 'capability'
        if not output_obj.value:
            yield LintProblem(
                token.line, None,
                '{} {} does not provide a value.'.format(
                    desig, output_obj.name)
            )
        if not output_obj.description:
            yield LintProblem(
                token.line, None,
                '{} {} does not provide a description.'.format(
                    desig, output_obj.name)
            )


class NEOutput(object):
    def __init__(self, nodes):
        self.name, self.mapping = self.get_name_mapping(nodes)
        if self.name and self.mapping:
            for key in list(self.mapping.keys()):
                if key not in ['description', 'value']:
                    del self.mapping[key]
            self.value = self.mapping.get('value')
            self.description = self.mapping.get('description')

    def get_name_mapping(self, nodes):
        return get_output(nodes)

    def not_output(self):
        return all([not k for k in self.mapping.values()])

    def __dict__(self):
        return {
            self.name: self.mapping
        }


class NECapability(NEOutput):

    def get_name_mapping(self, nodes):
        return get_capability(nodes)

    def not_capability(self):
        return all([not k for k in self.mapping.values()])


def get_capability(nodes):
    if len(nodes) != 2:
        name = None
        mapping = None
    else:
        name = get_node_name(nodes[0])
        mapping = get_capability_mapping(nodes[1])
    return name, mapping


def get_output(nodes):
    if len(nodes) != 2:
        name = None
        mapping = None
    else:
        name = get_node_name(nodes[0])
        mapping = get_capability_mapping(nodes[1])
    return name, mapping


def get_node_name(node):
    if isinstance(node, yaml.nodes.ScalarNode):
        return node.value


def get_capability_mapping(node):
    mapping = {
        'description': None,
        'value': None,
    }
    if isinstance(node, yaml.nodes.MappingNode):
        for tup in node.value:
            if not len(tup) == 2:
                continue
            mapping_name = tup[0].value
            mapping_value = get_mapping_value(mapping_name, tup[1].value)
            mapping[mapping_name] = mapping_value
    return mapping


def get_mapping_value(name, value):
    if name not in ['value']:
        return value
    else:
        return recurse_mapping(value)
