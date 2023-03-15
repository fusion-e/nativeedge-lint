########
# Copyright (c) 2014-2023 Cloudify Platform Ltd. All rights reserved
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

CONCAT = 'concat'
GET_INPUT = 'get_input'
GET_SECRET = 'get_secret'
GET_PROPERTY = 'get_property'
GET_ATTRIBUTE = 'get_attribute'
GET_CAPABILITY = 'get_capability'
GET_ENVIRONMENT_CAPABILITY = 'get_environment_capability'
INSTRINSIC_FUNCTIONS = [
    CONCAT,
    GET_INPUT,
    GET_SECRET,
    GET_PROPERTY,
    GET_ATTRIBUTE,
    GET_CAPABILITY,
    GET_ENVIRONMENT_CAPABILITY
]
