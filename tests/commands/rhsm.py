#
# Copyright 2019 Red Hat, Inc.
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


class RHEL8_TestCase(CommandTest):
    def runTest(self):
        # basic parsing
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --connect-to-insights')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --server-hostname="https://rhsm.example.com"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --rhsm-baseurl="https://content.example.com"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --server-hostname="https://rhsm.example.com" --connect-to-insights')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://proxy.com"')
        # just the rhsm command without any options is not valid
        self.assert_parse_error('rhsm')

        # multiple activation keys can be passed
        self.assert_parse('rhsm --organization="12345" --activation-key="a" --activation-key="b" --activation-key="c"')

        # at least one activation key needs to be present
        self.assert_parse_error('rhsm --organization="12345"')

        # empty string is not a valid activation key
        self.assert_parse_error('rhsm --organization="12345" --activation-key=""')
        self.assert_parse_error('rhsm --organization="12345" --activation-key="a" --activation-key="b" --activation-key=""')

        # organization id needs to be always specified
        self.assert_parse_error('rhsm --activation-key="a"')
        self.assert_parse_error('rhsm --activation-key="a" --activation-key="b" --activation-key="c"')

        # check proxy parsing
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://proxy.com"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://proxy.com:9001"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://username@proxy.com:9001"')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://username:password@proxy.com:9001"')

        # unknown options are an error
        self.assert_parse_error('rhsm --organization="12345" --activation-key="abcd" --unknown=stuff')

        # test output kickstart generation
        # TODO: check if it is OK to have the organization name & activation key in output kickstart
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd"',
                          'rhsm --organization="12345" --activation-key="abcd"\n')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --activation-key="efgh"',
                          'rhsm --organization="12345" --activation-key="abcd" --activation-key="efgh"\n')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --server-hostname="https://rhsm.example.com" --connect-to-insights',
                          'rhsm --organization="12345" --activation-key="abcd" --connect-to-insights --server-hostname="https://rhsm.example.com"\n')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --rhsm-baseurl="https://content.example.com" --connect-to-insights',
                          'rhsm --organization="12345" --activation-key="abcd" --connect-to-insights --rhsm-baseurl="https://content.example.com"\n')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --rhsm-baseurl="https://content.example.com" --server-hostname="https://rhsm.example.com"',
                          'rhsm --organization="12345" --activation-key="abcd" --server-hostname="https://rhsm.example.com" --rhsm-baseurl="https://content.example.com"\n')
        self.assert_parse('rhsm --organization="12345" --activation-key="abcd" --proxy="http://username:password@proxy.com:9001"',
                          'rhsm --organization="12345" --activation-key="abcd" --proxy="http://username:password@proxy.com:9001"\n')

if __name__ == "__main__":
    unittest.main()
