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
from tests.baseclass import CommandTest
from pykickstart.commands.liveimg import F19_Liveimg

class LiveImg_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F19_Liveimg()
        self.assertFalse(cmd == None)

        op = cmd._getParser()
        for action in op._actions:
            if '--url' in action.option_strings:
                self.assertEqual(action.required, True)
            elif '--noverifyssl' in action.option_strings:
                self.assertEqual(action.default, False)

class F19_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other "
                          "--noverifyssl --checksum=e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\" "
                          "--noverifyssl --checksum=\"e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba\"\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other "
                          "--noverifyssl",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\" "
                          "--noverifyssl\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other ",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\"\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere",
                          "liveimg --url=\"http://someplace/somewhere\"\n")

        # equality
        self.assertEqual(self.assert_parse("liveimg --url=http://one"), self.assert_parse("liveimg --url=http://one"))
        self.assertEqual(self.assert_parse("liveimg --url=http://one --proxy=http://wherever"), self.assert_parse("liveimg --url=http://one --proxy=http://wherever"))
        self.assertEqual(self.assert_parse("liveimg --url=http://one --noverifyssl"), self.assert_parse("liveimg --url=http://one --noverifyssl"))
        self.assertEqual(self.assert_parse("liveimg --url=http://one --checksum=deadbeef"), self.assert_parse("liveimg --url=http://one --checksum=deadbeef"))

        self.assertNotEqual(self.assert_parse("liveimg --url=http://one"), self.assert_parse("liveimg --url=http://two"))
        self.assertNotEqual(self.assert_parse("liveimg --url=http://one --proxy=http://wherever"), self.assert_parse("liveimg --url=http://two"))
        self.assertNotEqual(self.assert_parse("liveimg --url=http://one --proxy=http://wherever"), self.assert_parse("liveimg --url=http://one, --proxy=http://somewhere"))
        self.assertNotEqual(self.assert_parse("liveimg --url=http://one --noverifyssl"), self.assert_parse("liveimg --url=http://one"))
        self.assertNotEqual(self.assert_parse("liveimg --url=http://one --checksum=deadbeef"), self.assert_parse("liveimg --url=http://one"))
        self.assertNotEqual(self.assert_parse("liveimg --url=http://one --checksum=deadbeef"), self.assert_parse("liveimg --url=http://one --checksum=abababab"))

        self.assertFalse(self.assert_parse("liveimg --url=http://one") == None)

        # fail
        self.assert_parse_error("liveimg")
        self.assert_parse_error("liveimg --url")
        self.assert_parse_error("liveimg --url=http://someplace/somewhere --proxy")
        self.assert_parse_error("liveimg --proxy=http://someplace/somewhere")
        self.assert_parse_error("liveimg --noverifyssl")
        self.assert_parse_error("liveimg --checksum=e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba")

if __name__ == "__main__":
    unittest.main()
