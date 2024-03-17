# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import yaml

# TODO: Determine if we warn Cloudify node types.
deprecated_node_types = {
    'cloudify.azure.nodes.resources.Azure':
        'nativeedge.nodes.azure.resources.Azure',
    'cloudify.azure.nodes.compute.ManagedCluster':
        'nativeedge.nodes.azure.compute.ManagedCluster',
    'cloudify.azure.nodes.compute.ContainerService':
        'nativeedge.nodes.azure.compute.ContainerService',
    'cloudify.azure.nodes.network.LoadBalancer.Probe':
        'nativeedge.nodes.azure.network.LoadBalancer.Probe',
    'cloudify.azure.nodes.network.LoadBalancer.BackendAddressPool':
        'nativeedge.nodes.azure.network.LoadBalancer.BackendAddressPool',
    'cloudify.azure.nodes.network.LoadBalancer.IncomingNATRule':
        'nativeedge.nodes.azure.network.LoadBalancer.IncomingNATRule',
    'cloudify.azure.nodes.network.LoadBalancer.Rule':
        'nativeedge.nodes.azure.network.LoadBalancer.Rule',
    'cloudify.azure.nodes.network.LoadBalancer':
        'nativeedge.nodes.azure.network.LoadBalancer',
    'cloudify.azure.nodes.compute.VirtualMachineExtension':
        'nativeedge.nodes.azure.compute.VirtualMachineExtension',
    'cloudify.azure.nodes.PublishingUser':
        'nativeedge.nodes.azure.PublishingUser',
    'cloudify.azure.nodes.WebApp':
        'nativeedge.nodes.azure.WebApp',
    'cloudify.azure.nodes.Plan':
        'nativeedge.nodes.azure.Plan',
    'cloudify.azure.nodes.compute.WindowsVirtualMachine':
        'nativeedge.nodes.azure.compute.WindowsVirtualMachine',
    'cloudify.azure.nodes.compute.AvailabilitySet':
        'nativeedge.nodes.azure.compute.AvailabilitySet',
    'cloudify.azure.nodes.network.Route':
        'nativeedge.nodes.azure.network.Route',
    'cloudify.azure.nodes.network.NetworkSecurityRule':
        'nativeedge.nodes.azure.network.NetworkSecurityRule',
    'cloudify.azure.nodes.network.RouteTable':
        'nativeedge.nodes.azure.network.RouteTable',
    'cloudify.azure.nodes.network.Subnet':
        'nativeedge.nodes.azure.network.Subnet',
    'cloudify.azure.nodes.compute.VirtualMachine':
        'nativeedge.nodes.azure.compute.VirtualMachine',
    'cloudify.azure.nodes.network.NetworkInterfaceCard':
        'nativeedge.nodes.azure.network.NetworkInterfaceCard',
    'cloudify.azure.nodes.network.NetworkSecurityGroup':
        'nativeedge.nodes.azure.network.NetworkSecurityGroup',
    'cloudify.azure.nodes.network.IPConfiguration':
        'nativeedge.nodes.azure.network.IPConfiguration',
    'cloudify.azure.nodes.network.VirtualNetwork':
        'nativeedge.nodes.azure.network.VirtualNetwork',
    'cloudify.azure.nodes.network.PublicIPAddress':
        'nativeedge.nodes.azure.network.PublicIPAddress',
    'cloudify.azure.nodes.ResourceGroup':
        'nativeedge.nodes.azure.ResourceGroup',
    'cloudify.azure.nodes.storage.StorageAccount':
        'nativeedge.nodes.azure.storage.StorageAccount',
    'cloudify.azure.nodes.storage.DataDisk':
        'nativeedge.nodes.azure.storage.DataDisk',
    'cloudify.azure.nodes.storage.FileShare':
        'nativeedge.nodes.azure.storage.FileShare',
    'cloudify.azure.nodes.storage.VirtualNetwork':
        'nativeedge.nodes.azure.storage.VirtualNetwork',
    'cloudify.azure.nodes.storage.NetworkSecurityGroup':
        'nativeedge.nodes.azure.storage.NetworkSecurityGroup',
    'cloudify.azure.nodes.storage.NetworkSecurityRule':
        'nativeedge.nodes.azure.storage.NetworkSecurityRule',
    'cloudify.azure.nodes.storage.RouteTable':
        'nativeedge.nodes.azure.storage.RouteTable',
    'cloudify.azure.nodes.storage.Route':
        'nativeedge.nodes.azure.storage.Route',
    'cloudify.azure.nodes.storage.IPConfiguration':
        'nativeedge.nodes.azure.storage.IPConfiguration',
    'cloudify.azure.nodes.storage.PublicIPAddress':
        'nativeedge.nodes.azure.storage.PublicIPAddress',
    'cloudify.azure.nodes.storage.AvailabilitySet':
        'nativeedge.nodes.azure.storage.AvailabilitySet',
    'cloudify.azure.nodes.storage.VirtualMachine':
        'nativeedge.nodes.azure.storage.VirtualMachine',
    'cloudify.azure.nodes.storage.WindowsVirtualMachine':
        'nativeedge.nodes.azure.storage.WindowsVirtualMachine',
    'cloudify.azure.nodes.storage.VirtualMachineExtension':
        'nativeedge.nodes.azure.storage.VirtualMachineExtension',
    'cloudify.azure.nodes.storage.LoadBalancer':
        'nativeedge.nodes.azure.storage.LoadBalancer',
    'cloudify.azure.nodes.storage.BackendAddressPool':
        'nativeedge.nodes.azure.storage.BackendAddressPool',
    'cloudify.azure.nodes.storage.Probe':
        'nativeedge.nodes.azure.storage.Probe',
    'cloudify.azure.nodes.storage.IncomingNATRule':
        'nativeedge.nodes.azure.storage.IncomingNATRule',
    'cloudify.azure.nodes.storage.Rule':
        'nativeedge.nodes.azure.storage.Rule',
    'cloudify.azure.nodes.storage.ContainerService':
        'nativeedge.nodes.azure.storage.ContainerService',
    'cloudify.azure.nodes.storage.Plan':
        'nativeedge.nodes.azure.storage.Plan',
    'cloudify.azure.nodes.storage.WebApp':
        'nativeedge.nodes.azure.storage.WebApp',
    'cloudify.azure.nodes.storage.PublishingUser':
        'nativeedge.nodes.azure.storage.PublishingUser',
    'cloudify.azure.nodes.storage.ManagedCluster':
        'nativeedge.nodes.azure.storage.ManagedCluster',
    'cloudify.azure.nodes.storage.Azure':
        'nativeedge.nodes.azure.storage.Azure',

    'cloudify.openstack.nodes.Server':
        'nativeedge.nodes.openstack.Server',
    'cloudify.openstack.nodes.WindowsServer':
        'nativeedge.nodes.openstack.WindowsServer',
    'cloudify.openstack.nodes.KeyPair':
        'nativeedge.nodes.openstack.KeyPair',
    'cloudify.openstack.nodes.Subnet':
        'nativeedge.nodes.openstack.Subnet',
    'cloudify.openstack.nodes.SecurityGroup':
        'nativeedge.nodes.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Router':
        'nativeedge.nodes.openstack.Router',
    'cloudify.openstack.nodes.Port':
        'nativeedge.nodes.openstack.Port',
    'cloudify.openstack.nodes.Network':
        'nativeedge.nodes.openstack.Network',
    'cloudify.openstack.nodes.FloatingIP':
        'nativeedge.nodes.openstack.FloatingIP',
    'cloudify.openstack.nodes.RBACPolicy':
        'nativeedge.nodes.openstack.RBACPolicy',
    'cloudify.openstack.nodes.Volume':
        'nativeedge.nodes.s.openstack.Volume',
    'cloudify.openstack.nova_net.nodes.FloatingIP':
        'nativeedge.nodes.openstack.FloatingIP',
    'cloudify.openstack.nova_net.nodes.SecurityGroup':
        'nativeedge.nodes.s.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Flavor':
        'nativeedge.nodes.s.openstack.Flavor',
    'cloudify.openstack.nodes.Image':
        'nativeedge.nodes.openstack.Image',
    'cloudify.openstack.nodes.Project':
        'nativeedge.nodes.openstack.Project',
    'cloudify.openstack.nodes.User':
        'nativeedge.nodes.openstack.User',
    'cloudify.openstack.nodes.HostAggregate':
        'nativeedge.nodes.openstack.HostAggregate',
    'cloudify.openstack.nodes.ServerGroup':
        'nativeedge.nodes.openstack.ServerGroup',
    'cloudify.openstack.nodes.Routes':
        'nativeedge.nodes.openstack.Router',

    'cloudify.gcp.nodes.project':
        'nativeedge.nodes.gcp.project',
    'cloudify.gcp.nodes.PolicyBinding':
        'nativeedge.nodes.gcp.PolicyBinding',
    'cloudify.gcp.nodes.Instance':
        'nativeedge.nodes.gcp.Instance',
    'cloudify.gcp.nodes.InstanceGroup':
        'nativeedge.nodes.gcp.InstanceGroup',
    'cloudify.gcp.nodes.Volume':
        'nativeedge.nodes.gcp.Volume',
    'cloudify.gcp.nodes.Snapshot':
        'nativeedge.nodes.gcp.Snapshot',
    'cloudify.gcp.nodes.Network':
        'nativeedge.nodes.gcp.Network',
    'cloudify.gcp.nodes.SubNetwork':
        'nativeedge.nodes.gcp.SubNetwork',
    'cloudify.gcp.nodes.VPCNetworkPeering':
        'nativeedge.nodes.gcp.VPCNetworkPeering',
    'cloudify.gcp.nodes.Route':
        'nativeedge.nodes.gcp.Route',
    'cloudify.gcp.nodes.FirewallRule':
        'nativeedge.nodes.gcp.FirewallRule',
    'cloudify.gcp.nodes.SecurityGroup':
        'nativeedge.nodes.gcp.SecurityGroup',
    'cloudify.gcp.nodes.Access':
        'nativeedge.nodes.gcp.Access',
    'cloudify.gcp.nodes.KeyPair':
        'nativeedge.nodes.gcp.KeyPair',
    'cloudify.gcp.nodes.ExternalIP':
        'nativeedge.nodes.gcp.ExternalIP',
    'cloudify.gcp.nodes.GlobalAddress':
        'nativeedge.nodes.gcp.GlobalAddress',
    'cloudify.gcp.nodes.StaticIP':
        'nativeedge.nodes.gcp.StaticIP',
    'cloudify.gcp.nodes.Address':
        'nativeedge.nodes.gcp.Address',
    'cloudify.gcp.nodes.Imagev':
        'nativeedge.nodes.gcp.Image',
    'cloudify.gcp.nodes.HealthCheck':
        'nativeedge.nodes.gcp.HealthCheck',
    'cloudify.gcp.nodes.BackendService':
        'nativeedge.nodes.gcp.BackendService',
    'cloudify.gcp.nodes.RegionBackendService':
        'nativeedge.nodes.gcp.RegionBackendService',
    'cloudify.gcp.nodes.UrlMap':
        'nativeedge.nodes.s.gcp.UrlMap',
    'cloudify.gcp.nodes.TargetProxy':
        'nativeedge.nodes.gcp.TargetProxy',
    'cloudify.gcp.nodes.SslCertificate':
        'nativeedge.nodes.gcp.SslCertificate',
    'cloudify.gcp.nodes.ForwardingRule':
        'nativeedge.nodes.gcp.ForwardingRule',
    'cloudify.gcp.nodes.GlobalForwardingRule':
        'nativeedge.nodes.gcp.GlobalForwardingRule',
    'cloudify.gcp.nodes.DNSZone':
        'nativeedge.nodes.gcp.DNSZone',
    'cloudify.gcp.nodes.DNSRecord':
        'nativeedge.nodes.gcp.DNSRecord',
    'cloudify.gcp.nodes.DNSAAAARecord':
        'nativeedge.nodes.gcp.DNSAAAARecord',
    'cloudify.gcp.nodes.DNSMXRecord':
        'nativeedge.nodes.gcp.DNSMXRecord',
    'cloudify.gcp.nodes.DNSNSRecord':
        'nativeedge.nodes.gcp.DNSNSRecord',
    'cloudify.gcp.nodes.DNSTXTRecord':
        'nativeedge.nodes.gcp.DNSTXTRecord',
    'cloudify.gcp.nodes.KubernetesCluster':
        'nativeedge.nodes.gcp.KubernetesCluster',
    'cloudify.gcp.nodes.KubernetesNodePool':
        'nativeedge.nodes.gcp.KubernetesNodePool',
    'cloudify.gcp.nodes.KubernetesClusterMonitoring':
        'nativeedge.nodes.gcp.KubernetesClusterMonitoring',
    'cloudify.gcp.nodes.KubernetesClusterlegacyAbac':
        'nativeedge.nodes.gcp.KubernetesClusterlegacyAbac',
    'cloudify.gcp.nodes.KubernetesClusterNetworkPolicy':
        'nativeedge.nodes.gcp.KubernetesClusterNetworkPolicy',
    'cloudify.gcp.nodes.Topic':
        'nativeedge.nodes.gcp.Topic',
    'cloudify.gcp.nodes.TopicPolicy':
        'nativeedge.nodes.gcp.TopicPolicy',
    'cloudify.gcp.nodes.TopicMessage':
        'nativeedge.nodes.gcp.TopicMessage',
    'cloudify.gcp.nodes.Subscription':
        'nativeedge.nodes.gcp.Subscription',
    'cloudify.gcp.nodes.SubscriptionPolicy':
        'nativeedge.nodes.gcp.SubscriptionPolicy',
    'cloudify.gcp.nodes.Acknowledge':
        'nativeedge.nodes.gcp.Acknowledge',
    'cloudify.gcp.nodes.PullRequest':
        'nativeedge.nodes.gcp.PullRequest',
    'cloudify.gcp.nodes.StackDriverGroup':
        'nativeedge.nodes.gcp.StackDriverGroup',
    'cloudify.gcp.nodes.StackDriverTimeSeries':
        'nativeedge.nodes.gcp.StackDriverTimeSeries',
    'cloudify.gcp.nodes.StackDriverUpTimeCheckConfig':
        'nativeedge.nodes.gcp.StackDriverUpTimeCheckConfig',
    'cloudify.gcp.nodes.LoggingSink':
        'nativeedge.nodes.gcp.LoggingSink',
    'cloudify.gcp.nodes.LoggingExclusion':
        'nativeedge.nodes.gcp.LoggingExclusion',
    'cloudify.gcp.nodes.Logging.BillingAccounts.sinks':
        'nativeedge.nodes.gcp.Logging.BillingAccounts.sinks',
    'cloudify.gcp.nodes.Logging.Folders.sinks':
        'nativeedge.nodes.gcp.Logging.Folders.sinks',
    'cloudify.gcp.nodes.Logging.Organizations.sinks':
        'nativeedge.nodes.gcp.Logging.Organizations.sinks',
    'cloudify.gcp.nodes.Logging.Projects.sinks':
        'nativeedge.nodes.gcp.Logging.Projects.sinks',
    'cloudify.gcp.nodes.Logging.BillingAccounts.exclusions':
        'nativeedge.nodes.gcp.Logging.BillingAccounts.exclusions',
    'cloudify.gcp.nodes.Logging.Folders.exclusions':
        'nativeedge.nodes.gcp.Logging.Folders.exclusions',
    'cloudify.gcp.nodes.Logging.Organizations.exclusions':
        'nativeedge.nodes.gcp.Logging.Organizations.exclusions',
    'cloudify.gcp.nodes.Logging.Organizatios.exclusions':
        'nativeedge.nodes.gcp.Logging.Organizatios.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.exclusions':
        'nativeedge.nodes.gcp.Logging.Projects.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.metrics':
        'nativeedge.nodes.gcp.Logging.Projects.metrics',
    'cloudify.gcp.nodes.IAM.Role':
        'nativeedge.nodes.gcp.IAM.Role',
    'cloudify.gcp.nodes.Gcp':
        'nativeedge.nodes.gcp.Gcp',

    'cloudify.vsphere.nodes.Server':
        'nativeedge.nodes.vsphere.Server',
    'cloudify.vsphere.nodes.WindowsServer':
        'nativeedge.nodes.vsphere.WindowsServer',
    'cloudify.vsphere.nodes.Network':
        'nativeedge.nodes.vsphere.Network',
    'cloudify.vsphere.nodes.Storage':
        'nativeedge.nodes.vsphere.Storage',
    'cloudify.vsphere.nodes.IPPool':
        'nativeedge.nodes.vsphere.IPPool',
    'cloudify.vsphere.nodes.CloudInitISO':
        'nativeedge.nodes.vsphere.CloudInitISO',
    'cloudify.vsphere.nodes.Datacenter':
        'nativeedge.nodes.vsphere.Datacenter',
    'cloudify.vsphere.nodes.Datastore':
        'nativeedge.nodes.vsphere.Datastore',
    'cloudify.vsphere.nodes.Cluster':
        'nativeedge.nodes.vsphere.Cluster',
    'cloudify.vsphere.nodes.ResourcePool':
        'nativeedge.nodes.vsphere.ResourcePool',
    'cloudify.vsphere.nodes.VMFolder':
        'nativeedge.nodes.vsphere.VMFolder',
    'cloudify.vsphere.nodes.Host':
        'nativeedge.nodes.s.vsphere.Host',
    'cloudify.vsphere.nodes.ContentLibraryDeployment':
        'nativeedge.nodes.vsphere.ContentLibraryDeployment',
    'cloudify.vsphere.nodes.NIC':
        'nativeedge.nodes.vsphere.NIC',
    'cloudify.vsphere.nodes.SCSIController':
        'nativeedge.nodes.vsphere.SCSIController'
}

