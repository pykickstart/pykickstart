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
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.rootpw import *

class F22_TestCase(CommandTest):
    command = "sshkey"
    key = "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJGDmFSzIWSvnFYhExf+FbzSiZxsoohJdrKlmPKQhdts8nSg5PH7jyG5X+w6RgWhSetlD3WouKoo3zFOR5nCYq4= bcl@notae.us"

    def runTest(self):
        # pass
        self.assert_parse('sshkey --username=root "%s"' % self.key, 'sshkey --username=root "%s"\n' % self.key)

        # fail
        self.assert_parse_error("sshkey", KickstartValueError)
        self.assert_parse_error("sshkey --foo", KickstartParseError)
        self.assert_parse_error("sshkey --username", KickstartParseError)
        self.assert_parse_error("sshkey --username=root", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
