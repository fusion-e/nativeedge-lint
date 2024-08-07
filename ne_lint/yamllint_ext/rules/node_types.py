# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext import LintProblem
from ne_lint.yamllint_ext.rules import constants
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    check_node_imported,
    recurse_get_readable_object,
    context as ctx
    )
from ne_lint.yamllint_ext.rules.node_templates import (
    remove_node_type_from_context
)

VALUES = []

ID = 'node_types'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(NENode, 'node_types')
def check(token=None, skip_suggestions=None, **_):
    for node_type in token.node.value:
        types = get_type_and_check_dsl(node_type)
        dsl = ctx.get("dsl_version")
        for value in types:
            if value not in constants.INPUTS_BY_DSL.get(dsl, []):
                if value not in ctx['data_types'].keys():
                    yield LintProblem(
                        get_line_from_buffer(
                            value,
                            token.node.start_mark,
                            token.node.end_mark,
                            token.node.end_mark.buffer.split('\n')
                        ) or token.line,
                        None,
                        f'Type {value} is not supported by DSL {dsl} '
                        'and has not been defined in the blueprint or plugin.'
                    )
        if check_node_imported(node_type[0].value):
            yield from node_type_follows_naming_conventions(
                node_type[0].value, token.line, skip_suggestions)
    remove_node_type_from_context(node_type)


def get_line_from_buffer(value, start_mark, end_mark, all_lines):
    counter = 0
    start_line = start_mark.line
    end_line = end_mark.line + 1
    # all_lines = token.node.end_mark.buffer.split('\n')
    for line in all_lines[start_line:end_line]:
        if value in line:
            return start_mark.line + counter + 1
        counter += 1


def get_values_by_key_type(dictionary):
    values = []
    if 'type' in dictionary:
        values.append(dictionary['type'])
    for value in dictionary.values():
        if isinstance(value, dict):
            nested_values = get_values_by_key_type(value)
            values.extend(nested_values)
    return values


def get_type_and_check_dsl(node_type):
    node_type = recurse_get_readable_object(node_type)
    return get_values_by_key_type(node_type)


def node_type_follows_naming_conventions(value, line, skip_suggestions=None):
    suggestions = 'node_templates' in skip_suggestions
    split_node_type = value.split('.')
    last_key = split_node_type.pop()
    # TODO: This will need to be nativeedge.
    if not {'nativeedge', 'nodes'} <= set(split_node_type):
        yield LintProblem(
            line,
            None,
            "node types should follow naming convention nativeedge.nodes.*: "
            "{}".format(value))
    elif not {'nativeedge', 'nodes'} <= set(split_node_type):
        yield LintProblem(
            line,
            None,
            "node types should follow naming convention nativeedge.nodes.*: "
            "{}".format(value))
    if not good_camel_case(last_key, split_node_type) and not suggestions:
        new_value = '.'.join(
            [k.lower() for k in split_node_type]) + '.{}'.format(last_key)
        yield LintProblem(
            line,
            None,
            "incorrect camel case {}. Suggested: {} ".format(value, new_value))


def good_camel_case(last_key, split_node_type):
    if not last_key[0].isupper():
        return False
    for key in split_node_type:
        if key[0].isupper():
            return False
    return True
