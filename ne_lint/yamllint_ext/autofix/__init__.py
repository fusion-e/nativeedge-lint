# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from ne_lint.yamllint_ext.autofix.truthy import fix_truthy
from ne_lint.yamllint_ext.autofix.colons import fix_colons
from ne_lint.yamllint_ext.autofix.commas import fix_commas
from ne_lint.yamllint_ext.autofix.indentation import fix_indentation
from ne_lint.yamllint_ext.autofix.brackets import fix_spaces_in_brackets
from ne_lint.yamllint_ext.autofix.trailing_spaces import fix_trailing_spaces
from ne_lint.yamllint_ext.autofix.deprecated_node_types import \
    fix_deprecated_node_types
from ne_lint.yamllint_ext.autofix.deprecated_relationships import \
    fix_deprecated_relationships


def fix_problem(problem):
    if problem.file or problem.line:
        fix_truthy(problem)
        fix_indentation(problem)
        fix_trailing_spaces(problem)
        fix_deprecated_node_types(problem)
        fix_deprecated_relationships(problem)
        fix_colons(problem)
        fix_commas(problem)
        fix_spaces_in_brackets(problem)
