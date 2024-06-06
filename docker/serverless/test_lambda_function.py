import os
import json
import requests


def get_data():
    with open('docker/serverless/blueprint.yaml', 'r') as outfile:
        data = json.dumps(
            {
                'blueprintFileContent': outfile.read()
            }
        )
        return data


def make_request():
    url = f'https://{os.environ["API_GATEWAY_DOMAIN"]}/test/diagnostics'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }
    result = requests.post(
        url,
        headers=headers,
        data=get_data(),
    )
    return result


if __name__ == "__main__":

    json_response = make_request().json()
    for error in json_response['body']['lintingData']['errors']:
        message = f"Line {error['line']}: {error['rule']}/{error['message']}"
        print(message)
