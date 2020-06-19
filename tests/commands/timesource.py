#
# Copyright 2020 Red Hat, Inc.
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

from pykickstart.version import F33
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.timesource import F33_TimesourceData

class F33_TestCase(CommandTest):
    command = "timesource"

    def runTest(self):
        data1 = F33_TimesourceData()
        data1.ntp_server="ntp.example.com"
        data2 = F33_TimesourceData()
        data2.ntp_server="ntp.example.com"
        self.assertEqual(data1, data2)
        self.assertFalse(data1 != data2) # test __ne__ method
        self.assertNotEqual(data1, None)

        for attr in ['ntp_server', 'ntp_pool']:
            data1 = F33_TimesourceData()
            data2 = F33_TimesourceData()
            setattr(data1, attr, 'foo')
            setattr(data2, attr, 'test')
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, attr, '')
            setattr(data2, attr, '')

        # pass
        self.assert_parse("timesource --ntp-server=ntp.example.com")
        self.assert_parse("timesource --ntp-pool=pool.example.com")
        self.assert_parse("timesource --ntp-server=ntp.example.com --nts")
        self.assert_parse("timesource --ntp-pool=pool.example.com --nts")
        self.assert_parse("timesource --ntp-disable")

        # fail
        # server and pool can't be used at the same time
        self.assert_parse_error("timesource --ntp-server=ntp.example.com --ntp-pool=pool.example.com")
        self.assert_parse_error("timesource --ntp-server=ntp.example.com --ntp-pool=pool.example.com --nts")
        # disable can't be used with neither server or pool
        self.assert_parse_error("timesource --ntp-disable --ntp-pool=pool.example.com")
        self.assert_parse_error("timesource --ntp-server=ntp.example.com --ntp-disable")
        # --ntp-server requires an argument
        self.assert_parse_error("timesource --ntp-server")
        self.assert_parse_error("timesource --ntp-server --nts")
        # --ntp-pool requires int argument
        self.assert_parse_error("timesource --ntp-pool")
        self.assert_parse_error("timesource --ntp-pool --nts")
        # unknown option
        self.assert_parse_error("timesource --ntp-server=ntp.example.com --unknown=value")
        # required option arguments
        self.assert_parse_error("timesource")
        self.assert_parse_error("timesource --nts")

        # test output kickstart generation
        self.assert_parse('timesource --ntp-server=ntp.example.com',
                          'timesource --ntp-server=ntp.example.com\n')
        self.assert_parse('timesource --ntp-pool=pool.example.com',
                          'timesource --ntp-pool=pool.example.com\n')
        self.assert_parse('timesource --ntp-server=ntp.example.com --nts',
                          'timesource --ntp-server=ntp.example.com --nts\n')
        self.assert_parse('timesource --ntp-pool=pool.example.com --nts',
                          'timesource --ntp-pool=pool.example.com --nts\n')
        self.assert_parse('timesource --ntp-disable',
                          'timesource --ntp-disable\n')

        # extra test coverage
        td = self.handler().TimesourceData()
        td.ntp_server = ""
        td.ntp_pool = ""
        self.assertEqual(td.__str__(), "")
        self.assertEqual(td._getArgsAsStr(), "")

        cmd = self.handler().commands[self.command]
        cmd.timesource_list = [td]
        self.assertEqual(cmd.__str__(), "")


class F33_MultiCommand_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F33

    def runTest(self):
        self.assert_parse("""
timesource --ntp-server=ntp.example.com
timesource --ntp-pool=pool.example.com
timesource --ntp-disable
""")

        self.assert_parse_error("""
timesource --ntp-server=ntp.example.com
timesource --ntp-pool=pool.example.com
timesource --nts
""")

        self.assert_parse_error("""
timesource --ntp-server=ntp.example.com
timesource --ntp-pool=pool.example.com
timesource --ntp-server=ntp.example.com --ntp-pool=pool.example.com
""")


if __name__ == "__main__":
    unittest.main()
