import re
from ne_lint.yamllint_ext.autofix.utils import filelines


def fix_line_endings(problem):
    with filelines(problem.file) as lines:
        line = lines[problem.line - 1]
        string = re.compile('\r\n').sub('\n', line)
        lines[problem.line - 1] = string
    problem.fixed = True
