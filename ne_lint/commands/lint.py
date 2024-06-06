# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import io
import os
import re
import sys
import json
import urllib
from re import sub
from logging import (Formatter, StreamHandler)

from ne_lint import cli, __version__
from ne_lint.yamllint_ext import (run, rules)
from ne_lint.logger import logger, stream_handler
from ne_lint.yamllint_ext.config import YamlLintConfigExt


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
         fix_only=False,
         **_):

    if fix_only:
        autofix = True

    fix = report_both_fix_autofix(autofix, fix)
    format_json(format)

    yaml_config = YamlLintConfigExt(content=config, yamllint_rules=rules)
    skip_suggestions = skip_suggestions or ()
    try:
        report = create_report_for_file(
            blueprint_path,
            yaml_config,
            skip_suggestions=skip_suggestions,
            fix=fix,
            fix_only=fix_only)
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
                           fix=None,
                           fix_only=False):
    if not os.path.exists(file_path):
        raise RuntimeError('File path does not exist: {}.'.format(file_path))
    logger.info('Linting blueprint: {}'.format(file_path))
    with io.open(file_path, newline='') as f:
        return run(f,
                   conf,
                   create_report_for_file,
                   skip_suggestions,
                   fix,
                   fix_only)


def formatted_message(item, format=None, json_dumps=True):
    if format == 'json':
        rule, item_message = item.message.split(':', 1)
        try:
            result = re.split(r'available\),\sSeverity:\s', item_message)
            if len(result) == 2:
                severity = 2
            else:
                raise Exception('Something is up with that line.')
        except Exception:
            severity = '0'
        data = {
            "level": item.level,
            "line": item.line,
            "rule": sub(r"[()]", "", rule),
            "message": item_message,
            "severity": int(severity),
        }
        if json_dumps:
            data = json.dumps(data)
        return data
    return '{0: <4}: {1:>4}'.format(item.line, item.message)
