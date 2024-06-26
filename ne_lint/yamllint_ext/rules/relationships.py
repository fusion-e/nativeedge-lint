# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml
from ne_lint.yamllint_ext import LintProblem

from ne_lint.yamllint_ext.rules import constants
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    recurse_get_readable_object
)

VALUES = []

ID = 'relationships'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
LIFECYCLE_OPS = {'preconfigure', 'postconfigure', 'establish', 'unlink'}
OP_KEYS = {'implementation', 'inputs'}


@process_relevant_tokens(NENode, 'relationships')
def check(token=None, **_):
    relationship_type = NERelationshipType(token.node)
    if relationship_type.malformed_relationship:
        yield from relationships_not_list(token.node, token.line)
    if relationship_type.is_relationship_type:
        yield from check_relationship_types(relationship_type, token.line)
    for list_item in token.node.value:
        if isinstance(list_item, tuple) or \
                isinstance(list_item.value, dict):
            yield from relationship_not_dict(list_item)
            continue
        is_target = False
        is_type = False
        for tup in list_item.value:
            if not len(tup) == 2:
                yield LintProblem(
                    list_item.value.start_mark.line + 1,
                    None,
                    "relationship dict must contain two entries, "
                    "type and target "
                    "The provided type is {}".format(type(len(tup)))
                )
            if tup[0].value == 'target':
                is_target = True
                yield from relationship_target_not_exist(
                    token, tup[1].value, tup[1].start_mark.line)
            elif tup[0].value == 'type':
                is_type = True
                yield from deprecated_type(
                    tup[1].value, tup[1].end_mark.line)
        yield from no_type(is_type, tup[1].start_mark.line)
        yield from no_target(is_target, tup[1].start_mark.line)


def no_type(type_bool, line):
    if not type_bool:
        yield LintProblem(
            line,
            None,
            "no relationship type provided. "
        )


def no_target(target, line):
    if not target:
        yield LintProblem(
            line,
            None,
            "no relationship target provided. "
        )


def deprecated_type(type_name, line):
    if type_name in constants.deprecated_relationship_types:
        yield LintProblem(
            line,
            None,
            "deprecated relationship type. "
            "Replace usage of {} with {}.".format(
                type_name,
                constants.deprecated_relationship_types[type_name]),
            fixable=True)


def get_yaml_type(node):
    if isinstance(node, yaml.nodes.MappingNode):
        return type(dict())
    return type(node.value).mro()[0]


def relationships_not_list(node, line):
    if not isinstance(node, yaml.nodes.SequenceNode):
        relationship_type = get_yaml_type(node)
        yield LintProblem(
            line,
            None,
            "relationships block must be a list. "
            "The provided type is {}".format(relationship_type)
        )


def relationship_not_dict(list_item):
    if not isinstance(list_item, yaml.nodes.MappingNode):
        if isinstance(list_item, tuple):
            yield LintProblem(
                list_item[0].start_mark.line,
                None,
                "relationship must be a dict. "
                "The provided type is {}".format(type(list_item).mro()[0])
            )
        else:
            yield LintProblem(
                list_item.start_mark.line,
                None,
                "relationship must be a dict. "
                "The provided type is {}".format(type(list_item).mro()[0])
            )


def relationship_target_not_exist(token, target, line):
    if target not in token.node_templates:
        yield LintProblem(
            line,
            None,
            "relationship target node instance does not exist. "
            "The provided target is {}. Possible options are: {}.".format(
                target,
                [k for k in token.node_templates.keys()])
        )


class NERelationshipType(object):

    def __init__(self, node):
        self._node = node
        self._is_relationship_type = None
        self._name = None
        self.parsed = recurse_get_readable_object(self._node)
        self.derived_from = None
        self.connection_type = None
        self.source_interfaces = None
        self.target_interfaces = None
        self.malformed_relationship = False

        try:
            for k, v in self.parsed.items():
                self.name = k
                self.definition = v or {}
                break
        except (AttributeError, ValueError, KeyError):
            self.is_relationship_type = False
        else:
            self.is_relationship_type = True
            if isinstance(self.definition, dict):
                self.derived_from = self.definition.get('derived_from')
                self.connection_type = self.definition.get('connection_type')
                self.source_interfaces = self.definition.get(
                    'source_interfaces')
                self.target_interfaces = self.definition.get(
                    'target_interfaces')
            else:
                self.malformed_relationship = True

    @property
    def interfaces(self):
        return [NERelationshipInterface(self.source_interfaces),
                NERelationshipInterface(self.target_interfaces)]


class NERelationshipInterfaces(object):
    def __init__(self, source, target):
        self.source = NERelationshipInterface(source)
        self.target = NERelationshipInterface(target)


class NERelationshipInterface(object):

    def __init__(self, data):
        self._data = data or {}

    @property
    def lifecycle(self):
        # TODO: This will need to be nativeedge.
        return self._data.get('nativeedge.interfaces.relationship_lifecycle')


def check_relationship_types(relationship_type, line):
    # TODO: This will need to be nativeedge.
    if not relationship_type.name.startswith('nativeedge.relationships.'):
        yield LintProblem(
            line,
            None,
            'relationship type name "{}" should '
            'start with "nativeedge.relationships."'.format(
                relationship_type.name)
        )
    for interface in relationship_type.interfaces:
        if interface.lifecycle:
            keys = interface.lifecycle.keys()
            if not set(keys).issubset(LIFECYCLE_OPS):
                unexpected = set(keys) - LIFECYCLE_OPS
                # TODO: This will need to be nativeedge.
                yield LintProblem(
                    line,
                    None,
                    'unexpected {} in nativeedge.interfaces.lifecycle: '
                    '{}'.format(
                        'operation' if len(unexpected) == 1 else 'operations',
                        unexpected
                    )
                )
            for op in LIFECYCLE_OPS:
                keys = interface.lifecycle.get(op, {}).keys()
                if not set(keys).issubset(OP_KEYS):
                    unexpected = set(keys) - OP_KEYS
                    yield LintProblem(
                        line,
                        None,
                        'unexpected key in {} operation definition: {}'.format(
                            op, unexpected
                        )
                    )
                elif op in interface.lifecycle.keys() and \
                        'implementation' not in keys:
                    yield LintProblem(
                        line,
                        None,
                        '{} operation definition does not declare '
                        'required implementation'.format(op)
                    )
