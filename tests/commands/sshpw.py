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
from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.errors import KickstartParseError, KickstartValueError

class F13_TestCase(CommandTest):
    command = "sshpw"

    def runTest(self):
        # pass
        self.assert_parse("sshpw --username=someguy --iscrypted secrethandshake", "sshpw --username=someguy --iscrypted secrethandshake\n")

        self.assertFalse(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") == None)
        self.assertTrue(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") != \
                        self.assert_parse("sshpw --username=B --iscrypted secrethandshake"))
        self.assertFalse(self.assert_parse("sshpw --username=A --iscrypted secrethandshake") == \
                         self.assert_parse("sshpw --username=B --iscrypted secrethandshake"))

        # fail
        self.assert_parse_error("sshpw", KickstartValueError)
        self.assert_parse_error("sshpw --username=someguy", KickstartValueError)
        self.assert_parse_error("sshpw --username=someguy --iscrypted=OMGSEKRITZ", KickstartParseError)
        self.assert_parse_error("sshpw --username=someguy --iscrypted", KickstartValueError)

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
        self.assert_parse_error("sshpw --username=someguy --plaintext=ISEEENGLAND secrethandshake", KickstartParseError)
        self.assert_parse_error("sshpw --username=someguy --lock=NOKEYSFORYOU secrethandshake", KickstartParseError)
        self.assert_parse_error("sshpw --username=someguy --plaintext", KickstartValueError)
        self.assert_parse_error("sshpw --username=someguy --lock", KickstartValueError)

class F13_Duplicate_TestCase(CommandSequenceTest):
    def runTest(self):
        self.assert_parse("""
sshpw --username=someguy --iscrypted passwordA
sshpw --username=otherguy --iscrypted passwordA""")

        self.assert_parse_error("""
sshpw --username=someguy --iscrypted passwordA
sshpw --username=someguy --iscrypted passwordB""", UserWarning)

if __name__ == "__main__":
    unittest.main()
