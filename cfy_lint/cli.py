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

import click

CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'])


def init():
    pass


def group(name):
    return click.group(name=name, context_settings=CLICK_CONTEXT_SETTINGS)


def command(*args, **kwargs):
    return click.command(*args, **kwargs)


class Options(object):
    def __init__(self):
        self.blueprint_path = click.option(
            '-b',
            '--blueprint-path',
            default='blueprint.yaml',
            type=click.Path(),
            multiple=False,
            show_default='blueprint.yaml',
            help='Path to the blueprint file that you want to lint.')

        self.config = click.option(
            '-c',
            '--config',
            default=None,
            type=click.Path(),
            multiple=False,
            help='ability to use configuration file or options.')


options = Options()
