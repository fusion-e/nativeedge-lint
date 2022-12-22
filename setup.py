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

from setuptools import (setup, find_packages)

setup(
    name='cfy-lint',
    version='0.0.22',
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
    install_requires=[
        'click',
        'pyyaml',
        'yamllint',
        'packaging'
    ]
)
