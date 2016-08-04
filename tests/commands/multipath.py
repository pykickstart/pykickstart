# Chris Lumens <clumens@redhat.com>
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
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.multipath import FC6_MultiPath
from pykickstart.base import DeprecatedCommand
from pykickstart.version import FC6

class FC6_TestCase(CommandTest):
    command = "multipath"

    def runTest(self):
        for action in FC6_MultiPath()._getParser()._actions:
            if '--name' in action.option_strings:
                self.assertTrue(action.required)

            for a in ['--device', '--rule']:
                if a in action.option_strings:
                    self.assertTrue(action.required)
                    self.assertTrue(action.notest)

        # pass
        self.assert_parse("multipath --name=mpath0 --device=/dev/sdc --rule=failover",
                          "multipath --name=mpath0 --device=/dev/sdc --rule=\"failover\"\n")

        # extra test coverage
        multipath = self.handler().commands["multipath"]
        multipath.dataList().append(multipath.parse("--name=mpath0 --device=/dev/sdc --rule=failover".split(" ")))
        self.assertEqual(multipath.__str__(), "multipath --name=mpath0 --device=/dev/sdc --rule=\"failover\"\n")

        # fail
        self.assert_parse_error("multipath")
        self.assert_parse_error("multipath --name")
        self.assert_parse_error("multipath --device")
        self.assert_parse_error("multipath --rule")
        self.assert_parse_error("multipath --name=mpath0")
        self.assert_parse_error("multipath --name mpath0")
        self.assert_parse_error("multipath --device /dev/sdc")
        self.assert_parse_error("multipath --device=/dev/sdc")
        self.assert_parse_error("multipath --magic")

class FC6_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = FC6

    def runTest(self):
        self.assert_parse_error("""
multipath --name=mpath0 --device=/dev/sda --rule=failover
multipath --name=mpath1 --device=/dev/sda --rule=failover""")

        self.assert_parse("""
multipath --name=mpath0 --device=/dev/sda --rule=failover
multipath --name=mpath0 --device=/dev/sdb --rule=failover""")

class F24_TestCase(FC6_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("multipath")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)

if __name__ == "__main__":
    unittest.main()
