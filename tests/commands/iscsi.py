#
# Martin Gracik <mgracik@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
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
from tests.baseclass import CommandTest

class FC6_TestCase(CommandTest):
    command = "iscsi"

    def runTest(self):
        # pass
        self.assert_parse("iscsi --ipaddr=1.1.1.1", "iscsi --ipaddr=1.1.1.1\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --target=tar --port=1234 --user=name --password=secret",
                          "iscsi --target=tar --ipaddr=1.1.1.1 --port=1234 --user=name --password=secret\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --target=tar", "iscsi --target=tar --ipaddr=1.1.1.1\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --port=4321", "iscsi --ipaddr=1.1.1.1 --port=4321\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --user=name", "iscsi --ipaddr=1.1.1.1 --user=name\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --password=secret", "iscsi --ipaddr=1.1.1.1 --password=secret\n")

        # fail
        # missing required option --ipaddr
        self.assert_parse_error("iscsi")
        self.assert_parse_error("iscsi --target=tar --user=name --password=secret --port=1234")
        # missing --ipaddr argument
        self.assert_parse_error("iscsi --ipaddr")
        # unexpected arguments
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 not expected")
        # unknown flag
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --unknown=value")
        # empty arguments
        self.assert_parse_error("iscsi --target --ipaddr=1.2.3.4")
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --user")
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --password")
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --port")
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --port=''")

        # extra test coverage
        data = self.handler().IscsiData()
        data.ipaddr = ""
        self.assertEqual(data._getArgsAsStr(), "")

        cmd = self.handler().commands[self.command]
        cmd.iscsi= [data]
        self.assertEqual(cmd.__str__(), "iscsi\n")
        self.assertEqual(cmd.dataList(), [data])

class F10_TestCase(FC6_TestCase):
    def runTest(self):
        # run FC6 test case
        FC6_TestCase.runTest(self)

        # pass
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-user=name --reverse-password=secret",
                          "iscsi --ipaddr=1.1.1.1 --reverse-user=name --reverse-password=secret\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-user=name", "iscsi --ipaddr=1.1.1.1 --reverse-user=name\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-password=secret", "iscsi --ipaddr=1.1.1.1 --reverse-password=secret\n")

        # fail
        # empty arguments
        self.assert_parse_error("iscsi --ipaddr=1.1.1.1 --reverse-user")
        self.assert_parse_error("iscsi --ipaddr=1.1.1.1 --reverse-password")

class RHEL6_TestCase(F10_TestCase):
    def runTest(self):
        F10_TestCase.runTest(self)

        self.assert_parse("iscsi --ipaddr=1.1.1.1 --iface=eth0\n")

        # extra test coverage
        data = self.handler().IscsiData()
        data.iface = "eth0"
        self.assertEqual(data._getArgsAsStr(), " --iface=eth0")

class F17_TestCase(F10_TestCase):
    def runTest(self):
        F10_TestCase.runTest(self)

        self.assert_parse("iscsi --ipaddr=1.1.1.1 --iface=eth0\n")

        # extra test coverage
        data = self.handler().IscsiData()
        data.iface = "eth0"
        self.assertEqual(data._getArgsAsStr(), " --iface=eth0")

if __name__ == "__main__":
    unittest.main()
