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
from pykickstart.version import F20
from pykickstart.errors import KickstartParseError
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.partition import FC3_PartData, FC3_Partition

class Partition_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = FC3_Partition()
        self.assertEqual(cmd.__str__(), '')

        data1 = FC3_PartData()
        data2 = FC3_PartData()

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['mountpoint']:
            setattr(data1, atr, '')
            setattr(data2, atr, 'test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')


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
        self.assert_parse("part /home --onpart=/dev/sda1", "part /home --onpart=sda1%s\n" % self.bytesPerInode)

        if "--start" in self.optionList:
            self.assert_parse("partition raid.1 --active --asprimary --start=0 --end=10 --fstype=ext3 --noformat",
                              "part raid.1 --active --asprimary --end=10 --fstype=\"ext3\" --noformat%s\n" % self.bytesPerInode)
            self.assert_parse("partition raid.1 --start=1 --end=10",
                              "part raid.1 --end=10 --start=1%s\n" % self.bytesPerInode)
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
        self.assert_parse_error("part")
        self.assert_parse_error("part --ondisk=sda --size=100")

        # multiple mountpoint
        self.assert_parse_error("part /home / --ondisk=sda --size=100")

        int_params = ["size", "maxsize"]
        if "--start" in self.optionList:
            int_params += ["start", "end"]
        for opt in int_params:
            # integer argument required
            self.assert_parse_error("part / --%s=string" % opt)
            # value required
            self.assert_parse_error("part / --%s" % opt)

        for opt in ("fstype", "onbiosdisk", "ondisk", "ondrive", "onpart", "usepart"):
            # value required
            self.assert_parse_error("part / --%s" % opt)

        # only one argument allowed
        self.assert_parse_error("part / /home /usr")
        # unknown option
        self.assert_parse_error("part /home --unknown=value")
        self.assert_parse_error("part --bogus-option")

        parser = self.handler().commands["part"]
        pd = parser.parse(["/home"])
        self.assertFalse(pd == "")
        self.assertTrue(pd != "")

        # extra test coverage
        parser.partitions = [pd]
        if "--bytes-per-inode" in self.optionList:
            self.assertEqual(parser.__str__(), "# Disk partitioning information\npart /home --bytes-per-inode=4096\n")
        else:
            self.assertEqual(parser.__str__(), "# Disk partitioning information\npart /home\n")


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
            self.assert_parse_error("part /home --bytes-per-inode=string")
            self.assert_parse_error("part /home --bytes-per-inode")

        # missing required arguments
        for opt in ("--fsoptions", "--label"):
            if opt in self.optionList:
                self.assert_parse_error("part /home %s" % opt)

class RHEL5_TestCase(FC4_TestCase):
    def runTest(self):
        # run FC4 test case
        FC4_TestCase.runTest(self)

        # pass
        self.assert_parse("part / --encrypted --passphrase=blahblah",
                          "part / --bytes-per-inode=4096 --encrypted --passphrase=\"blahblah\"\n")

        # fail
        # missing required --passphrase argument
        self.assert_parse_error("part / --encrypted --passphrase")

        # extra test coverage
        data = self.handler().PartData()
        data.encrypted = True
        data.passphrase = ""
        self.assertEqual(data._getArgsAsStr(), " --bytes-per-inode=4096 --encrypted")

class F9_TestCase(FC3_TestCase):
    def runTest(self):
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
        self.assert_parse_error("part / --encrypted --passphrase")
        # missing required --fsprofile argument
        self.assert_parse_error("part / --fsprofile")

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

        self.assert_parse("part swap --hibernation", "part swap --hibernation\n")
        self.assert_parse("part swap --recommended --hibernation")

        with self.assertRaises(KickstartParseError):
            parser = self.handler().commands["part"]
            parser.handler.autopart.seen = True
            parser.parse(["autopart"])

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
        self.assert_parse("part swap --hibernation", "part swap --hibernation\n")
        self.assert_parse("part swap --recommended")
        self.assert_parse("part swap --recommended --hibernation")

        self.assert_parse("part / --encrypted --cipher=3-rot13",
                          "part / --encrypted --cipher=\"3-rot13\"\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("part / --cipher=3-rot13",
                          "part /\n")

        self.assert_parse_error("part / --cipher")

class F20_TestCase(F18_TestCase):
    def runTest(self):
        F18_TestCase.runTest(self)

        self.assert_parse("part /tmp --fstype=tmpfs")

        # --grow and --maxsize isn't supported with tmpfs
        self.assert_parse_error("part /tmp --fstype=tmpfs --grow")
        self.assert_parse_error("part /tmp --fstype=tmpfs --maxsize=10")


class F20_Conflict_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F20

    def runTest(self):
        self.assert_parse_error("""
autopart
part / --size=1024 --fstype=ext4""")

class F23_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)

        # pass
        self.assert_parse("part / --size=4096 --mkfsoptions=some,thing",
                          "part / --size=4096 --mkfsoptions=\"some,thing\"\n")

        # can't use --mkfsoptions if you're not formatting
        self.assert_parse_error("part / --size=4096 --mkfsoptions=some,thing --noformat")

        # can't use --mkfsoptions with --fsprofile
        self.assert_parse_error("part / --size=4096 --mkfsoptions=some,thing --fsprofile=PROFILE")

class RHEL7_TestCase(F23_TestCase):
    def runTest(self):
        F23_TestCase.runTest(self)

class F29_TestCase(F23_TestCase):
    def runTest(self):
        F23_TestCase.runTest(self)

        self.assert_deprecated("part", "--active")
        self.assert_deprecated("partition", "--active")

        self.assert_parse("part / --encrypted --luks-version=luks2",
                          "part / --encrypted --luks-version=luks2\n")

        self.assert_parse("part / --encrypted --pbkdf=argon2i",
                          "part / --encrypted --pbkdf=argon2i\n")

        self.assert_parse("part / --encrypted --pbkdf-memory=256",
                          "part / --encrypted --pbkdf-memory=256\n")

        self.assert_parse("part / --encrypted --pbkdf-time=100",
                          "part / --encrypted --pbkdf-time=100\n")

        self.assert_parse("part / --encrypted --pbkdf-iterations=1000",
                          "part / --encrypted --pbkdf-iterations=1000\n")

        self.assert_parse_error("part / --encrypted --pbkdf-time=100 --pbkdf-iterations=1000")


class RHEL8_TestCase(F29_TestCase):
    def  runTest(self):
        F29_TestCase.runTest(self)
        self.assert_parse_error("part / --fstype=btrfs")

if __name__ == "__main__":
    unittest.main()
