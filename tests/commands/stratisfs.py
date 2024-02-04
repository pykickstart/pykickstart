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
            "stratisfs / --name=root --pool=mypool",
            "stratisfs / --name=root --pool=mypool\n"
        )
        self.assert_parse(
            "stratisfs / --name=root --pool=mypool --size=6000",
            "stratisfs / --name=root --pool=mypool --size=6000\n"
        )

        # fail - no mount point
        self.assert_parse_error("stratisfs")
        self.assert_parse_error("stratisfs --name=root")
        self.assert_parse_error("stratisfs --pool=mypool")
        self.assert_parse_error("stratisfs --name=root --pool=mypool")

        # fail - no name
        self.assert_parse_error("stratisfs /")
        self.assert_parse_error("stratisfs / --pool=mypool")

        # fail - no pool
        self.assert_parse_error("stratisfs / --name=root")

        # fail - invalid arguments
        self.assert_parse_error("stratisfs / --name")
        self.assert_parse_error("stratisfs / --pool")
        self.assert_parse_error("stratisfs / --size")
        self.assert_parse_error("stratisfs / --invalid")


class F39_Duplicate_TestCase(CommandSequenceTest):

    def runTest(self):
        self.assert_parse(dedent(
            """
            stratisfs / --name=fs1 --pool=pool1
            stratisfs /home --name=fs2 --pool=pool1
            """
        ))
        self.assert_parse(dedent(
            """
            stratisfs / --name=fs1 --pool=pool1
            stratisfs /home --name=fs1 --pool=pool2
            """
        ))
        self.assert_parse_error(dedent(
            """
            stratisfs / --name=fs1 --pool=pool1
            stratisfs /home --name=fs1 --pool=pool1
            """),
            KickstartParseWarning,
            "A Stratis filesystem with the name fs1 has "
            "already been defined in Stratis pool pool1."
        )


if __name__ == "__main__":
    unittest.main()
