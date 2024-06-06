# Build and Publish

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ************.dkr.ecr.us-east-1.amazonaws.com
docker build -t nativeedge-linting-service:latest -f docker/serverless/Dockerfile .
docker tag nativeedge-linting-service:latest ************.dkr.ecr.us-east-1.amazonaws.com/nativeedge-linting-service:latest
docker push ************.dkr.ecr.us-east-1.amazonaws.com/nativeedge-linting-service:latest
```

# Test

Get the AWS API GATEWAY domain from us.
Export the variable:
```bash
export API_GATEWAY_DOMAIN=******.execute-api.us-east-1.amazonaws.com
```
And run the test script.
```bash
python docker/serverless/test_lambda_function.py 
Line 10: inputs/ Input endpoint is missing a display_label. (auto-fix available), Severity: 1
Line 16: node_templates/ The node template "resource" has an invalid property "client_config". The intrinsic function "get_input" has the target input "endpoint", which declares a type "string" but the node property is expected to be a dict representation of the custom data type "nativeedge.types.kubernetes.ClientConfig". (auto-fix unavailable), Severity: 2
```
