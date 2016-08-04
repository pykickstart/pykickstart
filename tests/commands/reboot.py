#
# Brian C. Lane <bcl@redhat.com>
#
# Copyright 2012 Red Hat, Inc.
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
from pykickstart.commands.reboot import FC6_Reboot, F23_Reboot
from pykickstart.constants import KS_REBOOT, KS_SHUTDOWN, KS_WAIT

class FC3_TestCase(CommandTest):
    command = "reboot"

    def runTest(self):
        # pass
        cmd = self.assert_parse("reboot")
        self.assertEqual(cmd.action, KS_REBOOT)
        self.assertEqual(str(cmd), "# Reboot after installation\nreboot\n")
        cmd = self.assert_parse("shutdown")
        self.assertEqual(cmd.action, KS_SHUTDOWN)
        self.assertEqual(str(cmd), "# Shutdown after installation\nshutdown\n")

        cmd = self.assert_parse("halt")
        # halt changed in F18
        if self.__class__.__name__ in ("FC3_TestCase", "FC6_TestCase"):
            self.assertEqual(cmd.action, KS_SHUTDOWN)

        cmd = self.assert_parse("poweroff")
        self.assertEqual(cmd.action, KS_SHUTDOWN)

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # assert default values
        cmd = FC6_Reboot()
        self.assertFalse(cmd.eject)

        # pass
        cmd = self.assert_parse("reboot --eject")
        self.assertEqual(cmd.action, KS_REBOOT)
        self.assertEqual(cmd.eject, True)
        self.assertEqual(str(cmd), "# Reboot after installation\nreboot --eject\n")

class F18_TestCase(FC6_TestCase):
    def runTest(self):
        FC6_TestCase.runTest(self)

        # pass
        cmd = self.assert_parse("halt")
        self.assertEqual(cmd.action, KS_WAIT)
        self.assertEqual(str(cmd), "# Halt after installation\nhalt\n")
        cmd = self.assert_parse("halt --eject")
        self.assertEqual(cmd.eject, True)
        self.assertEqual(str(cmd), "# Halt after installation\nhalt --eject\n")

class F23_TestCase(F18_TestCase):
    def runTest(self):
        F18_TestCase.runTest(self)

        # assert default values
        cmd = F23_Reboot()
        self.assertFalse(cmd.kexec)

        # pass
        cmd = self.assert_parse("reboot --kexec")
        self.assertEqual(cmd.kexec, True)
        self.assertEqual(str(cmd), "# Reboot after installation\nreboot --kexec\n")
        cmd = self.assert_parse("reboot --eject --kexec")
        self.assertEqual(cmd.kexec, True)
        self.assertEqual(cmd.eject, True)
        self.assertEqual(str(cmd), "# Reboot after installation\nreboot --eject --kexec\n")


if __name__ == "__main__":
    unittest.main()
