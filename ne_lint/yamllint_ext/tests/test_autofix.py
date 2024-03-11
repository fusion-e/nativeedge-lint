# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import os
from mock import Mock
from tempfile import NamedTemporaryFile

from ne_lint.cli import FixParamValue
from ne_lint.yamllint_ext import autofix
from ne_lint.yamllint_ext.autofix import colons
from ne_lint.yamllint_ext.autofix import commas
from ne_lint.yamllint_ext.autofix import brackets
from ne_lint.yamllint_ext.autofix import add_label
from ne_lint.yamllint_ext.autofix import indentation
from ne_lint.yamllint_ext.autofix import empty_lines
from ne_lint.yamllint_ext.overrides import LintProblem
from ne_lint.yamllint_ext.autofix import trailing_spaces
from ne_lint.yamllint_ext.autofix import deprecated_node_types
from ne_lint.yamllint_ext.autofix import deprecated_relationships


def test_indentation_autofix():
    relative_root = os.path.join(os.path.dirname(__file__), 'resources')
    good_blueprint = os.path.join(relative_root, 'blueprint.yaml')
    bad_blueprint = os.path.join(relative_root, 'bad-blueprint.yaml')
    good_content = open(good_blueprint).readlines()
    bad_content = open(bad_blueprint).readlines()
    outfile = NamedTemporaryFile(mode='w', delete=False)
    outfile.writelines(bad_content)
    outfile.close()
    try:
        for line in [26, 35, 70]:
            indentation_problem = LintProblem(
                line=line,
                desc='wrong indentation: expected 6 but found 4',
                rule='indentation',
                column=None,
                file=outfile.name,
            )
            indentation_problem.fixes = [Mock(line=line, rule='indentation')]
            indentation.fix_indentation(problem=indentation_problem)
            if line != 70:
                notfixed = open(outfile.name)
                not_fixed_content = notfixed.readlines()
                notfixed.close()
                assert good_content != not_fixed_content
        fixed = open(outfile.name)
        fixed_content = fixed.readlines()
        fixed.close()
        assert good_content == fixed_content
    finally:
        os.remove(outfile.name)


