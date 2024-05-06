# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

af = """Fix all (supported autofix) issues in place.
This is the equivalent of --fix all=-1.
Not all issues can be solved automatically."""

bp = """Deprecated. Blueprint Path is now a positional argument.
E.g, "ne-lint blueprint.yaml."""

c = """A path to your own yamllint config file."""

f = """Toggle the ne-lint output format. Currently default or "-f json"."""

fix = """Fix a single issue in place.
The format is key=value, where key is issue type and value is line number,
e.g. "--fix inputs:21". The "--fix" flag can be used multiple times.
Not all issues can be solved automatically."""

v = """Show verbose output, including exceptions."""

xs = """Do not display suggested values for supported sections."""

fo = """Fix all issues like autofix flage without linting again."""
