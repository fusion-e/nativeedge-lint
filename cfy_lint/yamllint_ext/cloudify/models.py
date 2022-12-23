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


class CloudifyDSLObject(object):

    def __init__(self, tokens=None):
        self._tokens = tokens or []

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    def seek(self, token_class, index):
        while True:
            try:
                if isinstance(self.tokens[index], token_class):
                    return index
            except IndexError:
                return
            index += 1


class NodeTemplate(object):
    def __init__(self, name):
        self.name = name
        self._type = None
        self._properties = None
        self._interfaces = None
        self._relationships = []
        self._line = None
        self._required_relationships = {}
        self._relationships_mapping = {}
        self._unsatisfied_relationships = {}

    @property
    def node_type(self):
        return self._type

    @node_type.setter
    def node_type(self, value):
        self._type = value

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def interfaces(self):
        return self._interfaces

    @interfaces.setter
    def interfaces(self, value):
        self._interfaces = value

    @property
    def relationships(self):
        return self._relationships

    @relationships.setter
    def relationships(self, value):
        self._relationships = value

    def set_values(self, values):
        if 'type' in values:
            self.node_type = values['type']
        if 'properties' in values:
            self.properties = values['properties']
        if 'interfaces' in values:
            self.interfaces = values['interfaces']
        if 'relationships' in values:
            self.relationships = values['relationships']

    @property
    def dict(self):
        return {
            self.name: {
                'type': self.node_type,
                'properties': self.properties,
                'interfaces': self.interfaces,
                'relationships': self.relationships
            }
        }

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    @property
    def required_relationships(self):
        return self._required_relationships or {}

    @required_relationships.setter
    def required_relationships(self, value):
        self._required_relationships = value

    def required_relationships_not_met(self,
                                       node_templates=None,
                                       imported=None):
        node_templates = node_templates or {}
        if imported:
            for k, v in imported.items():
                node_templates[k] = NodeTemplate(v)
        if not self._relationships_mapping:
            for relationship in self.relationships:
                if isinstance(relationship, dict):
                    rel_type = relationship.get('type')
                    rel_target_name = relationship.get('target')
                    rel_target = node_templates.get(
                        rel_target_name, UnknownNodeType(rel_target_name))
                    self._relationships_mapping[rel_target.node_type] = \
                        rel_type
        for k, v in self.required_relationships.items():
            if k not in self._relationships_mapping or v != \
                    self._relationships_mapping[k]:
                self._unsatisfied_relationships[k] = v
        return self._unsatisfied_relationships.items()

    @property
    def required_relationships_message(self):
        messages = []
        for k, v in self.required_relationships_not_met():
            messages.append(
                'relationship type {} to a node type {}'.format(v, k))
        return 'The node template {} has unsatisfied required relationships' \
               ', which have not been provided: {}.'.format(
                   self.name, ', '.join(messages))


class RelationshipsList(CloudifyDSLObject):

    kind = 'relationships'

    def __init__(self, current, tokens):
        self.current = current
        super().__init__(tokens)
        self._relationship_items = []

    def setup(self):
        index = 0
        limit = len(self.tokens)
        while not index >= limit:
            if isinstance(self.tokens[index],
                          yaml.tokens.BlockMappingStartToken):
                block_end = self.seek(yaml.tokens.BlockEndToken, index + 1)
                if block_end:
                    self._relationship_items.append(
                        [RelationshipItem(self.tokens[index:block_end])])
                index = block_end
            else:
                index += 1

    @property
    def relationship_items(self):
        return self._relationship_items


class RelationshipItem(CloudifyDSLObject):
    kind = ('type', 'target')

    def __init__(self, tokens):
        self._type = None
        self._target = None
        super().__init__(tokens)
        self.setup()

    def setup(self):
        index = 0
        limit = len(self.tokens)
        while not self._type and not self._target:
            if index >= limit:
                break
            if isinstance(self.tokens[index], yaml.tokens.ScalarToken):
                if isinstance(self.tokens[index + 2], yaml.tokens.ScalarToken):
                    if self.tokens[index].value == 'type':
                        self._type = self.tokens[index + 2]
                    elif self.tokens[index].value == 'target':
                        self._target = self.tokens[index + 2]
            index += 1

    def validate(self):
        return self._type and self._target


class UnknownNodeType(NodeTemplate):
    def __init__(self, name):
        super().__init__(name)
        self.node_type = 'Unknown Node Type'
