# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import re

from ne_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_commas(problem):
    if problem.rule == 'commas':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            new_line = re.sub(r'\s*,\s*', ', ', line)
            striped_new_line, eol = get_eol(new_line)
            if new_line[-1] != eol:
                new_line = striped_new_line + eol
            lines[problem.line - 1] = new_line
        problem.fixed = True
