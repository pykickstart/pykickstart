#
# James Laska <jlaska@redhat.com>
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
from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.errors import KickstartParseError, KickstartValueError

class FC3_TestCase(CommandTest):
    command = "raid"

    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.validLevels = ["RAID0", "RAID1", "RAID5", "RAID6"]
        self.minorBasedDevice = True
        self.bytesPerInode = ""

    def runTest(self):
        if "--bytes-per-inode" in self.optionList:
            self.bytesPerInode = " --bytes-per-inode=4096"

        # pass
        # valid levels
        for level in self.validLevels:
            self.assert_parse("raid / --device=md0 --level=%s%s raid.01" % (level, self.bytesPerInode), \
                              "raid / --device=0 --level=%s%s raid.01\n" % (level, self.bytesPerInode))

        # device=md0, level=0
        self.assert_parse("raid / --device=md0 --level=0%s raid.01" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID0%s raid.01\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md0 --level=raid0%s raid.01" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID0%s raid.01\n" % (self.bytesPerInode))
        # device=0, level=1
        self.assert_parse("raid / --device=0 --level=1%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID1%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=0 --level=raid1%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID1%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        # device=2, level=RAID1
        self.assert_parse("raid / --device=md0 --level=RAID1%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID1%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        # spares=0
        self.assert_parse("raid / --device=md2 --level=5 --spares=0%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=2 --level=RAID5%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md2 --level=raid5 --spares=0%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=2 --level=RAID5%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        # spares != 0
        self.assert_parse("raid / --device=md2 --level=5 --spares=2%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=2 --level=RAID5 --spares=2%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md2 --level=raid5 --spares=2%s raid.01 raid.02 raid.03" % (self.bytesPerInode), \
                          "raid / --device=2 --level=RAID5 --spares=2%s raid.01 raid.02 raid.03\n" % (self.bytesPerInode))

        # fstype
        self.assert_parse("raid / --device=md0 --fstype=ASDF --level=6%s raid.01 raid.02" % (self.bytesPerInode), \
                          "raid / --device=0 --fstype=\"ASDF\" --level=RAID6%s raid.01 raid.02\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md0 --fstype=ASDF --level=raid6%s raid.01 raid.02" % (self.bytesPerInode), \
                          "raid / --device=0 --fstype=\"ASDF\" --level=RAID6%s raid.01 raid.02\n" % (self.bytesPerInode))
        # useexisting
        self.assert_parse("raid / --device=md0 --level=6 --useexisting%s" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID6 --useexisting%s\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md0 --level=raid6 --useexisting%s" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID6 --useexisting%s\n" % (self.bytesPerInode))

        # noformat
        self.assert_parse("raid / --device=md0 --level=6 --noformat --useexisting%s" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID6 --noformat --useexisting%s\n" % (self.bytesPerInode))
        self.assert_parse("raid / --device=md0 --level=raid6 --noformat --useexisting%s" % (self.bytesPerInode), \
                          "raid / --device=0 --level=RAID6 --noformat --useexisting%s\n" % (self.bytesPerInode))

        # fail
        # no mountpoint or options
        self.assert_parse_error("raid", KickstartValueError)
        # no mountpoint or options ... just partitions
        self.assert_parse_error("raid part.01 part.01", KickstartValueError)
        # no mountpoint
        self.assert_parse_error("raid --level=0 --device=md0", KickstartValueError)
        # no options
        self.assert_parse_error("raid /", KickstartValueError)
        # no device
        self.assert_parse_error("raid / --level=0", KickstartValueError)
        # no level
        self.assert_parse_error("raid / --device=md0 raid.01 raid.02", KickstartValueError)
        # No raid members defined
        self.assert_parse_error("raid / --level=0 --device=md0", KickstartValueError)
        # Both raid members and useexisting given
        self.assert_parse_error("raid / --level=0 --device=md0 --useexisting raid.01 raid.02", KickstartValueError)
        # no pre-existing device defined
        self.assert_parse_error("raid / --level=0 --useexisting", KickstartValueError)

        if self.minorBasedDevice:
            # Invalid device string - device=asdf0 (--device=(md)?<minor>)
            self.assert_parse_error("raid / --device=asdf0 --level=RAID1 raid.01 raid.02 raid.03", ValueError)
        else:
            # --device=<name>
            self.assert_parse("raid / --device=root --level=RAID1 raid.01 raid.02 raid.03",
                              "raid / --device=root --level=RAID1 raid.01 raid.02 raid.03\n")
        # extra test coverage
        rd = self.handler().RaidData()
        self.assertTrue(rd == rd)
        self.assertFalse(rd == None)
        self.assertFalse(rd != rd)
        rd.device = ""
        rd.level = ""
        cmd = self.handler().commands[self.command]
        cmd.raidList = [rd]
        if "--bytes-per-inode" in self.optionList:
            self.assertEqual(rd._getArgsAsStr(), " --bytes-per-inode=4096")
            self.assertEqual(cmd.__str__(), "raid  --bytes-per-inode=4096\n")
        else:
            self.assertEqual(rd._getArgsAsStr(), "")
            self.assertEqual(cmd.__str__(), "raid\n")

class FC3_Duplicate_TestCase(CommandSequenceTest):
    def runTest(self):
        self.assert_parse("""
raid / --device=md0 --level=0 raid.01 raid.02
raid /usr --device=md1 --level=0 raid.01 raid.02
""")

        self.assert_parse_error("""
raid / --device=md0 --level=0 raid.01 raid.02
raid / --device=md0 --level=0 raid.01 raid.02
""", UserWarning)

class FC4_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        # fsoptions
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=6 --fsoptions \"these=are,options\"%s raid.01 raid.02" % (self.bytesPerInode), \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID6 --fsoptions=\"these=are,options\"%s raid.01 raid.02\n" % (self.bytesPerInode))

class FC5_TestCase(FC4_TestCase):
    def runTest(self):
        # run FC4 test case
        FC4_TestCase.runTest(self)

        # pass
        # fsoptions
        self.assert_parse("raid / --device=md0 --fstype=\"ext2\" --level=RAID0%s raid.01 raid.02" % (self.bytesPerInode,), \
                          "raid / --device=0 --fstype=\"ext2\" --level=RAID0%s raid.01 raid.02\n" % (self.bytesPerInode,))

        if "--encrypted" in self.optionList:
            # pass
            # encrypted
            self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1%s --encrypted raid.01 raid.02" % (self.bytesPerInode), \
                              "raid / --device=0 --fstype=\"ext3\" --level=RAID1%s --encrypted raid.01 raid.02\n" % (self.bytesPerInode))
            # passphrase
            # FIXME - should this fail since no --encrypted?
            self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1%s --passphrase=asdf raid.01 raid.02" % (self.bytesPerInode), \
                              "raid / --device=0 --fstype=\"ext3\" --level=RAID1%s raid.01 raid.02\n" % (self.bytesPerInode))

            # encrypted w/ passphrase
            self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1%s --encrypted --passphrase=asdf raid.01 raid.02" % (self.bytesPerInode), \
                              "raid / --device=0 --fstype=\"ext3\" --level=RAID1%s --encrypted --passphrase=\"asdf\" raid.01 raid.02\n" % (self.bytesPerInode))

            # fail
            # --encrypted=<value>
            self.assert_parse_error("raid / --device=md0 --level=1 --encrypted=1", KickstartParseError)

