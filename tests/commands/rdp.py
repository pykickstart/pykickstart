#
# Copyright 2025 Red Hat, Inc.
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
from pykickstart.commands.rdp import F43_RDP

class RDP_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F43_RDP()
        self.assertEqual(cmd.enabled, False)

class F43_TestCase(CommandTest):
    command = "rdp"

    def runTest(self):
        # pass
        self.assert_parse("rdp", "rdp\n")
        self.assert_parse("rdp --password=PASSWORD", "rdp --password=PASSWORD\n")
        self.assert_parse("rdp --username=USERNAME", "rdp --username=USERNAME\n")
        self.assert_parse("rdp --username=USERNAME --password=PASSWORD",
                          "rdp --username=USERNAME --password=PASSWORD\n")

        # fail
        self.assert_parse_error("rdp --password")
        self.assert_parse_error("rdp --username")

if __name__ == "__main__":
    unittest.main()
