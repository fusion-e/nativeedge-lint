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

GCP_TYPES = [
    'cloudify.gcp.project',
    'cloudify.nodes.gcp.PolicyBinding',
    'cloudify.gcp.nodes.Instance',
    'cloudify.gcp.nodes.InstanceGroup',
    'cloudify.gcp.nodes.Volume',
    'cloudify.gcp.nodes.Snapshot',
    'cloudify.gcp.nodes.Network',
    'cloudify.gcp.nodes.SubNetwork',
    'cloudify.gcp.nodes.VPCNetworkPeering',
    'cloudify.gcp.nodes.Route',
    'cloudify.gcp.nodes.FirewallRule',
    'cloudify.gcp.nodes.SecurityGroup',
    'cloudify.gcp.nodes.Access',
    'cloudify.gcp.nodes.KeyPair',
    'cloudify.gcp.nodes.ExternalIP',
    'cloudify.gcp.nodes.GlobalAddress',
    'cloudify.gcp.nodes.StaticIP',
    'cloudify.gcp.nodes.Address',
    'cloudify.gcp.nodes.Image',
    'cloudify.gcp.nodes.HealthCheck',
    'cloudify.gcp.nodes.BackendService',
    'cloudify.gcp.nodes.RegionBackendService',
    'cloudify.gcp.nodes.UrlMap',
    'cloudify.gcp.nodes.TargetProxy',
    'cloudify.gcp.nodes.SslCertificate',
    'cloudify.gcp.nodes.ForwardingRule',
    'cloudify.gcp.nodes.GlobalForwardingRule',
    'cloudify.gcp.nodes.DNSZone',
    'cloudify.gcp.nodes.DNSRecord',
    'cloudify.gcp.nodes.DNSAAAARecord',
    'cloudify.gcp.nodes.DNSMXRecord',
    'cloudify.gcp.nodes.DNSNSRecord',
    'cloudify.gcp.nodes.DNSTXTRecord',
    'cloudify.gcp.nodes.KubernetesCluster',
    'cloudify.gcp.nodes.KubernetesNodePool',
    'cloudify.gcp.nodes.KubernetesClusterMonitoring',
    'cloudify.gcp.nodes.KubernetesClusterlegacyAbac',
    'cloudify.gcp.nodes.KubernetesClusterNetworkPolicy',
    'cloudify.gcp.nodes.Topic',
    'cloudify.gcp.nodes.TopicPolicy',
    'cloudify.gcp.nodes.TopicMessage',
    'cloudify.gcp.nodes.Subscription',
    'cloudify.gcp.nodes.SubscriptionPolicy',
    'cloudify.gcp.nodes.Acknowledge',
    'cloudify.gcp.nodes.PullRequest',
    'cloudify.gcp.nodes.StackDriverGroup',
    'cloudify.gcp.nodes.StackDriverTimeSeries',
    'cloudify.gcp.nodes.StackDriverUpTimeCheckConfig',
    'cloudify.gcp.nodes.LoggingSink',
    'cloudify.gcp.nodes.LoggingExclusion',
    'cloudify.gcp.nodes.Logging.BillingAccounts.sinks',
    'cloudify.gcp.nodes.Logging.Folders.sinks',
    'cloudify.gcp.nodes.Logging.Organizations.sinks',
    'cloudify.gcp.nodes.Logging.Projects.sinks',
    'cloudify.gcp.nodes.Logging.BillingAccounts.exclusions',
    'cloudify.gcp.nodes.Logging.Folders.exclusions',
    'cloudify.gcp.nodes.Logging.Organizations.exclusions',
    'cloudify.gcp.nodes.Logging.Organizatios.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.metrics',
    'cloudify.nodes.gcp.IAM.Role',
    'cloudify.nodes.gcp.Project',
    'cloudify.gcp.nodes.IAM.Role',
    'cloudify.nodes.gcp.Gcp'
]

