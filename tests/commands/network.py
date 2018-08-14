#
# Radek Vykydal <rvykydal@redhat.com>
#
# Copyright 2013 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#
import unittest

from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.network import FC3_NetworkData, FC4_NetworkData, \
    FC6_NetworkData, F16_NetworkData, F25_NetworkData, \
    RHEL4_NetworkData, RHEL6_NetworkData, RHEL7_NetworkData
from pykickstart.constants import BIND_TO_MAC
from pykickstart.version import FC3

class Network_TestCase(unittest.TestCase):
    def runTest(self):
        fc3_data1 = FC3_NetworkData()
        fc3_data2 = FC3_NetworkData()
        # test default values
        self.assertFalse(fc3_data1.nodns)
        self.assertTrue(fc3_data1.onboot)

        # test equality/non-equality
        self.assertEqual(fc3_data1, fc3_data2)
        self.assertFalse(fc3_data1 != fc3_data2) # test the __ne__ method
        self.assertNotEqual(fc3_data1, None)

        for attr in ['device']:
            setattr(fc3_data1, attr, '')
            setattr(fc3_data2, attr, 'test')
            self.assertNotEqual(fc3_data1, fc3_data2)
            self.assertNotEqual(fc3_data2, fc3_data1)
            setattr(fc3_data1, attr, '')
            setattr(fc3_data2, attr, '')

        fc4_data = FC4_NetworkData()
        self.assertFalse(fc4_data.notksdevice)

        fc6_data = FC6_NetworkData()
        self.assertFalse(fc6_data.noipv4)
        self.assertFalse(fc6_data.noipv6)

        f16_data = F16_NetworkData()
        self.assertFalse(f16_data.activate)
        self.assertFalse(f16_data.nodefroute)

        f25_data = F25_NetworkData(activate=False)
        self.assertTrue(f25_data._getArgsAsStr().find('--no-activate') > -1)

        rhel4_data = RHEL4_NetworkData()
        self.assertFalse(rhel4_data.notksdevice)

        rhel6_data = RHEL6_NetworkData()
        self.assertFalse(rhel6_data.activate)
        self.assertFalse(rhel6_data.nodefroute)

        rhel7_data = RHEL7_NetworkData(activate=False)
        self.assertTrue(rhel7_data._getArgsAsStr().find('--no-activate') > -1)


class FC3_TestCase(CommandTest):
    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.bootProtos = ["dhcp", "bootp", "static"]

    def runTest(self):
        # equality
        self.assertEqual(self.assert_parse("network --device=eth0"), self.assert_parse("network --device=eth0"))
        self.assertNotEqual(self.assert_parse("network --device=eth0"), None)
        self.assertNotEqual(self.assert_parse("network --device=eth0"), self.assert_parse("network --device=eth1"))

        # pass
        self.assert_parse("network --device=eth0 --dhcpclass CLASS",
                          "network  --bootproto=dhcp --dhcpclass=CLASS --device=eth0\n")
        self.assert_parse("network --device=eth0 --essid ESSID --wepkey WEPKEY",
                          "network  --bootproto=dhcp --device=eth0 --essid=\"ESSID\" --wepkey=WEPKEY\n")
        self.assert_parse("network --device=eth0 --ethtool \"gro on\" --mtu=1200",
                          "network  --bootproto=dhcp --device=eth0 --ethtool=\"gro on\" --mtu=1200\n")
        self.assert_parse("network --device=eth0 --gateway gateway.wherever.com --hostname server.wherever.com",
                          "network  --bootproto=dhcp --device=eth0 --gateway=gateway.wherever.com --hostname=server.wherever.com\n")
        self.assert_parse("network --device=eth0 --ip 1.2.3.4 --netmask 255.255.255.0",
                          "network  --bootproto=dhcp --device=eth0 --ip=1.2.3.4 --netmask=255.255.255.0\n")
        self.assert_parse("network --device=eth0 --nameserver ns.wherever.com",
                          "network  --bootproto=dhcp --device=eth0 --nameserver=ns.wherever.com\n")
        self.assert_parse("network --device=eth0 --nodns",
                          "network  --bootproto=dhcp --device=eth0 --nodns\n")
        self.assert_parse("network --device=eth0 --onboot=off",
                          "network  --bootproto=dhcp --device=eth0 --onboot=off\n")

        for bp in self.bootProtos:
            self.assert_parse("network --device=eth0 --bootproto=%s" % bp,
                              "network  --bootproto=%s --device=eth0\n" % bp)

        # fail - invalid bootproto
        self.assert_parse_error("network --device=eth0 --bootproto=bogus")

        # fail - invalid option
        self.assert_parse_error("network --bogus-option")

        # extra test coverage
        nic = self.handler().NetworkData(device='eth0')
        cmd = self.handler().commands['network']
        self.assertEqual(cmd.__str__(), "")
        cmd.network.append(nic)
        self.assertEqual(cmd.__str__(), "# Network information\nnetwork  --bootproto=dhcp --device=eth0\n")


