# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from cfy_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_trailing_spaces(problem):
    if problem.rule == 'trailing-spaces':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            new_line, eol = get_eol(line)
            lines[problem.line - 1] = new_line + eol
        problem.fixed = True
