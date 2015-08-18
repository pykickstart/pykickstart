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

from pykickstart.errors import KickstartParseError, KickstartValueError

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("harddrive --dir=/install --biospart=part", "harddrive --dir=/install --biospart=part\n")
        self.assert_parse("harddrive --dir=/install --partition=part", "harddrive --dir=/install --partition=part\n")

        self.assertFalse(self.assert_parse("harddrive --dir=/install --partition=sda1") == None)
        self.assertTrue(self.assert_parse("harddrive --dir=/install --partition=sda1") != \
                        self.assert_parse("harddrive --dir=/install --partition=sda2"))
        self.assertFalse(self.assert_parse("harddrive --dir=/install --biospart=80p1") == \
                         self.assert_parse("harddrive --dir=/install --biospart=80p2"))
        self.assertFalse(self.assert_parse("harddrive --dir=/install --biospart=sda1") == \
                         self.assert_parse("harddrive --dir=/other-install --biospart=sda1"))

        # fail
        # required option --dir missing
        self.assert_parse_error("harddrive", KickstartValueError)
        # required --dir argument missing
        self.assert_parse_error("harddrive --dir", KickstartParseError)
        # missing --biospart or --partition option
        self.assert_parse_error("harddrive --dir=/install", KickstartValueError)
        # both --biospart and --partition specified
        self.assert_parse_error("harddrive --dir=/install --biospart=bios --partition=part", KickstartValueError)
        # --biospart and --partition require argument
        self.assert_parse_error("harddrive --dir=/install --biospart", KickstartParseError)
        self.assert_parse_error("harddrive --dir=/install --partition", KickstartParseError)
        # unknown option
        self.assert_parse_error("harddrive --unknown=value", KickstartParseError)

if __name__ == "__main__":
    unittest.main()