deprecated_relationship_types = {
    'cloudify.azure.relationships.contained_in_resource_group':
        'nativeedge.relationships.azure.contained_in_resource_group',
    'cloudify.azure.relationships.contained_in_storage_account':
        'nativeedge.relationships.azure.contained_in_storage_account',
    'cloudify.azure.relationships.contained_in_virtual_network':
        'nativeedge.relationships.azure.contained_in_virtual_network',
    'cloudify.azure.relationships.contained_in_network_security_group':
        'nativeedge.relationships.azure.contained_in_network_security_group',
    'cloudify.azure.relationships.contained_in_route_table':
        'nativeedge.relationships.azure.contained_in_route_table',
    'cloudify.azure.relationships.contained_in_load_balancer':
        'nativeedge.relationships.azure.contained_in_load_balancer',
    'cloudify.azure.relationships.network_security_group_attached_to_subnet':
        'nativeedge.relationships.azure.network_security_group_attached_to_subnet', # noqa
    'cloudify.azure.relationships.route_table_attached_to_subnet':
        'nativeedge.relationships.azure.route_table_attached_to_subnet',
    'cloudify.azure.relationships.nic_connected_to_ip_configuration':
        'nativeedge.relationships.azure.nic_connected_to_ip_configuration',
    'cloudify.azure.relationships.ip_configuration_connected_to_subnet':
        'nativeedge.relationships.azure.ip_configuration_connected_to_subnet',
    'cloudify.azure.relationships.ip_configuration_connected_to_public_ip':
        'nativeedge.relationships.azure.ip_configuration_connected_to_public_ip', # noqa
    'cloudify.azure.relationships.connected_to_storage_account':
        'nativeedge.relationships.azure.connected_to_storage_account',
    'cloudify.azure.relationships.connected_to_data_disk':
        'nativeedge.relationships.azure.connected_to_data_disk',
    'cloudify.azure.relationships.connected_to_nic':
        'nativeedge.relationships.azure.connected_to_nic',
    'cloudify.azure.relationships.connected_to_availability_set':
        'nativeedge.relationships.azure.connected_to_availability_set',
    'cloudify.azure.relationships.connected_to_ip_configuration':
        'nativeedge.relationships.azure.connected_to_ip_configuration',
    'cloudify.azure.relationships.connected_to_lb_be_pool':
        'nativeedge.relationships.azure.connected_to_lb_be_pool',
    'cloudify.azure.relationships.connected_to_lb_probe':
        'nativeedge.relationships.azure.connected_to_lb_probe',
    'cloudify.azure.relationships.vmx_contained_in_vm':
        'nativeedge.relationships.azure.vmx_contained_in_vm',
    'cloudify.azure.relationships.nic_connected_to_lb_be_pool':
        'nativeedge.relationships.azure.nic_connected_to_lb_be_pool',
    'cloudify.azure.relationships.vm_connected_to_datadisk':
        'nativeedge.relationships.azure.vm_connected_to_datadisk',
    'cloudify.azure.relationships.connected_to_aks_cluster':
        'nativeedge.relationships.azure.connected_to_aks_cluster',

    'cloudify.openstack.server_connected_to_server_group':
        'nativeedge.relationships.openstack.server_connected_to_server_group',
    'cloudify.openstack.server_connected_to_keypair':
        'nativeedge.relationships.openstack.server_connected_to_keypair',
    'cloudify.openstack.server_connected_to_port':
        'nativeedge.relationships.openstack.server_connected_to_port',
    'cloudify.openstack.server_connected_to_floating_ip':
        'nativeedge.relationships.openstack.server_connected_to_floating_ip',
    'cloudify.openstack.server_connected_to_security_group':
        'nativeedge.relationships.openstack.server_connected_to_security_group', # noqa
    'cloudify.openstack.port_connected_to_security_group':
        'nativeedge.relationships.openstack.port_connected_to_security_group',
    'cloudify.openstack.port_connected_to_floating_ip':
        'nativeedge.relationships.openstack.port_connected_to_floating_ip',
    'cloudify.openstack.port_connected_to_subnet':
        'nativeedge.relationships.openstack.port_connected_to_subnet',
    'cloudify.openstack.subnet_connected_to_router':
        'nativeedge.relationships.openstack.subnet_connected_to_router',
    'cloudify.openstack.volume_attached_to_server':
        'nativeedge.relationships.openstack.volume_attached_to_server',
    'cloudify.openstack.route_connected_to_router':
        'nativeedge.relationships.openstack.route_connected_to_router',
    'cloudify.openstack.rbac_policy_applied_to':
        'nativeedge.relationships.openstack.rbac_policy_applied_to',

    'cloudify.gcp.relationships.instance_connected_to_security_group':
        'nativeedge.relationships.gcp.instance_connected_to_security_group',
    'cloudify.gcp.relationships.instance_connected_to_ip':
        'nativeedge.relationships.gcp.instance_connected_to_ip',
    'cloudify.gcp.relationships.instance_connected_to_keypair':
        'nativeedge.relationships.gcp.instance_connected_to_keypair',
    'cloudify.gcp.relationships.instance_connected_to_disk':
        'nativeedge.relationships.gcp.instance_connected_to_disk',
    'cloudify.gcp.relationships.instance_connected_to_instance_group':
        'nativeedge.relationships.gcp.instance_connected_to_instance_group',
    'cloudify.gcp.relationships.uses_as_backend':
        'nativeedge.relationships.gcp.uses_as_backend',
    'cloudify.gcp.relationships.uses_as_region_backend':
        'nativeedge.relationships.gcp.uses_as_region_backend',
    'cloudify.gcp.relationships.contained_in_compute':
        'nativeedge.relationships.gcp.contained_in_compute',
    'cloudify.gcp.relationships.dns_record_contained_in_zone':
        'nativeedge.relationships.gcp.dns_record_contained_in_zone',
    'cloudify.gcp.relationships.dns_record_connected_to_instance':
        'nativeedge.relationships.gcp.dns_record_connected_to_instance',
    'cloudify.gcp.relationships.dns_record_connected_to_ip':
        'nativeedge.relationships.gcp.dns_record_connected_to_ip',
    'cloudify.gcp.relationships.contained_in_network':
        'nativeedge.relationships.gcp.contained_in_network',
    'cloudify.gcp.relationships.instance_contained_in_network':
        'nativeedge.relationships.gcp.instance_contained_in_network',
    'cloudify.gcp.relationships.forwarding_rule_connected_to_target_proxy':
        'nativeedge.relationships.gcp.forwarding_rule_connected_to_target_proxy', # noqa
    'cloudify.gcp.relationships.vpn_network_peering_connected_to_network':
        'nativeedge.relationships.gcp.vpn_network_peering_connected_to_network', # noqa
    'cloudify.gcp.relationships.subscription_connected_to_topic':
        'nativeedge.relationships.gcp.subscription_connected_to_topic',
    'cloudify.gcp.relationships.instance_remove_access_config':
        'nativeedge.relationships.gcp.instance_remove_access_config',

    'cloudify.vsphere.port_connected_to_network':
        'nativeedge.relationships.vsphere.port_connected_to_network',
    'cloudify.vsphere.port_connected_to_server':
        'nativeedge.relationships.vsphere.port_connected_to_server',
    'cloudify.vsphere.storage_connected_to_server':
        'nativeedge.relationships.vsphere.storage_connected_to_server',
    'cloudify.vsphere.nic_connected_to_server':
        'nativeedge.relationships.vsphere.nic_connected_to_server',
    'cloudify.vsphere.controller_connected_to_vm':
        'nativeedge.relationships.vsphere.controller_connected_to_vm',
}