def test_fix_commas():
    expected = [
        "aws_region_name, z\n",
        "display_label, Aws Region Name\n",
        "type, string\n",
        "default, us-east-1\n",
        "constraints, f\n",
        "valid_values,",
    ]
    lines = """aws_region_name      ,z
display_label     ,     Aws Region Name
type , string
default    , us-east-1
constraints,      f
valid_values ,
"""

    fix_commas_file = get_file(lines)

    try:
        problems = [
            LintProblem(
                line=1,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
            LintProblem(
                line=2,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
            LintProblem(
                line=3,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
            LintProblem(
                line=4,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
            LintProblem(
                line=5,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
            LintProblem(
                line=6,
                column=0,
                desc='too many spaces before colon',
                rule='commas',
                file=fix_commas_file.name
            ),
        ]
        for problem in problems:
            commas.fix_commas(problem)
    finally:
        f = open(fix_commas_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_commas_file.name)
    assert expected == result_lines


def test_fix_colons():
    expected = [
        "aws_region_name: z\n",
        "display_label: Aws Region Name\n",
        "type: string\n",
        "default: us-east-1\n",
        "constraints: f\n",
        "valid_values: \n",
    ]
    lines = """aws_region_name      :z
display_label     :     Aws Region Name
type : string
default    : us-east-1
constraints:      f
valid_values :
"""

    fix_colons_file = get_file(lines)

    try:
        problems = [
            LintProblem(
                line=1,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
            LintProblem(
                line=2,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
            LintProblem(
                line=3,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
            LintProblem(
                line=4,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
            LintProblem(
                line=5,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
            LintProblem(
                line=6,
                column=0,
                desc='too many spaces before colon',
                rule='colons',
                file=fix_colons_file.name
            ),
        ]
        for problem in problems:
            colons.fix_colons(problem)
    finally:
        f = open(fix_colons_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_colons_file.name)
    assert expected == result_lines


def get_file(lines):
    fix_truthy_file = NamedTemporaryFile(delete=False)
    f = open(fix_truthy_file.name, 'w')
    if isinstance(lines, str):
        f.write(lines)
    else:
        f.writelines(lines)
    f.close()
    return f


def test_fix_add_label():
    content = """
foo:
  type: bar
baz:
  type: qux
"""
    expected = """
foo:
  display_label: Foo
  type: bar
baz:
  display_label: Baz
  type: qux
"""

    fix_indentation_file = get_file(content)
    problems = [
        LintProblem(
            line=2,
            column=0,
            desc=' is missing a display_label.',
            rule='inputs',
            file=fix_indentation_file.name
        ),
        LintProblem(
            line=4,
            column=0,
            desc=' is missing a display_label.',
            rule='inputs',
            file=fix_indentation_file.name
        ),
    ]
    fix = FixParamValue('all=-1')
    problems[0].fixes = [fix]
    problems[1].fixes = [fix]
    try:
        add_label.fix_add_label(problems)
    finally:
        f = open(fix_indentation_file.name, 'r')
        result = f.read()
        f.close()
        os.remove(fix_indentation_file.name)
    assert expected == result


def test_fix_indentation():
    lines = [
        'foobar:\n',
        '      - foo\n',
        '      - bar\n',
    ]
    expected = [
        'foobar:\n',
        '  - foo\n',
        '  - bar\n',
    ]
    fix_indentation_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='wrong indentation: expected 2 but found 6',
                rule='indentation',
                file=fix_indentation_file.name
            )
            indentation.fix_indentation(problem)
    finally:
        f = open(fix_indentation_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_indentation_file.name)
    assert expected == result_lines


def test_braces():
    lines = [
        '{   They wanna get my      } \n',
        '{They wanna get my gold on the ceiling}\n',
        "{     I ain't blind, just a matter of time  }   \n",
        '{ Before you steal it }         \n',
        "{Its all right, ain't no guarding my high   }   \n"
    ]
    expected_lines = [
        '{ They wanna get my } \n',
        '{They wanna get my gold on the ceiling}\n',
        "{ I ain't blind, just a matter of time }   \n",
        '{ Before you steal it }         \n',
        "{Its all right, ain't no guarding my high }   \n"
    ]
    fix_braces_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='too many spaces inside braces',
                rule='braces',
                file=fix_braces_file.name
            )
            brackets.fix_spaces_in_brackets(problem)
    finally:
        f = open(fix_braces_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_braces_file.name)
    assert result_lines == expected_lines


def test_brackets():
    lines = [
        '[   They wanna get my      ] \n',
        '[They wanna get my gold on the ceiling]\n',
        "[     I ain't blind, just a matter of time  ]   \n",
        '[ Before you steal it ]         \n',
        "[Its all right, ain't no guarding my high   ]   \n"
    ]
    expected_lines = [
        '[ They wanna get my ] \n',
        '[They wanna get my gold on the ceiling]\n',
        "[ I ain't blind, just a matter of time ]   \n",
        '[ Before you steal it ]         \n',
        "[Its all right, ain't no guarding my high ]   \n"
    ]
    fix_brackets_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='too many spaces inside brackets',
                rule='brackets',
                file=fix_brackets_file.name
            )
            brackets.fix_spaces_in_brackets(problem)
    finally:
        f = open(fix_brackets_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_brackets_file.name)
    assert result_lines == expected_lines


def test_trailing_spaces():
    lines = [
        'They wanna get my      \n',
        'They wanna get my gold on the ceiling      \n',
        "I ain't blind, just a matter of time     \n",
        'Before you steal it         \n',
        "Its all right, ain't no guarding my high      \n"
    ]
    expected_lines = [
        'They wanna get my\n',
        'They wanna get my gold on the ceiling\n',
        "I ain't blind, just a matter of time\n",
        'Before you steal it\n',
        "Its all right, ain't no guarding my high\n"
    ]
    fix_trailing_spaces_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='foo',
                rule='trailing-spaces',
                file=fix_trailing_spaces_file.name
            )
            trailing_spaces.fix_trailing_spaces(problem)
    finally:
        f = open(fix_trailing_spaces_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_trailing_spaces_file.name)
    assert result_lines == expected_lines


def test_fix_truthy():
    lines = [
        '\n',
        'True, not everything is tRue.\n'
        'And if I say TRUE to you!\n',
        'true TruE TRue TrUE truE\n',
        'False falSe FalsE FALSE false,\n',
        '     "False"      "falsE"\n',
        '\n',
    ]
    expected_lines = [
        '\n',
        'True, not everything is tRue.\n',
        'And if I say true to you!\n',
        'true true true true true\n',
        'false false false false false,\n',
        '     "False"      "falsE"\n',
        '\n'
    ]
    fix_truthy_file = get_file(lines)
    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i + 1,
                column=0,
                desc='foo',
                rule='truthy',
                file=fix_truthy_file.name
            )
            autofix.fix_truthy(problem)
    finally:
        f = open(fix_truthy_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_truthy_file.name)
    assert result_lines == expected_lines


def test_empty_lines():
    lines = [
        "\n",
        "They wanna get my\n",
        "\n",
        "\n",
        "\n",
        "They wanna get my gold on the ceiling\n",
        "I ain't blind, just a matter of time\n",
        "Before you steal it\n",
        "\n",
        "\n",
        "\n",
        "Its all right, ain't no guarding my high\n",
        "\n",
        "\n",
        "\n"
    ]
    expected_lines = [
        "They wanna get my\n",
        "\n",
        "They wanna get my gold on the ceiling\n",
        "I ain't blind, just a matter of time\n",
        "Before you steal it\n",
        "\n",
        "Its all right, ain't no guarding my high\n",
    ]
    fix_empty_lines_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='foo',
                rule='trailing-spaces',
                file=fix_empty_lines_file.name
            )
            fix = FixParamValue('all=-1')
            problem.fixes = [fix]
            empty_lines.fix_empty_lines(problem)
    finally:
        f = open(fix_empty_lines_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_empty_lines_file.name)
    assert result_lines == expected_lines


def test_deprecated_node_types():
    # TODO: Update this to nativeedge.
    lines = [
        'cloudify.azure.nodes.resources.Azure\n',
        'cloudify.azure.nodes.compute.ManagedCluster\n',
        'cloudify.azure.nodes.compute.ContainerService\n',
        'cloudify.azure.nodes.network.LoadBalancer.Probe\n',
        'cloudify.azure.nodes.network.LoadBalancer.BackendAddressPool\n',
        'cloudify.azure.nodes.network.LoadBalancer.IncomingNATRule\n',
        'cloudify.azure.nodes.network.LoadBalancer.Rule\n',
        'cloudify.azure.nodes.network.LoadBalancer\n',
        'cloudify.azure.nodes.compute.VirtualMachineExtension\n',
        'cloudify.azure.nodes.PublishingUser\n',
        'cloudify.azure.nodes.WebApp\n',
        'cloudify.azure.nodes.Plan\n',
        'cloudify.azure.nodes.compute.WindowsVirtualMachine\n',
        'cloudify.azure.nodes.compute.AvailabilitySet\n',
        'cloudify.azure.nodes.network.Route\n',
        'cloudify.azure.nodes.network.NetworkSecurityRule\n',
        'cloudify.azure.nodes.network.RouteTable\n',
        'cloudify.azure.nodes.network.Subnet\n',
        'cloudify.azure.nodes.compute.VirtualMachine\n',
        'cloudify.azure.nodes.network.NetworkInterfaceCard\n',
        'cloudify.azure.nodes.network.NetworkSecurityGroup\n',
        'cloudify.azure.nodes.network.IPConfiguration\n',
        'cloudify.azure.nodes.network.VirtualNetwork\n',
        'cloudify.azure.nodes.network.PublicIPAddress\n',
        'cloudify.azure.nodes.ResourceGroup\n',
        'cloudify.azure.nodes.storage.StorageAccount\n',
        'cloudify.azure.nodes.storage.DataDisk\n',
        'cloudify.azure.nodes.storage.FileShare\n',
        'cloudify.azure.nodes.storage.VirtualNetwork\n',
        'cloudify.azure.nodes.storage.NetworkSecurityGroup\n',
        'cloudify.azure.nodes.storage.NetworkSecurityRule\n',
        'cloudify.azure.nodes.storage.RouteTable\n',
        'cloudify.azure.nodes.storage.Route\n',
        'cloudify.azure.nodes.storage.IPConfiguration\n',
        'cloudify.azure.nodes.storage.PublicIPAddress\n',
        'cloudify.azure.nodes.storage.AvailabilitySet\n',
        'cloudify.azure.nodes.storage.VirtualMachine\n',
        'cloudify.azure.nodes.storage.WindowsVirtualMachine\n',
        'cloudify.azure.nodes.storage.VirtualMachineExtension\n',
        'cloudify.azure.nodes.storage.LoadBalancer\n',
        'cloudify.azure.nodes.storage.BackendAddressPool\n',
        'cloudify.azure.nodes.storage.Probe\n',
        'cloudify.azure.nodes.storage.IncomingNATRule\n',
        'cloudify.azure.nodes.storage.Rule\n',
        'cloudify.azure.nodes.storage.ContainerService\n',
        'cloudify.azure.nodes.storage.Plan\n',
        'cloudify.azure.nodes.storage.WebApp\n',
        'cloudify.azure.nodes.storage.PublishingUser\n',
        'cloudify.azure.nodes.storage.ManagedCluster\n',
        'cloudify.azure.nodes.storage.Azure\n',

        'cloudify.openstack.nodes.Server\n',
        'cloudify.openstack.nodes.WindowsServer\n',
        'cloudify.openstack.nodes.KeyPair\n',
        'cloudify.openstack.nodes.Subnet\n',
        'cloudify.openstack.nodes.SecurityGroup\n',
        'cloudify.openstack.nodes.Router\n',
        'cloudify.openstack.nodes.Port\n',
        'cloudify.openstack.nodes.Network\n',
        'cloudify.openstack.nodes.FloatingIP\n',
        'cloudify.openstack.nodes.RBACPolicy\n',
        'cloudify.openstack.nodes.Volume\n',
        'cloudify.openstack.nova_net.nodes.FloatingIP\n',
        'cloudify.openstack.nova_net.nodes.SecurityGroup\n',
        'cloudify.openstack.nodes.Flavor\n',
        'cloudify.openstack.nodes.Image\n',
        'cloudify.openstack.nodes.Project\n',
        'cloudify.openstack.nodes.User\n',
        'cloudify.openstack.nodes.HostAggregate\n',
        'cloudify.openstack.nodes.ServerGroup\n',
        'cloudify.openstack.nodes.Routes\n'
    ]

    expected_lines = [
        'nativeedge.nodes.azure.resources.Azure\n',
        'nativeedge.nodes.azure.compute.ManagedCluster\n',
        'nativeedge.nodes.azure.compute.ContainerService\n',
        'nativeedge.nodes.azure.network.LoadBalancer.Probe\n',
        'nativeedge.nodes.azure.network.LoadBalancer.BackendAddressPool\n',
        'nativeedge.nodes.azure.network.LoadBalancer.IncomingNATRule\n',
        'nativeedge.nodes.azure.network.LoadBalancer.Rule\n',
        'nativeedge.nodes.azure.network.LoadBalancer\n',
        'nativeedge.nodes.azure.compute.VirtualMachineExtension\n',
        'nativeedge.nodes.azure.PublishingUser\n',
        'nativeedge.nodes.azure.WebApp\n',
        'nativeedge.nodes.azure.Plan\n',
        'nativeedge.nodes.azure.compute.WindowsVirtualMachine\n',
        'nativeedge.nodes.azure.compute.AvailabilitySet\n',
        'nativeedge.nodes.azure.network.Route\n',
        'nativeedge.nodes.azure.network.NetworkSecurityRule\n',
        'nativeedge.nodes.azure.network.RouteTable\n',
        'nativeedge.nodes.azure.network.Subnet\n',
        'nativeedge.nodes.azure.compute.VirtualMachine\n',
        'nativeedge.nodes.azure.network.NetworkInterfaceCard\n',
        'nativeedge.nodes.azure.network.NetworkSecurityGroup\n',
        'nativeedge.nodes.azure.network.IPConfiguration\n',
        'nativeedge.nodes.azure.network.VirtualNetwork\n',
        'nativeedge.nodes.azure.network.PublicIPAddress\n',
        'nativeedge.nodes.azure.ResourceGroup\n',
        'nativeedge.nodes.azure.storage.StorageAccount\n',
        'nativeedge.nodes.azure.storage.DataDisk\n',
        'nativeedge.nodes.azure.storage.FileShare\n',
        'nativeedge.nodes.azure.storage.VirtualNetwork\n',
        'nativeedge.nodes.azure.storage.NetworkSecurityGroup\n',
        'nativeedge.nodes.azure.storage.NetworkSecurityRule\n',
        'nativeedge.nodes.azure.storage.RouteTable\n',
        'nativeedge.nodes.azure.storage.Route\n',
        'nativeedge.nodes.azure.storage.IPConfiguration\n',
        'nativeedge.nodes.azure.storage.PublicIPAddress\n',
        'nativeedge.nodes.azure.storage.AvailabilitySet\n',
        'nativeedge.nodes.azure.storage.VirtualMachine\n',
        'nativeedge.nodes.azure.storage.WindowsVirtualMachine\n',
        'nativeedge.nodes.azure.storage.VirtualMachineExtension\n',
        'nativeedge.nodes.azure.storage.LoadBalancer\n',
        'nativeedge.nodes.azure.storage.BackendAddressPool\n',
        'nativeedge.nodes.azure.storage.Probe\n',
        'nativeedge.nodes.azure.storage.IncomingNATRule\n',
        'nativeedge.nodes.azure.storage.Rule\n',
        'nativeedge.nodes.azure.storage.ContainerService\n',
        'nativeedge.nodes.azure.storage.Plan\n',
        'nativeedge.nodes.azure.storage.WebApp\n',
        'nativeedge.nodes.azure.storage.PublishingUser\n',
        'nativeedge.nodes.azure.storage.ManagedCluster\n',
        'nativeedge.nodes.azure.storage.Azure\n',

        'nativeedge.nodes.openstack.Server\n',
        'nativeedge.nodes.openstack.WindowsServer\n',
        'nativeedge.nodes.openstack.KeyPair\n',
        'nativeedge.nodes.openstack.Subnet\n',
        'nativeedge.nodes.openstack.SecurityGroup\n',
        'nativeedge.nodes.openstack.Router\n',
        'nativeedge.nodes.openstack.Port\n',
        'nativeedge.nodes.openstack.Network\n',
        'nativeedge.nodes.openstack.FloatingIP\n',
        'nativeedge.nodes.openstack.RBACPolicy\n',
        'nativeedge.nodes.openstack.Volume\n',
        'nativeedge.nodes.openstack.FloatingIP\n',
        'nativeedge.nodes.openstack.SecurityGroup\n',
        'nativeedge.nodes.openstack.Flavor\n',
        'nativeedge.nodes.openstack.Image\n',
        'nativeedge.nodes.openstack.Project\n',
        'nativeedge.nodes.openstack.User\n',
        'nativeedge.nodes.openstack.HostAggregate\n',
        'nativeedge.nodes.openstack.ServerGroup\n',
        'nativeedge.nodes.openstack.Router\n'
    ]

    fix_trailing_spaces_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i+1,
                column=0,
                desc='deprecated node type. Replace usage of {} with '
                     '{}'.format(lines[i], expected_lines[i]),
                rule='node_templates',
                file=fix_trailing_spaces_file.name,
                fixable=True
            )
            deprecated_node_types.fix_deprecated_node_types(problem)
    finally:
        f = open(fix_trailing_spaces_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_trailing_spaces_file.name)
    assert result_lines == expected_lines


def test_relationships_types():
    lines = [
        'cloudify.azure.relationships.contained_in_resource_group\n',
        'cloudify.azure.relationships.contained_in_storage_account\n',
        'cloudify.azure.relationships.contained_in_virtual_network\n',
        'cloudify.azure.relationships.contained_in_network_security_group\n',
        'cloudify.azure.relationships.contained_in_route_table\n',
        'cloudify.azure.relationships.contained_in_load_balancer\n',
        'cloudify.azure.relationships.'
        'network_security_group_attached_to_subnet\n',
        'cloudify.azure.relationships.route_table_attached_to_subnet\n',
        'cloudify.azure.relationships.nic_connected_to_ip_configuration\n',
        'cloudify.azure.relationships.ip_configuration_connected_to_subnet\n',
        'cloudify.azure.relationships.'
        'ip_configuration_connected_to_public_ip\n',
        'cloudify.azure.relationships.connected_to_storage_account\n',
        'cloudify.azure.relationships.connected_to_data_disk\n',
        'cloudify.azure.relationships.connected_to_nic\n',
        'cloudify.azure.relationships.connected_to_availability_set\n',
        'cloudify.azure.relationships.connected_to_ip_configuration\n',
        'cloudify.azure.relationships.connected_to_lb_be_pool\n',
        'cloudify.azure.relationships.connected_to_lb_probe\n',
        'cloudify.azure.relationships.vmx_contained_in_vm\n',
        'cloudify.azure.relationships.nic_connected_to_lb_be_pool\n',
        'cloudify.azure.relationships.vm_connected_to_datadisk\n',
        'cloudify.azure.relationships.connected_to_aks_cluster\n',

        'cloudify.openstack.server_connected_to_server_group\n',
        'cloudify.openstack.server_connected_to_keypair\n',
        'cloudify.openstack.server_connected_to_port\n',
        'cloudify.openstack.server_connected_to_floating_ip\n',
        'cloudify.openstack.server_connected_to_security_group\n',
        'cloudify.openstack.port_connected_to_security_group\n',
        'cloudify.openstack.port_connected_to_floating_ip\n',
        'cloudify.openstack.port_connected_to_subnet\n',
        'cloudify.openstack.subnet_connected_to_router\n',
        'cloudify.openstack.volume_attached_to_server\n',
        'cloudify.openstack.route_connected_to_router\n',
        'cloudify.openstack.rbac_policy_applied_to\n'
    ]

    expected_lines = [
        'nativeedge.relationships.azure.contained_in_resource_group\n',
        'nativeedge.relationships.azure.contained_in_storage_account\n',
        'nativeedge.relationships.azure.contained_in_virtual_network\n',
        'nativeedge.relationships.azure.contained_in_network_security_group\n',
        'nativeedge.relationships.azure.contained_in_route_table\n',
        'nativeedge.relationships.azure.contained_in_load_balancer\n',
        'nativeedge.relationships.azure.network_security_group_attached_'
        'to_subnet\n',
        'nativeedge.relationships.azure.route_table_attached_to_subnet\n',
        'nativeedge.relationships.azure.nic_connected_to_ip_configuration\n',
        'nativeedge.relationships.azure.ip_configuration_connected_to_subnet\n', # noqa
        'nativeedge.relationships.azure.ip_configuration_connected_'
        'to_public_ip\n',
        'nativeedge.relationships.azure.connected_to_storage_account\n',
        'nativeedge.relationships.azure.connected_to_data_disk\n',
        'nativeedge.relationships.azure.connected_to_nic\n',
        'nativeedge.relationships.azure.connected_to_availability_set\n',
        'nativeedge.relationships.azure.connected_to_ip_configuration\n',
        'nativeedge.relationships.azure.connected_to_lb_be_pool\n',
        'nativeedge.relationships.azure.connected_to_lb_probe\n',
        'nativeedge.relationships.azure.vmx_contained_in_vm\n',
        'nativeedge.relationships.azure.nic_connected_to_lb_be_pool\n',
        'nativeedge.relationships.azure.vm_connected_to_datadisk\n',
        'nativeedge.relationships.azure.connected_to_aks_cluster\n',

        'nativeedge.relationships.openstack.server_connected_to_server_group\n', # noqa
        'nativeedge.relationships.openstack.server_connected_to_keypair\n',
        'nativeedge.relationships.openstack.server_connected_to_port\n',
        'nativeedge.relationships.openstack.server_connected_to_floating_ip\n',
        'nativeedge.relationships.openstack.server_connected_'
        'to_security_group\n',
        'nativeedge.relationships.openstack.port_connected_to_security_group\n', # noqa
        'nativeedge.relationships.openstack.port_connected_to_floating_ip\n',
        'nativeedge.relationships.openstack.port_connected_to_subnet\n',
        'nativeedge.relationships.openstack.subnet_connected_to_router\n',
        'nativeedge.relationships.openstack.volume_attached_to_server\n',
        'nativeedge.relationships.openstack.route_connected_to_router\n',
        'nativeedge.relationships.openstack.rbac_policy_applied_to\n'
    ]

    fix_trailing_spaces_file = get_file(lines)

    try:
        for i in range(0, len(lines)):
            problem = LintProblem(
                line=i,
                column=0,
                desc='deprecated relationship type. Replace usage '
                     'of {} with {}'.format(lines[i], expected_lines[i]),
                rule='relationships',
                file=fix_trailing_spaces_file.name,
                fixable=True
            )
            deprecated_relationships.fix_deprecated_relationships(problem)
    finally:
        f = open(fix_trailing_spaces_file.name, 'r')
        result_lines = f.readlines()
        f.close()
        os.remove(fix_trailing_spaces_file.name)

    assert result_lines == expected_lines


def test_client_config():
    # TODO: Update to nativeedge.
    lines = [
        '  vm:\n',
        '    type: nativeedge.nodes.aws.ec2.Instances\n',
        '    properties:\n',
        '      aws_config: *client_config\n',
    ]
    expected_lines = [
        '  vm:\n',
        '    type: nativeedge.nodes.aws.ec2.Instances\n',
        '    properties:\n',
        '      client_config: *client_config\n'
    ]
    fix_clinet_config_file = get_file(lines)

    problem = LintProblem(
        line=3,
        column=0,
        desc='The node template "vm" has deprecated property '
             '"aws_config". please use "client_config"',
        rule='node_templates',
        file=fix_clinet_config_file.name,
        fixable=True
    )
    deprecated_node_types.fix_deprecated_node_types(problem)
    f = open(fix_clinet_config_file.name, 'r')
    result_lines = f.readlines()
    f.close()
    os.remove(fix_clinet_config_file.name)
    assert result_lines == expected_lines
