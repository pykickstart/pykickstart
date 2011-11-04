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
import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *

class FC3_TestCase(CommandTest):
    command = "bootloader"

    def runTest(self, iscrypted=False):
        if "--linear" in self.optionList:
            linear = "--linear "
        else:
            linear = ""

        # pass
        self.assert_parse("bootloader --append=rhgb","bootloader --append=\"rhgb\" %s--location=mbr\n" % linear)
        self.assert_parse("bootloader --append=\"rhgb quiet\"", "bootloader --append=\"rhgb quiet\" %s--location=mbr\n" % linear)
        self.assert_parse("bootloader", "bootloader %s--location=mbr\n" % linear)

        if "--linear" in self.optionList and "--nolinear" in self.optionList:
            self.assert_parse("bootloader --nolinear", "bootloader --location=mbr\n")
            self.assert_parse("bootloader --nolinear --linear", "bootloader --linear --location=mbr\n")
            self.assert_parse("bootloader --linear --nolinear", "bootloader --location=mbr\n")

        for loc in ["mbr", "partition", "none", "boot"]:
            self.assert_parse("bootloader --location=%s" % loc, "bootloader %s--location=%s\n" % (linear, loc))

        if "--lba32" in self.optionList:
            self.assert_parse("bootloader --lba32", "bootloader %s--location=mbr --lba32\n" % linear)

        self.assert_parse("bootloader --password=blahblah", "bootloader %s--location=mbr --password=\"blahblah\"\n" % linear)
        if not iscrypted:
            self.assert_parse("bootloader --md5pass=blahblah", "bootloader %s--location=mbr --md5pass=\"blahblah\"\n" % linear)
        self.assert_parse("bootloader --upgrade", "bootloader %s--location=mbr --upgrade\n" % linear)
        self.assert_parse("bootloader --driveorder=hda,sdb", "bootloader %s--location=mbr --driveorder=\"hda,sdb\"\n" % linear)

        if "--useLilo" in self.optionList:
            self.assert_parse("bootloader --useLilo", "bootloader %s--location=mbr --useLilo\n" % linear)

        # fail
        self.assert_parse_error("bootloader --append", KickstartParseError)
        self.assert_parse_error("bootloader --location=nowhere", KickstartParseError)
        self.assert_parse_error("bootloader --password", KickstartParseError)
        self.assert_parse_error("bootloader --md5pass", KickstartParseError)
        self.assert_parse_error("bootloader --driveorder", KickstartParseError)

class FC4_TestCase(FC3_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        FC3_TestCase.runTest(self, iscrypted)

        # Ensure these options have been removed.
        self.assert_removed("bootloader", "--linear")
        self.assert_removed("bootloader", "--nolinear")
        self.assert_removed("bootloader", "--useLilo")

class F8_TestCase(FC4_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        FC4_TestCase.runTest(self, iscrypted)

        # pass
        self.assert_parse("bootloader --timeout 47", "bootloader --location=mbr --timeout=47\n")
        self.assert_parse("bootloader --default=this", "bootloader --location=mbr --default=this\n")

        # fail
        self.assert_parse_error("bootloader --timeout", KickstartParseError)
        self.assert_parse_error("bootloader --default", KickstartParseError)

class F12_TestCase(F8_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        F8_TestCase.runTest(self, iscrypted)

        # deprecated
        self.assert_deprecated("bootloader", "--lba32")

class F14_TestCase(F12_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        F12_TestCase.runTest(self, iscrypted)

        # fail
        self.assert_parse_error("bootloader --lba32", KickstartParseError)

class F15_TestCase(F14_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        F14_TestCase.runTest(self, iscrypted=True)

        # pass
        self.assert_parse("bootloader --password=blahblah --iscrypted", "bootloader --location=mbr --password=\"blahblah\" --iscrypted\n")
        self.assert_parse("bootloader --md5pass=blahblah", "bootloader --location=mbr --password=\"blahblah\" --iscrypted\n")

class F17_TestCase(F15_TestCase):
    def runTest(self, iscrypted=False):
        # run parent tests
        F15_TestCase.runTest(self, iscrypted=iscrypted)

        self.assert_parse("bootloader --location=mbr --boot-drive=/dev/sda")
        self.assert_parse("bootloader --location=mbr --boot-drive=sda")
        self.assert_parse("bootloader --location=mbr --boot-drive=/dev/disk/by-path/pci-0000:00:0e.0-scsi-0:0:0:0")

class RHEL5_TestCase(FC4_TestCase):
    def runTest(self, iscrypted=False):
        FC4_TestCase.runTest(self, iscrypted)

        self.assert_parse("bootloader --hvargs=bleh",
                          "bootloader --location=mbr --hvargs=\"bleh\"\n")
        self.assert_parse("bootloader --hvargs=\"bleh bleh\"",
                          "bootloader --location=mbr --hvargs=\"bleh bleh\"\n")
        self.assert_parse_error("bootloader --hvargs", KickstartParseError)

class RHEL6_TestCase(F12_TestCase):
    def runTest(self, iscrypted=False):
        # Run parent tests
        F12_TestCase.runTest(self, iscrypted=True)

        # pass
        self.assert_parse("bootloader --password=blahblah --iscrypted", "bootloader --location=mbr --password=\"blahblah\" --iscrypted\n")
        self.assert_parse("bootloader --md5pass=blahblah", "bootloader --location=mbr --password=\"blahblah\" --iscrypted\n")

if __name__ == "__main__":
    unittest.main()