AZURE_TYPES = [
    'cloudify.azure.nodes.ResourceGroup',
    'cloudify.azure.nodes.storage.StorageAccount'
    'cloudify.azure.nodes.storage.DataDisk'
    'cloudify.azure.nodes.storage.FileShare'
    'cloudify.azure.nodes.network.VirtualNetwork'
    'cloudify.azure.nodes.network.NetworkSecurityGroup'
    'cloudify.azure.nodes.network.NetworkSecurityRule'
    'cloudify.azure.nodes.network.Subnet'
    'cloudify.azure.nodes.network.RouteTable'
    'cloudify.azure.nodes.network.Route'
    'cloudify.azure.nodes.network.NetworkInterfaceCard'
    'cloudify.azure.nodes.network.IPConfiguration'
    'cloudify.azure.nodes.network.PublicIPAddress'
    'cloudify.azure.nodes.compute.AvailabilitySet'
    'cloudify.azure.nodes.compute.VirtualMachine'
    'cloudify.azure.nodes.compute.WindowsVirtualMachine'
    'cloudify.azure.nodes.compute.VirtualMachineExtension'
    'cloudify.azure.nodes.network.LoadBalancer'
    'cloudify.azure.nodes.network.LoadBalancer.BackendAddressPool'
    'cloudify.azure.nodes.network.LoadBalancer.Probe'
    'cloudify.azure.nodes.network.LoadBalancer.IncomingNATRule'
    'cloudify.azure.nodes.network.LoadBalancer.Rule'
    'cloudify.azure.Deployment'
    'cloudify.azure.nodes.compute.ContainerService'
    'cloudify.azure.nodes.Plan'
    'cloudify.azure.nodes.WebApp'
    'cloudify.azure.nodes.PublishingUser'
    'cloudify.azure.nodes.compute.ManagedCluster'
    'cloudify.nodes.azure.ResourceGroup'
    'cloudify.nodes.azure.storage.StorageAccount'
    'cloudify.nodes.azure.storage.DataDisk'
    'cloudify.nodes.azure.storage.FileShare'
    'cloudify.nodes.azure.network.VirtualNetwork'
    'cloudify.nodes.azure.network.NetworkSecurityGroup'
    'cloudify.nodes.azure.network.NetworkSecurityRule'
    'cloudify.nodes.azure.network.Subnet'
    'cloudify.nodes.azure.network.RouteTable'
    'cloudify.nodes.azure.network.Route'
    'cloudify.nodes.azure.network.NetworkInterfaceCard'
    'cloudify.nodes.azure.network.IPConfiguration'
    'cloudify.nodes.azure.network.PublicIPAddress'
    'cloudify.nodes.azure.compute.AvailabilitySet'
    'cloudify.nodes.azure.compute.VirtualMachine'
    'cloudify.nodes.azure.compute.WindowsVirtualMachine'
    'cloudify.nodes.azure.compute.VirtualMachineExtension'
    'cloudify.nodes.azure.network.LoadBalancer'
    'cloudify.nodes.azure.network.LoadBalancer.BackendAddressPool'
    'cloudify.nodes.azure.network.LoadBalancer.Probe'
    'cloudify.nodes.azure.network.LoadBalancer.IncomingNATRule'
    'cloudify.nodes.azure.network.LoadBalancer.Rule'
    'cloudify.nodes.azure.compute.ContainerService'
    'cloudify.nodes.azure.Plan'
    'cloudify.nodes.azure.WebApp'
    'cloudify.nodes.azure.PublishingUser'
    'cloudify.nodes.azure.compute.ManagedCluster'
    'cloudify.nodes.azure.resources.Azure'
    'cloudify.azure.nodes.resources.Azure'
    'cloudify.nodes.azure.CustomTypes'
]


REQUIRED_RELATIONSHIPS = {
    'cloudify.nodes.aws.ec2.Subnet': {
        'cloudify.nodes.aws.ed2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.SecurityGroup': {
        'cloudify.nodes.aws.ed2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.InternetGateway': {
        'cloudify.nodes.aws.ed2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.RouteTable': {
        'cloudify.nodes.aws.ed2.Vpc': 'cloudify.relationships.contained_in',
        'cloudify.nodes.aws.ec2.Subnet': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.Route': {
        'cloudify.nodes.aws.ec2.RouteTable':
            'cloudify.relationships.contained_in',
    },
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress': {
        'cloudify.nodes.aws.ec2.SecurityGroup':
            'cloudify.relationships.contained_in',
    },
    'cloudify.nodes.aws.ec2.Interface': {
        'cloudify.nodes.aws.ec2.Subnet': 'cloudify.relationships.depends_on',
        'cloudify.nodes.aws.ec2.SecurityGroup':
            'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.ElasticIP': {
        'cloudify.nodes.aws.ec2.Interface':
            'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.Instances': {
        'cloudify.nodes.aws.ec2.Image':
            'cloudify.relationships.depends_on',
        'cloudify.nodes.aws.ec2.Interface':
            'cloudify.relationships.depends_on',
    },
}


AZURE_VALID_KEY = ['subscription_id', 'tenant_id', 'client_id', 'client_secret']
