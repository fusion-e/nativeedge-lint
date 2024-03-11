# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext import LintProblem

from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import process_relevant_tokens, context

VALUES = []

ID = 'dsl_version'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}

LINTING_VERSIONS = ['nativeedge_1_0']


@process_relevant_tokens(NENode, ['tosca_definitions_version', 'type'])
def check(token=None, **_):
    if token.prev and token.prev.node.value == 'tosca_definitions_version':
        context['dsl_version'] = token.node.value
        yield from validate_supported_dsl_version(token.node.value, token.line)
    if token.prev and token.prev.node.value == 'type':
        pass


def validate_supported_dsl_version(value, line):
    if value not in LINTING_VERSIONS:
        yield LintProblem(
            line,
            None,
            f'{value} is not a supported DSL Version. '
            f'Only these versions are supported: {LINTING_VERSIONS}'
        )
