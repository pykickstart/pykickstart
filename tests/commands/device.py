#
# James Laska <jlaska@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from pykickstart.commands.device import *

class FC3_TestCase(CommandTest):
    command = "device"

    def runTest(self):
        # pass
        self.assert_parse("device TYPE MODNAME", "device TYPE MODNAME\n")
        self.assert_parse("device TYPE MODNAME --opts=key1",
                          "device TYPE MODNAME --opts=\"key1\"\n")
        self.assert_parse("device TYPE MODNAME --opts=key1=val1",
                          "device TYPE MODNAME --opts=\"key1=val1\"\n")
        self.assert_parse("device TYPE MODNAME --opts=\"key1=val1\"",
                          "device TYPE MODNAME --opts=\"key1=val1\"\n")
        self.assert_parse("device TYPE MODNAME --opts=\"key1=val1 key2=val2\"",
                          "device TYPE MODNAME --opts=\"key1=val1 key2=val2\"\n")

        # fail
        self.assert_parse_error("device", KickstartValueError)
        self.assert_parse_error("device MODNAME", KickstartValueError)
        self.assert_parse_error("device TYPE MODNAME GARBAGE", KickstartValueError)
        self.assert_parse_error("device --opts=foo", KickstartValueError)
        self.assert_parse_error("device --opts=\"foo\"", KickstartValueError)

class F8_TestCase(CommandTest):
    command = "device"

    def runTest(self):
        # pass
        self.assert_parse("device MODNAME", "device MODNAME\n")
        self.assert_parse("device MODNAME --opts=key1",
                          "device MODNAME --opts=\"key1\"\n")
        self.assert_parse("device MODNAME --opts=key1=val1",
                          "device MODNAME --opts=\"key1=val1\"\n")
        self.assert_parse("device MODNAME --opts=\"key1=val1\"",
                          "device MODNAME --opts=\"key1=val1\"\n")
        self.assert_parse("device MODNAME --opts=\"key1=val1 key2=val2\"",
                          "device MODNAME --opts=\"key1=val1 key2=val2\"\n")

        # fail - TYPE is no longer accepted
        self.assert_parse_error("device TYPE MODNAME", KickstartValueError)
        self.assert_parse_error("device TYPE MODNAME --opts=\"foo\"", KickstartValueError)

        # fail
        self.assert_parse_error("device", KickstartValueError)
        self.assert_parse_error("device MODNAME GARBAGE", KickstartValueError)
        self.assert_parse_error("device --opts=foo", KickstartValueError)
        self.assert_parse_error("device --opts=\"foo\"", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
