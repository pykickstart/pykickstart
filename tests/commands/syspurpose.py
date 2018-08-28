#
# Martin Kolman <mkolman@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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
        self.assert_parse('syspurpose --role="foo" --sla="bar" --usage="baz" --addon="a" --addon="b" --addon="c"')
        self.assert_parse('syspurpose --role="foo"')
        self.assert_parse('syspurpose --sla="bar"')
        self.assert_parse('syspurpose --usage="baz"')
        self.assert_parse('syspurpose --addon="a" --addon="b" --addon="c"')
        # just syspurpose without options is likely valid even though useless
        self.assert_parse('syspurpose')

        # multi word names
        self.assert_parse('syspurpose --role="foo a" --sla="bar b c" --usage="baz foo" --addon="a b" --addon="c d" --addon="e"')

        # no positional arguments are accepted
        self.assert_parse_error('syspurpose foo')
        self.assert_parse_error('syspurpose foo --role=foo --sla=bar --usage=baz')

        # unknown options are an error
        self.assert_parse_error('syspurpose --role=foo --unknown=stuff')

        # test output kickstart generation
        self.assert_parse("syspurpose", "")
        self.assert_parse('syspurpose --role="foo"', 'syspurpose --role="foo"\n')
        self.assert_parse('syspurpose --sla="bar"', 'syspurpose --sla="bar"\n')
        self.assert_parse('syspurpose --usage="baz"', 'syspurpose --usage="baz"\n')
        self.assert_parse('syspurpose --role="foo" --sla="bar" --usage="baz"\n',
                          'syspurpose --role="foo" --sla="bar" --usage="baz"\n')
        self.assert_parse('syspurpose --addon="a" --addon="b" --addon="c"', 'syspurpose --addon="a" --addon="b" --addon="c"\n')
        # multi word handling
        self.assert_parse('syspurpose --role="foo a" --sla="bar b" --usage="baz c" --addon="a b" --addon="c d" --addon="e"',
                          'syspurpose --role="foo a" --sla="bar b" --usage="baz c" --addon="a b" --addon="c d" --addon="e"\n')

if __name__ == "__main__":
    unittest.main()
