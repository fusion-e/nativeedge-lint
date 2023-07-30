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
import sys
import json
import urllib
from re import sub
from logging import (Formatter, StreamHandler)

from cfy_lint import cli, __version__
from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext import (run, rules)
from cfy_lint.logger import logger, stream_handler
from cfy_lint.yamllint_ext.autofix import fix_problem
from cfy_lint.yamllint_ext.config import YamlLintConfigExt
from cfy_lint.yamllint_ext.autofix.add_label import fix_add_label
from cfy_lint.yamllint_ext.autofix.empty_lines import fix_empty_lines


def report_both_fix_autofix(af, f):
    f = f or []
    if af and f:
        print('The parameters -af/--autofix and --fix are '
              'mutually exclusive. Use --help for more info.')
        sys.exit(1)
    elif af:
        f.insert(0, cli.FixParamValue('all=-1'))
    return f


def format_json(format):
    if format == 'json':
        logger.removeHandler(stream_handler)
        new_logging_handler = StreamHandler()
        new_logging_formatter = Formatter(fmt='%(message)s')
        new_logging_handler.setFormatter(new_logging_formatter)
        logger.addHandler(new_logging_handler)


@cli.command()
@cli.options.blueprint_path
@cli.options.config
@cli.options.verbose
@cli.options.format
@cli.options.skip_suggestions
@cli.options.autofix
@cli.options.fix
@cli.options.fix_only
@cli.click.version_option(__version__.version)
def lint(blueprint_path,
         config,
         verbose,
         format,
         skip_suggestions=None,
         autofix=False,
         fix=None,
         fix_only=None,
         **_):

    if fix_only:
        extra_empty_line = False
        add_label_offset = False
        problems = []
        for x in fix_only:
            x = json.loads(x)
            problem = LintProblem(
                line=x['line'],
                column=None,
                desc=x['message'],
                rule=x['rule'],
            )
            input_file_path = os.path.abspath(blueprint_path)
            problem.file = input_file_path
            # print(problems)
            if problem.rule == 'inputs' and \
                    'is missing a display_label' in problem.message:
                add_label_offset = True
                problems.append(problem)
            elif problem.rule == 'empty-lines':
                extra_empty_line = True
            else:
                fix_problem(problem)

        if add_label_offset:
            fix_add_label(problems, fix_only=True)

        if extra_empty_line:
            fix_empty_lines(problem)

        sys.exit(0)

    fix = report_both_fix_autofix(autofix, fix)
    format_json(format)

    yaml_config = YamlLintConfigExt(content=config, yamllint_rules=rules)
    skip_suggestions = skip_suggestions or ()
    try:
        report = create_report_for_file(
            blueprint_path,
            yaml_config,
            skip_suggestions=skip_suggestions,
            fix=fix)
    except Exception as e:
        if verbose:
            raise e
        else:
            exception_str = str(e)
        logger.error(exception_str)
        sys.exit(1)

    cnt = 0
    try:
        for item in report:
            message = formatted_message(item, format)
            if cnt == 0:
                logger.info('The following linting errors were found: ')
                cnt += 1
            if item.level == 'warning':
                logger.warning(message)
            elif item.level == 'error':
                logger.error(message)
            else:
                logger.info(message)
    except urllib.error.URLError as e:
        if verbose:
            raise e
        else:
            exception_str = str(e)
        logger.error(exception_str)
        sys.exit(1)


def create_report_for_file(file_path,
                           conf,
                           create_report_for_file=False,
                           skip_suggestions=None,
                           fix=None):
    if not os.path.exists(file_path):
        raise RuntimeError('File path does not exist: {}.'.format(file_path))
    logger.info('Linting blueprint: {}'.format(file_path))
    with io.open(file_path, newline='') as f:
        return run(f, conf, create_report_for_file, skip_suggestions, fix)


def formatted_message(item, format=None):
    if format == 'json':
        rule, item_message = item.message.split(':', 1)
        return json.dumps({
            "level": item.level,
            "line": item.line,
            "rule": sub(r"[()]", "", rule),
            "message": item_message,
        })
    return '{0: <4}: {1:>4}'.format(item.line, item.message)
