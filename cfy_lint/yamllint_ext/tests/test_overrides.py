# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from cfy_lint.yamllint_ext.overrides import LintProblem


def test_lint_problem_severity():
    problem = LintProblem(
        line=1,
        column=0,
        desc='foo',
        rule='bar',
    )
    problem.desc
