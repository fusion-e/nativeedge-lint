import json
import requests

FILECONTENT = ''

with open('blueprint.yaml', 'r') as outfile:
    FILECONTENT = outfile.read()

print(repr(FILECONTENT))
url = 'http://localhost:9000/2015-03-31/functions/function/invocations'
result = requests.post(
    url,
    data=json.dumps(
        {
            'blueprintFileContent': FILECONTENT
        }
    ),
)
print(json.dumps(result.json()))