ACCEPTED_LIST_TYPES = (
    yaml.tokens.BlockEntryToken,
    yaml.tokens.FlowSequenceStartToken
)

TERRAFORM_TYPES = [
    'nativeedge.nodes.terraform.Module',
]

AWS_TYPES = [
    'nativeedge.nodes.aws.dynamodb.Table',
    'nativeedge.nodes.aws.iam.Group',
    'nativeedge.nodes.aws.iam.AccessKey',
    'nativeedge.nodes.aws.iam.LoginProfile',
    'nativeedge.nodes.aws.iam.User',
    'nativeedge.nodes.aws.iam.Role',
    'nativeedge.nodes.aws.iam.RolePolicy',
    'nativeedge.nodes.aws.iam.InstanceProfile',
    'nativeedge.nodes.aws.iam.Policy',
    'nativeedge.nodes.aws.lambda.Function',
    'nativeedge.nodes.aws.lambda.Invoke',
    'nativeedge.nodes.aws.lambda.Permission',
    'nativeedge.nodes.aws.rds.Instance',
    'nativeedge.nodes.aws.rds.InstanceReadReplica',
    'nativeedge.nodes.aws.rds.SubnetGroup',
    'nativeedge.nodes.aws.rds.OptionGroup',
    'nativeedge.nodes.aws.rds.Option',
    'nativeedge.nodes.aws.rds.ParameterGroup',
    'nativeedge.nodes.aws.rds.Parameter',
    'nativeedge.nodes.aws.route53.HostedZone',
    'nativeedge.nodes.aws.route53.RecordSet',
    'nativeedge.nodes.aws.SQS.Queue',
    'nativeedge.nodes.aws.SNS.Topic',
    'nativeedge.nodes.aws.SNS.Subscription',
    'nativeedge.nodes.aws.elb.LoadBalancer',
    'nativeedge.nodes.aws.elb.Classic.LoadBalancer',
    'nativeedge.nodes.aws.elb.Classic.HealthCheck',
    'nativeedge.nodes.aws.elb.Listener',
    'nativeedge.nodes.aws.elb.Classic.Listener',
    'nativeedge.nodes.aws.elb.Rule',
    'nativeedge.nodes.aws.elb.TargetGroup',
    'nativeedge.nodes.aws.elb.Classic.Policy',
    'nativeedge.nodes.aws.elb.Classic.Policy.Stickiness',
    'nativeedge.nodes.aws.s3.BaseBucket',
    'nativeedge.nodes.aws.s3.BaseBucketObject',
    'nativeedge.nodes.aws.s3.Bucket',
    'nativeedge.nodes.aws.s3.BucketPolicy',
    'nativeedge.nodes.aws.s3.BucketLifecycleConfiguration',
    'nativeedge.nodes.aws.s3.BucketTagging',
    'nativeedge.nodes.aws.s3.BucketObject',
    'nativeedge.nodes.aws.ec2.BaseType',
    'nativeedge.nodes.aws.ec2.Vpc',
    'nativeedge.nodes.aws.ec2.VpcPeering',
    'nativeedge.nodes.aws.ec2.VpcPeeringRequest',
    'nativeedge.nodes.aws.ec2.VpcPeeringAcceptRequest',
    'nativeedge.nodes.aws.ec2.VpcPeeringRejectRequest',
    'nativeedge.nodes.aws.ec2.Subnet',
    'nativeedge.nodes.aws.ec2.SecurityGroup',
    'nativeedge.nodes.aws.ec2.SecurityGroupRuleIngress',
    'nativeedge.nodes.aws.ec2.SecurityGroupRuleEgress',
    'nativeedge.nodes.aws.ec2.NATGateway',
    'nativeedge.nodes.aws.ec2.Interface',
    'nativeedge.nodes.aws.ec2.Instances',
    'nativeedge.nodes.aws.ec2.SpotInstances',
    'nativeedge.nodes.aws.ec2.SpotFleetRequest',
    'nativeedge.nodes.aws.ec2.Keypair',
    'nativeedge.nodes.aws.ec2.ElasticIP',
    'nativeedge.nodes.aws.ec2.NetworkACL',
    'nativeedge.nodes.aws.ec2.NetworkAclEntry',
    'nativeedge.nodes.aws.ec2.DHCPOptions',
    'nativeedge.nodes.aws.ec2.VPNGateway',
    'nativeedge.nodes.aws.ec2.VPNConnection',
    'nativeedge.nodes.aws.ec2.VPNConnectionRoute',
    'nativeedge.nodes.aws.ec2.CustomerGateway',
    'nativeedge.nodes.aws.ec2.InternetGateway',
    'nativeedge.nodes.aws.ec2.TransitGateway',
    'nativeedge.nodes.aws.ec2.TransitGatewayRouteTable',
    'nativeedge.nodes.aws.ec2.TransitGatewayRoute',
    'nativeedge.nodes.aws.ec2.RouteTable',
    'nativeedge.nodes.aws.ec2.Route',
    'nativeedge.nodes.aws.ec2.Image',
    'nativeedge.nodes.aws.ec2.Tags',
    'nativeedge.nodes.aws.ec2.EBSVolume',
    'nativeedge.nodes.aws.ec2.EBSAttachment',
    'nativeedge.nodes.aws.autoscaling.Group',
    'nativeedge.nodes.aws.autoscaling.LaunchConfiguration',
    'nativeedge.nodes.aws.autoscaling.Policy',
    'nativeedge.nodes.aws.autoscaling.LifecycleHook',
    'nativeedge.nodes.aws.autoscaling.NotificationConfiguration',
    'nativeedge.nodes.aws.cloudwatch.Alarm',
    'nativeedge.nodes.aws.cloudwatch.Rule',
    'nativeedge.nodes.aws.cloudwatch.Event',
    'nativeedge.nodes.aws.cloudwatch.Target',
    'nativeedge.nodes.aws.efs.FileSystem',
    'nativeedge.nodes.aws.efs.MountTarget',
    'nativeedge.nodes.aws.efs.FileSystemTags',
    'nativeedge.nodes.aws.kms.CustomerMasterKey',
    'nativeedge.nodes.aws.kms.Alias',
    'nativeedge.nodes.aws.kms.Grant',
    'nativeedge.nodes.aws.CloudFormation.Stack',
    'nativeedge.nodes.aws.ecs.Cluster',
    'nativeedge.nodes.aws.ecs.Service',
    'nativeedge.nodes.aws.ecs.TaskDefinition',
    'nativeedge.nodes.swift.s3.Bucket',
    'nativeedge.nodes.swift.s3.BucketObject',
    'nativeedge.nodes.aws.eks.Cluster',
    'nativeedge.nodes.aws.eks.NodeGroup',
    'nativeedge.nodes.aws.codepipeline.Pipeline',
    'nativeedge.nodes.resources.AmazonWebServices']

