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
from tests.baseclass import CommandTest

from pykickstart.errors import KickstartValueError

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

        # noformat
        self.assert_parse("btrfs /foo --data=1 --noformat --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")
        self.assert_parse("btrfs /foo --data=RAID1 --noformat --useexisting LABEL=foo",
                          "btrfs /foo --noformat --useexisting --data=raid1 LABEL=foo\n")

        # fail
        # no mountpoint or options
        self.assert_parse_error("btrfs", KickstartValueError)

        # no options
        self.assert_parse_error("btrfs /", KickstartValueError)

        # No members
        self.assert_parse_error("btrfs / --data=0 --label=root", KickstartValueError)

        # subvol with no name
        self.assert_parse_error("btrfs / --subvol LABEL=test", KickstartValueError)

        # subvol with no parent
        self.assert_parse_error("btrfs / --subvol --name=root", KickstartValueError)

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

        # equality
        self.assertNotEqual(self.assert_parse("btrfs / part.01"), None)
        self.assertEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs / part.01"))
        self.assertEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs / part.02"))
        self.assertNotEqual(self.assert_parse("btrfs / part.01"), self.assert_parse("btrfs /home part.01"))

if __name__ == "__main__":
    unittest.main()
