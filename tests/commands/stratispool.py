#
# Copyright 2023 Red Hat, Inc.
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
from textwrap import dedent

from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandTest, CommandSequenceTest


class F39_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse(
            "stratispool mypool sda",
            "stratispool mypool sda\n"
        )
        self.assert_parse(
            "stratispool mypool sda1 sda2",
            "stratispool mypool sda1 sda2\n"
        )
        self.assert_parse(
            "stratispool mypool sda sdb sdc1",
            "stratispool mypool sda sdb sdc1\n"
        )
        self.assert_parse(
            "stratispool mypool --encrypted sda sdb sdc1",
            "stratispool mypool --encrypted sda sdb sdc1\n"
        )
        self.assert_parse(
            "stratispool mypool --encrypted --passphrase=whatever sda sdb sdc1",
            "stratispool mypool --encrypted --passphrase=\"whatever\" sda sdb sdc1\n"
        )

        # fail - no pool name
        self.assert_parse_error("stratispool")
        self.assert_parse_error("stratispool --encrypted sda")

        # fail - no block device
        self.assert_parse_error("stratispool mypool")
        self.assert_parse_error("stratispool mypool --encrypted")

        # fail - invalid arguments
        self.assert_parse_error("stratispool mypool sda --invalid")
        self.assert_parse_error("stratispool mypool --invalid sda")


class F39_Duplicate_TestCase(CommandSequenceTest):

    def runTest(self):
        self.assert_parse(dedent(
            """
            stratispool pool1 sda sdb
            stratispool pool2 sdc sdd
            """
        ))
        self.assert_parse_error(dedent(
            """
            stratispool pool1 sda sdb
            stratispool pool1 sdc sdd
            """),
            KickstartParseWarning,
            "A Stratis pool with the name pool1 has already been defined."
        )


if __name__ == "__main__":
    unittest.main()
