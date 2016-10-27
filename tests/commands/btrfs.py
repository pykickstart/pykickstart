#
# David Lehman <dlehman@redhat.com>
#
# Copyright 2011 Red Hat, Inc.
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
from pykickstart.commands.btrfs import F17_BTRFSData, F23_BTRFSData
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.version import F17

class BTRFS_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = F17_BTRFSData()
        data2 = F17_BTRFSData()

        # test default attribute values
        self.assertEqual(data1.format, True)
        self.assertEqual(data1.preexist, False)
        self.assertEqual(data1.subvol, False)

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['mountpoint']:
            setattr(data1, atr, '')
            setattr(data2, atr, '/test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')

        # test for attribute values based on prefered
        # parameter names
        for attr, attr_alt in [('data', 'dataLevel'),
                               ('metadata', 'metaDataLevel')]:
            for (v1, v2) in [(1, None), (None, 2), (1, 2)]:
                kwargs = { attr: v1, attr_alt: v2 }
                data = F17_BTRFSData(**kwargs)
                self.assertEqual(getattr(data, attr_alt), v1 or v2)

        for attr, attr_alt in [('mkfsoptions', 'mkfsopts')]:
            for (v1, v2) in [(1, ''), ('', 2), (1, 2)]:
                kwargs = { attr: v1, attr_alt: v2 }
                data = F23_BTRFSData(**kwargs)
                self.assertEqual(getattr(data, attr_alt), v1 or v2)


class F17_TestCase(CommandTest):
    command = "btrfs"

    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.validLevels = ["raid0", "raid1", "raid10", "single"]

    def runTest(self):
        # valid levels
        pre = "btrfs /"
        post = "btrfs.01"
        for data in self.validLevels:
            self.assert_parse("%s --data=%s %s" % (pre, data, post))
            for meta in self.validLevels:
                self.assert_parse("%s --data=%s --metadata=%s %s" % (pre, data,
                                                                     meta, post))
                self.assert_parse("%s --metadata=%s %s" % (pre, meta, post))

        # no mountpoint or options ... just partitions
        self.assert_parse("btrfs none part.01 part.01",
                          "btrfs none part.01 part.01\n")

        # useexisting
        self.assert_parse("btrfs /foo --data=1 --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")
        self.assert_parse("btrfs /foo --data=RAID1 --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")
        self.assert_parse("btrfs /foo --data=raid1 --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")
        self.assert_parse("btrfs /foo --data=1 --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")

        # noformat
        self.assert_parse("btrfs /foo --data=1 --noformat --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")
        self.assert_parse("btrfs /foo --data=RAID1 --noformat --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")

        # fail
        # no mountpoint or options
        self.assert_parse_error("btrfs")

        # no options
        self.assert_parse_error("btrfs /")

        # invalid argument
        self.assert_parse_error("btrfs / --bogus-option")

        # No members
        self.assert_parse_error("btrfs / --data=0 --label=root")

        # subvol with no name
        self.assert_parse_error("btrfs / --subvol LABEL=test")

        # subvol with no parent
        self.assert_parse_error("btrfs / --subvol --name=root")

        # bad level
        self.assert_parse_error("btrfs / --data=47 btrfs.01", KickstartParseError, 'Invalid btrfs level: 47')
        self.assert_parse_error("btrfs / --metadata=47 btrfs.01")

        self.assert_parse("btrfs / --subvol --name=root LABEL=test",
                          "btrfs / --subvol --name=root LABEL=test\n")
        self.assert_parse("btrfs / --subvol --name=root test",
                          "btrfs / --subvol --name=root test\n")

        # preexisting
        self.assert_parse("btrfs / --useexisting btrfs.01 btrfs.02",
                          "btrfs / --noformat --useexisting btrfs.01 btrfs.02\n")
        self.assert_parse("btrfs / --useexisting LABEL=test",
                          "btrfs / --noformat --useexisting LABEL=test\n")

        # preexisting subvol with parent specified by label
        self.assert_parse("btrfs /home --subvol --name=home --useexisting LABEL=test",
                          "btrfs /home --noformat --useexisting --subvol --name=home LABEL=test\n")

        # pass
        self.assert_parse("btrfs / --label=ROOT --data=1 part.01 part.02",
                          "btrfs / --label=ROOT --data=raid1 part.01 part.02\n")
        self.assert_parse("btrfs / --data=RAID1 --label=ROOT part.01 part.02",
                          "btrfs / --label=ROOT --data=raid1 part.01 part.02\n")
        self.assert_parse("btrfs / --label=ROOT --metadata=1 part.01 part.02",
                          "btrfs / --label=ROOT --metadata=raid1 part.01 part.02\n")

        # extra test coverage
        btrfs = self.handler().commands["btrfs"]
        btrfs.btrfsList.append(btrfs.parse("btrfs /home --subvol --name=home".split(" ")))

        # excercise F17_BTRFS.__str__() with non-empty btrfsList
        self.assertEqual(btrfs.__str__(), "btrfs btrfs --subvol --name=home /home\n")

        # check for duplicates in the btrfslist when parsing
        with self.assertRaises(KickstartParseWarning):
            btrfs.parse("btrfs /home --subvol --name=home".split(" "))

        # equality
        self.assertNotEqual(self.assert_parse("btrfs / part.01"), None)
        self.assertEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs / part.01"))
        self.assertEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs / part.02"))
        self.assertNotEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs /home part.01"))

class F17_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F17

    def runTest(self):
        self.assert_parse_error("""
btrfs / --data=1 part.01 part.02
btrfs / --data=1 part.01 part.02""",
            UserWarning, 'A btrfs volume with the mountpoint / has already been defined.')

class F23_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)

        # pass
        self.assert_parse("btrfs / --mkfsoptions=some,thing part.01",
                          "btrfs / --mkfsoptions=\"some,thing\" part.01\n")

        # can't use --mkfsoptions if you're not formatting
        self.assert_parse_error("btrfs / --useexisting --mkfsoptions=whatever")
        self.assert_parse_error("btrfs / --noformat --mkfsoptions=whatever")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        with self.assertRaises(KickstartParseError):
            cmd.parse(["btrfs", "/", "--noformat", "--useexisting", "--mkfsoptions=whatever"])

class RHEL7_TestCase(F23_TestCase):
    def runTest(self):
        F23_TestCase.runTest(self)

if __name__ == "__main__":
    unittest.main()
