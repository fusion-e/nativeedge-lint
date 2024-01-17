# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import re

from cfy_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_colons(problem):
    if problem.rule == 'colons':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            if re.match(r'^\s*([^:\n]+)\s*:\s*([^:\n]+)\s*$', line):
                new_line = re.sub(r'\s*:\s*', ': ', line)
            elif re.match(r'^\s*([^:\n]+)\s*:\s*$', line):
                new_line = re.sub(r'\s*:', ': ', line)
            striped_new_line, eol = get_eol(new_line)
            if new_line[-1] != eol:
                new_line = striped_new_line + eol
            lines[problem.line - 1] = new_line
        problem.fixed = True
