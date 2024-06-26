# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml

from ne_lint.yamllint_ext import LintProblem
from ne_lint.yamllint_ext.rules import constants
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.constants import UNUSED_INPUTS
from ne_lint.yamllint_ext.utils import (
    INTRINSIC_FNS,
    recurse_mapping,
    context as ctx, process_relevant_tokens)

VALUES = []

ID = 'inputs'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
ALLOWED_KEYS = [
    'type',
    'hidden',
    'default',
    'required',
    'constraints',
    'description',
    'display_label'
]
STR_INTRINSIC_FNS = [
    'concat',
    'string_lower',
    'string_upper',
    'string_replace'
]
DICT_INTRINSIC_FNS = [
    'merge'
]
INT_INTRINSIC_FNS = [
    'string_find'
]
LEVEL0 = 0
LEVEL1 = 1


@process_relevant_tokens(NENode, ['inputs', 'get_input'])
def check(token=None, skip_suggestions=None, **_):
    if not ctx['start_lines']['inputs']:
        ctx['start_lines']['inputs'] = token.node.start_mark.line
    not_input = False
    inputs_start_line = ctx['start_lines']['inputs']
    node_templates_start_line = ctx['start_lines'].get('node_templates')
    if all(isinstance(v, int) for v in [inputs_start_line,
                                        node_templates_start_line]):
        not_input = node_templates_start_line > inputs_start_line and \
            node_templates_start_line < token.node.start_mark.line
    if token.prev.node.value == 'inputs' and not not_input:
        for item in token.node.value:
            if isinstance(item, yaml.nodes.ScalarNode):
                yield LintProblem(
                    token.line,
                    None,
                    'Bad inputs format. '
                    'Input should be a key not a list item.')
            input_obj = NEInput(item)
            if not input_obj.name and not input_obj.mapping:
                continue
            if input_obj.not_input() and get_default_type(input_obj) != bool:
                continue
            ctx['inputs'].update(input_obj.__dict__())
            if input_obj.name not in ctx[UNUSED_INPUTS]:
                input_unused = item[LEVEL0]
                ctx[UNUSED_INPUTS].update(
                    {
                        input_obj.name: LintProblem(
                            token.line,
                            None,
                            desc='input {} is unused.'.format(input_obj.name),
                            start_mark=input_unused.start_mark.line,
                            end_mark=input_unused.end_mark.line
                        )
                    }
                )
            yield from validate_inputs(input_obj,
                                       input_obj.line or token.line,
                                       ctx.get("dsl_version", ''),
                                       skip_suggestions,
                                       item)

    if token.prev.node.value == 'get_input':
        if isinstance(token.node.value, list):
            if isinstance(token.node.value[0], yaml.nodes.ScalarNode):
                if token.node.value[0].value not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input {}'
                        .format(token.node.value[0].value))
                elif token.node.value[0].value in ctx[UNUSED_INPUTS]:
                    del ctx[UNUSED_INPUTS][token.node.value[0].value]
            if isinstance(token.node.value[0], tuple):
                if token.node.value[0][0] not in ctx['inputs']:
                    yield LintProblem(
                        token.line,
                        None,
                        'undefined input "{}"'.format(token.node.value[0][0]))
                elif token.node.value[0][0] in ctx[UNUSED_INPUTS]:
                    del ctx[UNUSED_INPUTS][token.node.value[0][0]]
        else:
            if token.node.value not in ctx['inputs']:
                yield LintProblem(
                    token.line,
                    None,
                    'undefined input "{}"'.format(token.node.value))
            elif token.node.value in ctx[UNUSED_INPUTS]:
                del ctx[UNUSED_INPUTS][token.node.value]


