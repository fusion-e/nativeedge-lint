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

from . import inputs
from . import imports
from . import node_types
from . import dsl_version
from . import capabilities
from . import relationships
from . import node_templates
from . import dsl_definitions

_CLOUDIFY_RULES = {
    inputs.ID: inputs,
    imports.ID: imports,
    node_types.ID: node_types,
    dsl_version.ID: dsl_version,
    capabilities.ID: capabilities,
    relationships.ID: relationships,
    node_templates.ID: node_templates,
    dsl_definitions.ID: dsl_definitions
}
ruleset.update(_CLOUDIFY_RULES)


def get(_id):
    if _id not in ruleset:
        raise ValueError('no such rule: "%s"' % _id)
    return ruleset[_id]
