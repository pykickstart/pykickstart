#
# Copyright 2019 Red Hat, Inc.
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


class RHEL8_TestCase(CommandTest):
    command = "zipl"

    def runTest(self):
        self.assert_parse("zipl", "")
        self.assert_parse("zipl --secure-boot", "zipl --secure-boot\n")
        self.assert_parse("zipl --force-secure-boot", "zipl --force-secure-boot\n")
        self.assert_parse("zipl --no-secure-boot", "zipl --no-secure-boot\n")

        self.assert_parse_error("zipl --invalid")
        self.assert_parse_error("zipl --secure-boot=")
        self.assert_parse_error("zipl --no-secure-boot=")
        self.assert_parse_error("zipl --force-secure-boot=")


if __name__ == "__main__":
    unittest.main()
