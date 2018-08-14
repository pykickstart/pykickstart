#
# Peter Jones <pjones@redhat.com>
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

from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.sshpw import F13_SshPwData, F13_SshPw, F24_SshPwData
from pykickstart.version import F13

class SshPw_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = F13_SshPwData()
        data2 = F13_SshPwData()
        self.assertEqual(data1, data2)
        self.assertFalse(data1 != data2)
        self.assertNotEqual(data1, None)

        # assert default values
        self.assertFalse(data1.isCrypted)
        self.assertFalse(data1.lock)

        # test for objects difference
        for atr in ['username']:
            setattr(data1, atr, None)
            setattr(data2, atr, 'test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, None)
            setattr(data2, atr, None)

        # check options defaults
        for action in F13_SshPw()._getParser()._actions:
            for a in ['--username']:
                if a in action.option_strings:
                    self.assertTrue(action.required)

            for a in ['--lock']:
                if a in action.option_strings:
                    self.assertFalse(action.default)

        # assert default values
        self.assertFalse(F24_SshPwData().sshkey)

class F13_TestCase(CommandTest):
    command = "sshpw"

    def runTest(self):
        # pass
        self.assert_parse("sshpw --username=someguy --iscrypted secrethandshake", "sshpw --username=someguy --iscrypted secrethandshake\n")

        self.assertFalse(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") is None)
        self.assertTrue(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") !=
                        self.assert_parse("sshpw --username=B --iscrypted secrethandshake"))
        self.assertFalse(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") ==
                         self.assert_parse("sshpw --username=B --iscrypted secrethandshake"))

        # fail
        self.assert_parse_error("sshpw")
        self.assert_parse_error("sshpw --username=someguy --bogus-option")
        self.assert_parse_error("sshpw --username=someguy pass-phrase --bogus-option")
        self.assert_parse_error("sshpw --username=someguy")
        self.assert_parse_error("sshpw --username=someguy --iscrypted=OMGSEKRITZ")
        self.assert_parse_error("sshpw --username=someguy --iscrypted")

        # pass
        self.assert_parse("sshpw --username=someguy --lock secrethandshake", "sshpw --username=someguy --lock --plaintext secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --plaintext secrethandshake", "sshpw --username=someguy --plaintext secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --plaintext --iscrypted secrethandshake", "sshpw --username=someguy --iscrypted secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --iscrypted --plaintext secrethandshake\n", "sshpw --username=someguy --plaintext secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --lock --plaintext secrethandshake", "sshpw --username=someguy --lock --plaintext secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --iscrypted --lock secrethandshake", "sshpw --username=someguy --lock --iscrypted secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --lock --iscrypted --plaintext secrethandshake", "sshpw --username=someguy --lock --plaintext secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --lock --plaintext --iscrypted secrethandshake", "sshpw --username=someguy --lock --iscrypted secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --plaintext --iscrypted --lock secrethandshake", "sshpw --username=someguy --lock --iscrypted secrethandshake\n")
        self.assert_parse("sshpw --username=someguy --iscrypted --plaintext --lock secrethandshake", "sshpw --username=someguy --lock --plaintext secrethandshake\n")

        # fail
        self.assert_parse_error("sshpw --username=someguy --plaintext=ISEEENGLAND secrethandshake")
        self.assert_parse_error("sshpw --username=someguy --lock=NOKEYSFORYOU secrethandshake")
        self.assert_parse_error("sshpw --username=someguy --plaintext")
        self.assert_parse_error("sshpw --username=someguy --lock")

        # extra test coverage
        sshpw = self.handler().commands[self.command]
        sshpw.sshUserList.append("someguy")
        self.assertEqual(sshpw.__str__(), "someguy")

class F13_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F13

    def runTest(self):
        self.assert_parse("""
sshpw --username=someguy --iscrypted passwordA
sshpw --username=otherguy --iscrypted passwordA""")

        self.assert_parse_error("""
sshpw --username=someguy --iscrypted passwordA
sshpw --username=someguy --iscrypted passwordB""", KickstartParseWarning)

class F24_TestCase(F13_TestCase):
    def runTest(self):
        self.assert_parse("sshpw --username=someguy --sshkey a ssh key with spaces", "sshpw --username=someguy --sshkey a ssh key with spaces\n")
        self.assert_parse("sshpw --username=someguy a password with spaces", "sshpw --username=someguy --plaintext a password with spaces\n")
        self.assert_parse("sshpw --username=someguy --lock secretpassword", "sshpw --username=someguy --lock --plaintext secretpassword\n")
        self.assert_parse("sshpw --username=someguy --iscrypted secretpassword", "sshpw --username=someguy --iscrypted secretpassword\n")

if __name__ == "__main__":
    unittest.main()
