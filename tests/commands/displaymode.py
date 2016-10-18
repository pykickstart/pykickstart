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
from tests.baseclass import CommandTest
from pykickstart.errors import KickstartParseError


class FC3_TestCase(CommandTest):
    command = "displaymode"

    def runTest(self):
        # pass
        self.assert_parse("graphical", "graphical\n")
        self.assert_parse("text", "text\n")
        self.assert_parse("cmdline", "cmdline\n")

        # fail
        self.assert_parse_error("graphical --glitter=YES")
        self.assert_parse_error("graphical --shiny")
        self.assert_parse_error("graphical text")
        self.assert_parse_error("graphical cmdline")
        self.assert_parse_error("text --glitter=YES")
        self.assert_parse_error("text --shiny")
        self.assert_parse_error("text graphical")
        self.assert_parse_error("text cmdline")
        self.assert_parse_error("cmdline --glitter=YES")
        self.assert_parse_error("cmdline --shiny")
        self.assert_parse_error("cmdline graphical")
        self.assert_parse_error("cmdline text")

        # extra test coverage
        cmd = self.handler().commands["text"]
        self.assertIsNotNone(cmd._getParser())

        for mode in [None, 999, -1]:
            cmd.displayMode = mode
            self.assertEqual(cmd.__str__(), "")

        with self.assertRaises(KickstartParseError):
            cmd.currentCmd = None
            cmd.parse([])


class F26_TestCase(FC3_TestCase):
    def runTest(self):
        #pass
        self.assert_parse("text --non-interactive", "text --non-interactive\n")
        self.assert_parse("graphical --non-interactive", "graphical --non-interactive\n")

        #fail
        self.assert_parse_error("cmdline --non-interactive", KickstartParseError)
        self.assert_parse_error("text --non-interactive-test", KickstartParseError)
        self.assert_parse_error("text --non-interactive --test", KickstartParseError)
        self.assert_parse_error("graphical --non-interactive-test", KickstartParseError)
        self.assert_parse_error("graphical --non-interactive --test", KickstartParseError)

if __name__ == "__main__":
    unittest.main()
