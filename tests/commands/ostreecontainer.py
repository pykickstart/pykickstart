#
# Copyright 2023 Red Hat, Inc.
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
from pykickstart.commands.ostreecontainer import F38_OSTreeContainer

class OSTreeContainer_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F38_OSTreeContainer()
        self.assertEqual(cmd.noSignatureVerification, False)

        # test if arguments are required
        op = cmd._getParser()
        for action in op._actions:
            if '--url' in action.option_strings:
                self.assertEqual(action.required, True)

class F38_TestCase(CommandTest):
    command = "ostreecontainer"

    def runTest(self):
        # pass
        # the stateroot has default value "default" and remote is set from stateroot if not set
        cmdstr = "ostreecontainer --url=\"quay.io/test/test_c:stable\""
        self.assert_parse(cmdstr, cmdstr + "\n")
        cmdstr = "ostreecontainer --stateroot=\"fedora-silverblue\" --url=\"quay.io/test/test_c:stable\""
        cmdstr_expected = "ostreecontainer --stateroot=\"fedora-silverblue\" --remote=\"fedora-silverblue\" --url=\"quay.io/test/test_c:stable\""
        self.assert_parse(cmdstr, cmdstr_expected + "\n")
        cmdstr = "ostreecontainer --stateroot=\"fedora-silverblue\" --remote=\"test-remote\" --url=\"quay.io/test/test_c:stable\""
        self.assert_parse(cmdstr, cmdstr + "\n")
        cmdstr = "ostreecontainer --stateroot=\"fedora-silverblue\" --remote=\"test-remote\" --no-signature-verification --url=\"quay.io/test/test_c:stable\""
        self.assert_parse(cmdstr, cmdstr + "\n")
        cmdstr = "ostreecontainer --stateroot=\"fedora-silverblue\" --remote=\"test-remote\" --no-signature-verification --transport=\"repository\" --url=\"quay.io/test/test_c:stable\""
        self.assert_parse(cmdstr, cmdstr + "\n")

        # fail - we have required arguments
        self.assert_parse_error("ostreecontainer")
        self.assert_parse_error("ostreecontainer --bacon=tasty")
        self.assert_parse_error("ostreecontainer --os=fedora-silverblue")
        self.assert_parse_error("ostreecontainer --stateroot=fedora-silverblue")
        self.assert_parse_error("ostreecontainer --no-signature-verification")
        self.assert_parse_error("ostreecontainer --remote=\"sweet\"")
        self.assert_parse_error("ostreecontainer --transport=\"test\"")
