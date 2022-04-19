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


class CloudifyDSLObject(object):
    pass


class NodeTemplate(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def node_type(self):
        return self.data.get('type', {})

    def properties(self):
        return self.data.get('properties', {})

    def interfaces(self):
        return self.data.get('interfaces', {})

    def relationships(self):
        return self.data.get('relationships', [])
