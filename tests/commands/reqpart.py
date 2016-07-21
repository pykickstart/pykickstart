#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2015 Red Hat, Inc.
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
from pykickstart.version import F23
from pykickstart.commands.reqpart import F23_ReqPart
from tests.baseclass import CommandTest, CommandSequenceTest

class ReqPart_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F23_ReqPart()
        self.assertEqual(cmd.reqpart, False)
        self.assertEqual(cmd.addBoot, False)

class F23_TestCase(CommandTest):
    command = "reqpart"

    def runTest(self):
        # pass
        self.assert_parse("reqpart", "reqpart\n")

        # pass
        self.assert_parse("reqpart --add-boot", "reqpart --add-boot\n")

class F23_AutopartReqpart_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F23

    def runTest(self):
        # fail - can't use both autopart and reqpart
        self.assert_parse_error("""
autopart
reqpart""")

class RHEL7_TestCase(F23_TestCase):
    def runTest(self):
        F23_TestCase.runTest(self)

if __name__ == "__main__":
    unittest.main()
