# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

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
            (generators.NENode, generators.NEToken, yamllint.parser.Line))


def test_generate_nodes_recursively():
    yaml_loader = get_loader(YAML_CONTENT)
    yaml_loader.check_node()
    result = get_gen_as_list(
        generators.generate_nodes_recursively, yaml_loader.get_node().value)
    assert result[7].value == result[-4:-2]
