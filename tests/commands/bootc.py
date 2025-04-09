#
# Copyright 2025 Red Hat, Inc.
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
from pykickstart.commands.bootc import F43_Bootc
from pykickstart.version import F43

class Bootc_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F43_Bootc()

        # Test arguments that are required
        op = cmd._getParser()
        for action in op._actions:
            if '--source-imgref' in action.option_strings:
                self.assertEqual(action.required, True)

class F43_TestCase(CommandTest):
    command = "bootc"

    def runTest(self):
        # PASS tests
        cmdstr = "bootc --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\""
        self.assert_parse(cmdstr)

        cmdstr = "bootc --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --stateroot=\"default\""
        self.assert_parse(cmdstr)

        cmdstr = "bootc --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\""
        cmdstr_expected = "bootc --stateroot=\"default\" --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --target-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\"" + "\n"
        self.assert_parse(cmdstr, cmdstr_expected)

        cmdstr = "bootc --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --stateroot=\"test\""
        cmdstr_expected = "bootc --stateroot=\"test\" --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --target-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\"" + "\n"
        self.assert_parse(cmdstr, cmdstr_expected)

        cmdstr = "bootc --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --stateroot=\"test\" --target-imgref=\"quay.io/centos-bootc/centos-bootc:stream10\""
        cmdstr_expected = "bootc --stateroot=\"test\" --source-imgref=\"quay.io/centos-bootc/centos-bootc:stream9\" --target-imgref=\"quay.io/centos-bootc/centos-bootc:stream10\"" + "\n"
        self.assert_parse(cmdstr, cmdstr_expected)


        # FAIL tests
        # No required argument presented
        self.assert_parse_error("bootc")
        self.assert_parse_error("bootc --stateroot=default")
        self.assert_parse_error("bootc --target-imgref=default")

class F43_Conflict_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F43

    def runTest(self):
        # FAIL tests
        # bootc should not be used with ostreecontainer and ostreesetup
        self.assert_parse_error("""
        bootc --source-imgref=quay.io/centos-bootc/centos-bootc:stream9
        ostreecontainer --url=quay.io/fedora/silverblue:stable
        """)

        self.assert_parse_error("""
        bootc --source-imgref=quay.io/centos-bootc/centos-bootc:stream9
        ostreesetup --osname=fedora-atomic --url=http://example.com/repo --ref=fedora-atomic/sometest/base/core
        """)
