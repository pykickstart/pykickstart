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
from pykickstart.commands.rootpw import FC3_RootPw, F8_RootPw

class FC3_TestCase(CommandTest):
    command = "rootpw"

    def runTest(self):
        # assert default values
        self.assertFalse(FC3_RootPw().isCrypted)

        # pass
        self.assert_parse("rootpw --iscrypted secrethandshake", "rootpw --iscrypted secrethandshake\n")

        # fail
        self.assert_parse_error("rootpw")
        self.assert_parse_error("rootpw --iscrypted=OMGSEKRITZ")
        self.assert_parse_error("rootpw --iscrypted")
        self.assert_parse_error("rootpw pwd1 pwd2")

        # fail - unknown option
        self.assert_parse_error("rootpw pass-phrase --bogus-option")
        self.assert_parse_error("rootpw --bogus-option")

class F8_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # assert default values
        self.assertFalse(F8_RootPw().lock)

        # pass
        self.assert_parse("rootpw --lock secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --plaintext secrethandshake", "rootpw --plaintext secrethandshake\n")
        self.assert_parse("rootpw --plaintext --iscrypted secrethandshake", "rootpw --iscrypted secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --plaintext secrethandshake\n", "rootpw --plaintext secrethandshake\n")
        self.assert_parse("rootpw --lock --plaintext secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --lock secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --lock --iscrypted --plaintext secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --lock --plaintext --iscrypted secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --plaintext --iscrypted --lock secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --plaintext --lock secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        obj = self.assert_parse("rootpw --plaintext \"comment#inpassword\"", "rootpw --plaintext \"comment#inpassword\"\n")
        self.assertEqual(obj.password, "comment#inpassword")

        # fail
        self.assert_parse_error("rootpw --plaintext=ISEEENGLAND secrethandshake")
        self.assert_parse_error("rootpw --lock=NOKEYSFORYOU secrethandshake")
        self.assert_parse_error("rootpw --plaintext")

        if self.__class__.__name__ == "F8_TestCase":
            self.assert_parse_error("rootpw --lock")

class F18_TestCase(F8_TestCase):
    def runTest(self):
        F8_TestCase.runTest(self)

        self.assert_parse("rootpw --lock", "rootpw --lock\n")

if __name__ == "__main__":
    unittest.main()
