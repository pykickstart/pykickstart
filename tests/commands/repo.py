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
from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.errors import KickstartError, KickstartParseError

class FC6_TestCase(CommandTest):
    command = "repo"

    def runTest(self, urlRequired=True):
        # pass
        self.assert_parse("repo --name=blah --baseurl=http://www.domain.com",
                          "repo --name=\"blah\" --baseurl=http://www.domain.com\n")
        self.assert_parse("repo --name=blah --mirrorlist=http://www.domain.com",
                          "repo --name=\"blah\" --mirrorlist=http://www.domain.com\n")

        # equality
        self.assertEqual(self.assert_parse("repo --name=left --baseurl=http://wherever"), self.assert_parse("repo --name=left --baseurl=http://wherever"))
        self.assertEqual(self.assert_parse("repo --name=left --baseurl=http://wherever"), self.assert_parse("repo --name=left --baseurl=http://somewhere"))
        self.assertNotEqual(self.assert_parse("repo --name=left --baseurl=http://wherever"), None)
        self.assertNotEqual(self.assert_parse("repo --name=left --baseurl=http://wherever"), self.assert_parse("repo --name=right --baseurl=http://wherever"))

        # fail
        # missing required option --name
        self.assert_parse_error("repo --baseurl=www.domain.com")
        self.assert_parse_error("repo --name --baseurl=www.domain.com")
        # missing one of required options --baseurl or --mirrorlist
        if urlRequired:
            self.assert_parse_error("repo --name=blah")
            self.assert_parse_error("repo --name=blah --baseurl")
            self.assert_parse_error("repo --name=blah --mirrorlist")
        # only one of --baseurl or --mirrorlist must be specified
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com --mirrorlist=www.domain.com")
        # unknown option
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com --unknown", KickstartParseError)
        # not expected argument
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com blah")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.repoList = "--name=blah"
        self.assertEqual(cmd.__str__(), "--name=blah")

        data = self.handler().RepoData()
        data.baseurl = ""
        data.mirrorlist = ""
        self.assertEqual(data._getArgsAsStr(), "")

class FC6_Duplicate_TestCase(CommandSequenceTest):
    def runTest(self):
        self.assert_parse("""
repo --name=repoA --baseurl=http://www.domain.com
repo --name=repoB --baseurl=http://www.domain.com""")

        self.assert_parse_error("""
repo --name=repoA --baseurl=http://www.domain.com
repo --name=repoA --baseurl=http://www.domain.com""", UserWarning)

class F8_TestCase(FC6_TestCase):
    def runTest(self, urlRequired=True):
        # run FC6 test case
        FC6_TestCase.runTest(self, urlRequired=urlRequired)

        # pass
        self.assert_parse("repo --name=blah --baseurl=www.domain.com --cost=10 --excludepkgs=pkg1,pkg2 --includepkgs=pkg3,pkg4",
                          "repo --name=\"blah\" --baseurl=www.domain.com --cost=10 --includepkgs=\"pkg3,pkg4\" --excludepkgs=\"pkg1,pkg2\"\n")
        self.assert_parse("repo --name=blah --baseurl=123xyz --cost=10 --excludepkgs=pkg1,pkg2 --includepkgs=pkg3,pkg4",
                          "repo --name=\"blah\" --baseurl=123xyz --cost=10 --includepkgs=\"pkg3,pkg4\" --excludepkgs=\"pkg1,pkg2\"\n")

        # fail
        # missing required arguments
        for opt in ("--cost", "--includepkgs", "--excludepkgs"):
            self.assert_parse_error("repo --name=blah --baseurl=www.domain.com %s" % opt, KickstartParseError)
        # --cost argument not integer
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com --cost=high", KickstartParseError)

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.handler.method.url = "http://example.com"
        rd = cmd.methodToRepo()
        self.assertEqual(rd.name, "ks-method-url")
        self.assertEqual(rd.baseurl, "http://example.com")

        cmd.handler.method.url = ""
        with self.assertRaises(KickstartError):
            cmd.methodToRepo()

class F11_TestCase(F8_TestCase):
    def runTest(self, urlRequired=True):
        # run F8 test case
        F8_TestCase.runTest(self, urlRequired=urlRequired)

        # pass
        for val in ("1", "true", "on"):
            self.assert_parse("repo --name=blah --baseurl=www.domain.com --cost=10 --excludepkgs=pkg1,pkg2 --includepkgs=pkg3,pkg4 --ignoregroups=%s" % val,
                              "repo --name=\"blah\" --baseurl=www.domain.com --cost=10 --includepkgs=\"pkg3,pkg4\" --excludepkgs=\"pkg1,pkg2\" --ignoregroups=true\n")
        for val in ("0", "false", "off"):
            self.assert_parse("repo --name=blah --baseurl=www.domain.com --cost=10 --excludepkgs=pkg1,pkg2 --includepkgs=pkg3,pkg4 --ignoregroups=%s" % val,
                              "repo --name=\"blah\" --baseurl=www.domain.com --cost=10 --includepkgs=\"pkg3,pkg4\" --excludepkgs=\"pkg1,pkg2\"\n")

        # fail
        # missing --ignoregroups argument
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com --ignoregroups", KickstartParseError)

class F13_TestCase(F11_TestCase):
    def runTest(self, urlRequired=True):
        # run F11 test case
        F11_TestCase.runTest(self, urlRequired=urlRequired)

        # pass
        self.assert_parse("repo --name=blah --baseurl=www.domain.com --proxy=http://someplace/wherever",
                          "repo --name=\"blah\" --baseurl=www.domain.com --proxy=\"http://someplace/wherever\"\n")
        self.assert_parse("repo --name=blah --baseurl=www.domain.com --proxy=\"http://someplace/wherever\"",
                          "repo --name=\"blah\" --baseurl=www.domain.com --proxy=\"http://someplace/wherever\"\n")

        # fail
        # missing --proxy argument
        self.assert_parse_error("repo --name=blah --baseurl=www.domain.com --proxy",
                                KickstartParseError)

class F14_TestCase(F13_TestCase):
    def runTest(self, urlRequired=True):
        F13_TestCase.runTest(self, urlRequired=urlRequired)
        #pass
        self.assert_parse("repo --name=blah --baseurl=https://www.domain.com --noverifyssl",
                          "repo --name=\"blah\" --baseurl=https://www.domain.com --noverifyssl\n")
        #fail
        self.assert_parse_error("repo --name=blah --baseurl=https://www.domain.com --noverifyssl=yeeeaah", KickstartParseError)

class F15_TestCase(F14_TestCase):
    def runTest(self, urlRequired=False):
        F14_TestCase.runTest(self, urlRequired=urlRequired)

class F21_TestCase(F15_TestCase):
    def runTest(self, urlRequired=False):
        F15_TestCase.runTest(self, urlRequired=urlRequired)
        #pass
        self.assert_parse("repo --name=blah --baseurl=https://www.domain.com --install",
                          "repo --name=\"blah\" --baseurl=https://www.domain.com --install\n")
        #fail
        self.assert_parse_error("repo --name=blah --baseurl=https://www.domain.com --install=yeeeaah", KickstartParseError)


if __name__ == "__main__":
    unittest.main()