def validate_inputs(input_obj,
                    line,
                    dsl=None,
                    skip_suggestions=None,
                    item=None):
    dsl = dsl or 'null'
    skip_suggestions = skip_suggestions or ()
    suggestions = 'inputs' in skip_suggestions
    if input_obj.invalid_keys:
        yield LintProblem(
            line,
            None,
            'the following keys are invalid for inputs: {}'.format(
                input_obj.invalid_keys))
    if not input_obj.input_type:
        message = 'input "{}" does not specify a type. '.format(input_obj.name)
        if input_obj.default:
            if isinstance(input_obj.default, dict):
                for key in input_obj.default.keys():
                    if key in INTRINSIC_FNS:
                        input_obj.default = None
                        if key in STR_INTRINSIC_FNS:
                            message += 'The correct type could be "string".'
                        if key in DICT_INTRINSIC_FNS:
                            message += 'The correct type could be "dict".'
                        if key in INT_INTRINSIC_FNS:
                            message += 'The correct type could be "int".'
                if isinstance(input_obj.default, dict) and not suggestions:
                    message += 'The correct type could be "dict".'
            if get_default_type(input_obj) == str and not suggestions:
                message += 'The correct type could be "string".'
            if get_default_type(input_obj) == bool and not suggestions:
                message += 'The correct type could be "boolean".'
            if isinstance(input_obj.default, list) and not suggestions:
                message += 'The correct type could be "list".'
            if get_default_type(input_obj) == int and not suggestions:
                message += 'The correct type could be "integer".'
            if get_default_type(input_obj) == float and not suggestions:
                message += 'The correct type could be "float".'
        yield LintProblem(line, None, message)
    elif dsl not in constants.INPUTS_BY_DSL:
        input_type = item[LEVEL1]
        yield LintProblem(
            line,
            None,
            f'Unable to validate input type {get_type_name(input_obj)} '
            f'by DSL version: {dsl}. Please update DSL version to one of: '
            f'{", ".join(constants.INPUTS_BY_DSL.keys())}.',
            start_mark=input_type.start_mark.line,
            end_mark=input_type.end_mark.line
        )
    elif get_type_name(input_obj) not in constants.INPUTS_BY_DSL.get(dsl, []):
        input_type = item[LEVEL1]
        yield LintProblem(
            line,
            None,
            'Input of type {} is not supported by DSL {}.'.format(
                get_type_name(input_obj), dsl
            ),
            start_mark=input_type.start_mark.line,
            end_mark=input_type.end_mark.line
        )
    elif not input_obj.display_label:
        yield LintProblem(
            line,
            None,
            'Input {} is missing a display_label.'.format(input_obj.name),
            fixable=True
        )
    elif get_type(input_obj) and input_obj.default:
        message = ''
        if isinstance(input_obj.default, dict):
            for key in input_obj.default.keys():
                if key in INTRINSIC_FNS:
                    message = "intrinsic function"
                    if key in STR_INTRINSIC_FNS and not isinstance(
                            get_type_name(input_obj), str):
                        message = 'input "{}" specify a type {}, The correct'\
                            ' type is "string".'.format(
                                input_obj.name,
                                get_type_name(input_obj))
                    if key in INT_INTRINSIC_FNS and not\
                        isinstance(
                                   get_type(input_obj),
                                   int):
                        message = 'input "{}" specify a type {}, The correct'\
                            ' type is "int".'.format(
                                input_obj.name,
                                get_type_name(input_obj))
        if not (message or get_default_type(input_obj) == get_type(input_obj)):
            message = 'input "{}" specify a type {}, However this'\
                ' doesn\'t match default of type {}.'.format(
                    input_obj.name,
                    get_type_name(input_obj),
                    input_obj.default)
        if message and message not in ["intrinsic function"]:
            yield LintProblem(line, None, message)
    elif not input_obj.display_label:
        yield LintProblem(
            line,
            None,
            'Input {} is missing a display_label.'.format(input_obj.name),
            fixable=True
        )


def get_type_name(input_obj):
    if isinstance(input_obj.input_type, yaml.nodes.ScalarNode):
        return input_obj.input_type.value
    else:
        raise TypeError()


def get_type(input_obj):
    type_name = get_type_name(input_obj)
    if type_name == 'string':
        return str
    elif type_name == 'integer':
        return int
    elif type_name == 'boolean':
        return bool
    else:
        return globals().get('__builtins__').get(type_name)


def get_default_type(input_obj):
    default_value = input_obj.default
    if type(default_value) == str:  # noqa: E721
        if default_value.isdigit():
            result = int
        elif is_float(default_value):
            result = float
        else:
            result = str
    elif type(default_value) == bool:  # noqa: E721
        result = bool
    else:
        result = type(input_obj.default)
    return result


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


class NEInput(object):
    def __init__(self, nodes):
        self._line = None
        self.name, self.mapping = self.get_input(nodes)
        self.invalid_keys = []
        if self.name and self.mapping:
            for key in list(self.mapping.keys()):
                if key not in ALLOWED_KEYS:
                    self.invalid_keys.append(key)
                    del self.mapping[key]
            self.input_type = self.mapping.get('type')
            self.description = self.mapping.get('description')
            self._default = self.mapping.get('default')
            self.constraints = self.mapping.get('constraints')
            self.display_label = self.mapping.get('display_label')

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def line(self):
        return self._line

    def not_input(self):
        return all([not k for k in self.mapping.values()])

    def __dict__(self):
        return {
            self.name: self.mapping
        }

    def get_input(self, nodes):
        if not isinstance(nodes, tuple) or len(nodes) != 2:
            name = None
            mapping = None
        else:
            name = self.get_input_name(nodes[0])
            mapping = self.get_input_mapping(nodes[1])
        return name, mapping

    def get_input_name(self, node):
        if isinstance(node, yaml.nodes.ScalarNode):
            self._line = node.end_mark.line + 1
            return node.value

    def get_input_mapping(self, node):
        mapping = {
            'type': None,
            'default': None,
            'description': None,
            'constraints': None,
            'display_label': None,
        }
        if isinstance(node, yaml.nodes.MappingNode):
            for tup in node.value:
                if not len(tup) == 2:
                    continue
                mapping_name = tup[0].value
                mapping_value = self.get_mapping_value(
                    mapping_name, tup[1])
                mapping[mapping_name] = mapping_value
        return mapping

    def get_mapping_value(self, name, value):
        if name not in ['default', 'constraints']:
            return value
        else:
            return recurse_mapping(value)
