# Andy Lindeberg <alindebe@redhat.com>
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

from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.dmraid import FC6_DmRaidData
from pykickstart.base import DeprecatedCommand
from pykickstart.version import FC6

class DmRaid_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = FC6_DmRaidData()
        data2 = FC6_DmRaidData()
        self.assertEqual(data1, data2)

        # test that objects which differ in one
        # of these attributes are not equal
        data1.name = ''
        data2.name = 'test'
        self.assertNotEqual(data1, data2)
        self.assertNotEqual(data2, data1)
        data1.name = ''
        data2.name = ''

        data1.devices = []
        data2.devices = ['test']
        self.assertNotEqual(data1, data2)
        self.assertNotEqual(data2, data1)
        data1.devices = []
        data2.devices = []


class FC6_TestCase(CommandTest):
    command = "dmraid"

    def runTest(self):
        # pass
        self.assert_parse("dmraid --name=/dev/onamai --dev=debaisi", "dmraid --name=onamai --dev=\"debaisi\"\n")
        self.assert_parse("dmraid --name onamai --dev debaisi", "dmraid --name=onamai --dev=\"debaisi\"\n")
        self.assert_parse("dmraid --dev=deb1,deb2 --name onamai", "dmraid --name=onamai --dev=\"deb1,deb2\"\n")
        self.assert_parse("dmraid --dev \"deb1,deb2\" --name=onamai", "dmraid --name=onamai --dev=\"deb1,deb2\"\n")

        # equality
        self.assertEqual(self.assert_parse("dmraid --name=raidA --dev=deviceA"), self.assert_parse("dmraid --name=raidA --dev=deviceA"))
        self.assertNotEqual(self.assert_parse("dmraid --name=raidA --dev=deviceA"), None)
        self.assertNotEqual(self.assert_parse("dmraid --name=raidA --dev=deviceA"), self.assert_parse("dmraid --name=raidB --dev=deviceA"))
        self.assertNotEqual(self.assert_parse("dmraid --name=raidA --dev=deviceA"), self.assert_parse("dmraid --name=raidA --dev=deviceB"))

        # fail
        self.assert_parse_error("dmraid")
        self.assert_parse_error("dmraid --name")
        self.assert_parse_error("dmraid --dev")
        self.assert_parse_error("dmraid --name=onamai")
        self.assert_parse_error("dmraid --name onamai")
        self.assert_parse_error("dmraid --dev debaisi")
        self.assert_parse_error("dmraid --dev=deb1,deb2")
        self.assert_parse_error("dmraid --magic")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.dmraids = "--name=blah"
        self.assertEqual(cmd.__str__(), "--name=blah")

class FC6_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = FC6

    def runTest(self):
        self.assert_parse("""
dmraid --name=raidA --dev=deviceA
dmraid --name=raidB --dev=deviceB""")

        self.assert_parse_error("""
dmraid --name=raidA --dev=deviceA
dmraid --name=raidA --dev=deviceA""", KickstartParseWarning)

class F24_TestCase(FC6_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("dmraid")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)
        parser = parser._getParser()
        self.assertIsNotNone(parser)
        self.assertTrue(parser.description.find('deprecated:: Fedora24') > -1)

if __name__ == "__main__":
    unittest.main()
