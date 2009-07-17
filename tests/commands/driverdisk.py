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
import unittest, shlex
import warnings
from tests.baseclass import *
from pykickstart.errors import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("driverdisk /dev/sdb2", "driverdisk /dev/sdb2\n")
        self.assert_parse("driverdisk --source=http://10.0.0.1/disk.img", "driverdisk --source=http://10.0.0.1/disk.img\n")
        self.assert_parse("driverdisk /dev/sdb2 --type=vfat", "driverdisk /dev/sdb2 --type=vfat\n")
        # pass - need separate tests per fstype?
        self.assert_parse("driverdisk /dev/sdb2 --type=ext2", "driverdisk /dev/sdb2 --type=ext2\n")

        # fail - no arguments
        self.assert_parse_error("driverdisk", KickstartValueError)
        # fail - spurious argument or extra partition
        self.assert_parse_error("driverdisk /dev/sdb2 foobar", KickstartValueError)
        # fail - specifying both partition and source
        self.assert_parse_error("driverdisk /dev/sdb2 --source=http://10.0.0.1/disk.img", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
