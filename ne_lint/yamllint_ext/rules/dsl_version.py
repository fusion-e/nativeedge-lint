# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext import LintProblem

from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import process_relevant_tokens, context

VALUES = []

ID = 'dsl_version'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}

# TODO: Determine if we lint Cloudify versions.
LINTING_VERSIONS = ['cloudify_dsl_1_3', 'cloudify_dsl_1_4', 'cloudify_dsl_1_5']
INVALID_3_1 = [
    'blueprint_id',
    'deployment_id',
    'capability_value',
    'scaling_group',
    'secret_key',
    'node_id',
    'node_type',
    'node_instance'
]


@process_relevant_tokens(NENode, ['tosca_definitions_version', 'type'])
def check(token=None, **_):
    if token.prev and token.prev.node.value == 'tosca_definitions_version':
        context['dsl_version'] = token.node.value
        yield from validate_supported_dsl_version(token.node.value, token.line)
    if token.prev and token.prev.node.value == 'type':
        yield from validate_dsl_version_31(
            token.node.value, token.line, context.get('dsl_version'))


def validate_supported_dsl_version(value, line):
    if value not in LINTING_VERSIONS:
        yield LintProblem(
            line,
            None,
            "dsl_version not supported: {} ".format(value)
        )


def validate_dsl_version_31(value, line, dsl_version):
    if dsl_version and value in INVALID_3_1:
        yield LintProblem(
            line,
            None,
            "invalid type for {}: {} ".format(dsl_version, value)
        )
