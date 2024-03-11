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
    'cloudify-aws-plugin': 'https://github.com/cloudify-cosmo/cloudify-aws-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-azure-plugin': 'https://github.com/cloudify-cosmo/cloudify-azure-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-starlingx-plugin': 'https://github.com/cloudify-cosmo/cloudify-starlingx-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-gcp-plugin': 'https://github.com/cloudify-cosmo/cloudify-gcp-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-openstack-plugin': 'https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-vsphere-plugin': 'https://github.com/cloudify-cosmo/cloudify-vsphere-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-terraform-plugin': 'https://github.com/cloudify-cosmo/cloudify-terraform-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-terragrunt-plugin': 'https://github.com/cloudify-cosmo/cloudify-terragrunt-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-ansible-plugin': 'https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-kubernetes-plugin': 'https://github.com/cloudify-cosmo/cloudify-kubernetes-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-docker-plugin': 'https://github.com/cloudify-cosmo/cloudify-docker-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-netconf-plugin': 'https://github.com/cloudify-cosmo/cloudify-netconf-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-fabric-plugin': 'https://github.com/cloudify-cosmo/cloudify-fabric-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-libvirt-plugin': 'https://github.com/cloudify-incubator/cloudify-libvirt-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-utilities-plugin': 'https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-host-pool-plugin': 'https://github.com/cloudify-cosmo/cloudify-host-pool-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-vcloud-plugin': 'https://github.com/cloudify-cosmo/cloudify-vcloud-plugin/releases/download/latest/plugin.yaml', # noqa
    'cloudify-helm-plugin': 'https://github.com/cloudify-incubator/cloudify-helm-plugin/releases/download/latest/plugin.yaml' # noqa
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
    'nativeedge.nodes.CloudifyManager',
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
