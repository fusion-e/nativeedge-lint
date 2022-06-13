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

from yamllint.rules import _RULES as ruleset

from . import dsl_version
from . import relationships

_CLOUDIFY_RULES = {
    dsl_version.ID: dsl_version,
    relationships.ID: relationships
}
ruleset.update(_CLOUDIFY_RULES)


def get(_id):
    if _id not in ruleset:
        raise ValueError('no such rule: "%s"' % _id)

    return ruleset[_id]
