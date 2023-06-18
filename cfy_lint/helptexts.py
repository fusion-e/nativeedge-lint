########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

af = """Fix all (supported autofix) issues in place.
This is the equivalent of --fix all=-1.
Not all issues can be solved automatically."""

bp = """Path to the blueprint file that you want to lint."""

c = """A path to your own yamllint config file."""

f = """Toggle the cfy-lint output format. Currently default or "-f json"."""

fix = """Fix a single issue in place.
The format is key=value, where key is issue type and value is line number,
e.g. "--fix inputs:21". The "--fix" flag can be used multiple times.
Not all issues can be solved automatically."""

v = """Show verbose output, including exceptions."""

xs = """Do not display suggested values for supported sections."""

fo = """Fix a single issue without linting again.
The format is {"level":"value","line":value,"rule":"value","message":"value"},
where value is a string except in line where its the line number,
e.g. {"level":"error","line":9,"rule":"inputs","message":"Input
autosubnets is missing a display_label."}.
The "--fix-only" flag can be used multiple times.
Not all issues can be solved automatically."""
