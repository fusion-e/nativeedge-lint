########
# Copyright (c) 2018-2022 Cloudify Platform Ltd. All rights reserved
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
########

import os
import shutil
from unittest.mock import patch

from mock import MagicMock

from cloudify.state import current_ctx
from cloudify.mocks import MockCloudifyContext

from .. import node_templates

node_templates_content = """
    node_templates:

      cloud_resources:
        type: cloudify.nodes.terraform.Module
        properties:
          tflint_config:
            config:
            - type_name: config
              option_value:
                module: 'true'
            - type_name: plugin
              option_name: aws
              option_value:
                enabled: 'false'
            flags_override:
              - loglevel: info
            enable: true
          tfsec_config:
            config: {
                        "exclude" :
                        ['aws-vpc-add-description-to-security-group-rule','aws-vpc-no-public-egress-sgr','aws-vpc-no-public-ingress-sgr']
                    }
            flags_override: []
            enable: True
          terratag_config:
            tags: { 'name_company': 'cloudify' }
            flags_override:
              - -verbose: True
              - filter: 'aws_vpc'
            enable: True
    """


def test_check_terraform():

    node_templates.check_terraform(node_templates_content, 100)

    # elem = get_mock_cfy_node(node_templates_content, 'node_templates')
    # context = {
    #     'foo': models.NodeTemplate('foo'),
    # }
    # with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
    #     ctx['inputs'] = {}
    #     result = get_gen_as_list(rules.node_templates.check,
    #                              {'token': elem, 'context': context})
    #     assert isinstance(result[0], LintProblem)
    #     assert 'tfsec_config will have no effect if "enable: false".' in result[0].message
