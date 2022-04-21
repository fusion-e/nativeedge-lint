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
        self._relationships = None

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
