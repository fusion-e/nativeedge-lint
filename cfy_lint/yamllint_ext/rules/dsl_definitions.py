# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml

from cfy_lint.yamllint_ext import LintProblem

from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.utils import process_relevant_tokens

VALUES = []

ID = 'dsl_definitions'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, ['dsl_definitions'])
def check(token=None, **_):
    for dsl_definition in token.node.value:
        if not isinstance(dsl_definition[0].value,
                          str) or dsl_definition[0].value.isdigit():
            yield LintProblem(
                token.line,
                None,
                'dsl definition should be a string and '
                'should not start with a numeric character: {}'
                .format(dsl_definition[0].value)
            )
        if not isinstance(dsl_definition[1], yaml.nodes.MappingNode):
            yield LintProblem(
                token.line,
                None,
                'dsl definition {} content must be a dict: {}'
                .format(dsl_definition[0].value,
                        type(dsl_definition[1].value))
            )
