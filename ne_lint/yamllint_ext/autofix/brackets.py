# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import re

from ne_lint.yamllint_ext.autofix.utils import filelines


def fix_spaces_in_brackets(problem):
    if problem.rule in ['brackets', 'braces'] and \
            'too many spaces inside ' in problem.message:
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            if problem.rule == 'braces':
                new_line = re.sub(r'{\s+', '{ ', line)
                new_line = re.sub(r'\s+}', ' }', new_line)
                lines[problem.line - 1] = new_line
                problem.fixed = True
            elif problem.rule == 'brackets':
                new_line = re.sub(r'\[\s+', '[ ', line)
                new_line = re.sub(r'\s+\]', ' ]', new_line)
                lines[problem.line - 1] = new_line
                problem.fixed = True
