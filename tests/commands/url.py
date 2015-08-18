#
# Martin Gracik <mgracik@redhat.com>
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

from pykickstart.errors import KickstartParseError, KickstartValueError

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("url --url=http://domain.com", "url --url=\"http://domain.com\"\n")

        self.assertFalse(self.assert_parse("url --url=http://domain.com") == None)
        self.assertTrue(self.assert_parse("url --url=http://domainA.com") != \
                        self.assert_parse("url --url=http://domainB.com"))
        self.assertFalse(self.assert_parse("url --url=http://domainA.com") == \
                         self.assert_parse("url --url=http://domainB.com"))

        # fail
        # missing required option --url
        self.assert_parse_error("url", KickstartValueError)
        self.assert_parse_error("url --url", KickstartParseError)

class F13_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=http://someplace/somewhere --proxy=http://wherever/other",
                          "url --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\"\n")

        self.assertTrue(self.assert_parse("url --url=http://domain.com --proxy=http://proxy.com") == \
                        self.assert_parse("url --url=http://domain.com --proxy=http://proxy.com"))
        self.assertFalse(self.assert_parse("url --url=http://domain.com --proxy=http://proxyA.com") == \
                         self.assert_parse("url --url=http://domain.com --proxy=http://proxyB.com"))

        # fail
        self.assert_parse_error("cdrom --proxy=http://someplace/somewhere", KickstartParseError)
        self.assert_parse_error("url --url=http://someplace/somewhere --proxy", KickstartParseError)
        self.assert_parse_error("url --proxy=http://someplace/somewhere", KickstartValueError)

class F14_TestCase(F13_TestCase):
    def runTest(self):
        # run FC6 test case
        F13_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=https://someplace/somewhere --noverifyssl",
                          "url --url=\"https://someplace/somewhere\" --noverifyssl\n")

        self.assertTrue(self.assert_parse("url --url=https://domain.com --noverifyssl") == \
                        self.assert_parse("url --url=https://domain.com --noverifyssl"))
        self.assertFalse(self.assert_parse("url --url=https://domain.com") == \
                         self.assert_parse("url --url=https://domain.com --noverifyssl"))

        # fail
        self.assert_parse_error("cdrom --noverifyssl", KickstartParseError)

class F18_TestCase(F14_TestCase):
    def runTest(self):
        # run F14 test case.
        F14_TestCase.runTest(self)

        # pass
        self.assert_parse("url --mirrorlist=http://www.wherever.com/mirror",
                          "url --mirrorlist=\"http://www.wherever.com/mirror\"\n")

        self.assertTrue(self.assert_parse("url --mirrorlist=https://domain.com") == \
                        self.assert_parse("url --mirrorlist=https://domain.com"))
        self.assertFalse(self.assert_parse("url --url=https://domain.com") == \
                         self.assert_parse("url --mirrorlist=https://domain.com"))

        # fail
        # missing one of required options --url or --mirrorlist
        self.assert_parse_error("url", KickstartValueError)
        self.assert_parse_error("url --mirrorlist", KickstartParseError)

        # It's --url, not --baseurl.
        self.assert_parse_error("url --baseurl=www.wherever.com", KickstartParseError)

        # only one of --url or --mirrorlist may be specified
        self.assert_parse_error("url --url=www.wherever.com --mirrorlist=www.wherever.com",
                                KickstartValueError)

if __name__ == "__main__":
    unittest.main()
