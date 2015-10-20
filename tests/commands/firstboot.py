#
# FD Cami <fcami@fedoraproject.org>
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

class FC3_TestCase(CommandTest):
    command = "firstboot"

    def runTest(self):
        # pass
        self.assert_parse("firstboot")
        self.assert_parse("firstboot --enable", "firstboot --enable\n")
        self.assert_parse("firstboot --enabled", "firstboot --enable\n")
        self.assert_parse("firstboot --disable", "firstboot --disable\n")
        self.assert_parse("firstboot --disabled", "firstboot --disable\n")
        self.assert_parse("firstboot --reconfig", "firstboot --reconfig\n")

        # fail
        self.assert_parse_error("firstboot --enable=FOO")
        self.assert_parse_error("firstboot --enabled=FOO")
        self.assert_parse_error("firstboot --disable=FOO")
        self.assert_parse_error("firstboot --disabled=FOO")
        self.assert_parse_error("firstboot --reconfig=FOO")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.firstboot = 999
        self.assertEqual(cmd.__str__(), "")

if __name__ == "__main__":
    unittest.main()
