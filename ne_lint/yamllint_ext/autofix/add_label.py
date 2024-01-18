# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import re

from ne_lint.yamllint_ext.utils import context
from ne_lint.yamllint_ext.autofix.utils import filelines

TYP = 'inputs'
MSG = r'is\smissing\sa\sdisplay_label'
INDENT = r'^\s+'
INDENT_EMPTY_LINES = r'^ \s+'
EMPTY = r'^\s*$'


def fix_add_label(problems, fix_only=False):
    counter = 0
    for problem in problems:
        if not problem.fix and not fix_only:
            continue
        if problem.rule == TYP and re.search(MSG, problem.message):
            with filelines(problem.file) as lines:
                label = lines[problem.line - 1 + counter]
                try:
                    is_empty_line = re.findall(EMPTY,
                                               lines[problem.line + counter])
                    if is_empty_line:
                        while not re.findall(EMPTY,
                                             lines[problem.line + counter]):
                            counter += 1
                        indentation = re.search(
                            INDENT_EMPTY_LINES,
                            lines[problem.line + counter]).group()
                    else:
                        indentation = re.search(
                            INDENT,
                            lines[problem.line + counter]).group()
                except AttributeError:
                    indentation = ''.join(
                        re.search(INDENT, label).group() +
                        re.search(INDENT, label).group()
                    )

                label = label.strip().replace('_', ' ').replace(':', '')
                label = '{indentation}display_label: ' \
                        '{label}{linesep}'.format(
                            indentation=indentation,
                            label=label.title(),
                            linesep='\n')
                lines.insert(problem.line + counter, label)
                counter += 1
                context['add_label'].append(problem.line)
