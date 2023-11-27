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

import os
import re
import sys
import pathlib
from setuptools import (setup, find_packages)


def get_version():
    current_dir = pathlib.Path(__file__).parent.resolve()

    with open(os.path.join(current_dir,
                           'cfy_lint/__version__.py'),
              'r') as outfile:
        var = outfile.read()
        return re.search(r'\d+.\d+.\d+', var).group()


install_requires = [
    'click>8,<9',
    'yamllint==1.28.0',
    'packaging>=17.1,<=21.3',
]

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    install_requires += [
        'pyyaml>=5.4.1',
        'networkx>=1.9.1,<=3.1'
    ]
else:
    install_requires += [
        'pyyaml>=6.0.1',
        'networkx>=3.2.1'
    ]


setup(
    name='cfy-lint',
    version=get_version(),
    license='LICENSE',
    packages=find_packages(),
    description='Linter for Cloudify Blueprints',
    entry_points={
        "console_scripts": [
            "cfy-lint = cfy_lint.main:lint",
        ]
    },
    package_data={
        'cfy_lint': [
            'yamllint_ext/cloudify/__cfylint_runtime_cache/README.md',
        ]
    },
    install_requires=install_requires
)
