# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_deprecated_relationships(problem):
    if problem.rule == 'relationships' and \
            'deprecated relationship type' in problem.message:
        with filelines(problem.file) as lines:
            line = lines[problem.line]
            line, eol = get_eol(line)
            split = problem.message.split()
            new_line = line.replace(split[-5], split[-3].rstrip('.'))
            lines[problem.line] = new_line + eol
        problem.fixed = True
