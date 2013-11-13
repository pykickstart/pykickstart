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

from pykickstart.base import DeprecatedCommand

import unittest
from tests.baseclass import *

class FC3_TestCase(CommandTest):
    command = "upgrade"

    def runTest(self):
        # pass
        self.assert_parse("upgrade", "upgrade\n")
        self.assert_parse("install", "install\n")

        # fail
        self.assert_parse_error("upgrade install", KickstartValueError)
        self.assert_parse_error("upgrade --bad-flag")
        self.assert_parse_error("install --bad-flag")


class F11_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("upgrade", "upgrade\n")
        self.assert_parse("install", "install\n")
        self.assert_parse("upgrade --root-device=/dev/sda", "upgrade --root-device=/dev/sda\n")
        self.assert_parse("install --root-device=/dev/sda", "install\n")

        # fail
        # --root-device requires argument
        self.assert_parse_error("upgrade --root-device", KickstartParseError)
        self.assert_parse_error("upgrade --root-device=\"\"", KickstartValueError)
        # unknown option
        self.assert_parse_error("upgrade --bad-flag", KickstartParseError)

class F20_TestCase(F11_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("upgrade")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)

if __name__ == "__main__":
    unittest.main()
