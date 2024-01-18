# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import sys

from ne_lint.yamllint_ext.autofix.utils import filelines
from ne_lint.yamllint_ext.autofix.indentation.utils import (
    get_yaml_dict,
    get_file_content,
    filter_corrections,
    get_compare_file_content,
    indentify_indentation_corrections
)


def fix_indentation(problem):
    if problem.rule == 'indentation':
        with filelines(problem.file) as lines:
            original = get_file_content(problem.file)
            compare = get_compare_file_content(get_yaml_dict(problem.file))
            corrections = filter_corrections(
                indentify_indentation_corrections(original, compare),
                problem.line)
            for line, correction in sorted(corrections.items()):
                if line == -1:
                    print('Unable to autofix indentation for line {}. '
                          'Unsupported YAML.'.format(problem.line))
                    sys.exit(1)
                lines[line - 1] = correction['new']
            problem.fixed = True