class FC3_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = FC3

    def runTest(self):
        self.assert_parse("""
network --device=eth0
network --device=eth1""")

        self.assert_parse_error("""
network --device=eth0
network --device=eth0""", KickstartParseWarning)

class RHEL4_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        self.assert_parse("network --notksdevice",
                          "network  --bootproto=dhcp --notksdevice\n")

class FC4_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        self.assert_parse("network --notksdevice",
                          "network  --bootproto=dhcp --notksdevice\n")

class FC6_TestCase(FC4_TestCase):
    def runTest(self):
        FC4_TestCase.runTest(self)

        # bootproto is removed if --noipv4 is given in F24.
        if isinstance(self, F24_TestCase):
            self.assert_parse("network --device=eth0 --noipv4",
                              "network  --device=eth0 --noipv4\n")
        else:
            self.assert_parse("network --device=eth0 --noipv4",
                              "network  --bootproto=dhcp --device=eth0 --noipv4\n")

        self.assert_parse("network --device=eth0 --noipv6",
                          "network  --bootproto=dhcp --device=eth0 --noipv6\n")

class F8_TestCase(FC6_TestCase):
    def runTest(self):
        FC6_TestCase.runTest(self)

        self.assert_parse("network --device=eth0 --ipv6=1:2:3:4",
                          "network  --bootproto=dhcp --device=eth0 --ipv6=1:2:3:4\n")

class RHEL6_TestCase(F8_TestCase):
    def runTest(self):
        F8_TestCase.runTest(self)

        self.assert_parse("network --device=eth0 --activate",
                          "network  --bootproto=dhcp --device=eth0 --activate\n")
        self.assert_parse("network --device=eth0 --nodefroute",
                          "network  --bootproto=dhcp --device=eth0 --nodefroute\n")
        self.assert_parse("network --device=eth0 --bondslaves=A,B --bondopts=opt1,opt2",
                          "network  --bootproto=dhcp --device=eth0 --bondslaves=A,B --bondopts=opt1,opt2\n")
        self.assert_parse("network --device=eth0 --vlanid=ID",
                          "network  --bootproto=dhcp --device=eth0 --vlanid=ID\n")

class F9_TestCase(F8_TestCase):
    def __init__(self, *kargs, **kwargs):
        F8_TestCase.__init__(self, *kargs, **kwargs)
        self.bootProtos.append("query")

class F16_TestCase(F9_TestCase):
    def __init__(self, *kargs, **kwargs):
        F9_TestCase.__init__(self, *kargs, **kwargs)
        self.bootProtos.append("ibft")

    def runTest(self):
        F9_TestCase.runTest(self)

        self.assert_parse("network --device=eth0 --activate",
                          "network  --bootproto=dhcp --device=eth0 --activate\n")
        self.assert_parse("network --device=eth0 --nodefroute",
                          "network  --bootproto=dhcp --device=eth0 --nodefroute\n")
        self.assert_parse("network --device=eth0 --wpakey WPAKEY",
                          "network  --bootproto=dhcp --device=eth0 --wpakey=WPAKEY\n")

