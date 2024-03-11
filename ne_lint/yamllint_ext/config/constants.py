# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

DEFAULT_YAMLLINT_CONFIG = """
extends: default

rules:
  braces:
    max-spaces-inside: 1
    min-spaces-inside: 0
    min-spaces-inside-empty: 0
    max-spaces-inside-empty: 0
  brackets:
    max-spaces-inside: 1
    min-spaces-inside: 0
    min-spaces-inside-empty: 0
    max-spaces-inside-empty: 0
  colons:
    max-spaces-before: 0
    max-spaces-after: 1
  commas:
    max-spaces-after: 1
    max-spaces-before: 0
  comments: disable
  comments-indentation: disable
  document-start:
    present: false
  empty-lines:
    max: 1
  empty-values:
    forbid-in-block-mappings: true
    forbid-in-flow-mappings: true
  hyphens:
    max-spaces-after: 1
  key-duplicates: {}
  indentation:
    spaces: 2
    indent-sequences: consistent
  line-length:
    max: 120
    level: warning
  quoted-strings:
    required: only-when-needed
    extra-allowed: ["^http://", "^ftp://", "(?![A-Za-z0-9])"]
  truthy:
    allowed-values: ['true', 'false']
    check-keys: true
  new-line-at-end-of-file: disable
  new-lines:
    type: platform
  inputs: enable
  imports: enable
  node_types: enable
  dsl_version: enable
  capabilities: enable
  relationships: enable
  node_templates: enable
  dsl_definitions: enable
  blueprint_labels: enable
"""
