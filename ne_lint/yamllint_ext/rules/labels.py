# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext import LintProblem
from ne_lint.yamllint_ext.generators import NENode
from ne_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    recurse_get_readable_object,
    context as ctx
)

VALUES = []

ID = 'labels'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}
LEVEL0 = 0
LEVEL1 = 1


@process_relevant_tokens(NENode, ['labels'])
def check(token=None, **_):
    # dsl = ctx.get("dsl_version")
    for item in token.node.value:
        dictionary = recurse_get_readable_object(item)
        if not isinstance(dictionary, dict):
            yield LintProblem(
                token.line,
                None,
                desc='Every label should be a dictionary')
        else:
            for k, v in dictionary.items():
                if k not in ctx['labels']:
                    ctx['labels'].update({k: None})
                if not isinstance(v, dict):
                    yield LintProblem(
                        token.line,
                        None,
                        desc='labels contains nested dictionaries',
                        start_mark=item[LEVEL0].start_mark.line,
                        end_mark=item[LEVEL0].end_mark.line)
                else:
                    nested_key = list(v.keys())[LEVEL0]
                    nested_value = list(v.values())[LEVEL0]
                    if nested_key != 'values':
                        yield LintProblem(
                            token.line,
                            None,
                            desc='The name of the key should be "values"',
                            start_mark=item[LEVEL1].start_mark.line,
                            end_mark=item[LEVEL1].end_mark.line)

                    if not isinstance(nested_value, list):
                        non_list_item = item[LEVEL1].value[LEVEL0][LEVEL1]
                        yield LintProblem(
                            token.line,
                            None,
                            'The value of the "values" is should be a list',
                            start_mark=non_list_item.start_mark.line,
                            end_mark=non_list_item.end_mark.line)

                    if k == 'hidden' and nested_value != ['true']:
                        yield LintProblem(
                            token.line,
                            None,
                            f'The "hidden" label with the values {nested_value} '
                            'is functionally the same as removing the "hidden" '
                            'label. For consciseness, remove the "hidden" label.',
                            start_mark=item[LEVEL1].start_mark.line,
                            end_mark=item[LEVEL1].end_mark.line)
