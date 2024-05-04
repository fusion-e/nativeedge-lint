from ne_lint.yamllint_ext.autofix.utils import filelines


def fix_line_endings(problem):
    if problem.rule == 'new-lines':
        with filelines(problem.file, binary=True) as lines:
            line = lines[problem.line - 1]
            string = line.replace(b'\r\n', b'\n')
            lines[problem.line - 1] = string
        problem.fixed = True
