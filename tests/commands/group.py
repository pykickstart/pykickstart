#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2013 Red Hat, Inc.
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

from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.group import F12_GroupData
from pykickstart.version import F12

class Group_TestCase(unittest.TestCase):
    def runTest(self):
        # test that new objects are always equal
        data1 = F12_GroupData()
        data2 = F12_GroupData()
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['name']:
            setattr(data1, atr, '')
            setattr(data2, atr, 'test-group')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')


class F12_TestCase(CommandTest):
    command = "group"

    def runTest(self):
        # pass
        self.assert_parse("group --name=test", "group --name=test\n")
        self.assert_parse("group --name=test --gid=1000", "group --name=test --gid=1000\n")

        self.assertFalse(self.assert_parse("group --name=test") is None)
        self.assertTrue(self.assert_parse("group --name=testA") != self.assert_parse("group --name=testB"))
        self.assertFalse(self.assert_parse("group --name=testA") == self.assert_parse("group --name=testB"))

        # fail
        # missing required option --name
        self.assert_parse_error("group")
        # --name requires an argument
        self.assert_parse_error("group --name")
        # --gid requires int argument
        self.assert_parse_error("group --name=test --uid=id")
        # unknown option
        self.assert_parse_error("group --name=test --unknown=value")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.groupList = ["test"]
        self.assertEqual(cmd.__str__(), "test")

        gd = self.handler().GroupData()
        gd.name = ""
        self.assertEqual(gd.__str__(), "group\n")

class F12_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F12

    def runTest(self):
        self.assert_parse("""
group --name=test
group --name=othertest""")

        self.assert_parse_error("""
group --name=test --gid=1000
group --name=test --gid=1010""", KickstartParseWarning)

if __name__ == "__main__":
    unittest.main()
