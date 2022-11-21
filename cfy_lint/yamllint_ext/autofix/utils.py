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
from contextlib import contextmanager


@contextmanager
def filelines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    yield lines
    with open(filename, 'w') as file:
        file.writelines(lines)


def is_list(line):
    if line.lstrip().startswith('-'):
        return True


def get_indented_regex(line, found):
    if is_list(line):
        regex = r'^\s{%s}[\-\s{1}A-Za-z]' % found
    else:
        regex = r'^\s{%s}[A-Za-z]' % found
    return re.compile(regex)
