from ne_lint.yamllint_ext.autofix.utils import filelines_binary


def fix_line_endings(problem):
    if problem.rule == 'new-lines':
        with filelines_binary(problem.file, binary=True) as lines:
            line = lines[problem.line - 1]
            string = line.replace(b'\r\n', b'\n')
            lines[problem.line - 1] = string
        problem.fixed = True
