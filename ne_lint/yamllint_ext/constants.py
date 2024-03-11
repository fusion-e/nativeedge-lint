# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

UNUSED_INPUTS = 'unused_inputs'
UNUSED_IMPORT = 'node_types_by_plugin'
UNUSED_IMPORT_CTX = 'imported_node_types_by_plugin'

BLUEPRINT_MODEL = {
    'tosca_definitions_version': None,
    'imports': {},
    'inputs': {},
    'dsl_definitions': {},
    'node_templates': {},
    'capabilities': {},
}

NODE_TEMPLATE_MODEL = {
    'type': '',
    'properties': {},
    'interfaces': {},
    'relationships': {},
    'capabilities': {},
}

# TODO: Deprecate c-l-o-u-d-i-f-y
LATEST_PLUGIN_YAMLS = {
    'nativeedge-aws-plugin': 'https://github.com/fusion-e/nativeedge-aws-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-azure-plugin': 'https://github.com/fusion-e/nativeedge-azure-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-starlingx-plugin': 'https://github.com/fusion-e/nativeedge-starlingx-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-gcp-plugin': 'https://github.com/fusion-e/nativeedge-gcp-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-openstack-plugin': 'https://github.com/fusion-e/nativeedge-openstack-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-vsphere-plugin': 'https://github.com/fusion-e/nativeedge-vsphere-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-terraform-plugin': 'https://github.com/fusion-e/nativeedge-terraform-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-terragrunt-plugin': 'https://github.com/fusion-e/nativeedge-terragrunt-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-ansible-plugin': 'https://github.com/fusion-e/nativeedge-ansible-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-kubernetes-plugin': 'https://github.com/fusion-e/nativeedge-kubernetes-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-docker-plugin': 'https://github.com/fusion-e/nativeedge-docker-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-netconf-plugin': 'https://github.com/fusion-e/nativeedge-netconf-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-fabric-plugin': 'https://github.com/fusion-e/nativeedge-fabric-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-libvirt-plugin': 'https://github.com/fusion-e/nativeedge-libvirt-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-utilities-plugin': 'https://github.com/fusion-e/nativeedge-utilities-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-host-pool-plugin': 'https://github.com/fusion-e/nativeedge-host-pool-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-vcloud-plugin': 'https://github.com/fusion-e/nativeedge-vcloud-plugin/releases/download/latest/plugin.yaml', # noqa
    'nativeedge-helm-plugin': 'https://github.com/fusion-e/nativeedge-helm-plugin/releases/download/latest/plugin.yaml' # noqa
}

DEFAULT_NODE_TYPES = [
    'nativeedge.nodes.Port',
    'nativeedge.nodes.Root',
    'nativeedge.nodes.Tier',
    'nativeedge.nodes.Router',
    'nativeedge.nodes.Subnet',
    'nativeedge.nodes.Volume',
    'nativeedge.nodes.Network',
    'nativeedge.nodes.Compute',
    'nativeedge.nodes.Container',
    'nativeedge.nodes.VirtualIP',
    'nativeedge.nodes.FileSystem',
    'nativeedge.nodes.ObjectStorage',
    'nativeedge.nodes.LoadBalancer',
    'nativeedge.nodes.SecurityGroup',
    'nativeedge.nodes.SoftwareComponent',
    'nativeedge.nodes.DBMS',
    'nativeedge.nodes.Database',
    'nativeedge.nodes.WebServer',
    'nativeedge.nodes.ApplicationServer',
    'nativeedge.nodes.MessageBusServer',
    'nativeedge.nodes.ApplicationModule',
    'nativeedge.nodes.NativeEdgeManager',
    'nativeedge.nodes.Component',
    'nativeedge.nodes.ServiceComponent',
    'nativeedge.nodes.SharedResource',
    'nativeedge.nodes.Blueprint',
    'nativeedge.nodes.PasswordSecret'
]

DEFAULT_RELATIONSHIPS = [
    'nativeedge.relationships.depends_on',
    'nativeedge.relationships.connected_to',
    'nativeedge.relationships.contained_in',
    'nativeedge.relationships.depends_on_lifecycle_operation',
    'nativeedge.relationships.depends_on_shared_resource',
    'nativeedge.relationships.connected_to_shared_resource',
    'nativeedge.relationships.file_system_depends_on_volume',
    'nativeedge.relationships.file_system_contained_in_compute'
]

DEFAULT_TYPES = {
    'node_types': {key: {} for key in DEFAULT_NODE_TYPES},
    'relationships': {key: {} for key in DEFAULT_RELATIONSHIPS},
}
