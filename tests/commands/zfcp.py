#
# Chris Lumens <clumens@redhat.com>
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

from pykickstart.version import F12

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5",
                          "zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5\n")

        self.assertFalse(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5") == None)
        self.assertTrue(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5") != \
                        self.assert_parse("zfcp --devnum=6 --wwpn=7 --fcplun=8 --scsiid=9 --scsilun=10"))
        self.assertFalse(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5") == \
                         self.assert_parse("zfcp --devnum=6 --wwpn=7 --fcplun=8 --scsiid=9 --scsilun=10"))
        self.assertTrue(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5") == \
                        self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4 --scsilun=5"))

        # fail
        self.assert_parse_error("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsiid=4")
        self.assert_parse_error("zfcp --devnum=1 --wwpn=2 --fcplun=3 --scsilun=4")
        self.assert_parse_error("zfcp --devnum=1 --wwpn=2 --fcplun=3")
        self.assert_parse_error("zfcp --devnum --wwpn --fcplun --scsiid --scsilun")

class F12_TestCase(FC3_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3",
                          "zfcp --devnum=1 --wwpn=2 --fcplun=3\n")

        # deprecated
        self.assert_deprecated("zfcp", "--scsiid")
        self.assert_deprecated("zfcp", "--scsilun")

        # equality
        self.assertEqual(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"), self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"))
        self.assertNotEqual(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"), None)
        self.assertNotEqual(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"), self.assert_parse("zfcp --devnum=10 --wwpn=2 --fcplun=3"))
        self.assertNotEqual(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"), self.assert_parse("zfcp --devnum=1 --wwpn=20 --fcplun=3"))
        self.assertNotEqual(self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=3"), self.assert_parse("zfcp --devnum=1 --wwpn=2 --fcplun=30"))

class F12_Duplicate_TestCase(CommandSequenceTest):
    version = F12

    def runTest(self):
        self.assert_parse("""
zfcp --devnum=1 --wwpn=2 --fcplun=3
zfcp --devnum=10 --wwpn=20 --fcplun=30""")

        self.assert_parse_error("""
zfcp --devnum=1 --wwpn=2 --fcplun=3
zfcp --devnum=1 --wwpn=2 --fcplun=3""", UserWarning)

class F14_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        self.assert_removed("zfcp", "--scsiid")
        self.assert_removed("zfcp", "--scsilun")

if __name__ == "__main__":
    unittest.main()
