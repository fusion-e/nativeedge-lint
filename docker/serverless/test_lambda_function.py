import os
import json
import requests

BLUEPRINT_PATH = 'docker/serverless/test.yaml'


def get_data():
    with open(BLUEPRINT_PATH, 'r') as outfile:
        data = json.dumps(
            {
                'blueprintFileContent': outfile.read()
            }
        )
        return data


def make_request():
    if 'API_DOMAIN_GATEWAY' not in os.environ:
        url = 'http://localhost:9000/2015-03-31/functions/function/invocations'
    else:
        url = f'http://{os.environ["API_GATEWAY_DOMAIN"]}/test/diagnostics'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }
    data = get_data()
    result = requests.post(
        url,
        headers=headers,
        data=data,
    )
    if result.ok:
        return result
    raise Exception(f'Failed to call API: {result}')


if __name__ == "__main__":
    json_response = make_request().json()
    for error in json_response['body']['lintingData']['errors']:
        message = f"Line {error['line']}: {error['rule']}/{error['message']}"
        print(message)
