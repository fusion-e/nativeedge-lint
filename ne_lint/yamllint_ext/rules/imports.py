# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import os
import re
import yaml
from packaging import version
from urllib.parse import urlparse

from ne_lint.yamllint_ext import LintProblem

from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import (
    context as ctx,
    process_relevant_tokens
)

VALUES = []

ID = 'imports'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(NENode, 'imports')
def check(token=None, **_):
    for import_item in token.node.value:
        yield from validate_string(import_item, token.line)
        yield from validate_import_items(import_item, token)
        yield from unused_imports(import_item, token)
        token.line = token.line + 1


def validate_import_items(item, token):
    try:
        url = urlparse(item.value)
    except AttributeError:
        url = None
    # if not url:
    #     yield LintProblem(
    #         token.line,
    #         None,
    #         f'Invalid value for import item: {item.value}.'
    #     )
    if url and url.scheme not in ['http', 'https', 'plugin']:
        if not url.scheme and url.path.split('/')[-1].endswith('.yaml'):
            # TODO: Do we need to be backward compatible here?
            if url.path not in ['nativeedge/types/types.yaml',
                                'cloudify/types/types.yaml']:
                import_path = os.path.join(token.blueprint_path, url.path)
                if not os.path.exists(import_path):
                    yield LintProblem(
                        token.line,
                        None,
                        'relative import "- {}" declared, '
                        'but the file path does not exist.'.format(url.path)
                    )
        else:
            yield LintProblem(
                token.line,
                None,
                'invalid import. {} scheme not accepted'.format(url.scheme)
            )
    if url and url.scheme in ['plugin'] and url.path in [
            'nativeedge-openstack-plugin',
            'cloudify-openstack-plugin']:
        yield from check_openstack_plugin_version(url, token.line)
    elif url and url.scheme in ['https', 'https'] and not \
            url.path.endswith('.yaml'):
        yield LintProblem(
            token.line,
            None,
            'invalid import. {}'.format(url)
        )
    elif url and url.scheme in ['https', 'https']:
        yield from validate_imported_dsl_version(
            token.line, ctx.get('dsl_version', ''),
            ctx.get('imported_tosca_definitions_version'))


def validate_string(item, line):
    if isinstance(item, yaml.nodes.MappingNode) and \
            item.value[0][0].value == 'plugin':
        # This will be caught in validate mapping
        pass
    elif not isinstance(item, yaml.nodes.ScalarNode):
        yield LintProblem(line, None, 'import is not a string.')


def check_openstack_plugin_version(url, line):
    version_openstack = url.query.split(',')
    if version_openstack[0]:
        for str_version in version_openstack:
            only_version = re.findall('(\\d+.\\d+.\\d+)', str_version)
            if version.parse(only_version[0]) >= version.parse('3.0.0') and \
                    "<=" not in str_version:
                return
        yield LintProblem(
            line, None,
            f'The Openstack Plugin version {version_openstack}'
            ' is deprecated. Please update to Openstack version 3 or higher.')


def validate_imported_dsl_version(line, dsl_version, imported_dsl):
    if isinstance(imported_dsl, list):
        imported_dsl = imported_dsl.pop(0)
    for dsl in imported_dsl:
        if dsl not in dsl_version:
            yield LintProblem(
                line,
                None,
                "imports dsl version doesn't match blueprint {}: {} ".format(
                    dsl_version, imported_dsl)
            )


def unused_imports(item, token):
    if 'post_processing_problems' not in ctx:
        ctx['post_processing_problems'] = {}
    problem = LintProblem(
        token.line,
        None,
        'unused import item: {}'.format(item.value)
    )
    try:
        ctx['post_processing_problems'].update({item.value: problem})
    except TypeError:
        pass
    if False:
        yield problem
