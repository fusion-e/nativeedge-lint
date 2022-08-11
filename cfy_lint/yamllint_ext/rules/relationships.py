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
from .. import LintProblem

from . import constants
from ..generators import CfyNode
from .node_templates import recurse_node_template
from ..utils import process_relevant_tokens

VALUES = []

ID = 'relationships'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
LIFECYCLE_OPS = {'preconfigure', 'postconfigure', 'establish', 'unlink'}
OP_KEYS = {'implementation', 'inputs'}


@process_relevant_tokens(CfyNode, 'relationships')
def check(token=None, **_):
    # raise Exception(token.node)
    relationship_type = CfyRelationshipType(token.node)
    if relationship_type.is_relationship_type:
        yield from check_relationship_types(relationship_type, token.line)
        return
    yield from relationships_not_list(token.node, token.line)
    for list_item in token.node.value:
        if isinstance(list_item, tuple) or isinstance(
                list_item.value, dict):
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
                constants.deprecated_relationship_types[type_name]))


def relationships_not_list(node, line):
    if not isinstance(node, yaml.nodes.SequenceNode):
        yield LintProblem(
            line,
            None,
            "relationships block must be a list. "
            "The provided type is {}".format(type(node.value).mro()[0])
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


class CfyRelationshipType(object):

    def __init__(self, node):
        self._node = node
        self._is_relationship_type = None
        self._name = None
        self.parsed = recurse_node_template(self._node)

        try:
            for k, v in self.parsed.items():
                self.name = k
                self.definition = v or {}
                break
        except (AttributeError, ValueError, KeyError):
            self.is_relationship_type = False
        else:
            self.is_relationship_type = True
            self.derived_from = self.definition.get('derived_from')
            self.connection_type = self.definition.get('connection_type')
            self.source_interfaces = self.definition.get('source_interfaces')
            self.target_interfaces = self.definition.get('target_interfaces')

    @property
    def interfaces(self):
        return [CfyRelationshipInterface(self.source_interfaces),
                CfyRelationshipInterface(self.target_interfaces)]


class CfyRelationshipInterfaces(object):
    def __init__(self, source, target):
        self.source = CfyRelationshipInterface(source)
        self.target = CfyRelationshipInterface(target)


class CfyRelationshipInterface(object):

    def __init__(self, data):
        self._data = data or {}

    @property
    def lifecycle(self):
        return self._data.get('cloudify.interfaces.relationship_lifecycle')


def check_relationship_types(relationship_type, line):
    if not relationship_type.name.startswith('cloudify.relationships.'):
        yield LintProblem(
            line,
            None,
            'relationship type name "{}" should '
            'start with "cloudify.relationships."'.format(
                relationship_type.name)
        )
    for interface in relationship_type.interfaces:
        if interface.lifecycle:
            keys = interface.lifecycle.keys()
            if not set(keys).issubset(LIFECYCLE_OPS):
                unexpected = set(keys) - LIFECYCLE_OPS
                yield LintProblem(
                    line,
                    None,
                    'unexpected {} in cloudify.interfaces.lifecycle: '
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
