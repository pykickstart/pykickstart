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
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.network import *

class F20_TestCase(CommandTest):
    command = "network"

    def runTest(self):

        # team device

        cmd = "network --device team0 --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --teamslaves=\"p3p1'{\\\"prio\\\": -10, \\\"sticky\\\": true}',p3p2'{\\\"prio\\\": 100}'\" --teamconfig=\"{\\\"runner\\\": {\\\"name\\\": \\\"activebackup\\\"}}\" --activate"
        self.assert_parse(cmd)

        cmd = "network --device team0 --bootproto dhcp --teamslaves=p3p1,p3p2 --teamconfig=\"{\\\"runner\\\": {\\\"name\\\": \\\"roundrobin\\\"}}\" --activate"
        self.assert_parse(cmd)

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
            [('eth1',""), ('eth2',"")],
            [('eth1',""), ('eth2','{"prio": 100}')],
            [('eth1','{"prio": -10, "sticky": true}'), ('eth2',"")],
            [('eth1','{"prio": -10, "sticky": true}'), ('eth2','{"prio": 100}')],
            [('eth1',""), ('eth2',""), ('eth3',"")],
            [('eth1',""), ('eth2','{"prio": 100}'), ('eth3',"")],
        ]

        for string, value in zip(teamslaves_strings, teamslaves_values):
            network_data = self.assert_parse("network --device team0 --bootproto=dhcp --teamslaves=\"%s\"" % string)
            self.assertEquals(network_data.teamslaves, value)

        for value in teamslaves_values:
            nd = self.assert_parse("network --device team0 --bootproto=dhcp")
            nd.teamslaves = value
            s = "%s" % nd
            nd2 = self.assert_parse(s)
            self.assertEquals(value, nd2.teamslaves)

class RHEL7_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)
        # there needs to be a vlan id after a dot & only one dot is allowed
        self.assert_parse_error("network --interfacename=abc.", KickstartValueError)
        self.assert_parse_error("network --interfacename=abc.def", KickstartValueError)
        self.assert_parse_error("network --interfacename=abc..", KickstartValueError)
        self.assert_parse_error("network --interfacename=abc.123.456", KickstartValueError)
        # 'vlan' can't be followed by a '.'
        self.assert_parse_error("network --interfacename=vlan.123", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlan.", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlan..", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlan.abc", KickstartValueError)
        self.assert_parse("network --interfacename=abc.123")

        # if the device name begins with 'vlan', vlan id needs to follow
        self.assert_parse_error("network --interfacename=vlan", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlanabcd", KickstartValueError)
        # a valid vlan id needs to directly follow the 'vlan' prefix
        self.assert_parse_error("network --interfacename=vlanabcd123", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlanabcd123zxy", KickstartValueError)
        self.assert_parse_error("network --interfacename=vlan123zxy", KickstartValueError)
        self.assert_parse("network --interfacename=vlan123")

        # vlan ids go from 0 to 4095
        self.assert_parse("network --interfacename=vlan0")
        self.assert_parse("network --interfacename=vlan4095")
        self.assert_parse("network --interfacename=abc.0")
        self.assert_parse("network --interfacename=abc.4095")
        self.assert_parse_error("network --interfacename=vlan9001", KickstartValueError)
        self.assert_parse_error("network --interfacename=abc.9001", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
