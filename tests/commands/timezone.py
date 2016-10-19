#
# Chris Lumens <clumens@redhat.com>
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
from pykickstart.errors import KickstartParseError
from pykickstart.commands.timezone import FC3_Timezone, F18_Timezone


class Timezone_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F18_Timezone()
        self.assertEqual(cmd.__str__(), '')


class FC3_TestCase(CommandTest):
    command = "timezone"

    def runTest(self):
        # assert defaults
        self.assertFalse(FC3_Timezone().isUtc)
        self.assertFalse(F18_Timezone().nontp)

        # pass
        self.assert_parse("timezone Eastern", "timezone  Eastern\n")

        # On FC6 and later, we write out --isUtc regardless of what the input was.
        if self.__class__.__name__ == "FC3_TestCase":
            self.assert_parse("timezone --utc Eastern", "timezone --utc Eastern\n")
        else:
            self.assert_parse("timezone --utc Eastern", "timezone --isUtc Eastern\n")

        # fail
        self.assert_parse_error("timezone")
        self.assert_parse_error("timezone Eastern Central")
        self.assert_parse_error("timezone --blah Eastern")
        self.assert_parse_error("timezone --utc")
        self.assert_parse_error("timezone --bogus-option")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.timezone = None
        self.assertEqual(cmd.__str__(), "")

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("timezone --isUtc Eastern", "timezone --isUtc Eastern\n")

        # fail
        self.assert_parse_error("timezone --isUtc")

class F18_TestCase(FC6_TestCase):
    def runTest(self):
        # pass
        self.assert_parse("timezone --utc Europe/Prague")
        self.assert_parse("timezone --isUtc Europe/Prague\n")
        self.assert_parse("timezone --isUtc Eastern", "timezone Eastern --isUtc\n")
        self.assert_parse("timezone Europe/Prague")
        self.assert_parse("timezone Europe/Prague --nontp",
                          "timezone Europe/Prague --nontp\n")
        self.assert_parse("timezone Europe/Prague "
                          "--ntpservers=ntp.cesnet.cz,tik.nic.cz")
        self.assert_parse("timezone Europe/Prague --ntpservers=ntp.cesnet.cz",
                          "timezone Europe/Prague --ntpservers=ntp.cesnet.cz\n")

        # fail
        self.assert_parse_error("timezone")
        self.assert_parse_error("timezone Eastern Central")
        self.assert_parse_error("timezone --blah Eastern")
        self.assert_parse_error("timezone --utc")
        self.assert_parse_error("timezone --isUtc")
        self.assert_parse_error("timezone Europe/Prague --nontp "
                                "--ntpservers=ntp.cesnet.cz")
        self.assert_parse_error("timezone Europe/Prague --ntpservers="
                                "ntp.cesnet.cz, tik.nic.cz")

class F23_TestCase(F18_TestCase):
    def runTest(self):
        # should keep multiple instances of the same URL
        self.assert_parse("timezone --utc Europe/Prague --ntpservers=ntp.cesnet.cz,0.fedora.pool.ntp.org," +
                          "0.fedora.pool.ntp.org,0.fedora.pool.ntp.org,0.fedora.pool.ntp.org",
                          "timezone Europe/Prague --isUtc --ntpservers=ntp.cesnet.cz,0.fedora.pool.ntp.org," +
                          "0.fedora.pool.ntp.org,0.fedora.pool.ntp.org,0.fedora.pool.ntp.org\n")
        self.assert_parse("timezone --utc Europe/Sofia --ntpservers=,0.fedora.pool.ntp.org,")

        # fail
        self.assert_parse_error("timezone Europe/Sofia --nontp --ntpservers=0.fedora.pool.ntp.org,1.fedora.pool.ntp.org")


class RHEL7_TestCase(F18_TestCase):
    def runTest(self):
        # since RHEL7 command version the timezone command can be used
        # without a timezone specification
        self.assert_parse("timezone --utc")
        self.assert_parse("timezone Europe/Sofia")
        self.assert_parse("timezone --isUtc")
        self.assert_parse("timezone --ntpservers=ntp.cesnet.cz")
        self.assert_parse("timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz")
        # unknown argument
        self.assert_parse_error("timezone --blah")
        # more than two timezone specs
        self.assert_parse_error("timezone foo bar", exception=KickstartParseError)
        self.assert_parse_error("timezone --utc foo bar", exception=KickstartParseError)
        # just "timezone" without any arguments is also wrong as it really dosn't make sense
        self.assert_parse_error("timezone")

        # fail
        self.assert_parse_error("timezone Europe/Sofia --nontp --ntpservers=0.fedora.pool.ntp.org,1.fedora.pool.ntp.org")


class F25_TestCase(F23_TestCase):
    def runTest(self):
        # since RHEL7 command version the timezone command can be used
        # without a timezone specification
        self.assert_parse("timezone --utc")
        self.assert_parse("timezone --isUtc")
        self.assert_parse("timezone --ntpservers=ntp.cesnet.cz")
        self.assert_parse("timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz")
        # unknown argument
        self.assert_parse_error("timezone --blah")
        # more than two timezone specs
        self.assert_parse_error("timezone foo bar", exception=KickstartParseError)
        self.assert_parse_error("timezone --utc foo bar", exception=KickstartParseError)
        # just "timezone" without any arguments is also wrong as it really dosn't make sense
        self.assert_parse_error("timezone")

        # fail
        self.assert_parse_error("timezone Europe/Sofia --nontp --ntpservers=0.fedora.pool.ntp.org,1.fedora.pool.ntp.org")


if __name__ == "__main__":
    unittest.main()
