#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2016 Red Hat, Inc.
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
from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.version import F12

class F12_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("fcoe --nic=eth0",
                          "fcoe --nic=eth0\n")

        # fail - missing required argument
        self.assert_parse_error("fcoe")
        self.assert_parse_error("fcoe --nic")

        # fail - unknown argument
        self.assert_parse_error("fcoe --bogus-option")

        # equality
        self.assertEqual(self.assert_parse("fcoe --nic=eth0"), self.assert_parse("fcoe --nic=eth0"))
        self.assertNotEqual(self.assert_parse("fcoe --nic=eth0"), None)
        self.assertNotEqual(self.assert_parse("fcoe --nic=eth0"), self.assert_parse("fcoe --nic=eth1"))

        # extra test coverage
        cmd = self.handler().commands["fcoe"]
        cmd.fcoe = "--name=blah"
        self.assertEqual(cmd.__str__(), "--name=blah")

        data = self.handler().FcoeData()
        data.nic = ""
        self.assertEqual(data._getArgsAsStr(), "")

class F12_Duplicate_TestCase(CommandSequenceTest):
    version = F12

    def runTest(self):
        self.assert_parse("""
fcoe --nic=eth0
fcoe --nic=eth1""")

        self.assert_parse_error("""
fcoe --nic=eth0
fcoe --nic=eth0""", UserWarning)

class F13_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        self.assert_parse("fcoe --nic=eth0 --dcb",
                          "fcoe --nic=eth0 --dcb\n")

class RHEL7_TestCase(F13_TestCase):
    def runTest(self):
        F13_TestCase.runTest(self)

        self.assert_parse("fcoe --nic=eth0 --autovlan",
                          "fcoe --nic=eth0 --autovlan\n")

if __name__ == "__main__":
    unittest.main()