GCP_TYPES = [
    'cloudify.gcp.project',
    'nativeedge.nodes.gcp.PolicyBinding',
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
    'nativeedge.nodes.gcp.IAM.Role',
    'nativeedge.nodes.gcp.Project',
    'cloudify.gcp.nodes.IAM.Role',
    'nativeedge.nodes.gcp.Gcp'
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
    'nativeedge.nodes.azure.ResourceGroup'
    'nativeedge.nodes.azure.storage.StorageAccount'
    'nativeedge.nodes.azure.storage.DataDisk'
    'nativeedge.nodes.azure.storage.FileShare'
    'nativeedge.nodes.azure.network.VirtualNetwork'
    'nativeedge.nodes.azure.network.NetworkSecurityGroup'
    'nativeedge.nodes.azure.network.NetworkSecurityRule'
    'nativeedge.nodes.azure.network.Subnet'
    'nativeedge.nodes.azure.network.RouteTable'
    'nativeedge.nodes.azure.network.Route'
    'nativeedge.nodes.azure.network.NetworkInterfaceCard'
    'nativeedge.nodes.azure.network.IPConfiguration'
    'nativeedge.nodes.azure.network.PublicIPAddress'
    'nativeedge.nodes.azure.compute.AvailabilitySet'
    'nativeedge.nodes.azure.compute.VirtualMachine'
    'nativeedge.nodes.azure.compute.WindowsVirtualMachine'
    'nativeedge.nodes.azure.compute.VirtualMachineExtension'
    'nativeedge.nodes.azure.network.LoadBalancer'
    'nativeedge.nodes.azure.network.LoadBalancer.BackendAddressPool'
    'nativeedge.nodes.azure.network.LoadBalancer.Probe'
    'nativeedge.nodes.azure.network.LoadBalancer.IncomingNATRule'
    'nativeedge.nodes.azure.network.LoadBalancer.Rule'
    'nativeedge.nodes.azure.compute.ContainerService'
    'nativeedge.nodes.azure.Plan'
    'nativeedge.nodes.azure.WebApp'
    'nativeedge.nodes.azure.PublishingUser'
    'nativeedge.nodes.azure.compute.ManagedCluster'
    'nativeedge.nodes.azure.resources.Azure'
    'cloudify.azure.nodes.resources.Azure'
    'nativeedge.nodes.azure.CustomTypes'
]


