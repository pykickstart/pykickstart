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
from pykickstart.commands.harddrive import FC3_HardDrive

class HardDrive_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = FC3_HardDrive()
        data2 = FC3_HardDrive()

        # additional test coverage
        self.assertEqual(data1.__str__(), '')

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['biospart', 'partition', 'dir']:
            setattr(data1, atr, '')
            setattr(data2, atr, 'test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')


class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("harddrive --dir=/install --biospart=part", "harddrive --dir=/install --biospart=part\n")
        self.assert_parse("harddrive --dir=/install --partition=part", "harddrive --dir=/install --partition=part\n")

        self.assertFalse(self.assert_parse("harddrive --dir=/install --partition=sda1") is None)
        self.assertTrue(self.assert_parse("harddrive --dir=/install --partition=sda1") !=
                        self.assert_parse("harddrive --dir=/install --partition=sda2"))
        self.assertFalse(self.assert_parse("harddrive --dir=/install --biospart=80p1") ==
                         self.assert_parse("harddrive --dir=/install --biospart=80p2"))
        self.assertFalse(self.assert_parse("harddrive --dir=/install --biospart=sda1") ==
                         self.assert_parse("harddrive --dir=/other-install --biospart=sda1"))

        # fail
        # required option --dir missing
        self.assert_parse_error("harddrive")
        # required --dir argument missing
        self.assert_parse_error("harddrive --dir")
        # missing --biospart or --partition option
        self.assert_parse_error("harddrive --dir=/install")
        # both --biospart and --partition specified
        self.assert_parse_error("harddrive --dir=/install --biospart=bios --partition=part")
        # --biospart and --partition require argument
        self.assert_parse_error("harddrive --dir=/install --biospart")
        self.assert_parse_error("harddrive --dir=/install --partition")
        # unknown option
        self.assert_parse_error("harddrive --unknown=value")

if __name__ == "__main__":
    unittest.main()
