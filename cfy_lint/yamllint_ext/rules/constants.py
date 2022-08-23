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
    'cloudify.openstack.nodes.Server':
        'cloudify.nodes.openstack.Server',
    'cloudify.openstack.nodes.WindowsServer':
        'cloudify.nodes.openstack.WindowsServer',
    'cloudify.openstack.nodes.KeyPair':
        'cloudify.nodes.openstack.KeyPair',
    'cloudify.openstack.nodes.Subnet':
        'cloudify.nodes.openstack.Subnet',
    'cloudify.openstack.nodes.SecurityGroup':
        'cloudify.nodes.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Router':
        'cloudify.nodes.openstack.Router',
    'cloudify.openstack.nodes.Port':
        'cloudify.nodes.openstack.Port',
    'cloudify.openstack.nodes.Network':
        'cloudify.nodes.openstack.Network',
    'cloudify.openstack.nodes.FloatingIP':
        'cloudify.nodes.openstack.FloatingIP',
    'cloudify.openstack.nodes.RBACPolicy':
        'cloudify.nodes.openstack.RBACPolicy',
    'cloudify.openstack.nodes.Volume':
        'cloudify.nodes.openstack.Volume',
    'cloudify.openstack.nova_net.nodes.FloatingIP':
        'cloudify.nodes.openstack.FloatingIP',
    'cloudify.openstack.nova_net.nodes.SecurityGroup':
        'cloudify.nodes.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Flavor':
        'cloudify.nodes.openstack.Flavor',
    'cloudify.openstack.nodes.Image':
        'cloudify.nodes.openstack.Image',
    'cloudify.openstack.nodes.Project':
        'cloudify.nodes.openstack.Project',
    'cloudify.openstack.nodes.User':
        'cloudify.nodes.openstack.User',
    'cloudify.openstack.nodes.HostAggregate':
        'cloudify.nodes.openstack.HostAggregate',
    'cloudify.openstack.nodes.ServerGroup':
        'cloudify.nodes.openstack.ServerGroup',
    'cloudify.openstack.nodes.Routes':
        'cloudify.nodes.openstack.Router'
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
        'cloudify.relationships.azure.network_security_group_attached_to_subnet', # noqa
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
    'cloudify.openstack.server_connected_to_server_group':
        'cloudify.relationships.openstack.server_connected_to_server_group',
    'cloudify.openstack.server_connected_to_keypair':
        'cloudify.relationships.openstack.server_connected_to_keypair',
    'cloudify.openstack.server_connected_to_port':
        'cloudify.relationships.openstack.server_connected_to_port',
    ' cloudify.openstack.server_connected_to_floating_ip':
        'cloudify.relationships.openstack.server_connected_to_floating_ip',
    'cloudify.openstack.server_connected_to_security_group':
        'cloudify.relationships.openstack.server_connected_to_security_group',
    'cloudify.openstack.port_connected_to_security_group':
        'cloudify.relationships.openstack.port_connected_to_security_group',
    'cloudify.openstack.port_connected_to_floating_ip':
        'cloudify.relationships.openstack.port_connected_to_floating_ip',
    'cloudify.openstack.port_connected_to_subnet':
        'cloudify.relationships.openstack.port_connected_to_subnet',
    'cloudify.openstack.subnet_connected_to_router':
        'cloudify.relationships.openstack.subnet_connected_to_router',
    'cloudify.openstack.volume_attached_to_server':
        'cloudify.relationships.openstack.volume_attached_to_server',
    'cloudify.openstack.route_connected_to_router':
        'cloudify.relationships.openstack.route_connected_to_router',
    'cloudify.openstack.rbac_policy_applied_to':
        'cloudify.relationships.openstack.rbac_policy_applied_to'
}

ACCEPTED_LIST_TYPES = (
    yaml.tokens.BlockEntryToken,
    yaml.tokens.FlowSequenceStartToken
)

TERRAFORM_TYPES = [
    'cloudify.nodes.terraform.Module',
]

