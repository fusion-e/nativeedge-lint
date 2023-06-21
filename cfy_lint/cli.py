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
from cfy_lint import helptexts

CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'])


class FixParamType(click.types.StringParamType):
    pass


class FixParamValue(object):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError()
        try:
            rule, line = value.split('=')
        except ValueError:
            raise ValueError(
                'Fix must be in the format rule=lineno.')
        self.line = int(line)
        self.rule = rule


def get_fix(ctx, *args, **_):
    fixes = []
    if not args or \
            isinstance(args[-1], click.Option) or \
            len(args[-1]) < 1:
        return
    for item in args[-1]:
        try:
            fixes.append(FixParamValue(item))
        except (TypeError, ValueError) as e:
            print('Invalid parameter for --fix.')
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(str(e))
            ctx.abort()
    return fixes


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
            help=helptexts.bp)

        self.config = click.option(
            '-c',
            '--config',
            default=None,
            type=click.Path(),
            multiple=False,
            help=helptexts.c)

        self.verbose = click.option(
            '-v',
            '--verbose',
            default=False,
            type=click.BOOL,
            is_flag=True,
            multiple=False,
            help=helptexts.v)

        self.format = click.option(
            '-f',
            '--format',
            default=None,
            type=click.STRING,
            multiple=False,
            help=helptexts.f)

        self.skip_suggestions = click.option(
            '-xs',
            '--skip-suggestions',
            default=None,
            type=click.STRING,
            multiple=True,
            help=helptexts.xs)

        self.autofix = click.option(
            '-af',
            '--autofix',
            default=False,
            type=click.BOOL,
            is_flag=True,
            multiple=False,
            help=helptexts.af)

        self.fix = click.option(
            '--fix',
            type=FixParamType(),
            callback=get_fix,
            multiple=True,
            help=helptexts.fix)

        self.fix_only = click.option(
            '-fo',
            '--fix-only',
            default=None,
            type=click.STRING,
            multiple=True,
            help=helptexts.fo)


options = Options()
