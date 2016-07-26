#
# Paul W. Frields <pfrields@redhat.com>
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
    command = "keyboard"

    def runTest(self):
        # pass
        self.assert_parse("keyboard us", "keyboard us\n")

        # fail
        self.assert_parse_error("keyboard")
        self.assert_parse_error("keyboard us uk")
        self.assert_parse_error("keyboard --foo us")
        self.assert_parse_error("keyboard --bogus-option")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.keyboard = ""
        self.assertEqual(cmd.__str__(), "")


class F18_TestCase(FC3_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("keyboard us",
                          "keyboard 'us'\n")
        self.assert_parse("keyboard --vckeymap=us",
                          "keyboard --vckeymap=us\n")
        # This is tedious - I'm only going to check it once.
        self.assert_parse("keyboard --vckeymap=us sk",
                          "# old format: keyboard sk\n# new format:\nkeyboard --vckeymap=us\n")
        self.assert_parse("keyboard --xlayouts='cz (qwerty)'",
                          "keyboard --xlayouts='cz (qwerty)'\n")
        self.assert_parse("keyboard --xlayouts=cz,'cz (qwerty)'",
                          "keyboard --xlayouts='cz','cz (qwerty)'\n")
        self.assert_parse("keyboard --xlayouts=cz sk")
        self.assert_parse("keyboard --vckeymap=us --xlayouts=cz",
                          "keyboard --vckeymap=us --xlayouts='cz'\n")
        self.assert_parse("keyboard --vckeymap=us --xlayouts=cz,'cz (qwerty)' sk")
        self.assert_parse("keyboard --vckeymap=us --xlayouts=cz --switch=grp:alt_shift_toggle",
                          "keyboard --vckeymap=us --xlayouts='cz' --switch='grp:alt_shift_toggle'\n")
        self.assert_parse("keyboard --vckeymap=us --xlayouts=cz --switch=grp:alt_shift_toggle,grp:switch",
                          "keyboard --vckeymap=us --xlayouts='cz' --switch='grp:alt_shift_toggle','grp:switch'\n")

        # fail
        self.assert_parse_error("keyboard")
        self.assert_parse_error("keyboard cz sk")
        self.assert_parse_error("keyboard --vckeymap=us --xlayouts=cz,"
                                "'cz (qwerty)' cz sk")
        self.assert_parse_error("keyboard --foo us")
        self.assert_parse_error("keyboard --bogus-option")

        # keyboard property
        obj = self.assert_parse("keyboard us")
        self.assertEqual(obj.keyboard, "us")

        obj = self.assert_parse("keyboard --xlayouts=us,cz")
        self.assertEqual(obj.keyboard, "us")

        obj = self.assert_parse("keyboard --xlayouts=,bg")
        self.assertEqual(obj.x_layouts, ["bg"])

        obj.keyboard = "cz"
        self.assertEqual(obj.keyboard, "cz")

if __name__ == "__main__":
    unittest.main()
