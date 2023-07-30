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
import re

from cfy_lint.yamllint_ext.utils import context
from cfy_lint.yamllint_ext.autofix.utils import filelines

TYP = 'inputs'
MSG = r'is\smissing\sa\sdisplay_label'
INDENT = r'^\s+'
INDENT_EMPTY_LINES = r'^ \s+'
EMPTY = r'^\s*$'


def fix_add_label(problems, fix_only=False):
    counter = 0
    for problem in problems:
        if not problem.fix and not fix_only:
            continue
        if problem.rule == TYP and re.search(MSG, problem.message):
            with filelines(problem.file) as lines:
                label = lines[problem.line - 1 + counter]
                try:
                    is_empty_line = re.findall(EMPTY,
                                               lines[problem.line + counter])
                    if is_empty_line:
                        while not re.findall(EMPTY,
                                             lines[problem.line + counter]):
                            counter += 1
                        indentation = re.search(
                            INDENT_EMPTY_LINES,
                            lines[problem.line + counter]).group()
                    else:
                        indentation = re.search(
                            INDENT,
                            lines[problem.line + counter]).group()
                except AttributeError:
                    indentation = ''.join(
                        re.search(INDENT, label).group() +
                        re.search(INDENT, label).group()
                    )

                label = label.strip().replace('_', ' ').replace(':', '')
                label = '{indentation}display_label: ' \
                        '{label}{linesep}'.format(
                            indentation=indentation,
                            label=label.title(),
                            linesep='\n')
                lines.insert(problem.line + counter, label)
                counter += 1
                context['add_label'].append(problem.line)