class F18_TestCase(F16_TestCase):
    def runTest(self):
        F16_TestCase.runTest(self)

        cmd = self.handler().commands['network']
        self.assertEqual(cmd.hostname, None)

        cmd.network.append(self.handler().NetworkData(device='eth0'))
        cmd.network.append(
            self.handler().NetworkData(device='eth1', hostname='example.com')
        )
        self.assertEqual(cmd.hostname, 'example.com')


class F19_TestCase(F18_TestCase):
    def runTest(self):
        F18_TestCase.runTest(self)

        self.assert_parse("network --device=eth0 --bondslaves=A,B --bondopts=opt1,opt2",
                          "network  --bootproto=dhcp --device=eth0 --bondslaves=A,B --bondopts=opt1,opt2\n")
        self.assert_parse("network --device=eth0 --vlanid=ID",
                          "network  --bootproto=dhcp --device=eth0 --vlanid=ID\n")
        self.assert_parse("network --device=eth0 --ipv6gateway=gateway6.wherever.com",
                          "network  --bootproto=dhcp --device=eth0 --ipv6gateway=gateway6.wherever.com\n")

class F20_TestCase(F19_TestCase):
    def runTest(self):
        F19_TestCase.runTest(self)

        # team device

        cmd = "network --device team0 --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --teamslaves=\"p3p1'{\\\"prio\\\": -10, \\\"sticky\\\": true}',p3p2'{\\\"prio\\\": 100}'\" --teamconfig=\"{\\\"runner\\\": {\\\"name\\\": \\\"activebackup\\\"}}\" --activate"
        self.assert_parse(cmd)

        cmd = "network --device team0 --bootproto dhcp --teamslaves=p3p1,p3p2 --teamconfig=\"{\\\"runner\\\": {\\\"name\\\": \\\"roundrobin\\\"}}\" --activate"
        outputCmd = "network  --bootproto=dhcp --device=team0 --activate --teamslaves=\"p3p1,p3p2\" --teamconfig=\"{\\\"runner\\\": {\\\"name\\\": \\\"roundrobin\\\"}}\"\n"
        self.assert_parse(cmd, outputCmd)

        cmd = "network --device team0 --bootproto dhcp --teamslaves=''"
        outputCmd = "network  --bootproto=dhcp --device=team0\n"
        self.assert_parse(cmd, outputCmd)

        # --teamslaves
        # --teamslaves="<DEV1>['<CONFIG1>'],<DEV2>['<CONFIG2>'],..."
        # CONFIGX is json with " escaped to \"

        teamslaves_strings = [
            r"eth1,eth2",
            r"eth1,eth2'{\"prio\": 100}'",
            r"eth1'{\"prio\": -10, \"sticky\": true}',eth2",
            r"eth1'{\"prio\": -10, \"sticky\": true}',eth2'{\"prio\": 100}'",
            r"eth1,eth2,eth3",
            r"eth1,eth2'{\"prio\": 100}',eth3",
        ]

        teamslaves_values = [
            [('eth1', ""), ('eth2', "")],
            [('eth1', ""), ('eth2', '{"prio": 100}')],
            [('eth1', '{"prio": -10, "sticky": true}'), ('eth2', "")],
            [('eth1', '{"prio": -10, "sticky": true}'), ('eth2', '{"prio": 100}')],
            [('eth1', ""), ('eth2', ""), ('eth3', "")],
            [('eth1', ""), ('eth2', '{"prio": 100}'), ('eth3', "")],
        ]

        for string, value in zip(teamslaves_strings, teamslaves_values):
            network_data = self.assert_parse("network --device team0 --bootproto=dhcp --teamslaves=\"%s\"" % string)
            self.assertEqual(network_data.teamslaves, value)

        for value in teamslaves_values:
            nd = self.assert_parse("network --device team0 --bootproto=dhcp")
            nd.teamslaves = value
            s = "%s" % nd
            nd2 = self.assert_parse(s)
            self.assertEqual(value, nd2.teamslaves)

