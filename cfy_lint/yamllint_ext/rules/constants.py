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

import yaml

deprecated_node_types = {
    'cloudify.azure.nodes.ResourceGroup':
        'cloudify.nodes.azure.ResourceGroup',
    'cloudify.azure.nodes.storage.StorageAccount':
        'cloudify.nodes.azure.storage.StorageAccount',
    'cloudify.azure.nodes.storage.DataDisk':
        'cloudify.nodes.azure.storage.DataDisk',
    'cloudify.azure.nodes.storage.FileShare':
        'cloudify.nodes.azure.storage.FileShare',
    'cloudify.azure.nodes.storage.VirtualNetwork':
        'cloudify.nodes.azure.storage.VirtualNetwork',
    'cloudify.azure.nodes.storage.NetworkSecurityGroup':
        'cloudify.nodes.azure.storage.NetworkSecurityGroup',
    'cloudify.azure.nodes.storage.NetworkSecurityRule':
        'cloudify.nodes.azure.storage.NetworkSecurityRule',
    'cloudify.azure.nodes.storage.RouteTable':
        'cloudify.nodes.azure.storage.RouteTable',
    'cloudify.azure.nodes.storage.Route':
        'cloudify.nodes.azure.storage.Route',
    'cloudify.azure.nodes.storage.IPConfiguration':
        'cloudify.nodes.azure.storage.IPConfiguration',
    'cloudify.azure.nodes.storage.PublicIPAddress':
        'cloudify.nodes.azure.storage.PublicIPAddress',
    'cloudify.azure.nodes.storage.AvailabilitySet':
        'cloudify.nodes.azure.storage.AvailabilitySet',
    'cloudify.azure.nodes.storage.VirtualMachine':
        'cloudify.nodes.azure.storage.VirtualMachine',
    'cloudify.azure.nodes.storage.WindowsVirtualMachine':
        'cloudify.nodes.azure.storage.WindowsVirtualMachine',
    'cloudify.azure.nodes.storage.VirtualMachineExtension':
        'cloudify.nodes.azure.storage.VirtualMachineExtension',
    'cloudify.azure.nodes.storage.LoadBalancer':
        'cloudify.nodes.azure.storage.LoadBalancer',
    'cloudify.azure.nodes.storage.BackendAddressPool':
        'cloudify.nodes.azure.storage.BackendAddressPool',
    'cloudify.azure.nodes.storage.Probe':
        'cloudify.nodes.azure.storage.Probe',
    'cloudify.azure.nodes.storage.IncomingNATRule':
        'cloudify.nodes.azure.storage.IncomingNATRule',
    'cloudify.azure.nodes.storage.Rule':
        'cloudify.nodes.azure.storage.Rule',
    'cloudify.azure.nodes.storage.ContainerService':
        'cloudify.nodes.azure.storage.ContainerService',
    'cloudify.azure.nodes.storage.Plan':
        'cloudify.nodes.azure.storage.Plan',
    'cloudify.azure.nodes.storage.WebApp':
        'cloudify.nodes.azure.storage.WebApp',
    'cloudify.azure.nodes.storage.PublishingUser':
        'cloudify.nodes.azure.storage.PublishingUser',
    'cloudify.azure.nodes.storage.ManagedCluster':
        'cloudify.nodes.azure.storage.ManagedCluster',
    'cloudify.azure.nodes.storage.Azure':
        'cloudify.nodes.azure.storage.Azure',
}

deprecated_relationship_types = {
    'cloudify.azure.relationships.contained_in_resource_group':
        'cloudify.relationships.azure.contained_in_resource_group',
    'cloudify.azure.relationships.contained_in_storage_account':
        'cloudify.relationships.azure.contained_in_storage_account',
    'cloudify.azure.relationships.contained_in_virtual_network':
        'cloudify.relationships.azure.contained_in_virtual_network',
    'cloudify.azure.relationships.contained_in_network_security_group':
        'cloudify.relationships.azure.contained_in_network_security_group',
    'cloudify.azure.relationships.contained_in_route_table':
        'cloudify.relationships.azure.contained_in_route_table',
    'cloudify.azure.relationships.contained_in_load_balancer':
        'cloudify.relationships.azure.contained_in_load_balancer',
    'cloudify.azure.relationships.network_security_group_attached_to_subnet':
        'cloudify.relationships.azure.network_security_group_attached_to_subnet',
    'cloudify.azure.relationships.route_table_attached_to_subnet':
        'cloudify.relationships.azure.route_table_attached_to_subnet',
    'cloudify.azure.relationships.nic_connected_to_ip_configuration':
        'cloudify.relationships.azure.nic_connected_to_ip_configuration',
    'cloudify.azure.relationships.ip_configuration_connected_to_subnet':
        'cloudify.relationships.azure.ip_configuration_connected_to_subnet',
    'cloudify.azure.relationships.ip_configuration_connected_to_public_ip':
        'cloudify.relationships.azure.ip_configuration_connected_to_public_ip',
    'cloudify.azure.relationships.connected_to_storage_account':
        'cloudify.relationships.azure.connected_to_storage_account',
    'cloudify.azure.relationships.connected_to_data_disk':
        'cloudify.relationships.azure.connected_to_data_disk',
    'cloudify.azure.relationships.connected_to_nic':
        'cloudify.relationships.azure.connected_to_nic',
    'cloudify.azure.relationships.connected_to_availability_set':
        'cloudify.relationships.azure.connected_to_availability_set',
    'cloudify.azure.relationships.connected_to_ip_configuration':
        'cloudify.relationships.azure.connected_to_ip_configuration',
    'cloudify.azure.relationships.connected_to_lb_be_pool':
        'cloudify.relationships.azure.connected_to_lb_be_pool',
    'cloudify.azure.relationships.connected_to_lb_probe':
        'cloudify.relationships.azure.connected_to_lb_probe',
    'cloudify.azure.relationships.vmx_contained_in_vm':
        'cloudify.relationships.azure.vmx_contained_in_vm',
    'cloudify.azure.relationships.nic_connected_to_lb_be_pool':
        'cloudify.relationships.azure.nic_connected_to_lb_be_pool',
    'cloudify.azure.relationships.vm_connected_to_datadisk':
        'cloudify.relationships.azure.vm_connected_to_datadisk',
    'cloudify.azure.relationships.connected_to_aks_cluster':
        'cloudify.relationships.azure.connected_to_aks_cluster',
}

ACCEPTED_LIST_TYPES = (
    yaml.tokens.BlockEntryToken,
    yaml.tokens.FlowSequenceStartToken
)
