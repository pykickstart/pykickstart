#
# Brian C. Lane <bcl@redhat.com>
#
# Copyright 2014 Red Hat, Inc.
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

from pykickstart.version import F22

class F22_TestCase(CommandTest):
    command = "sshkey"
    key = "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJGDmFSzIWSvnFYhExf+FbzSiZxsoohJdrKlmPKQhdts8nSg5PH7jyG5X+w6RgWhSetlD3WouKoo3zFOR5nCYq4= bcl@notae.us"

    def runTest(self):
        # pass
        self.assert_parse('sshkey --username=root "%s"' % self.key, 'sshkey --username=root "%s"\n' % self.key)

        self.assertFalse(self.assert_parse("sshkey --username=root '%s'" % self.key) == None)
        self.assertTrue(self.assert_parse("sshkey --username=A '%s'" % self.key) != \
                        self.assert_parse("sshkey --username=B '%s'" % self.key))
        self.assertFalse(self.assert_parse("sshkey --username=A '%s'" % self.key) == \
                         self.assert_parse("sshkey --username=B '%s'" % self.key))

        # fail
        self.assert_parse_error("sshkey")
        self.assert_parse_error("sshkey --foo")
        self.assert_parse_error("sshkey --username=root --bogus-option")
        self.assert_parse_error("sshkey --username")
        self.assert_parse_error("sshkey --username=root")

        # extra test coverage
        sshkey = self.handler().commands[self.command]
        sshkey.sshUserList.append("someguy")
        self.assertEqual(sshkey.__str__(), "someguy")

class F22_Duplicate_TestCase(CommandSequenceTest):
    version = F22

    def runTest(self):
        self.assert_parse("""
sshkey --username=someguy 'this is the key'
sshkey --username=otherguy 'this is the key'""")

        self.assert_parse_error("""
sshkey --username=someguy 'this is the key'
sshkey --username=someguy 'this is the key'""", UserWarning)

if __name__ == "__main__":
    unittest.main()
