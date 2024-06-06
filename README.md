# ne-lint

A novel linter for NativeEdge Blueprints.

The **ne lint** tool is for NativeEdge users who:

- wish to follow best practices.
- prefer to discover potential issues before uploading to NativeEdge manager.
- would like to be notified of deprecated node_types, relationships, plugin versions, etc.


## Requirements:

 - Python 3.6, or higher.
 - Internet connection. (In order to check if the specified imported plugin versions contain the types you are using.)


## How to install

```bash
pip3 install ne-lint
```


## How to use

```bash
ne-lint blueprint.yaml
```

## Lambda Service

Build the image:

```bash
docker build -t nativeedge-linting-service:latest -f docker/serverless/Dockerfile .
```

Tag the image:

```bash
docker tag nativeedge-linting-service:latest 728050044221.dkr.ecr.us-east-1.amazonaws.com/nativeedge-linting-service:latest
```

Push:
```bash
docker push 728050044221.dkr.ecr.us-east-1.amazonaws.com/nativeedge-linting-service:latest
```

Run the service:
```bash
docker run --platform linux/amd64 -p 9000:8080 nativeedge-linting-service:latest
```
