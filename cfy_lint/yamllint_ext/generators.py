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

from yamllint.parser import (
    Token,
    line_generator,
    comments_between_tokens)


class CfyToken(Token):
    def __init__(self, line_no, curr, prev, after, nextnext, stack):
        super().__init__(line_no, curr, prev, after, nextnext)
        self.after = self.next
        self.stack = stack
        self._node = None

    @staticmethod
    def from_token(token):
        return CfyToken(token.line_no,
                        token.curr,
                        token.prev,
                        token.next,
                        token.nextnext)

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value


class CfyNode(object):

    def __init__(self, node, prev=None):
        """
        :param node: yaml.nodes.Node
        :param cfy_token: CfyToken from current or previous loop.
        """
        self.node = node
        self._prev = prev
        self._prev_prev = None
        self._next = None
        self._node_templates = None

        try:
            self._line = node.start_mark.line + 1
        except AttributeError:
            self._line = None

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, value):
        self._prev = value

    @property
    def prev_prev(self):
        return self._prev_prev

    @prev_prev.setter
    def prev_prev(self, value):
        self._prev_prev = value

    @property
    def next_token(self):
        return self._next

    @next_token.setter
    def next_token(self, value):
        self._next = value

    @property
    def node_templates(self):
        return self._node_templates

    @node_templates.setter
    def node_templates(self, value):
        self._node_templates = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value


class SafeLineLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(
            node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def generate_nodes_recursively(node):
    # print(node)
    if isinstance(node, (tuple, list)):
        for sub in node:
            yield from generate_nodes_recursively(sub)
    else:
        yield node
        if isinstance(node, yaml.nodes.CollectionNode):
            for sub in node.value:
                yield from generate_nodes_recursively(sub)


def node_generator(buffer):
    yaml_loader = SafeLineLoader(buffer)
    if not yaml_loader.check_node():
        raise Exception('No nodes in document.')
    yield from generate_nodes_recursively(yaml_loader.get_node().value)


def token_or_comment_generator(buffer):
    yaml_loader = SafeLineLoader(buffer)

    try:
        stack = []
        prev = None
        curr = yaml_loader.get_token()
        while curr is not None:
            next = yaml_loader.get_token()
            nextnext = (yaml_loader.peek_token()
                        if yaml_loader.check_token() else None)

            yield CfyToken(
                curr.start_mark.line + 1, curr, prev, next, nextnext, stack)

            for comment in comments_between_tokens(curr, next):
                yield comment

            prev = curr
            curr = next

    except yaml.scanner.ScannerError:
        pass


def token_or_comment_or_line_generator(buffer):
    """Generator that mixes tokens and lines, ordering them by line number"""

    tok_or_com_gen = token_or_comment_generator(buffer)
    line_gen = line_generator(buffer)
    node_gen = node_generator(buffer)

    tok_or_com = next(tok_or_com_gen, None)
    line = next(line_gen, None)
    node = CfyNode(next(node_gen, None))

    prev_node = None

    while any([g for g in [tok_or_com, line, node.node] if g is not None]):
        if should_yield_line(tok_or_com, line, node):
            yield line
            line = next(line_gen, None)
        if node.node is None or (
                tok_or_com is not None and
                node.node.start_mark.line > tok_or_com.line_no
        ):
            # while token_in_node(node, tok_or_com.line_no) is False:
            #     # We want to find a node that the token is contained in.
            #     node = next(node_gen, None)
            # if node and isinstance(tok_or_com, CfyToken):
            #     tok_or_com.node = node
            yield tok_or_com
            tok_or_com = next(tok_or_com_gen, None)
        else:
            yield node
            prev_prev_node = prev_node
            prev_node = node
            node = CfyNode(next(node_gen, None), prev_node)
            node.prev_prev = prev_prev_node


def token_in_node(node, line_no):
    try:
        return node.start_mark.line - 1 <= line_no <= node.end_mark.line - 1
    except AttributeError:
        return None


def should_yield_line(tok_or_com, line, node):
    a = tok_or_com is None or (
            line is not None and tok_or_com.line_no > line.line_no)
    b = node.node is None or (
            node is not None and node.node.start_mark.line > line.line_no)
    return a or b