class RHEL5_TestCase(FC5_TestCase):
    def __init__(self, *kargs, **kwargs):
        FC5_TestCase.__init__(self, *kargs, **kwargs)
        self.validLevels.append("RAID10")

    def runTest(self):
        FC5_TestCase.runTest(self)
        self.assert_parse("raid / --device=md0 --level=10%s raid.01 raid.02" % (self.bytesPerInode,), \
                          "raid / --device=0 --level=RAID10%s raid.01 raid.02\n" % (self.bytesPerInode,))
        self.assert_parse("raid / --device=md0 --level=raid10%s raid.01 raid.02" % (self.bytesPerInode,), \
                          "raid / --device=0 --level=RAID10%s raid.01 raid.02\n" % (self.bytesPerInode,))

F7_TestCase = RHEL5_TestCase

class F9_TestCase(F7_TestCase):
    '''F9_TestCase'''
    def runTest(self):
        # run F7 test case
        F7_TestCase.runTest(self)

        # fsprofile
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1 --fsprofile=ASDF raid.01 raid.02", \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID1 --fsprofile=\"ASDF\" raid.01 raid.02\n")

        # deprecated
        self.assert_deprecated("raid", "--bytes-per-inode")

class F12_TestCase(F9_TestCase):
    '''F12_TestCase'''
    def runTest(self):
        # run F9 test case
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("raid / --device=md0 --escrowcert=\"http://x/y\" --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted --backuppassphrase --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted --escrowcert=\"http://x/y\" --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted --escrowcert=\"http://x/y\" raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted --escrowcert=\"http://x/y\" --backuppassphrase --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted --escrowcert=\"http://x/y\" --backuppassphrase raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted --escrowcert=http://x/y --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted --escrowcert=\"http://x/y\" raid.01 raid.02\n")

        # fail
        self.assert_parse_error("raid / --device=md0 --level=1 raid.01 raid.02 -escrowcert")
        self.assert_parse_error("raid / --device=md0 --escrowcert --backuppassphrase --level=1 raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --encrypted --escrowcert --backuppassphrase --level=1 raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --backuppassphrase=False --level=1 raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --backuppassphrase=True --level=1 raid.01 raid.02")

