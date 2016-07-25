#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2015 Red Hat, Inc.
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
from pykickstart.commands.xconfig import FC3_XConfig, FC6_XConfig

class XConfig_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = FC3_XConfig()
        self.assertEqual(cmd.noProbe, False)
        self.assertEqual(cmd.startX, False)
        self.assertEqual(cmd.depth, 0)

        cmd.depth = -1
        self.assertTrue(cmd.__str__().find('--depth') > -1)

        cmd6 = FC6_XConfig()
        cmd6.depth = -1
        self.assertTrue(cmd6.__str__().find('--depth') > -1)


class FC3_TestCase(CommandTest):
    command = "xconfig"

    def runTest(self):
        # pass
        if "--card" in self.optionList:
            self.assert_parse("xconfig --card=cardA --hsync=H --vsync=V --monitor=monitorA --noprobe",
                              "xconfig  --card=cardA --hsync=H --monitor=monitorA --noprobe --vsync=V\n")

        if "--depth" in self.optionList:
            self.assert_parse("xconfig --depth=16 --resolution=1280x1024 --videoram=32000",
                              "xconfig  --depth=16 --resolution=1280x1024 --videoram=32000\n")

        self.assert_parse("xconfig --defaultdesktop=xfce --startxonboot",
                          "xconfig  --defaultdesktop=xfce --startxonboot\n")

        if "--server" in self.optionList:
            self.assert_parse("xconfig --server=Xvfb",
                              "xconfig  --server=Xvfb\n")

        # no arguments means don't print anything out
        self.assert_parse("xconfig", "")

        # fail
        # incorrect parameters
        self.assert_parse_error("xconfig --startxonboot=yes")

        # extra arguments
        self.assert_parse_error("xconfig --extra --arguments --here")
        self.assert_parse_error("xconfig extra arguments here")

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        if "--driver" in self.optionList:
            self.assert_parse("xconfig --driver=vesa",
                              "xconfig  --driver=vesa\n")

        # deprecated
        self.assert_deprecated("xconfig", "--card")
        self.assert_deprecated("xconfig", "--hsync")
        self.assert_deprecated("xconfig", "--monitor")
        self.assert_deprecated("xconfig", "--noprobe")
        self.assert_deprecated("xconfig", "--vsync")

        # removed
        self.assert_removed("xconfig", "--server")

class F9_TestCase(FC6_TestCase):
    def runTest(self):
        FC6_TestCase.runTest(self)

        self.assert_removed("xconfig", "--card")
        self.assert_removed("xconfig", "--hsync")
        self.assert_removed("xconfig", "--monitor")
        self.assert_removed("xconfig", "--noprobe")
        self.assert_removed("xconfig", "--vsync")

class F10_TestCase(F9_TestCase):
    def runTest(self):
        F9_TestCase.runTest(self)

        # deprecated
        self.assert_deprecated("xconfig", "--driver")
        self.assert_deprecated("xconfig", "--depth")
        self.assert_deprecated("xconfig", "--resolution")
        self.assert_deprecated("xconfig", "--videoram")

class F14_TestCase(F10_TestCase):
    def runTest(self):
        F10_TestCase.runTest(self)

        self.assert_removed("xconfig", "--driver")
        self.assert_removed("xconfig", "--depth")
        self.assert_removed("xconfig", "--resolution")
        self.assert_removed("xconfig", "--videoram")

if __name__ == "__main__":
    unittest.main()
