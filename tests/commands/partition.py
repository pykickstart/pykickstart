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

from pykickstart.errors import KickstartParseError, KickstartValueError

class FC3_TestCase(CommandTest):
    command = "partition"

    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.bytesPerInode = ""

    def runTest(self):
        if "--bytes-per-inode" in self.optionList:
            self.bytesPerInode = " --bytes-per-inode=4096"

        # pass
        self.assert_parse("part /home", "part /home%s\n" % self.bytesPerInode)

        if "--start" in self.optionList:
            self.assert_parse("partition raid.1 --active --asprimary --start=0 --end=10 --fstype=ext3 --noformat",
                              "part raid.1 --active --asprimary --end=10 --fstype=\"ext3\" --noformat%s\n" % self.bytesPerInode)
        else:
            self.assert_parse("partition raid.1 --active --asprimary --fstype=ext3 --noformat",
                              "part raid.1 --active --asprimary --fstype=\"ext3\" --noformat%s\n" % self.bytesPerInode)

        self.assert_parse("part pv.1 --ondisk=sda --onpart=sda1 --recommended",
                          "part pv.1 --ondisk=sda --onpart=sda1 --recommended%s\n" % self.bytesPerInode)
        self.assert_parse("part pv.1 --ondrive=sda --usepart=sda1 --recommended",
                          "part pv.1 --ondisk=sda --onpart=sda1 --recommended%s\n" % self.bytesPerInode)
        self.assert_parse("part / --onbiosdisk=hda --size=100", "part / --onbiosdisk=hda --size=100%s\n" % self.bytesPerInode)
        self.assert_parse("part swap --grow --maxsize=100", "part swap --grow --maxsize=100%s\n" % self.bytesPerInode)

        # does not remove the /dev/ part
        self.assert_parse("part /usr --ondisk=/dev/sda --recommended --noformat --active",
                          "part /usr --active --noformat --ondisk=/dev/sda --recommended%s\n" % self.bytesPerInode)

        # fail
        # missing mountpoint
        self.assert_parse_error("part", KickstartValueError)
        self.assert_parse_error("part --ondisk=sda --size=100", KickstartValueError)

        int_params = ["size", "maxsize"]
        if "--start" in self.optionList:
            int_params += ["start", "end"]
        for opt in int_params:
            # integer argument required
            self.assert_parse_error("part / --%s=string" % opt, KickstartParseError)
            # value required
            self.assert_parse_error("part / --%s" % opt, KickstartParseError)

        for opt in ("fstype", "onbiosdisk", "ondisk", "ondrive", "onpart", "usepart"):
            # value required
            self.assert_parse_error("part / --%s" % opt, KickstartParseError)

        # only one argument allowed
        self.assert_parse_error("part / /home /usr", KickstartValueError)
        # unknown option
        self.assert_parse_error("part /home --unknown=value", KickstartParseError)

class FC4_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        if "--bytes-per-inode" in self.optionList:
            # pass
            self.assert_parse("part /home --bytes-per-inode=2048 --fsoptions=blah --label=home",
                              "part /home --bytes-per-inode=2048 --fsoptions=\"blah\" --label=home\n")

            # fail
            # --bytes-per-inode requires int argument
            self.assert_parse_error("part /home --bytes-per-inode=string", KickstartParseError)
            self.assert_parse_error("part /home --bytes-per-inode", KickstartParseError)

        # missing required arguments
        for opt in ("--fsoptions", "--label"):
            if opt in self.optionList:
                self.assert_parse_error("part /home %s" % opt, KickstartParseError)

class RHEL5_TestCase(FC4_TestCase):
    def runTest(self):
        # run FC4 test case
        FC4_TestCase.runTest(self)

        # pass
        self.assert_parse("part / --encrypted --passphrase=blahblah",
                          "part / --bytes-per-inode=4096 --encrypted --passphrase=\"blahblah\"\n")

        # fail
        # missing required --passphrase argument
        self.assert_parse_error("part / --encrypted --passphrase", KickstartParseError)

class F9_TestCase(FC3_TestCase):
    def runTest(self, start_end=True):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("part / --encrypted --passphrase=blahblah",
                          "part / --encrypted --passphrase=\"blahblah\"\n")
        self.assert_parse("part /home --fsprofile=blah", "part /home --fsprofile=\"blah\"\n")

        # deprecated
        self.assert_deprecated("part", "--bytes-per-inode")

        # fail
        # missing required --passphrase argument
        self.assert_parse_error("part / --encrypted --passphrase", KickstartParseError)
        # missing required --fsprofile argument
        self.assert_parse_error("part / --fsprofile", KickstartParseError)

class F12_TestCase(F9_TestCase):
    def runTest(self):
        # Run F9 test case
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("part / --escrowcert=\"http://x/y\"", "part /\n")
        self.assert_parse("part / --encrypted --backuppassphrase",
                          "part / --encrypted\n")
        self.assert_parse("part / --encrypted --escrowcert=\"http://x/y\"",
                          "part / --encrypted --escrowcert=\"http://x/y\"\n")
        self.assert_parse("part / --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase",
                          "part / --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase\n")
        self.assert_parse("part / --encrypted --escrowcert=http://x/y",
                          "part / --encrypted --escrowcert=\"http://x/y\"\n")

        # fail
        self.assert_parse_error("part / --escrowcert")
        self.assert_parse_error("part / --escrowcert --backuppassphrase")
        self.assert_parse_error("part / --encrypted --escrowcert "
                                "--backuppassphrase")
        self.assert_parse_error("part / --backuppassphrase=False")
        self.assert_parse_error("part / --backuppassphrase=True")

class RHEL6_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        self.assert_parse("part / --encrypted --cipher=3-rot13",
                          "part / --encrypted --cipher=\"3-rot13\"\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("part / --cipher=3-rot13",
                          "part /\n")

        self.assert_parse_error("part / --cipher")

        self.assert_parse("part swap --hibernation")
        self.assert_parse("part swap --recommended --hibernation")

class F14_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)
        self.assert_removed("partition", "--bytes-per-inode")
        self.assert_removed("partition", "--start")
        self.assert_removed("partition", "--end")

class F17_TestCase(F14_TestCase):
    def runTest(self):
        F14_TestCase.runTest(self)
        self.assert_parse("part /foo --resize --size 500 --onpart=sda3",
                          "part /foo --onpart=sda3 --size=500 --resize\n")

        # no onpart or size
        self.assert_parse_error("part /foo --resize")

        # no onpart
        self.assert_parse_error("part /foo --size=999 --resize")

        # no size
        self.assert_parse_error("part /foo --onpart=LABEL=var --resize")

class F18_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)
        self.assert_parse("part swap --hibernation")
        self.assert_parse("part swap --recommended")
        self.assert_parse("part swap --recommended --hibernation")

        self.assert_parse("part / --encrypted --cipher=3-rot13",
                          "part / --encrypted --cipher=\"3-rot13\"\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("part / --cipher=3-rot13",
                          "part /\n")

        self.assert_parse_error("part / --cipher")

if __name__ == "__main__":
    unittest.main()
