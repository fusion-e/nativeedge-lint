# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

from cfy_lint.logger import logger
from cfy_lint.yamllint_ext.autofix.utils import filelines, get_eol

TRUE_PATTERN = 'TRUE'
FALSE_PATTERN = 'FALSE'
TRUE_REPLACEMENT = 'true'
FALSE_REPLACEMENT = 'false'


def fix_truthy(problem):
    if problem.rule == 'truthy':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            line = replace_words(line, TRUE_PATTERN, TRUE_REPLACEMENT)
            line = replace_words(line, FALSE_PATTERN, FALSE_REPLACEMENT)
            lines[problem.line - 1] = line
        problem.fixed = True


def replace_words(line, pattern, replacement):
    clean_line, eol = get_eol(line)
    new_words = []
    for word in clean_line.split(' '):
        if word.upper() == pattern:
            logger.debug('Replacing {} with {}.'.format(word, replacement))
            word = word.upper().replace(pattern, replacement)
        new_words.append(word)
    if clean_line != line:
        new_words[-1] += eol
    return ' '.join(new_words)
