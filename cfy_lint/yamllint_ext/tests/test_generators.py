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

import yamllint

from .. import generators
from . import get_buffer
from . import get_loader
from . import get_gen_as_list

YAML_CONTENT = """
a:
  aa: aa
  ab: ab
b:
- ba
- bb
c: c
"""


def test_token_or_comment_or_line_generator():
    buffer = get_buffer().read()
    for item in generators.token_or_comment_or_line_generator(buffer):
        if not item:
            continue
        assert isinstance(
            item,
            (generators.CfyNode, generators.CfyToken, yamllint.parser.Line))


def test_generate_nodes_recursively():
    yaml_loader = get_loader(YAML_CONTENT)
    yaml_loader.check_node()
    result = get_gen_as_list(
        generators.generate_nodes_recursively, yaml_loader.get_node().value)
    assert result[7].value == result[-4:-2]
