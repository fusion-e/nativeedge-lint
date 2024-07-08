
import tempfile

from ne_lint.yamllint_ext import (rules)
from ne_lint.commands.lint import (
    formatted_message,
    create_report_for_file
)
from ne_lint.yamllint_ext.config import YamlLintConfigExt


def handler(event, *_, **__):
    blueprint_file_content = event.get('blueprintFileContent')
    errors = get_linting_errors(blueprint_file_content)
    return format_response(errors)


def get_linting_errors(blueprint_file_content):
    named_temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(named_temp_file.name, 'w') as infile:
        infile.write(blueprint_file_content)
    yaml_config = YamlLintConfigExt(content=None, yamllint_rules=rules)
    report = create_report_for_file(
        named_temp_file.name,
        yaml_config,
    )
    errors = []
    for item in report:
        error = formatted_message(item, 'json', False)
        if error['rule'] == 'imports' and 'relative import' in error['message']:
            continue
        errors.append(error)
    return errors


def format_response(errors):
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'
        },
        'body': {
            'lintingData': {
                'errors': errors
            }
        }
    }
    return response
