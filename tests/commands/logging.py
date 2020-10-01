# Andy Lindeberg <alindebe@redhat.com>
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
from pykickstart.commands.logging import FC6_Logging
from pykickstart.errors import KickstartDeprecationWarning


class FC6_TestCase(CommandTest):
    command = "logging"

    def runTest(self):
        cmd = FC6_Logging()
        self.assertEqual(cmd.__str__(), '\n')
        self.assertEqual(cmd.level, "info")

        # pass
        self.assert_parse("logging", "logging --level=info\n")
        self.assert_parse("logging --level=debug", "logging --level=debug\n")
        self.assert_parse("logging --level=info", "logging --level=info\n")
        self.assert_parse("logging --level=warning", "logging --level=warning\n")
        self.assert_parse("logging --level=error", "logging --level=error\n")
        self.assert_parse("logging --level=critical", "logging --level=critical\n")
        self.assert_parse("logging --host=HOSTNAME", "logging --level=info --host=HOSTNAME\n")
        self.assert_parse("logging --host=HOSTNAME --port=PORT", "logging --level=info --host=HOSTNAME --port=PORT\n")

        # fail
        self.assert_parse_error("logging --level")
        self.assert_parse_error("logging --level=''")
        self.assert_parse_error("logging --level=theprincessisinanothercastle")
        self.assert_parse_error("logging --host")
        self.assert_parse_error("logging --port")
        self.assert_parse_error("logging --port=PORT")


class F34_TestCase(CommandTest):
    command = "logging"

    def runTest(self):
        # pass
        self.assert_parse("logging", "")
        self.assert_parse("logging --host=HOSTNAME", "logging --host=HOSTNAME\n")
        self.assert_parse("logging --host=HOSTNAME --port=PORT", "logging --host=HOSTNAME --port=PORT\n")

        # fail
        self.assert_parse_error("logging --host")
        self.assert_parse_error("logging --port")
        self.assert_parse_error("logging --port=PORT")

        # deprecated
        self.assert_deprecated("logging", "--level")

        with self.assertWarns(KickstartDeprecationWarning):
            self.assert_parse("logging --level=info", "")

        with self.assertWarns(KickstartDeprecationWarning):
            self.assert_parse("logging --level=info --host=HOSTNAME", "logging --host=HOSTNAME\n")

        with self.assertWarns(KickstartDeprecationWarning):
            self.assert_parse("logging --level=info --host=HOSTNAME --port=PORT", "logging --host=HOSTNAME --port=PORT\n")


if __name__ == "__main__":
    unittest.main()
