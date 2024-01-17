# Copyright © 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

import os
import re
import sys
import pathlib
from setuptools import (setup, find_packages)


def get_version():
    current_dir = pathlib.Path(__file__).parent.resolve()

    with open(os.path.join(current_dir,
                           'nativeedge_lint/__version__.py'),
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
    name='ne-lint',
    version=get_version(),
    license='LICENSE',
    packages=find_packages(),
    description='Linter for NativeEdge Blueprints',
    entry_points={
        "console_scripts": [
            "ne-lint = ne_lint.main:lint",
        ]
    },
    package_data={
        'ne_lint': [
            'yamllint_ext/nativeedge/__nelint_runtime_cache/README.md',
        ]
    },
    install_requires=install_requires
)
