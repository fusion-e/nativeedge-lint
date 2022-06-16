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

VALUES = []

ID = 'relationships'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


def check(conf=None, token=None, prev=None, next=None, nextnext=None, context=None):

    if isinstance(token, CfyNode):
        line = token.node.start_mark.line + 1
        if not token.prev or not token.prev.node.value == 'relationships':
            return
        elif token.prev_prev:
            print('this {} {}'.format(vars(token), vars(token.prev_prev)))
        if CfyRelationshipType(token.node).is_relationship_type:
            yield from check_relationship_types()
            return
        yield from relationships_not_list(token.node, line)
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
                        tup[1].value, tup[1].start_mark.line)
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
        self.is_relationship_type = False
        if isinstance(node, yaml.nodes.MappingNode) and isinstance(
                node.value, list) and len(node.value) == 1:
            if isinstance(node.value[0], tuple) and len(node.value[0]) == 2:
                if isinstance(node.value[0][0], yaml.nodes.ScalarNode) and \
                        isinstance(node.value[0][1], yaml.nodes.MappingNode):
                    if node.value[0][0].value == 'derived_from':
                        self.is_relationship_type = True


def check_relationship_types():
    pass
