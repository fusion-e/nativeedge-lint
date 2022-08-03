########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

LATEST_PLUGIN_YAMLS = {
    'cloudify-aws-plugin': 'https://github.com/cloudify-cosmo/cloudify-aws-plugin/releases/download/latest/plugin.yaml',
    'cloudify-azure-plugin': 'https://github.com/cloudify-cosmo/cloudify-azure-plugin/releases/download/latest/plugin.yaml',
    'cloudify-starlingx-plugin': 'https://github.com/cloudify-cosmo/cloudify-starlingx-plugin/releases/download/latest/plugin.yaml',
    'cloudify-gcp-plugin': 'https://github.com/cloudify-cosmo/cloudify-gcp-plugin/releases/download/latest/plugin.yaml',
    'cloudify-openstack-plugin': 'https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/latest/plugin.yaml',
    'cloudify-vsphere-plugin': 'https://github.com/cloudify-cosmo/cloudify-vsphere-plugin/releases/download/latest/plugin.yaml',
    'cloudify-terraform-plugin': 'https://github.com/cloudify-cosmo/cloudify-terraform-plugin/releases/download/latest/plugin.yaml',
    'cloudify-terragrunt-plugin': 'https://github.com/cloudify-cosmo/cloudify-terragrunt-plugin/releases/download/latest/plugin.yaml',
    'cloudify-ansible-plugin': 'https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases/download/latest/plugin.yaml',
    'cloudify-kubernetes-plugin': 'https://github.com/cloudify-cosmo/cloudify-kubernetes-plugin/releases/download/latest/plugin.yaml',
    'cloudify-docker-plugin': 'https://github.com/cloudify-cosmo/cloudify-docker-plugin/releases/download/latest/plugin.yaml',
    'cloudify-netconf-plugin': 'https://github.com/cloudify-cosmo/cloudify-netconf-plugin/releases/download/latest/plugin.yaml',
    'cloudify-fabric-plugin': 'https://github.com/cloudify-cosmo/cloudify-fabric-plugin/releases/download/latest/plugin.yaml',
    'cloudify-libvirt-plugin': 'https://github.com/cloudify-incubator/cloudify-libvirt-plugin/releases/download/latest/plugin.yaml',
    'cloudify-utilities-plugin': 'https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/latest/plugin.yaml',
    'cloudify-host-pool-plugin': 'https://github.com/cloudify-cosmo/cloudify-host-pool-plugin/releases/download/latest/plugin.yaml',
    'cloudify-vcloud-plugin': 'https://github.com/cloudify-cosmo/cloudify-vcloud-plugin/releases/download/latest/plugin.yaml',
    'cloudify-helm-plugin': 'https://github.com/cloudify-incubator/cloudify-helm-plugin/releases/download/latest/plugin.yaml'
}
