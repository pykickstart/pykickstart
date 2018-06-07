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

from pykickstart.base import DeprecatedCommand
from tests.baseclass import CommandTest

class FC3_TestCase(CommandTest):
    command = "deviceprobe"

    def runTest(self):
        # pass
        self.assert_parse("deviceprobe")
        self.assert_parse("deviceprobe --cheese", "deviceprobe --cheese\n")
        self.assert_parse("deviceprobe --cracker=CRUNCHY", "deviceprobe --cracker=CRUNCHY\n")

class F29_TestCase(FC3_TestCase):
    def runTest(self):
        # make sure we've been deprecated
        parser = self.getParser("deviceprobe")
        self.assertTrue(issubclass(parser.__class__, DeprecatedCommand))

        # make sure we are still able to parse
        self.assert_parse("deviceprobe")

class RHEL8_TestCase(F29_TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
