import re
import os
import tempfile
import unittest
from unittest import TestCase
import unittest.mock as mock
from tools import ksvalidator
from pykickstart import parser
from tests.tools.utils import mktempfile
from pykickstart.version import versionMap
from pykickstart.errors import KickstartDeprecationWarning

class Remove_Non_Existing_File_TestCase(TestCase):
    def runTest(self):
        destdir = tempfile.mkdtemp("", "ksvalidator-test-tmp-", "/tmp")
        # no exception should be raised
        ksvalidator.cleanup(destdir, "/non/existing/file")

class No_Parameters_TestCase(TestCase):
    """
        Executing ksvalidator.py w/o any arguments
        should print usage information.
    """
    def runTest(self):
        retval, messages = ksvalidator.main([])
        self.assertNotEqual(retval, 0)
        self.assertTrue("usage:" in " ".join(messages))

class Show_Param_Help_TestCase(TestCase):
    """
    Help with specified command line options should be printed
    when ksvalidator is run with "--help" argument
    """
    def runTest(self):
        expected_pos_args = {"ksfile"}
        expected_opt_args = {("-h", "--help"),
                             ("-e", "--firsterror"),
                             ("-i", "--followincludes"),
                             ("-l", "--listversions"),
                             ("-v", "--version")}
        retval, messages = ksvalidator.main(["--help"])
        pos_args = set()
        opt_args = set()
        pos = False
        opt = False
        for line in messages:
            if line == "positional arguments:":
                pos = True
                continue
            if line in ("optional arguments:", "options:"):
                pos = False
                opt = True
                continue

            if pos:
                pos_arg = re.search("[a-zA-Z]+", line)
                if pos_arg:
                    pos_args.add(pos_arg.group(0))
            if opt:
                opt_arg = tuple(re.findall("--?[a-zA-Z]+", line))
                if opt_arg:
                    opt_args.add(opt_arg)

        self.assertEqual(expected_pos_args, pos_args)
        self.assertEqual(expected_opt_args, opt_args)
        self.assertEqual(retval, 0)


