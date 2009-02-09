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
from tests.baseclass import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("ignoredisk --drives=sda", "ignoredisk --drives=sda\n")
        self.assert_parse("ignoredisk --drives=sda,sdb", "ignoredisk --drives=sda,sdb\n")

        # fail
        # wrong option name
        self.assert_parse_error("ignoredisk --devices=sda", KickstartParseError)
        # missing arguments
        self.assert_parse_error("ignoredisk --drives", KickstartParseError)
        # empty
        self.assert_parse_error("ignoredisk", KickstartValueError)

class F8_TestCase(FC3_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("ignoredisk --drives=sda", "ignoredisk --drives=sda\n")
        self.assert_parse("ignoredisk --drives=sda,sdb", "ignoredisk --drives=sda,sdb\n")
        self.assert_parse("ignoredisk --only-use=sda", "ignoredisk --only-use=sda\n")
        self.assert_parse("ignoredisk --only-use=sda,sdb", "ignoredisk --only-use=sda,sdb\n")

        # fail
        # missing arguments
        self.assert_parse_error("ignoredisk --only-use", KickstartParseError)
        # wrong option name
        self.assert_parse_error("ignoredisk --devices=sda", KickstartParseError)
        # missing arguments
        self.assert_parse_error("ignoredisk --drives", KickstartParseError)
        # empty
        self.assert_parse_error("ignoredisk", KickstartValueError)
        # both options provided
        self.assert_parse_error("ignoredisk --drives=sda --only-use=sdb", KickstartValueError)
        self.assert_parse_error("ignoredisk --only-use=sda --drives=sdb", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
