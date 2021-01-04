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
from pykickstart.commands.lilocheck import FC3_LiloCheck
from pykickstart.base import RemovedCommand

class FC3_TestCase(CommandTest):
    command = "lilocheck"

    def runTest(self):
        #pass
        self.assert_parse("lilocheck", "lilocheck\n")

        #fail
        self.assert_parse_error("lilocheck foo")
        self.assert_parse_error("lilocheck --whatever")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.check = False
        self.assertEqual(cmd.__str__(), "")

class FC4_TestCase(CommandTest):
    def runTest(self):
        # make sure that lilocheck is removed
        cmd = self.handler().commands["lilocheck"]
        self.assertTrue(issubclass(cmd.__class__, RemovedCommand))

class LiloCheck_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = FC3_LiloCheck()
        self.assertEqual(cmd.check, False)

if __name__ == "__main__":
    unittest.main()