AWS_TYPES = [
    'cloudify.nodes.aws.dynamodb.Table',
    'cloudify.nodes.aws.iam.Group',
    'cloudify.nodes.aws.iam.AccessKey',
    'cloudify.nodes.aws.iam.LoginProfile',
    'cloudify.nodes.aws.iam.User',
    'cloudify.nodes.aws.iam.Role',
    'cloudify.nodes.aws.iam.RolePolicy',
    'cloudify.nodes.aws.iam.InstanceProfile',
    'cloudify.nodes.aws.iam.Policy',
    'cloudify.nodes.aws.lambda.Function',
    'cloudify.nodes.aws.lambda.Invoke',
    'cloudify.nodes.aws.lambda.Permission',
    'cloudify.nodes.aws.rds.Instance',
    'cloudify.nodes.aws.rds.InstanceReadReplica',
    'cloudify.nodes.aws.rds.SubnetGroup',
    'cloudify.nodes.aws.rds.OptionGroup',
    'cloudify.nodes.aws.rds.Option',
    'cloudify.nodes.aws.rds.ParameterGroup',
    'cloudify.nodes.aws.rds.Parameter',
    'cloudify.nodes.aws.route53.HostedZone',
    'cloudify.nodes.aws.route53.RecordSet',
    'cloudify.nodes.aws.SQS.Queue',
    'cloudify.nodes.aws.SNS.Topic',
    'cloudify.nodes.aws.SNS.Subscription',
    'cloudify.nodes.aws.elb.LoadBalancer',
    'cloudify.nodes.aws.elb.Classic.LoadBalancer',
    'cloudify.nodes.aws.elb.Classic.HealthCheck',
    'cloudify.nodes.aws.elb.Listener',
    'cloudify.nodes.aws.elb.Classic.Listener',
    'cloudify.nodes.aws.elb.Rule',
    'cloudify.nodes.aws.elb.TargetGroup',
    'cloudify.nodes.aws.elb.Classic.Policy',
    'cloudify.nodes.aws.elb.Classic.Policy.Stickiness',
    'cloudify.nodes.aws.s3.BaseBucket',
    'cloudify.nodes.aws.s3.BaseBucketObject',
    'cloudify.nodes.aws.s3.Bucket',
    'cloudify.nodes.aws.s3.BucketPolicy',
    'cloudify.nodes.aws.s3.BucketLifecycleConfiguration',
    'cloudify.nodes.aws.s3.BucketTagging',
    'cloudify.nodes.aws.s3.BucketObject',
    'cloudify.nodes.aws.ec2.BaseType',
    'cloudify.nodes.aws.ec2.Vpc',
    'cloudify.nodes.aws.ec2.VpcPeering',
    'cloudify.nodes.aws.ec2.VpcPeeringRequest',
    'cloudify.nodes.aws.ec2.VpcPeeringAcceptRequest',
    'cloudify.nodes.aws.ec2.VpcPeeringRejectRequest',
    'cloudify.nodes.aws.ec2.Subnet',
    'cloudify.nodes.aws.ec2.SecurityGroup',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleEgress',
    'cloudify.nodes.aws.ec2.NATGateway',
    'cloudify.nodes.aws.ec2.Interface',
    'cloudify.nodes.aws.ec2.Instances',
    'cloudify.nodes.aws.ec2.SpotInstances',
    'cloudify.nodes.aws.ec2.SpotFleetRequest',
    'cloudify.nodes.aws.ec2.Keypair',
    'cloudify.nodes.aws.ec2.ElasticIP',
    'cloudify.nodes.aws.ec2.NetworkACL',
    'cloudify.nodes.aws.ec2.NetworkAclEntry',
    'cloudify.nodes.aws.ec2.DHCPOptions',
    'cloudify.nodes.aws.ec2.VPNGateway',
    'cloudify.nodes.aws.ec2.VPNConnection',
    'cloudify.nodes.aws.ec2.VPNConnectionRoute',
    'cloudify.nodes.aws.ec2.CustomerGateway',
    'cloudify.nodes.aws.ec2.InternetGateway',
    'cloudify.nodes.aws.ec2.TransitGateway',
    'cloudify.nodes.aws.ec2.TransitGatewayRouteTable',
    'cloudify.nodes.aws.ec2.TransitGatewayRoute',
    'cloudify.nodes.aws.ec2.RouteTable',
    'cloudify.nodes.aws.ec2.Route',
    'cloudify.nodes.aws.ec2.Image',
    'cloudify.nodes.aws.ec2.Tags',
    'cloudify.nodes.aws.ec2.EBSVolume',
    'cloudify.nodes.aws.ec2.EBSAttachment',
    'cloudify.nodes.aws.autoscaling.Group',
    'cloudify.nodes.aws.autoscaling.LaunchConfiguration',
    'cloudify.nodes.aws.autoscaling.Policy',
    'cloudify.nodes.aws.autoscaling.LifecycleHook',
    'cloudify.nodes.aws.autoscaling.NotificationConfiguration',
    'cloudify.nodes.aws.cloudwatch.Alarm',
    'cloudify.nodes.aws.cloudwatch.Rule',
    'cloudify.nodes.aws.cloudwatch.Event',
    'cloudify.nodes.aws.cloudwatch.Target',
    'cloudify.nodes.aws.efs.FileSystem',
    'cloudify.nodes.aws.efs.MountTarget',
    'cloudify.nodes.aws.efs.FileSystemTags',
    'cloudify.nodes.aws.kms.CustomerMasterKey',
    'cloudify.nodes.aws.kms.Alias',
    'cloudify.nodes.aws.kms.Grant',
    'cloudify.nodes.aws.CloudFormation.Stack',
    'cloudify.nodes.aws.ecs.Cluster',
    'cloudify.nodes.aws.ecs.Service',
    'cloudify.nodes.aws.ecs.TaskDefinition',
    'cloudify.nodes.swift.s3.Bucket',
    'cloudify.nodes.swift.s3.BucketObject',
    'cloudify.nodes.aws.eks.Cluster',
    'cloudify.nodes.aws.eks.NodeGroup',
    'cloudify.nodes.aws.codepipeline.Pipeline',
    'cloudify.nodes.resources.AmazonWebServices']

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
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.SecurityGroup': {
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.RouteTable': {
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.contained_in',
        'cloudify.nodes.aws.ec2.Subnet': 'cloudify.relationships.connected_to',
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
    'cloudify.nodes.aws.ec2.Instances': {
        'cloudify.nodes.aws.ec2.Image':
            'cloudify.relationships.depends_on',
        'cloudify.nodes.aws.ec2.Interface':
            'cloudify.relationships.depends_on',
    },
    # azure
    'cloudify.nodes.azure.compute.VirtualMachine': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group',
        'cloudify.nodes.azure.storage.StorageAccount':
            'cloudify.relationships.azure.connected_to_storage_account',
        'cloudify.nodes.azure.network.NetworkInterfaceCard':
            'cloudify.relationships.azure.connected_to_nic',
    },
    'cloudify.nodes.azure.network.NetworkInterfaceCard': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group',
        'cloudify.nodes.azure.network.NetworkSecurityGroup':
            'cloudify.relationships.azure.'
            'nic_connected_to_network_security_group',
        'cloudify.nodes.azure.network.IPConfiguration':
            'cloudify.relationships.azure.nic_connected_to_ip_configuration'
    },
    'cloudify.nodes.azure.network.IPConfiguration': {
        'cloudify.nodes.azure.network.Subnet':
            'cloudify.relationships.azure.ip_configuration_connected_to_subnet', # noqa
    },
    'cloudify.nodes.azure.network.NetworkSecurityGroup': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    'cloudify.nodes.azure.network.PublicIPAddress': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    'cloudify.nodes.azure.network.Subnet': {
        'cloudify.nodes.azure.network.VirtualNetwork':
            'cloudify.relationships.azure.contained_in_virtual_network'
    },
    'cloudify.nodes.azure.network.VirtualNetwork': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    # gcp
    'cloudify.nodes.gcp.Instance': {
        'cloudify.nodes.gcp.FirewallRule':
            'cloudify.relationships.gcp.connected_to',
        'cloudify.nodes.gcp.SubNetwork':
            'cloudify.relationships.gcp.depends_on',
        'cloudify.nodes.gcp.Volume': 'cloudify.relationships.gcp.depends_on'
    },
    'cloudify.nodes.gcp.FirewallRule': {
        'cloudify.nodes.gcp.Network': 'cloudify.relationships.gcp.connected_to'
    },
    'cloudify.nodes.gcp.SubNetwork': {
        'cloudify.nodes.gcp.Network':
            'cloudify.relationships.gcp.contained_in_network'
    },
    # openstack
    'cloudify.nodes.openstack.Server': {
        'cloudify.nodes.openstack.Port':
            'cloudify.relationships.openstack.server_connected_to_port',
        'cloudify.nodes.CloudInit.CloudConfig':
            'cloudify.relationships.depends_on'
    },
    'cloudify.nodes.openstack.Subnet': {
        'cloudify.nodes.openstack.Network':
            'cloudify.relationships.contained_in',
        # 'cloudify.nodes.openstack.Router':
        #     'cloudify.relationships.openstack.subnet_connected_to_router'
    },
    'cloudify.nodes.openstack.FloatingIP': {
        'cloudify.nodes.openstack.Network':
            'cloudify.relationships.connected_to'
    },
    'cloudify.nodes.openstack.Port': {
        # 'cloudify.nodes.openstack.Subnet':
        #     'cloudify.relationships.openstack.port_connected_to_subnet',
        'cloudify.nodes.openstack.SecurityGroup':
            'cloudify.relationships.openstack.port_connected_to_security_group', # noqa
        # 'cloudify.nodes.openstack.FloatingIP':
        #     'cloudify.relationships.openstack.port_connected_to_floating_ip'
    },
    # terraform
    'cloudify.nodes.terraform.Module': {
        'cloudify.nodes.terraform':
            'cloudify.relationships.terraform.run_on_host',
    }
}

security_group_validation_aws = [
    'cloudify.nodes.aws.ec2.SecurityGroupRuleEgress',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress',
    'cloudify.nodes.aws.ec2.SecurityGroup'
]

security_group_validation_azure = [
    'cloudify.azure.nodes.network.NetworkSecurityGroup',
    'cloudify.azure.nodes.network.NetworkSecurityRule'
]

security_group_validation_openstack = [
    'cloudify.nodes.openstack.SecurityGroup'
]

AZURE_VALID_KEY = [
    'subscription_id',
    'tenant_id',
    'client_id',
    'client_secret']

AWS_VALID_KEY = [
    'aws_access_key_id',
    'aws_secret_access_key',
    'region_name',
    'aws_session_token']

firewall_rule_gcp = ['cloudify.gcp.nodes.FirewallRule']


TFLINT_SUPPORTED_CONFIGS = [
    'config',
    'plugin',
    'rule',
    'variables',
    'varfile',
    'ignore_module',
    'disabled_by_default',
    'force',
    'module',
    'plugin_dir'
]

TERRATAG_SUPPORTED_FLAGS = [
    'dir',
    'skipTerratagFiles',
    'verbose',
    'filter'
]
