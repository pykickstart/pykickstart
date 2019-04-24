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
from pykickstart.commands.url import FC3_Url

class Url_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = FC3_Url()
        data2 = FC3_Url()

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['url']:
            setattr(data1, atr, '')
            setattr(data2, atr, 'test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')


class FC3_TestCase(CommandTest):
    command = "url"

    def runTest(self):
        # pass
        self.assert_parse("url --url=http://domain.com", "url --url=\"http://domain.com\"\n")

        self.assertFalse(self.assert_parse("url --url=http://domain.com") is None)
        self.assertTrue(self.assert_parse("url --url=http://domainA.com") !=
                        self.assert_parse("url --url=http://domainB.com"))
        self.assertFalse(self.assert_parse("url --url=http://domainA.com") ==
                         self.assert_parse("url --url=http://domainB.com"))

        # fail
        # missing required option --url
        self.assert_parse_error("url")
        self.assert_parse_error("url --url")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.seen = False
        self.assertEqual(cmd.__str__(), "")

class F13_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=http://someplace/somewhere --proxy=http://wherever/other",
                          "url --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\"\n")

        self.assertTrue(self.assert_parse("url --url=http://domain.com --proxy=http://proxy.com") ==
                        self.assert_parse("url --url=http://domain.com --proxy=http://proxy.com"))
        self.assertFalse(self.assert_parse("url --url=http://domain.com --proxy=http://proxyA.com") ==
                         self.assert_parse("url --url=http://domain.com --proxy=http://proxyB.com"))

        # fail
        self.assert_parse_error("cdrom --proxy=http://someplace/somewhere")
        self.assert_parse_error("url --url=http://someplace/somewhere --proxy")
        self.assert_parse_error("url --proxy=http://someplace/somewhere")

class F14_TestCase(F13_TestCase):
    def runTest(self):
        # run FC6 test case
        F13_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=https://someplace/somewhere --noverifyssl",
                          "url --url=\"https://someplace/somewhere\" --noverifyssl\n")

        self.assertTrue(self.assert_parse("url --url=https://domain.com --noverifyssl") ==
                        self.assert_parse("url --url=https://domain.com --noverifyssl"))
        self.assertFalse(self.assert_parse("url --url=https://domain.com") ==
                         self.assert_parse("url --url=https://domain.com --noverifyssl"))

        # fail
        self.assert_parse_error("cdrom --noverifyssl")

class F18_TestCase(F14_TestCase):
    def runTest(self):
        # run F14 test case.
        F14_TestCase.runTest(self)

        # pass
        self.assert_parse("url --mirrorlist=http://www.wherever.com/mirror",
                          "url --mirrorlist=\"http://www.wherever.com/mirror\"\n")

        self.assertTrue(self.assert_parse("url --mirrorlist=https://domain.com") ==
                        self.assert_parse("url --mirrorlist=https://domain.com"))
        self.assertFalse(self.assert_parse("url --url=https://domain.com") ==
                         self.assert_parse("url --mirrorlist=https://domain.com"))

        # fail
        # missing one of required options --url or --mirrorlist
        self.assert_parse_error("url")
        self.assert_parse_error("url --mirrorlist")

        # It's --url, not --baseurl.
        self.assert_parse_error("url --baseurl=www.wherever.com")

        # only one of --url or --mirrorlist may be specified
        self.assert_parse_error("url --url=www.wherever.com --mirrorlist=www.wherever.com")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.seen = True
        cmd.url = None
        cmd.mirrorlist = None
        self.assertEqual(cmd.__str__(), "# Use network installation\n\n")

class RHEL7_TestCase(F18_TestCase):
    def runTest(self):
        # run F18 test case.
        F18_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=http://example.com --sslclientcert=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslclientcert=\"file:///foo/bar\"\n")
        self.assert_parse("url --url=http://example.com --sslclientkey=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslclientkey=\"file:///foo/bar\"\n")
        self.assert_parse("url --url=http://example.com --sslcacert=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslcacert=\"file:///foo/bar\"\n")

        # fail: all of these take arguments
        self.assert_parse_error("url --url=http://example.com --sslclientcert")
        self.assert_parse_error("url --url=http://example.com --sslclientkey")
        self.assert_parse_error("url --url=http://example.com --sslcacert")

class F27_TestCase(F18_TestCase):
    def runTest(self):
        # run F18 test case.
        F18_TestCase.runTest(self)

        # pass
        self.assert_parse("url --metalink=http://www.wherever.com/metalink",
                          "url --metalink=\"http://www.wherever.com/metalink\"\n")

        self.assertTrue(self.assert_parse("url --metalink=https://domain.com") == \
                        self.assert_parse("url --metalink=https://domain.com"))
        self.assertFalse(self.assert_parse("url --url=https://domain.com") == \
                         self.assert_parse("url --metalink=https://domain.com"))

        # fail
        self.assert_parse_error("url --metalink")

        # only one of --url, --mirrorlist, or --metalink may be specified
        self.assert_parse_error("url --url=www.wherever.com --metalink=www.wherever.com")
        self.assert_parse_error("url --mirrorlist=www.wherever.com --metalink=www.wherever.com")

class RHEL8_TestCase(F27_TestCase):
    def runTest(self):
        # run F27 test case.
        F27_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=http://example.com --sslclientcert=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslclientcert=\"file:///foo/bar\"\n")
        self.assert_parse("url --url=http://example.com --sslclientkey=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslclientkey=\"file:///foo/bar\"\n")
        self.assert_parse("url --url=http://example.com --sslcacert=file:///foo/bar",
                          "url --url=\"http://example.com\" --sslcacert=\"file:///foo/bar\"\n")

        # fail: all of these take arguments
        self.assert_parse_error("url --url=http://example.com --sslclientcert")
        self.assert_parse_error("url --url=http://example.com --sslclientkey")
        self.assert_parse_error("url --url=http://example.com --sslcacert")

if __name__ == "__main__":
    unittest.main()
