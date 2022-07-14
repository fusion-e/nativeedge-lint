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

import yaml
from urllib.parse import urlparse

from .. import LintProblem

from ..generators import CfyNode

VALUES = []

ID = 'imports'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


def check(conf=None,
          token=None,
          prev=None,
          next=None,
          nextnext=None,
          context=None):
    if isinstance(token, CfyNode):
        line = token.node.start_mark.line + 1
        if not token.prev or not token.prev.node.value == 'imports':
            return
        for import_item in token.node.value:
            if not isinstance(import_item, yaml.nodes.ScalarNode):
                yield LintProblem(line, None, 'import is not a string.')
            url = urlparse(import_item.value)
            if url.scheme not in ['http', 'https', 'plugin']:
                if not url.scheme and url.path.split('/')[-1].endswith('.yaml'):
                    continue
                yield LintProblem(
                    line,
                    None,
                    'invalid import. {}'.format(url)
                )

            elif url.scheme in ['https', 'https'] and not url.path.endswith('.yaml'):
                yield LintProblem(
                    line,
                    None,
                    'invalid import. {}'.format(url)
                )