REQUIRED_RELATIONSHIPS = {
    'nativeedge.nodes.aws.ec2.Subnet': {
        'nativeedge.nodes.aws.ec2.Vpc': 'nativeedge.relationships.depends_on',
    },
    'nativeedge.nodes.aws.ec2.SecurityGroup': {
        'nativeedge.nodes.aws.ec2.Vpc': 'nativeedge.relationships.depends_on',
    },
    'nativeedge.nodes.aws.ec2.RouteTable': {
        'nativeedge.nodes.aws.ec2.Vpc': 'nativeedge.relationships.contained_in', # noqa
        'nativeedge.nodes.aws.ec2.Subnet': 'nativeedge.relationships.connected_to', # noqa
    },
    'nativeedge.nodes.aws.ec2.Route': {
        'nativeedge.nodes.aws.ec2.RouteTable':
            'nativeedge.relationships.contained_in',
    },
    'nativeedge.nodes.aws.ec2.SecurityGroupRuleIngress': {
        'nativeedge.nodes.aws.ec2.SecurityGroup':
            'nativeedge.relationships.contained_in',
    },
    'nativeedge.nodes.aws.ec2.Interface': {
        'nativeedge.nodes.aws.ec2.Subnet': 'nativeedge.relationships.depends_on', # noqa
        'nativeedge.nodes.aws.ec2.SecurityGroup':
            'nativeedge.relationships.depends_on',
    },
    'nativeedge.nodes.aws.ec2.Instances': {
        # 'nativeedge.nodes.aws.ec2.Image':
        #     'nativeedge.relationships.depends_on',
        'nativeedge.nodes.aws.ec2.Interface':
            'nativeedge.relationships.depends_on',
    },
    # azure
    'nativeedge.nodes.azure.compute.VirtualMachine': {
        'nativeedge.nodes.azure.ResourceGroup':
            'nativeedge.relationships.azure.contained_in_resource_group',
        'nativeedge.nodes.azure.storage.StorageAccount':
            'nativeedge.relationships.azure.connected_to_storage_account',
        'nativeedge.nodes.azure.network.NetworkInterfaceCard':
            'nativeedge.relationships.azure.connected_to_nic',
    },
    'nativeedge.nodes.azure.network.NetworkInterfaceCard': {
        'nativeedge.nodes.azure.ResourceGroup':
            'nativeedge.relationships.azure.contained_in_resource_group',
        'nativeedge.nodes.azure.network.NetworkSecurityGroup':
            'nativeedge.relationships.azure.'
            'nic_connected_to_network_security_group',
        'nativeedge.nodes.azure.network.IPConfiguration':
            'nativeedge.relationships.azure.nic_connected_to_ip_configuration'
    },
    'nativeedge.nodes.azure.network.IPConfiguration': {
        'nativeedge.nodes.azure.network.Subnet':
            'nativeedge.relationships.azure.ip_configuration_connected_to_subnet', # noqa
    },
    'nativeedge.nodes.azure.network.NetworkSecurityGroup': {
        'nativeedge.nodes.azure.ResourceGroup':
            'nativeedge.relationships.azure.contained_in_resource_group'
    },
    'nativeedge.nodes.azure.network.PublicIPAddress': {
        'nativeedge.nodes.azure.ResourceGroup':
            'nativeedge.relationships.azure.contained_in_resource_group'
    },
    'nativeedge.nodes.azure.network.Subnet': {
        'nativeedge.nodes.azure.network.VirtualNetwork':
            'nativeedge.relationships.azure.contained_in_virtual_network'
    },
    'nativeedge.nodes.azure.network.VirtualNetwork': {
        'nativeedge.nodes.azure.ResourceGroup':
            'nativeedge.relationships.azure.contained_in_resource_group'
    },
    # gcp
    'nativeedge.nodes.gcp.Instance': {
        'nativeedge.nodes.gcp.FirewallRule':
            'nativeedge.relationships.gcp.connected_to',
        'nativeedge.nodes.gcp.SubNetwork':
            'nativeedge.relationships.gcp.depends_on',
        'nativeedge.nodes.gcp.Volume': 'nativeedge.relationships.gcp.depends_on' # noqa
    },
    'nativeedge.nodes.gcp.FirewallRule': {
        'nativeedge.nodes.gcp.Network': 'nativeedge.relationships.gcp.connected_to' # noqa
    },
    'nativeedge.nodes.gcp.SubNetwork': {
        'nativeedge.nodes.gcp.Network':
            'nativeedge.relationships.gcp.contained_in_network'
    },
    # openstack
    'nativeedge.nodes.openstack.Server': {
        'nativeedge.nodes.openstack.Port':
            'nativeedge.relationships.openstack.server_connected_to_port',
        'nativeedge.nodes.CloudInit.CloudConfig':
            'nativeedge.relationships.depends_on'
    },
    'nativeedge.nodes.openstack.Subnet': {
        'nativeedge.nodes.openstack.Network':
            'nativeedge.relationships.contained_in',
        # 'nativeedge.nodes.openstack.Router':
        #     'nativeedge.relationships.openstack.subnet_connected_to_router'
    },
    'nativeedge.nodes.openstack.FloatingIP': {
        'nativeedge.nodes.openstack.Network':
            'nativeedge.relationships.connected_to'
    },
    'nativeedge.nodes.openstack.Port': {
        # 'nativeedge.nodes.openstack.Subnet':
        #     'nativeedge.relationships.openstack.port_connected_to_subnet',
        'nativeedge.nodes.openstack.SecurityGroup':
            'nativeedge.relationships.openstack.port_connected_to_security_group', # noqa
        # 'nativeedge.nodes.openstack.FloatingIP':
        #     'nativeedge.relationships.openstack.port_connected_to_floating_ip'
    },
    # terraform
    'nativeedge.nodes.terraform.Module': {
        'nativeedge.nodes.terraform':
            'nativeedge.relationships.terraform.run_on_host',
    }
}

