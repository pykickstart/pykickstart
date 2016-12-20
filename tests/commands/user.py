#
# Martin Gracik <mgracik@redhat.com>
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
from pykickstart.commands.user import FC6_UserData
from pykickstart.version import FC6

class FC6_TestCase(CommandTest):
    command = "user"

    def runTest(self):
        data1 = FC6_UserData()
        data2 = FC6_UserData()
        self.assertEqual(data1, data2)
        self.assertFalse(data1 != data2) # test __ne__ method
        self.assertNotEqual(data1, None)

        for attr in ['name']:
            setattr(data1, attr, '')
            setattr(data2, attr, 'test')
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, attr, '')
            setattr(data2, attr, '')

        # pass
        self.assert_parse("user --name=user", "user --name=user\n")
        obj = self.assert_parse("user --name=user --password=\"comment#inpassword\"", "user --name=user --password=\"comment#inpassword\"\n")
        self.assertEqual(obj.password, "comment#inpassword")
        self.assert_parse("user --name=user --groups=grp1,grp2 --homedir=/home/user --shell=/bin/bash --uid=1000 --password=secret --iscrypted",
                          "user --groups=grp1,grp2 --homedir=/home/user --name=user --password=secret --iscrypted --shell=/bin/bash --uid=1000\n")
        self.assert_parse("user --name=user --groups=grp1", "user --groups=grp1 --name=user\n")
        self.assert_parse("user --name=user --homedir=/home/user --shell=/bin/bash", "user --homedir=/home/user --name=user --shell=/bin/bash\n")
        self.assert_parse("user --name=user --password=secret", "user --name=user --password=secret\n")
        self.assert_parse("user --name=user --uid=1000", "user --name=user --uid=1000\n")

        self.assertFalse(self.assert_parse("user --name=user") is None)
        self.assertTrue(self.assert_parse("user --name=userA") !=
                        self.assert_parse("user --name=userB"))
        self.assertFalse(self.assert_parse("user --name=userA") ==
                         self.assert_parse("user --name=userB"))

        # fail
        # missing required option --name
        self.assert_parse_error("user")
        # --name requires an argument
        self.assert_parse_error("user --name")
        # --uid requires int argument
        self.assert_parse_error("user --name=user --uid=id")
        # unknown option
        self.assert_parse_error("user --name=user --unknown=value")
        # required option arguments
        self.assert_parse_error("user --name=user --groups")
        self.assert_parse_error("user --name=user --homedir")
        self.assert_parse_error("user --name=user --shell")
        self.assert_parse_error("user --name=user --uid")
        self.assert_parse_error("user --name=user --password")

        # extra test coverage
        ud = self.handler().UserData()
        ud.uid = ""
        ud.name = ""
        self.assertEqual(ud.__str__(), "")
        self.assertEqual(ud._getArgsAsStr(), "")

        cmd = self.handler().commands[self.command]
        cmd.userList = [ud]
        self.assertEqual(cmd.__str__(), "")

class FC6_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = FC6

    def runTest(self):
        # pass - can use the command twice, as long as they have different names
        self.assert_parse("""
user --name=userA
user --name=userB""")

        # fail - can't have two users with the same name
        self.assert_parse_error("""
user --name=userA
user --name=userA""", KickstartParseWarning)

class F8_TestCase(FC6_TestCase):
    def runTest(self):
        # run FC6 test case
        FC6_TestCase.runTest(self)

        # pass
        self.assert_parse("user --name=user --lock --plaintext", "user --name=user --lock\n")
        self.assert_parse("user --name=user --lock", "user --name=user --lock\n")
        self.assert_parse("user --name=user --plaintext", "user --name=user\n")

        # fail

class F12_TestCase(F8_TestCase):
    def runTest(self):
        # run F8 test case
        F8_TestCase.runTest(self)

        # pass
        self.assert_parse("user --name=user --gecos=\"User Name\"", "user --name=user --gecos=\"User Name\"\n")

class F19_TestCase(F12_TestCase):
    def runTest(self):
        # run F12 test case
        F12_TestCase.runTest(self)

        # pass
        self.assert_parse("user --name=user --gid=500", "user --name=user --gid=500\n")

if __name__ == "__main__":
    unittest.main()
