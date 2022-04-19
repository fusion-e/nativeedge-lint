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

from .cloudify import NodeTemplate


class CfyToken(Token):
    def __init__(self, line_no, curr, prev, after, nextnext, stack):
        super().__init__(line_no, curr, prev, after, nextnext)
        self.after = self.next
        self.stack = stack

    @staticmethod
    def from_token(token):
        return CfyToken(
            token.line_no, token.curr, token.prev, token.next, token.nextnext)


class SafeLineLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def token_or_comment_generator(buffer):
    yaml_loader = SafeLineLoader(buffer)
    # data = yaml_loader.get_data()
    # print(data)

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

            print(curr)
            # stack.append(curr)

            # stack.insert(0, prev)
            prev = curr
            curr = next

    except yaml.scanner.ScannerError:
        pass


def generate_node_templates(node_templates):
    for key, value in node_templates.items():
        yield NodeTemplate(key, value)


def cloudify_dsl_generator(buffer):
    yaml_loader = yaml.SafeLoader(buffer)
    data = yaml_loader.get_single_data()
    yield generate_node_templates(data.get('node_templates'))


def token_or_comment_or_line_generator(buffer):
    """Generator that mixes tokens and lines, ordering them by line number"""
    tok_or_com_gen = token_or_comment_generator(buffer)
    line_gen = line_generator(buffer)

    tok_or_com = next(tok_or_com_gen, None)
    line = next(line_gen, None)

    while tok_or_com is not None or line is not None:
        if tok_or_com is None or (line is not None and
                                  tok_or_com.line_no > line.line_no):
            yield line
            line = next(line_gen, None)
        else:
            yield tok_or_com
            tok_or_com = next(tok_or_com_gen, None)

    # yield cloudify_dsl_generator(buffer)