class F21_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)

        self.assert_parse("network --device=eth0 --interfacename=BLAH",
                          "network  --bootproto=dhcp --device=eth0 --interfacename=BLAH\n")

class F22_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

        # bridge options
        # pass
        self.assert_parse("network --device bridge0 --bootproto dhcp --bridgeslaves=ens3,ens7 --bridgeopts=priority=40000",
                          "network  --bootproto=dhcp --device=bridge0 --bridgeslaves=ens3,ens7 --bridgeopts=priority=40000\n")
        self.assert_parse("network --device bridge0 --bootproto dhcp "
                          "--bridgeslaves=ens3,ens7 "
                          "--bridgeopts=priority=40000,hello-time=3")
        # fail
        # slaves missing
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeopts=priority=40000")
        # bad options format
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeslaves=ens3,ens7 "
                                '--bridgeopts="priority=40000 hello-time=3"')
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeslaves=ens3,ens7 "
                                "--bridgeopts=priority")

class F24_TestCase(F22_TestCase):
    def runTest(self):
        F22_TestCase.runTest(self)

        # Test ipv4 only settings
        cmd = "network --noipv4 --activate --hostname=blah.test.com --ipv6=1:2:3:4:5:6:7:8 --device eth0 --nameserver=1:1:1:1::,2:2:2:2::"
        nd = self.assert_parse(cmd)
        self.assertEqual(nd.bootProto, "")
        self.assertEqual(nd.hostname, "blah.test.com")
        self.assertTrue(nd.noipv4)
        self.assertEqual(nd.ipv6, "1:2:3:4:5:6:7:8")
        self.assertIn("1:1:1:1::", nd.nameserver)
        self.assertIn("2:2:2:2::", nd.nameserver)
        self.assertEqual(nd.device, "eth0")

class F25_TestCase(F24_TestCase):
    def runTest(self):
        F24_TestCase.runTest(self)

        # activating a device
        network_data = self.assert_parse("network --device eth0")
        self.assertEqual(network_data.activate, None)
        network_data = self.assert_parse("network --device eth0 --no-activate")
        self.assertEqual(network_data.activate, False)
        network_data = self.assert_parse("network --device eth0 --activate")
        self.assertEqual(network_data.activate, True)
        network_data = self.assert_parse("network --device eth0 --activate --no-activate")
        self.assertEqual(network_data.activate, False)
        network_data = self.assert_parse("network --device eth0 --no-activate --activate")
        self.assertEqual(network_data.activate, True)

class F27_TestCase(F25_TestCase):
    def runTest(self):
        F25_TestCase.runTest(self)

        # binding the configuration to mac
        network_data = self.assert_parse("network --device eth0 --bindto mac")
        self.assertEqual(network_data.bindto, BIND_TO_MAC)
        network_data = self.assert_parse("network --device eth0")
        self.assertIsNone(network_data.bindto)
        # not allowed for vlan device type
        vlan_cmd = "network --device ens3 --vlanid 222 --bootproto dhcp"
        self.assert_parse(vlan_cmd)
        self.assert_parse_error(vlan_cmd + " --bindto mac")
        # but allowed for vlan over bond defined by single command, binds bond slaves
        vlan_over_bond_cmd = "network --device bond0 --bootproto static --ip 10.34.39.222 --netmask 255.255.255.0 --gateway 10.34.39.254 --bondslaves=ens4,ens5 --bondopts=mode=active-backup,miimon-100,primary=ens4 --activate --vlanid=222 --activate --onboot=no"
        self.assert_parse(vlan_over_bond_cmd)
        self.assert_parse(vlan_over_bond_cmd + " --bindto mac")

