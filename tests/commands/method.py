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
import copy
from tests.baseclass import CommandTest
from pykickstart.base import DeprecatedCommand

class FC3_Proxy_TestCase(CommandTest):
    command = "method"

    def runTest(self):
        # Test the default method.
        handler = self.handler()
        self._test_seen(handler, None)

        # Try to access correct attribute.
        handler = self.handler()
        handler.method.method = "nfs"

        setattr(handler.method, "server", "1.2.3.4")
        handler.method.server = "1.2.3.4"
        getattr(handler.method, "server")
        if handler.method.server:
            pass

        # Try to access wrong attribute.
        handler = self.handler()
        handler.method.method = "url"

        with self.assertRaises(AttributeError):
            setattr(handler.method, "server", "1.2.3.4")

        with self.assertRaises(AttributeError):
            handler.method.server = "1.2.3.4"

        with self.assertRaises(AttributeError):
            getattr(handler.method, "server")

        with self.assertRaises(AttributeError):
            if handler.method.server:
                pass

        # Try to set a nonexistent method.
        handler = self.handler()
        with self.assertRaises(AttributeError):
            handler.method.method = "???"

        # Try to get and set a nonexistent attribute.
        handler = self.handler()
        handler.method.method = "url"

        with self.assertRaises(AttributeError):
            getattr(handler.method, "nonexistent_attribute")

        with self.assertRaises(AttributeError):
            if handler.method.nonexistent_attribute:
                pass

        with self.assertRaises(AttributeError):
            setattr(handler.method, "nonexistent_attribute", "some_value")

        with self.assertRaises(AttributeError):
            handler.method.nonexistent_attribute = "some_value"

        # Try to call a nonexistent method.
        handler = self.handler()
        with self.assertRaises(AttributeError):
            handler.method.nonexistent_method()

        # Test hasattr.
        handler = self.handler()
        self.assertEqual(hasattr(handler.method, "seen"), True)
        self.assertEqual(hasattr(handler.method, "server"), False)
        self.assertEqual(hasattr(handler.method, "nonexistent"), False)

        handler.method.method = "nfs"
        self.assertEqual(hasattr(handler.method, "seen"), True)
        self.assertEqual(hasattr(handler.method, "server"), True)
        self.assertEqual(hasattr(handler.method, "nonexistent"), False)

        # Test copy and deepcopy.
        handler = self.handler()
        handler.method.method = "url"
        handler.method.url = "http://domain.com"

        method2 = copy.copy(handler.method)
        self.assertEqual(method2.method, "url")
        self.assertEqual(method2.url, "http://domain.com")

        # TODO: Add test for copy.deepcopy.
        # The test now fails somewhere outside of the method command.
        # It should be fixed or anaconda should stop calling it.

        # Test an internal attribute.
        handler = self.handler()
        handler.method.method = "url"
        self.assertEqual(handler.method.lineno, 0)
        self.assertEqual(handler.url.lineno, 0)

        handler.method.lineno = 5
        self.assertEqual(handler.method.lineno, 5)
        self.assertEqual(handler.url.lineno, 0)

        handler.url.lineno = 10
        self.assertEqual(handler.method.lineno, 5)
        self.assertEqual(handler.url.lineno, 10)

        # Test command's attributes.
        # Try to switch between methods.
        handler = self.handler()
        self._set_default(handler)
        self._set_cdrom(handler)
        self._set_url(handler)
        self._set_nfs(handler)
        self._set_harddrive(handler)

    def _test_seen(self, handler, seen_method):
        self.assertEqual(handler.method.method, seen_method)

        for method in handler.method._methods:
            self.assertEqual(getattr(handler, method).seen, method == seen_method)

    def _set_default(self, handler):
        handler.method.method = None
        self._test_seen(handler, None)

        handler.method.url = "http://domain.com"
        self.assertEqual(handler.method.url, "http://domain.com")
        self.assertEqual(handler.url.url, "http://domain.com")
        self.assertEqual(getattr(handler.method, "url"), "http://domain.com")

    def _set_cdrom(self, handler):
        handler.method.method = "cdrom"
        self._test_seen(handler, "cdrom")

    def _set_url(self, handler):
        handler.method.method = "url"
        self._test_seen(handler, "url")

        handler.method.url = "http://domain.com"
        self.assertEqual(handler.method.url, "http://domain.com")
        self.assertEqual(handler.url.url, "http://domain.com")
        self.assertEqual(getattr(handler.method, "url"), "http://domain.com")

    def _set_nfs(self, handler):
        handler.method.method = "nfs"
        self._test_seen(handler, "nfs")

        handler.method.server = "1.2.3.4"
        self.assertEqual(handler.method.server, "1.2.3.4")
        self.assertEqual(handler.nfs.server, "1.2.3.4")
        self.assertEqual(getattr(handler.method, "server"), "1.2.3.4")

    def _set_harddrive(self, handler):
        handler.method.method = "harddrive"
        self._test_seen(handler, "harddrive")

        handler.method.dir = "/install"
        self.assertEqual(handler.method.dir, "/install")
        self.assertEqual(handler.harddrive.dir, "/install")
        self.assertEqual(getattr(handler.method, "dir"), "/install")

class FC3_TestCase(CommandTest):
    command = "method"

    def runTest(self):
        # pass
        # cdrom
        self.assert_parse("cdrom", "cdrom\n")

        # harddrive
        if "biospart" not in self.handler.commandMap["harddrive"].removedKeywords:
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

class F19_Proxy_TestCase(FC3_Proxy_TestCase):
    def runTest(self):
        FC3_Proxy_TestCase.runTest(self)

        # Test command's attributes.
        handler = self.handler()
        self._set_liveimg(handler)

        # Try to switch between methods.
        handler = self.handler()
        self._set_url(handler)
        self._set_liveimg(handler)
        self._set_nfs(handler)

    def _set_liveimg(self, handler):
        handler.method.method = "liveimg"
        self._test_seen(handler, "liveimg")

        handler.method.url = "http://someplace/somewhere"
        self.assertEqual(handler.method.url, "http://someplace/somewhere")
        self.assertEqual(handler.liveimg.url, "http://someplace/somewhere")
        self.assertEqual(getattr(handler.liveimg, "url"), "http://someplace/somewhere")

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

class RHEL7_Proxy_TestCase(F19_Proxy_TestCase):
    def runTest(self):
        F19_Proxy_TestCase.runTest(self)

        # Test command's attributes.
        handler = self.handler()
        self._set_hmc(handler)

        # Try to switch between methods.
        handler = self.handler()
        self._set_cdrom(handler)
        self._set_hmc(handler)
        self._set_harddrive(handler)

    def _set_hmc(self, handler):
        handler.method.method = "hmc"
        self._test_seen(handler, "hmc")

class RHEL7_TestCase(F19_TestCase):
    def runTest(self):
        F19_TestCase.runTest(self)

        # Test hmc.
        self.assert_parse("hmc", "hmc\n")

class F28_Proxy_TestCase(RHEL7_Proxy_TestCase):
    def runTest(self):
        RHEL7_Proxy_TestCase.runTest(self)

class F28_TestCase(RHEL7_TestCase):
    def runTest(self):
        RHEL7_TestCase.runTest(self)

class F34_TestCase(F28_TestCase):
    def runTest(self):
        F28_TestCase.runTest(self)

        # make sure we've been deprecated
        parser = self.getParser("method")
        self.assertEqual(issubclass(parser.__class__, DeprecatedCommand), True)

if __name__ == "__main__":
    unittest.main()
