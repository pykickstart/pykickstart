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
from pykickstart.base import DeprecatedCommand
from pykickstart.commands.interactive import FC3_Interactive

class FC3_TestCase(CommandTest):
    command = "interactive"

    def runTest(self):
        # pass
        self.assert_parse("interactive", "interactive\n")

        # fail
        self.assert_parse_error("interactive giveattentionpls")
        self.assert_parse_error("interactive --cheese")
        self.assert_parse_error("interactive --crackers=CRUNCHY")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.interactive = False
        self.assertEqual(cmd.__str__(), "")


class F14_TestCase(FC3_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("interactive")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)

class Interactive_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = FC3_Interactive()
        self.assertEqual(cmd.interactive, False)

if __name__ == "__main__":
    unittest.main()
