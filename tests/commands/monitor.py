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

from tests.baseclass import CommandTest
from pykickstart.base import DeprecatedCommand
from pykickstart.commands.monitor import FC6_Monitor

class FC3_TestCase(CommandTest):
    command = "monitor"

    def runTest(self):
        # pass
        self.assert_parse("monitor", "")
        self.assert_parse("monitor --hsync=HSYNC", "monitor --hsync=HSYNC\n")
        self.assert_parse("monitor --vsync=VSYNC", "monitor --vsync=VSYNC\n")
        self.assert_parse("monitor --monitor=MONITOR", "monitor --monitor=\"MONITOR\"\n")
        self.assert_parse("monitor --hsync=HSYNC --monitor=MONITOR",
                          "monitor --hsync=HSYNC --monitor=\"MONITOR\"\n")
        self.assert_parse("monitor --monitor=MONITOR --vsync=VSYNC",
                          "monitor --monitor=\"MONITOR\" --vsync=VSYNC\n")
        self.assert_parse("monitor --hsync=HSYNC --monitor=MONITOR --vsync=VSYNC",
                          "monitor --hsync=HSYNC --monitor=\"MONITOR\" --vsync=VSYNC\n")

        self.assert_parse_error("monitor BOGUS")
        self.assert_parse_error("monitor --monitor=SOMETHING GREAT")

        if "--noprobe" not in self.optionList:
            self.assert_parse_error("monitor --noprobe")

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("monitor --noprobe", "monitor --noprobe\n")
        # fail
        self.assert_parse_error("monitor --noprobe 1")
        # assert default values
        self.assertTrue(FC6_Monitor().probe)

class F10_TestCase(FC6_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("monitor")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)

        parser = parser._getParser()
        self.assertIsNotNone(parser)
        self.assertTrue(parser.description.find('deprecated:: Fedora10') > -1)

if __name__ == "__main__":
    unittest.main()