class RHEL7_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)

        # there needs to be a vlan id after a dot & only one dot is allowed
        self.assert_parse_error("network --interfacename=abc.")
        self.assert_parse_error("network --interfacename=abc.def")
        self.assert_parse_error("network --interfacename=abc..")
        self.assert_parse_error("network --interfacename=abc.123.456")
        # 'vlan' can't be followed by a '.'
        self.assert_parse_error("network --interfacename=vlan.123")
        self.assert_parse_error("network --interfacename=vlan.")
        self.assert_parse_error("network --interfacename=vlan..")
        self.assert_parse_error("network --interfacename=vlan.abc")
        self.assert_parse("network --interfacename=abc.123")

        # if the device name begins with 'vlan', vlan id needs to follow
        self.assert_parse_error("network --interfacename=vlan")
        self.assert_parse_error("network --interfacename=vlanabcd")
        # a valid vlan id needs to directly follow the 'vlan' prefix
        self.assert_parse_error("network --interfacename=vlanabcd123")
        self.assert_parse_error("network --interfacename=vlanabcd123zxy")
        self.assert_parse_error("network --interfacename=vlan123zxy")
        self.assert_parse("network --interfacename=vlan123")

        # vlan ids go from 0 to 4095
        self.assert_parse("network --interfacename=vlan0")
        self.assert_parse("network --interfacename=vlan4095")
        self.assert_parse("network --interfacename=abc.0")
        self.assert_parse("network --interfacename=abc.4095")
        self.assert_parse_error("network --interfacename=vlan4096")
        self.assert_parse_error("network --interfacename=vlan9001")
        self.assert_parse_error("network --interfacename=abc.9001")

        # bridge options
        # pass
        self.assert_parse("network --device bridge0 --bootproto dhcp --bridgeslaves=ens3,ens7 --bridgeopts=priority=40000",
                          "network  --bootproto=dhcp --device=bridge0 --bridgeslaves=ens3,ens7 --bridgeopts=priority=40000\n")
        self.assert_parse("network --device bridge0 --bootproto dhcp "
                          "--bridgeslaves=ens3,ens7 "
                          "--bridgeopts=priority=40000,hello-time=3")

        # fail
        # slaves missing
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeopts=priority=40000")
        # bad options format
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeslaves=ens3,ens7 "
                                '--bridgeopts="priority=40000 hello-time=3"')
        self.assert_parse_error("network --device bridge0 --bootproto dhcp "
                                "--bridgeslaves=ens3,ens7 "
                                "--bridgeopts=priority")

        # activating a device
        network_data = self.assert_parse("network --device eth0")
        self.assertEqual(network_data.activate, None)
        network_data = self.assert_parse("network --device eth0 --no-activate")
        self.assertEqual(network_data.activate, False)
        network_data = self.assert_parse("network --device eth0 --activate")
        self.assertEqual(network_data.activate, True)
        network_data = self.assert_parse("network --device eth0 --activate --no-activate")
        self.assertEqual(network_data.activate, False)
        network_data = self.assert_parse("network --device eth0 --no-activate --activate")
        self.assertEqual(network_data.activate, True)

        # binding the configuration to mac
        network_data = self.assert_parse("network --device eth0 --bindto mac")
        self.assertEqual(network_data.bindto, BIND_TO_MAC)
        network_data = self.assert_parse("network --device eth0")
        self.assertIsNone(network_data.bindto)
        # not allowed for vlan device type
        vlan_cmd = "network --device ens3 --vlanid 222 --bootproto dhcp"
        self.assert_parse(vlan_cmd)
        self.assert_parse_error(vlan_cmd + " --bindto mac")
        # but allowed for vlan over bond defined by single command, binds bond slaves
        vlan_over_bond_cmd = "network --device bond0 --bootproto static --ip 10.34.39.222 --netmask 255.255.255.0 --gateway 10.34.39.254 --bondslaves=ens4,ens5 --bondopts=mode=active-backup,miimon-100,primary=ens4 --activate --vlanid=222 --activate --onboot=no"
        self.assert_parse(vlan_over_bond_cmd)
        self.assert_parse(vlan_over_bond_cmd + " --bindto mac")

if __name__ == "__main__":
    unittest.main()
