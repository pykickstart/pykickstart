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
from pykickstart.commands.mouse import RHEL3_Mouse

class Mouse_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = RHEL3_Mouse()
        self.assertEqual(cmd.emulthree, False)

class RHEL3_TestCase(CommandTest):
    command = "mouse"

    def runTest(self):
        # pass
        self.assert_parse("mouse jerry", "mouse jerry\n")
        self.assert_parse("mouse --device=/dev/mice --emulthree jerry", "mouse --device=/dev/mice --emulthree jerry\n")
        self.assert_parse("mouse jerry --device=/dev/mice", "mouse --device=/dev/mice jerry\n")
        self.assert_parse("mouse jerry --emulthree", "mouse --emulthree jerry\n")

        # fail
        # empty
        self.assert_parse_error("mouse")
        # multiple mice specified
        self.assert_parse_error("mouse tom and jerry")
        # unknown option
        self.assert_parse_error("mouse --bad-flag")
        self.assert_parse_error("mouse jerry --bad-flag")
        # --device requires argument
        self.assert_parse_error("mouse jerry --device")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.mouse = False
        self.assertEqual(cmd.__str__(), "")

if __name__ == "__main__":
    unittest.main()
