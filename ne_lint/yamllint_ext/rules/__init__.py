# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from yamllint.rules import _RULES as ruleset

from . import inputs
from . import labels
from . import imports
from . import interfaces
from . import node_types
from . import dsl_version
from . import capabilities
from . import relationships
from . import node_templates
from . import dsl_definitions
from . import blueprint_labels

_RULES = {
    inputs.ID: inputs,
    labels.ID: labels,
    imports.ID: imports,
    node_types.ID: node_types,
    dsl_version.ID: dsl_version,
    capabilities.ID: capabilities,
    relationships.ID: relationships,
    node_templates.ID: node_templates,
    dsl_definitions.ID: dsl_definitions,
    blueprint_labels.ID: blueprint_labels
}
ruleset.update(_RULES)


def get(_id):
    if _id not in ruleset:
        raise ValueError('no such rule: "%s"' % _id)
    return ruleset[_id]
