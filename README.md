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