class F13_TestCase(F12_TestCase):
    def __init__(self, *kargs, **kwargs):
        F12_TestCase.__init__(self, *kargs, **kwargs)
        self.validLevels.append("RAID4")

    def runTest(self):
        F12_TestCase.runTest(self)
        self.assert_parse("raid / --device=md0 --level=4%s raid.01 raid.02" % (self.bytesPerInode,), \
                          "raid / --device=0 --level=RAID4%s raid.01 raid.02\n" % (self.bytesPerInode,))
        self.assert_parse("raid / --device=md0 --level=raid4%s raid.01 raid.02" % (self.bytesPerInode,), \
                          "raid / --device=0 --level=RAID4%s raid.01 raid.02\n" % (self.bytesPerInode,))

class RHEL6_TestCase(F13_TestCase):
    def runTest(self):
        F13_TestCase.runTest(self)

        self.assert_parse("raid / --device=md0 --level=1 --encrypted --cipher=3-rot13 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted --cipher=\"3-rot13\" raid.01 raid.02\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("raid / --device=md0 --level=1 --cipher=3-rot13 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 raid.01 raid.02\n")

        self.assert_parse_error("raid / --cipher --device=md0 --level=1 raid.01 raid.02")

        cmd = self.handler().commands[self.command]
        cmd.handler.autopart.seen = True
        with self.assertRaises(KickstartParseError):
            cmd.parse(["raid", "/", "--device=md0", "--level=0", "raid.01", "raid.02"])
        cmd.handler.autopart.seen = False

class F14_TestCase(F13_TestCase):
    def runTest(self):
        F13_TestCase.runTest(self)
        self.assert_removed("raid", "bytes-per-inode")

class F15_TestCase(F14_TestCase):
    def runTest(self):
        F14_TestCase.runTest(self)

        # pass
        self.assert_parse("raid / --device=md0 --label=ROOT --level=1 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --label=ROOT raid.01 raid.02\n")

class F18_TestCase(F15_TestCase):
    def runTest(self):
        F15_TestCase.runTest(self)

        self.assert_parse("raid / --device=md0 --level=1 --encrypted --cipher=3-rot13 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --encrypted --cipher=\"3-rot13\" raid.01 raid.02\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("raid / --device=md0 --level=1 --cipher=3-rot13 raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 raid.01 raid.02\n")

        self.assert_parse_error("raid / --cipher --device=md0 --level=1 raid.01 raid.02")

class F19_TestCase(F18_TestCase):
    def __init__(self, *kargs, **kwargs):
        F18_TestCase.__init__(self, *kargs, **kwargs)
        self.minorBasedDevice = False

class F23_TestCase(F19_TestCase):
    def runTest(self):
        F19_TestCase.runTest(self)

        # pass
        self.assert_parse("raid / --device=md0 --level=1 --mkfsoptions=some,thing raid.01 raid.02",
                          "raid / --device=0 --level=RAID1 --mkfsoptions=\"some,thing\" raid.01 raid.02\n")

        # can't use --mkfsoptions if you're not formatting
        self.assert_parse_error("raid / --device=md0 --level=1 --mkfsoptions=some,thing --noformat raid.01 raid.02",
                                KickstartValueError)

        self.assert_parse_error("raid / --device=md0 --level=1 --mkfsoptions=some,thing --noformat --useexisting",
                                KickstartValueError)

        # can't use --mkfsoptions with --fsprofile
        self.assert_parse_error("raid / --device=md0 --level=1 --mkfsoptions=some,thing --fsprofile=PROFILE raid.01 raid.02",
                                KickstartValueError)

RHEL7_TestCase = F23_TestCase

class F25_TestCase(F23_TestCase):
    def runTest(self):
        F23_TestCase.runTest(self)

        # pass
        self.assert_parse("raid / --device=md0 --level=1 --chunksize=512 raid.01 raid.02")

if __name__ == "__main__":
    unittest.main()
