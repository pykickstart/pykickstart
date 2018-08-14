#
# Alexander Todorov <atodorov@redhat.com>
#
# Copyright 2016 Red Hat, Inc.
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

from pykickstart.base import DeprecatedCommand
from tests.baseclass import CommandTest

class F20_TestCase(CommandTest):
    command = "install"

    def runTest(self):
        # pass
        self.assert_parse("install", "install\n")
        self.assert_parse("install", "install\n")
        self.assert_parse("install --root-device=/dev/sda", "install\n")

        # upgrade is always false
        cmd = self.handler().commands[self.command]
        cmd.parse([])
        self.assertFalse(cmd.upgrade)

        # fail
        self.assert_parse_error("install --bad-flag")
        # --root-device requires argument
        self.assert_parse_error("install --root-device")
        self.assert_parse_error("install --root-device=\"\"")

class F29_TestCase(F20_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("install")
        self.assertTrue(issubclass(parser.__class__, DeprecatedCommand))

        # make sure we are still able to parse it
        self.assert_parse("install")

class RHEL8_TestCase(F29_TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
