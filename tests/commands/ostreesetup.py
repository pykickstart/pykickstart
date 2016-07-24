#
# Colin Walters <walters@redhat.com>
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
from tests.baseclass import CommandTest
from pykickstart.commands.ostreesetup import F21_OSTreeSetup

class OSTreeSetup_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F21_OSTreeSetup()
        self.assertEqual(cmd.nogpg, False)

        # no remote, should equal osname
        cmd.parse('--osname=fedora-atomic --url=http://example.com/repo --ref=fedora-atomic/sometest/base/core'.split(' '))
        self.assertEqual(cmd.remote, cmd.osname)

        # test if arguments are required
        op = cmd._getParser()
        for action in op._actions:
            for a in ['--osname', '--url', '--ref']:
                if a in action.option_strings:
                    self.assertEqual(action.required, True)

class F21_TestCase(CommandTest):
    command = "ostreesetup"

    def runTest(self):
        # pass
        self.assert_parse("ostreesetup --osname=fedora-atomic --url=http://example.com/repo --ref=fedora-atomic/sometest/base/core")
        self.assert_parse("ostreesetup --osname=local-atomic --url=file:///home/ostree --ref=fedora-atomic/sometest/base/core")
        cmdstr = "ostreesetup --osname=\"fedora-atomic\" --remote=\"fedora-atomic\" --url=\"http://example.com/repo\" --ref=\"fedora-atomic/sometest/base/core\" --nogpg"
        self.assert_parse(cmdstr, cmdstr + '\n')

        # fail - we have required arguments
        self.assert_parse_error("ostreesetup")
        self.assert_parse_error("ostreesetup --os=fedora-atomic")
        self.assert_parse_error("ostreesetup --os=fedora-atomic --url=http://example.com/repo")
        self.assert_parse_error("ostreesetup --bacon=tasty")

        # fail - wrong protocol for repo
        self.assert_parse_error("ostreesetup --osname=fedora-atomic --url=ftp://example.com/repo --ref=fedora-atomic/sometest/base/core")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.osname = ""
        cmd.remote = ""
        cmd.url = ""
        cmd.ref = ""
        cmd.nogpg = False
        self.assertEqual(cmd._getArgsAsStr(), "")

class RHEL7_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

if __name__ == "__main__":
    unittest.main()
