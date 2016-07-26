#
# Paul W. Frields <pfrields@redhat.com>
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

class FC3_TestCase(CommandTest):
    command = "driverdisk"

    def runTest(self):
        # pass
        self.assert_parse("driverdisk /dev/sdb2", "driverdisk /dev/sdb2\n")
        self.assert_parse("driverdisk --source=http://10.0.0.1/disk.img", "driverdisk --source=http://10.0.0.1/disk.img\n")

        if "--type" in self.optionList:
            self.assert_parse("driverdisk /dev/sdb2 --type=vfat", "driverdisk /dev/sdb2 --type=vfat\n")
            # pass - need separate tests per fstype?
            self.assert_parse("driverdisk /dev/sdb2 --type=ext2", "driverdisk /dev/sdb2 --type=ext2\n")
        else:
            self.assert_parse("driverdisk /dev/sdb2", "driverdisk /dev/sdb2\n")
            # pass - need separate tests per fstype?
            self.assert_parse("driverdisk /dev/sdb2", "driverdisk /dev/sdb2\n")

        # fail - no arguments
        self.assert_parse_error("driverdisk")
        # fail - unrecognized argument
        self.assert_parse_error("driverdisk --bogus-option")
        # fail - spurious argument or extra partition
        self.assert_parse_error("driverdisk /dev/sdb2 foobar")
        # fail - specifying both partition and source
        self.assert_parse_error("driverdisk /dev/sdb2 --source=http://10.0.0.1/disk.img")

        # extra test coverage
        ddd = self.handler().DriverDiskData()
        ddd.source = None
        self.assertEqual(ddd._getArgsAsStr(), "")

        cmd = self.handler().commands[self.command]
        self.assertEqual(cmd.__str__(), "")
        cmd.driverdiskList = [ddd]
        self.assertEqual(cmd.__str__(), "driverdisk \n")
        self.assertEqual(cmd.dataList(), [ddd])

class FC4_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("driverdisk --biospart=0x82", "driverdisk --biospart=0x82\n")
        self.assert_parse("driverdisk --biospart=0x80p1", "driverdisk --biospart=0x80p1\n")

        # fail - no arguments
        self.assert_parse_error("driverdisk --biospart")
        # fail - specifying both biospart and partition
        self.assert_parse_error("driverdisk /dev/sdb2 --biospart=0x82")
        # fail - specifying both biospart and source
        self.assert_parse_error("driverdisk --source=http://10.0.0.1/disk.img --biospart=0x82")

class F12_TestCase(FC4_TestCase):
    def runTest(self):
        FC4_TestCase.runTest(self)
        self.assert_deprecated("driverdisk", "--type=ext4")

class F14_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)
        self.assert_removed("driverdisk", "--type=ext4")

if __name__ == "__main__":
    unittest.main()
