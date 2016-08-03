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
from pykickstart.commands.method import FC3_Method, F19_Method
from pykickstart.handlers.fc3 import FC3Handler
from pykickstart.handlers.f19 import F19Handler

class FC3_TestCase(CommandTest):
    command = "method"

    def runTest(self):
        # pass
        # cdrom
        self.assert_parse("cdrom", "cdrom\n")

        # harddrive
        self.assert_parse("harddrive --dir=/install --biospart=part", "harddrive --dir=/install --biospart=part\n")
        self.assert_parse("harddrive --dir=/install --partition=part", "harddrive --dir=/install --partition=part\n")

        # nfs
        self.assert_parse("nfs --server=1.2.3.4 --dir=/install", "nfs --server=1.2.3.4 --dir=/install\n")

        # url
        self.assert_parse("url --url=http://domain.com", "url --url=\"http://domain.com\"\n")

        # fail
        # harddrive
        # required option --dir missing
        self.assert_parse_error("harddrive")
        # required --dir argument missing
        self.assert_parse_error("harddrive --dir")
        # missing --biospart or --partition option
        self.assert_parse_error("harddrive --dir=/install")
        # both --biospart and --partition specified
        self.assert_parse_error("harddrive --dir=/install --biospart=bios --partition=part")
        # --biospart and --partition require argument
        self.assert_parse_error("harddrive --dir=/install --biospart")
        self.assert_parse_error("harddrive --dir=/install --partition")
        # unknown option
        self.assert_parse_error("harddrive --unknown=value")

        # nfs
        # missing required options --server and --dir
        self.assert_parse_error("nfs")
        self.assert_parse_error("nfs --server=1.2.3.4")
        self.assert_parse_error("nfs --server")
        self.assert_parse_error("nfs --dir=/install")
        self.assert_parse_error("nfs --dir")
        # unknown option
        self.assert_parse_error("nfs --unknown=value")

        # url
        # missing required option --url
        self.assert_parse_error("url")
        self.assert_parse_error("url --url")

        # __getattr__ + __setattr__
        method = FC3_Method()
        handler = FC3Handler()
        method.handler = handler
        self.assertEqual(method.method, None)
        for chosen_method in method._methods:
            method.method = chosen_method
            method.foo = chosen_method  # try to set an unused attribute
            for unseen_method in [m for m in method._methods if m != chosen_method]:
                self.assertFalse(getattr(method.handler, unseen_method).seen)
                self.assertEqual(method.foo, chosen_method)
            self.assertTrue(getattr(method.handler, chosen_method).seen)
            self.assertEqual(method.method, chosen_method)
        # last seen method should be returned when 'method' attribute doesn't exist
        del method.method
        self.assertEqual(method.method, method._methods[-1])

        # trying to get attributes that don't exist raises an AttributeError
        with self.assertRaises(AttributeError):
            method.internals.append('method1')
            getattr(method, 'method1')
        method.internals.remove('method1')

        with self.assertRaises(AttributeError):
            method.internals.append('0method')
            getattr(method, '0method')
        method.internals.remove('0method')

        # trying to set attributes with bogus values
        for value in ['aaa', 'xxx']:
            method.method = value
            for m in method._methods:
                self.assertFalse(getattr(method.handler, m).seen)

class FC6_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # pass
        # nfs
        self.assert_parse("nfs --server=1.2.3.4 --dir=/install --opts=options", "nfs --server=1.2.3.4 --dir=/install --opts=\"options\"\n")

        # fail
        # nfs
        # --opts requires argument if specified
        self.assert_parse_error("nfs --server=1.2.3.4 --dir=/install --opts")


class F13_TestCase(FC6_TestCase):
    def runTest(self):
        # run FC6 test case
        FC6_TestCase.runTest(self)

        # pass
        self.assert_parse("url --url=http://someplace/somewhere --proxy=http://wherever/other",
                          "url --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\"\n")

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

        # fail
        self.assert_parse_error("cdrom --noverifyssl")

class F18_TestCase(F14_TestCase):
    def runTest(self):
        # run F14 test case.
        F14_TestCase.runTest(self)

        # pass
        self.assert_parse("url --mirrorlist=http://www.wherever.com/mirror",
                          "url --mirrorlist=\"http://www.wherever.com/mirror\"\n")

        # fail
        # missing one of required options --url or --mirrorlist
        self.assert_parse_error("url")
        self.assert_parse_error("url --mirrorlist")

        # It's --url, not --baseurl.
        self.assert_parse_error("url --baseurl=www.wherever.com")

        # only one of --url or --mirrorlist may be specified
        self.assert_parse_error("url --url=www.wherever.com --mirrorlist=www.wherever.com")

class F19_TestCase(F18_TestCase):
    def runTest(self):
        # run F18 test case.
        F18_TestCase.runTest(self)

        # liveimg pass
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other "
                          "--noverifyssl --checksum=e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\" "
                          "--noverifyssl --checksum=\"e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba\"\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other "
                          "--noverifyssl",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\" "
                          "--noverifyssl\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere --proxy=http://wherever/other ",
                          "liveimg --url=\"http://someplace/somewhere\" --proxy=\"http://wherever/other\"\n")
        self.assert_parse("liveimg --url=http://someplace/somewhere",
                          "liveimg --url=\"http://someplace/somewhere\"\n")

        # liveimg fail
        self.assert_parse_error("liveimg")
        self.assert_parse_error("liveimg --url")
        self.assert_parse_error("liveimg --url=http://someplace/somewhere --proxy")
        self.assert_parse_error("liveimg --proxy=http://someplace/somewhere")
        self.assert_parse_error("liveimg --noverifyssl")
        self.assert_parse_error("liveimg --checksum=e7a9fe500330a1cae4ca114833bb3df014e6d14e63ea9566896a848f3832d0ba")

        # __getattr__ + __setattr__
        method = F19_Method()
        handler = F19Handler()
        method.handler = handler
        self.assertEqual(method.method, None)
        method.method = "liveimg"
        method.foo = "liveimg"  # try to set an unused attribute

        for unseen_method in [m for m in method._methods if m != "liveimg"]:
            self.assertFalse(getattr(method.handler, unseen_method).seen)
            self.assertEqual(method.foo, "liveimg")
        self.assertTrue(method.handler.liveimg.seen)    # pylint: disable=no-member
        self.assertEqual(method.method, "liveimg")
        # AttributeError should be raised when accessing nonexistent 'handler' attribute
        del method.handler
        self.assertRaises(AttributeError, getattr, method, "handler")


if __name__ == "__main__":
    unittest.main()