security_group_validation_aws = [
    'nativeedge.nodes.aws.ec2.SecurityGroupRuleEgress',
    'nativeedge.nodes.aws.ec2.SecurityGroupRuleIngress',
    'nativeedge.nodes.aws.ec2.SecurityGroup'
]

security_group_validation_azure = [
    'cloudify.azure.nodes.network.NetworkSecurityGroup',
    'cloudify.azure.nodes.network.NetworkSecurityRule'
]

security_group_validation_openstack = [
    'nativeedge.nodes.openstack.SecurityGroup'
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

firewall_rule_gcp = ['nativeedge.nodes.gcp.FirewallRule']


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

AWS_TYPE_WITH_TAGS = [
    # BaseType
    'nativeedge.nodes.aws.ec2.Vpc',
    'nativeedge.nodes.aws.ec2.VpcPeering',
    'nativeedge.nodes.aws.ec2.Subnet',
    'nativeedge.nodes.aws.ec2.SecurityGroup',
    'nativeedge.nodes.aws.ec2.NATGateway',
    'nativeedge.nodes.aws.ec2.Interface',
    'nativeedge.nodes.aws.ec2.SpotFleetRequest',
    'nativeedge.nodes.aws.ec2.Keypair',
    'nativeedge.nodes.aws.ec2.NetworkACL',
    'nativeedge.nodes.aws.ec2.VPNGateway',
    'nativeedge.nodes.aws.ec2.CustomerGateway',
    'nativeedge.nodes.aws.ec2.InternetGateway',
    'nativeedge.nodes.aws.ec2.TransitGateway',
    'nativeedge.nodes.aws.ec2.TransitGatewayRouteTable',
    'nativeedge.nodes.aws.ec2.RouteTable',
    'nativeedge.nodes.aws.ec2.EBSVolume',

    # tags_property
    'nativeedge.nodes.aws.ec2.Instances',
    'nativeedge.nodes.aws.ec2.SpotInstances',
    'nativeedge.nodes.aws.ec2.ElasticIP',
]

DSL_1_0 = [
    'list',
    'dict',
    'regex',
    'float',
    'string',
    'integer',
    'boolean',
    'node_id',
    'textarea'
    'node_ids',
    'blueprint_id',
    'node_template',
    'deployment_id',
    'blueprint_ids',
    'operation_name',
    'deployment_ids',
    'capability_value',
    'node_instance_ids',
]

INPUTS_BY_DSL = {
    'nativeedge_1_0': DSL_1_0,
}