class KS_With_Errors_TestCase(TestCase):
    def setUp(self):
        super(KS_With_Errors_TestCase, self).setUp()
        ks_content = """
firstb00t --enable
keyboard --vckeymap=cz --xlayoutz='cz'
unknown --foo='bar'
"""
        self._ks_path = mktempfile(ks_content)

    @mock.patch.object(parser, 'print', create=True)
    def runTest(self, _print):
        retval, _out = ksvalidator.main([self._ks_path])
        # kickstart file contains 3 erroneous lines - 3 error messages should be present
        self.assertEqual(_print.call_count, 3)
        self.assertNotEqual(retval, 0)

    def tearDown(self):
        super(KS_With_Errors_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class Stop_On_First_Error_TestCase(TestCase):
    def setUp(self):
        super(Stop_On_First_Error_TestCase, self).setUp()
        ks_content = """
firstb00t --enable
keyboard --vckeymap=cz --xlayoutz='cz'
unknown --foo='bar'
"""
        self._ks_path = mktempfile(ks_content)

    @mock.patch.object(parser, 'print', create=True)
    def runTest(self, _print):
        # kickstart file contains 3 erroneous lines, but ksvalidator is run
        # with "-e" option
        retval, out = ksvalidator.main([self._ks_path, "-e"])
        # print is not called b/c when errorsAreFatal
        # we raise an exception straight away
        self.assertEqual(_print.call_count, 0)
        # there is one error message only, coming from
        # ksvalidator itself
        self.assertTrue("Unknown command: firstb00t" in " ".join(out))
        self.assertNotEqual(retval, 0)

    def tearDown(self):
        super(Stop_On_First_Error_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class KS_With_Include_TestCase(TestCase):
    def setUp(self):
        super(KS_With_Include_TestCase, self).setUp()
        self._include_path = mktempfile("unknown_command --foo=bar", prefix="ks-include")
        ks_content = "autopart --type=lvm\n%%include %s" % self._include_path
        self._ks_path = mktempfile(ks_content)

    @mock.patch.object(parser, 'print', create=True)
    def runTest(self, _print):
        retval, out = ksvalidator.main([self._ks_path])
        self.assertEqual(len(out), 0)  # no output should be present
        self.assertEqual(retval, 0)

        # included snippet has errors
        retval, out = ksvalidator.main(["-i", self._ks_path])
        self.assertEqual(_print.call_count, 1)
        self.assertNotEqual(retval, 0)

    def tearDown(self):
        super(KS_With_Include_TestCase, self).tearDown()
        os.unlink(self._ks_path)
        os.unlink(self._include_path)


class Nonexistent_KS_File_TestCase(TestCase):
    def runTest(self):
        retval, out = ksvalidator.main(["/foo/bar/baz/ks.cfg"])
        self.assertNotEqual(retval, 0)
        self.assertTrue("No files match the patterns" in " ".join(out))


class URL_KS_File_TestCase(TestCase):
    def setUp(self):
        super(URL_KS_File_TestCase, self).setUp()
        ks_content = "text\n"
        self._ks_path = mktempfile(ks_content)

    @mock.patch("tools.ksvalidator.load_to_file")
    def runTest(self, load_mock):
        load_mock.return_value = self._ks_path
        retval, _ = ksvalidator.main(["http://example.com/some.kickstart/is/online"])
        print(locals())
        self.assertEqual(retval, 0)

    def tearDown(self):
        super(URL_KS_File_TestCase, self).tearDown()
        os.unlink(self._ks_path)

@unittest.skipUnless(os.getuid(), "test requires non-root access")
class KS_With_Wrong_Permissions_TestCase(TestCase):
    def setUp(self):
        super(KS_With_Wrong_Permissions_TestCase, self).setUp()
        self._ks_path = mktempfile()
        # create IOError, which further results in KickstartError
        os.chmod(self._ks_path, 0o000)

    def runTest(self):
        retval, out = ksvalidator.main([self._ks_path])
        read_error_seen = False
        for line in out:
            if re.search("Error reading %s.*" % self._ks_path, line):
                read_error_seen = True
        self.assertTrue(read_error_seen)
        self.assertNotEqual(retval, 0)

    def tearDown(self):
        super(KS_With_Wrong_Permissions_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class Wrong_KS_Version_TestCase(TestCase):
    def setUp(self):
        super(Wrong_KS_Version_TestCase, self).setUp()
        self._ks_path = mktempfile()

    def runTest(self):
        # run ksvalidator with nonexistent KS version (FC42)
        retval, out = ksvalidator.main([self._ks_path, "-v", "FC42"])
        self.assertNotEqual(retval, 0)
        self.assertTrue("The version FC42 is not supported by pykickstart" in " ".join(out))

    def tearDown(self):
        super(Wrong_KS_Version_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class List_Versions_TestCase(TestCase):
    def setUp(self):
        self.versions_list = sorted(versionMap.keys())

    def runTest(self):
        retval, out = ksvalidator.main(["-l"])
        self.assertEqual(self.versions_list, out)
        self.assertEqual(retval, 0)

class Raise_KickstartError_TestCase(TestCase):
    def setUp(self):
        super(Raise_KickstartError_TestCase, self).setUp()
        ks_content = "%ksappend /none.ks"
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        retval, out = ksvalidator.main([self._ks_path, "-v", "F10"])
        self.assertNotEqual(retval, 0)
        self.assertTrue("General kickstart error" in " ".join(out))

    def tearDown(self):
        super(Raise_KickstartError_TestCase, self).tearDown()
        os.unlink(self._ks_path)

class Raise_Exception_TestCase(TestCase):
    def setUp(self):
        super(Raise_Exception_TestCase, self).setUp()
        ks_content = "text'"  # extra quote here
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        retval, out = ksvalidator.main([self._ks_path, "-v", "F10"])
        self.assertNotEqual(retval, 0)
        self.assertTrue("General error in input file:  No closing quotation" in " ".join(out))

    def tearDown(self):
        super(Raise_Exception_TestCase, self).tearDown()
        os.unlink(self._ks_path)

class Raise_DeprecationWarning_TestCase(TestCase):
    def setUp(self):
        super(Raise_DeprecationWarning_TestCase, self).setUp()
        ks_content = "text"
        self._ks_path = mktempfile(ks_content)

    @mock.patch.object(parser.KickstartParser, 'readKickstart')
    def runTest(self, _mock):
        _mock.side_effect = KickstartDeprecationWarning('Raised by test')
        retval, out = ksvalidator.main([self._ks_path, "-v", "F10"])
        self.assertNotEqual(retval, 0)
        self.assertTrue("File uses a deprecated option or command" in " ".join(out))

    def tearDown(self):
        super(Raise_DeprecationWarning_TestCase, self).tearDown()
        os.unlink(self._ks_path)

class PackagesSectionCamelCase_TestCase(TestCase):
    def setUp(self):
        super(PackagesSectionCamelCase_TestCase, self).setUp()
        ks_content = "%packages --instLangs=en\n%end\n"
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        retval, out = ksvalidator.main([self._ks_path, "-v", "F9"])
        self.assertEqual(retval, 0)

        retval, out = ksvalidator.main([self._ks_path, "-v", "F32"])
        self.assertNotEqual(retval, 0)

    def tearDown(self):
        super(PackagesSectionCamelCase_TestCase, self).tearDown()
        os.unlink(self._ks_path)

class PackagesSectionLowerCase_TestCase(TestCase):
    def setUp(self):
        super(PackagesSectionLowerCase_TestCase, self).setUp()
        ks_content = "%packages --inst-langs=en\n%end\n"
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        retval, out = ksvalidator.main([self._ks_path, "-v", "F9"])
        self.assertNotEqual(retval, 0)

        retval, out = ksvalidator.main([self._ks_path, "-v", "F32"])
        self.assertEqual(retval, 0)

    def tearDown(self):
        super(PackagesSectionLowerCase_TestCase, self).tearDown()
        os.unlink(self._ks_path)
