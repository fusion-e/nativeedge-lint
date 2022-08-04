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

import io
import os

from ..logger import logger
from ..yamllint_ext.config import YamlLintConfigExt
from ..yamllint_ext import (run, rules)

from .. import cli


@cli.command()
@cli.options.blueprint_path
@cli.options.config
def lint(blueprint_path, config):
    yaml_config = YamlLintConfigExt(content=config, yamllint_rules=rules)

    report = create_report_for_file(blueprint_path, yaml_config)
    cnt = 0
    for item in report:
        message = '{0: <4}: {1:>4}'.format(item.line, item.message)
        if cnt == 0:
            logger.info('The following linting errors were found: ')
            cnt += 1
        if item.level == 'warning':
            logger.warning(message)
        elif item.level == 'error':
            logger.error(message)
        else:
            logger.info(message)


def create_report_for_file(file_path, conf):
    if not os.path.exists(file_path):
        raise RuntimeError('File path does not exist: {}.'.format(file_path))
    logger.info('Linting blueprint: {}'.format(file_path))
    with io.open(file_path, newline='') as f:
        return run(f, conf)
