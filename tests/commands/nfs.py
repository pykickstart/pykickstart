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
from pykickstart.commands.nfs import FC3_NFS

class NFS_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = FC3_NFS()
        data2 = FC3_NFS()

        # extra test coverage
        self.assertEqual(data1.__str__(), '')

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['server', 'dir']:
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
        self.assert_parse("nfs --server=1.2.3.4 --dir=/install", "nfs --server=1.2.3.4 --dir=/install\n")

        self.assertFalse(self.assert_parse("nfs --server=1.2.3.4 --dir=/install") is None)
        self.assertTrue(self.assert_parse("nfs --server=1.2.3.4 --dir=/install") !=
                        self.assert_parse("nfs --server=2.3.4.5 --dir=/install"))
        self.assertFalse(self.assert_parse("nfs --server=1.2.3.4 --dir=/install") ==
                         self.assert_parse("nfs --server=2.3.4.5 --dir=/install"))
        self.assertFalse(self.assert_parse("nfs --server=1.2.3.4 --dir=/install") ==
                         self.assert_parse("nfs --server=1.2.3.4 --dir=/install2"))

        # fail
        # missing required options --server and --dir
        self.assert_parse_error("nfs")
        self.assert_parse_error("nfs --server=1.2.3.4")
        self.assert_parse_error("nfs --server")
        self.assert_parse_error("nfs --dir=/install")
        self.assert_parse_error("nfs --dir")
        # unknown option
        self.assert_parse_error("nfs --unknown=value")

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=options", "nfs --server=1.2.3.4 --dir=/install --opts=\"options\"\n")

        self.assertTrue(self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=options") ==
                        self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=options"))
        self.assertFalse(self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=options") ==
                         self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=other,options"))

        # fail
        # --opts requires argument if specified
        self.assert_parse_error("nfs --server=1.2.3.4 --dir=/install --opts")

if __name__ == "__main__":
    unittest.main()
