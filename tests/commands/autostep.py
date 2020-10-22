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
from tests.baseclass import CommandTest
from pykickstart.commands.autostep import FC3_AutoStep
from pykickstart.base import DeprecatedCommand

class FC3_TestCase(CommandTest):
    command = "autostep"

    def runTest(self):
        # pass
        self.assert_parse("autostep", "autostep\n")
        self.assert_parse("autostep --autoscreenshot", "autostep --autoscreenshot\n")

        # fail
        self.assert_parse_error("autostep --autoscreenshot=FOO")

class RHEL8_TestCase(FC3_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("autostep")
        self.assertTrue(issubclass(parser.__class__, DeprecatedCommand))

        # make sure we are still able to parse it
        self.assert_parse("autostep")

class AutoStep_TestCase(unittest.TestCase):
    """
        Additional autostep tests
    """
    def runTest(self):
        # by default autostep is False if not specified
        cmd = FC3_AutoStep()
        self.assertEqual(cmd.autostep, False)
        self.assertEqual(cmd.autoscreenshot, False)

        # after parsing autostep becomes True
        cmd.parse(['--autoscreenshot'])
        self.assertEqual(cmd.autostep, True)
        self.assertEqual(cmd.autoscreenshot, True)

if __name__ == "__main__":
    unittest.main()
