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
    def runTest(self):
        # pass
        self.assert_parse("bootloader --append=rhgb", "bootloader --append=\"rhgb\" --linear --location=mbr\n")
        self.assert_parse("bootloader --append=\"rhgb quiet\"", "bootloader --append=\"rhgb quiet\" --linear --location=mbr\n")
        self.assert_parse("bootloader", "bootloader --linear --location=mbr\n")
        self.assert_parse("bootloader --nolinear", "bootloader --location=mbr\n")
        self.assert_parse("bootloader --nolinear --linear", "bootloader --linear --location=mbr\n")
        self.assert_parse("bootloader --linear --nolinear", "bootloader --location=mbr\n")

        for loc in ["mbr", "partition", "none", "boot"]:
            self.assert_parse("bootloader --location=%s" % loc, "bootloader --linear --location=%s\n" % loc)

        self.assert_parse("bootloader --lba32", "bootloader --linear --location=mbr --lba32\n")
        self.assert_parse("bootloader --password=blahblah", "bootloader --linear --location=mbr --password=\"blahblah\"\n")
        self.assert_parse("bootloader --md5pass=blahblah", "bootloader --linear --location=mbr --md5pass=\"blahblah\"\n")
        self.assert_parse("bootloader --upgrade", "bootloader --linear --location=mbr --upgrade\n")
        self.assert_parse("bootloader --useLilo", "bootloader --linear --location=mbr --useLilo\n")
        self.assert_parse("bootloader --driveorder=hda,sdb", "bootloader --linear --location=mbr --driveorder=\"hda,sdb\"\n")

        # fail
        self.assert_parse_error("bootloader --append", KickstartParseError)
        self.assert_parse_error("bootloader --location=nowhere", KickstartParseError)
        self.assert_parse_error("bootloader --password", KickstartParseError)
        self.assert_parse_error("bootloader --md5pass", KickstartParseError)
        self.assert_parse_error("bootloader --driveorder", KickstartParseError)

class FC4_TestCase(CommandTest):
    def runTest(self):
        # Ensure these options have been removed.
        self.assert_removed("bootloader", "--linear")
        self.assert_removed("bootloader", "--nolinear")
        self.assert_removed("bootloader", "--useLilo")

        # pass
        self.assert_parse("bootloader --append=rhgb", "bootloader --append=\"rhgb\" --location=mbr\n")
        self.assert_parse("bootloader --append=\"rhgb quiet\"", "bootloader --append=\"rhgb quiet\" --location=mbr\n")
        self.assert_parse("bootloader", "bootloader --location=mbr\n")

        for loc in ["mbr", "partition", "none", "boot"]:
            self.assert_parse("bootloader --location=%s" % loc, "bootloader --location=%s\n" % loc)

        self.assert_parse("bootloader --lba32", "bootloader --location=mbr --lba32\n")
        self.assert_parse("bootloader --password=blahblah", "bootloader --location=mbr --password=\"blahblah\"\n")
        self.assert_parse("bootloader --md5pass=blahblah", "bootloader --location=mbr --md5pass=\"blahblah\"\n")
        self.assert_parse("bootloader --upgrade", "bootloader --location=mbr --upgrade\n")
        self.assert_parse("bootloader --driveorder=hda,sdb", "bootloader --location=mbr --driveorder=\"hda,sdb\"\n")
        self.assert_parse("bootloader --driveorder hda,sdb", "bootloader --location=mbr --driveorder=\"hda,sdb\"\n")

        # fail
        self.assert_parse_error("bootloader --append", KickstartParseError)
        self.assert_parse_error("bootloader --location=nowhere", KickstartParseError)
        self.assert_parse_error("bootloader --password", KickstartParseError)
        self.assert_parse_error("bootloader --md5pass", KickstartParseError)
        self.assert_parse_error("bootloader --driveorder", KickstartParseError)

class F8_TestCase(FC4_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("bootloader --timeout 47", "bootloader --location=mbr --timeout=47\n")
        self.assert_parse("bootloader --default=this", "bootloader --location=mbr --default=this\n")

        # fail
        self.assert_parse_error("bootloader --timeout", KickstartParseError)
        self.assert_parse_error("bootloader --default", KickstartParseError)

if __name__ == "__main__":
    unittest.main()
