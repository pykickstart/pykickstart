#
# Chris Lumens <clumens@redhat.com>
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

from pykickstart.errors import KickstartValueError

class FC3_TestCase(CommandTest):
    command = "autopart"

    def runTest(self):
        # pass
        self.assert_parse("autopart", "autopart\n")

        # fail - on FC3, autopart  took no options so this raises a different
        # exception than later releases.
        if self.__class__.__name__ == "FC3_TestCase":
            self.assert_parse_error("autopart --blah", KickstartValueError)

class F9_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --passphrase=whatever", "autopart\n")
        self.assert_parse("autopart --encrypted", "autopart --encrypted\n")
        self.assert_parse("autopart --encrypted --passphrase=\"whatever\"",
                          "autopart --encrypted --passphrase=\"whatever\"\n")
        self.assert_parse("autopart --encrypted --passphrase=whatever",
                          "autopart --encrypted --passphrase=\"whatever\"\n")

        # fail
        self.assert_parse_error("autopart --passphrase")
        self.assert_parse_error("autopart --encrypted --passphrase")
        self.assert_parse_error("autopart --encrypted=False")
        self.assert_parse_error("autopart --encrypted=True")

class F12_TestCase(F9_TestCase):
    def runTest(self):
        # Run F9 test case
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --escrowcert=\"http://x/y\"", "autopart\n")
        self.assert_parse("autopart --encrypted --backuppassphrase",
                          "autopart --encrypted\n")
        self.assert_parse("autopart --encrypted --escrowcert=\"http://x/y\"",
                          "autopart --encrypted --escrowcert=\"http://x/y\"\n")
        self.assert_parse("autopart --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase",
                          "autopart --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase\n")
        self.assert_parse("autopart --encrypted --escrowcert=http://x/y",
                          "autopart --encrypted --escrowcert=\"http://x/y\"\n")

        # fail
        self.assert_parse_error("autopart --escrowcert")
        self.assert_parse_error("autopart --escrowcert --backuppassphrase")
        self.assert_parse_error("autopart --encrypted --escrowcert "
                                "--backuppassphrase")
        self.assert_parse_error("autopart --backuppassphrase=False")
        self.assert_parse_error("autopart --backuppassphrase=True")

class RHEL6_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --cipher=foo", "autopart\n")
        self.assert_parse("autopart --encrypted --cipher=3-rot13",
                          "autopart --encrypted --cipher=\"3-rot13\"\n")

        # fail
        self.assert_parse_error("autopart --cipher")
        self.assert_parse_error("autopart --encrypted --cipher")

class F16_TestCase(F12_TestCase):
    def runTest(self):
        # Run F12 test case
        F12_TestCase.runTest(self)

        if "--type" not in self.optionList:
            # pass
            self.assert_parse("autopart --nolvm",
                              "autopart --nolvm\n")

            # fail
            self.assert_parse_error("autopart --nolvm=asdf")
            self.assert_parse_error("autopart --nolvm True", KickstartValueError)
            self.assert_parse_error("autopart --nolvm=1")
            self.assert_parse_error("autopart --nolvm 0", KickstartValueError)

class F17_TestCase(F16_TestCase):
    def runTest(self):
        # Run F16 test case
        F16_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --type=plain",
                          "autopart --type=plain\n")
        self.assert_parse("autopart --type=partition",
                          "autopart --type=plain\n")
        self.assert_parse("autopart --type=lvm",
                          "autopart --type=lvm\n")
        self.assert_parse("autopart --type=btrfs",
                          "autopart --type=btrfs\n")

        self.assert_parse("autopart --nolvm",
                          "autopart --type=plain\n")

        # don't add --type= if none was specified
        self.assert_parse("autopart",
                          "autopart\n")

        # fail
        self.assert_parse_error("autopart --type")

class F18_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --cipher=foo", "autopart\n")
        self.assert_parse("autopart --encrypted --cipher=3-rot13",
                          "autopart --encrypted --cipher=\"3-rot13\"\n")

        # fail
        self.assert_parse_error("autopart --cipher")
        self.assert_parse_error("autopart --encrypted --cipher")

class F20_TestCase(F18_TestCase):
    def runTest(self):
        F18_TestCase.runTest(self)

        self.assert_parse("autopart --type=thinp",
                          "autopart --type=thinp\n")

class F21_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --fstype=ext4",
                          'autopart --fstype=ext4\n')
        self.assert_parse("autopart --encrypted --fstype=ext4",
                          'autopart --encrypted --fstype=ext4\n')
        self.assert_parse("autopart --type=lvm --fstype=xfs",
                          "autopart --type=lvm --fstype=xfs\n")

        # fail
        self.assert_parse_error("autopart --fstype")
        self.assert_parse_error("autopart --fstype=btrfs")
        self.assert_parse_error("autopart --type=btrfs --fstype=xfs")

class RHEL7_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --nohome",
                          'autopart --nohome\n')

        # fail
        self.assert_parse_error("autopart --nohome=xxx")
        self.assert_parse_error("autopart --nohome True", KickstartValueError)
        self.assert_parse_error("autopart --nohome=1")
        self.assert_parse_error("autopart --nohome 0", KickstartValueError)

class F26_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

        # pass
        self.assert_parse("autopart --nohome",
                          'autopart --nohome\n')
        self.assert_parse("autopart --noboot",
                          'autopart --noboot\n')
        self.assert_parse("autopart --noswap",
                          'autopart --noswap\n')
        self.assert_parse("autopart --nohome --noboot --noswap",
                          'autopart --nohome --noboot --noswap\n')

        # fail
        self.assert_parse_error("autopart --nohome=xxx")
        self.assert_parse_error("autopart --nohome True", KickstartValueError)
        self.assert_parse_error("autopart --nohome=1")
        self.assert_parse_error("autopart --nohome 0", KickstartValueError)

        self.assert_parse_error("autopart --noboot=xxx")
        self.assert_parse_error("autopart --noboot True", KickstartValueError)
        self.assert_parse_error("autopart --noboot=1")
        self.assert_parse_error("autopart --noboot 0", KickstartValueError)

        self.assert_parse_error("autopart --noswap=xxx")
        self.assert_parse_error("autopart --noswap True", KickstartValueError)
        self.assert_parse_error("autopart --noswap=1")
        self.assert_parse_error("autopart --noswap 0", KickstartValueError)


if __name__ == "__main__":
    unittest.main()
