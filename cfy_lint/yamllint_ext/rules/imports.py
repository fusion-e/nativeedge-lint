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

import os
import re
import yaml
from packaging import version
from urllib.parse import urlparse

from .. import LintProblem

from ..generators import CfyNode
from ..utils import process_relevant_tokens

VALUES = []

ID = 'imports'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, 'imports')
def check(token=None, **_):
    for import_item in token.node.value:
        yield from validate_string(import_item, token.line)
        yield from validate_import_items(import_item, token.line)


def validate_import_items(item, line):

    url = urlparse(item.value)

    if url.scheme not in ['http', 'https', 'plugin']:
        if not url.scheme and url.path.split('/')[-1].endswith('.yaml'):
            if not os.path.exists(url.path) and \
                    url.path != 'cloudify/types/types.yaml':
                yield LintProblem(
                    line,
                    None,
                    'relative import '
                    'declared but the file path does not exist.'
                )
        else:
            yield LintProblem(
                line,
                None,
                'invalid import. {} scheme not accepted'.format(url.scheme)
            )
    if url.scheme in ['plugin'] and url.path in ['cloudify-openstack-plugin']:
        yield from check_openstack_plugin_version(url, line)
    elif url.scheme in ['https', 'https'] and not url.path.endswith('.yaml'):
        yield LintProblem(
            line,
            None,
            'invalid import. {}'.format(url)
        )


def validate_string(item, line):
    if not isinstance(item, yaml.nodes.ScalarNode):
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
            'Cloudify Openstack Plugin version {} is deprecated.'
            ' Please update to Openstack version 3 or higher. '
            'Below are suggested node type changes.'
            ' For more information on conversion to Openstack Plugin v3, '
            'Please click on this link - https://docs.cloudify.co/latest/'
            'working_with/official_plugins/infrastructure/openstackv3/'
            .format(version_openstack))
