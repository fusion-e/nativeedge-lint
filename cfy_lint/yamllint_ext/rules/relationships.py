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
from .. import LintProblem

from . import constants

VALUES = []

ID = 'relationships'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


def check(conf, token, prev, next, nextnext, context):

    def skip():
        return not context.get('current_level') != 'node_templates' or \
                context.get('node_template_level') != ID

    if skip():
        return

    state = 'State: {}'.format(
        {
            'prev': prev,
            'token': token,
            'next': next,
            'nextnext': nextnext,
            'context': context
        }
    )
    if not isinstance(token, yaml.tokens.ScalarToken):
        return
    if token.value == ID:
        if not isinstance(nextnext, constants.ACCEPTED_LIST_TYPES):
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                "relationship must be a list. "
                "The provided type was {}.".format(type(nextnext))
            )
    elif token.value in constants.deprecated_relationship_types:
        yield LintProblem(
            token.start_mark.line + 1,
            token.start_mark.column + 1,
            "deprecated relationship type. "
            "Replace usage of {} with {}.".format(
                token.value,
                constants.deprecated_relationship_types[token.value])
        )
