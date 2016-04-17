from tooltest import KsvalidatorTest, mktempfile
from pykickstart.version import versionMap
import re
import tempfile
import os

class No_Parameters_TestCase(KsvalidatorTest):
    def runTest(self):
        retval, _out, _err = self.run_tool()
        self.assertNotEqual(retval, 0)

class Show_Param_Help_TestCase(KsvalidatorTest):
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
        retval, out, _err = self.run_tool(tool_params=["--help"])
        pos_args = set()
        opt_args = set()
        pos = False
        opt = False
        for line in out:
            if line == "positional arguments:":
                pos = True
                continue
            if line == "optional arguments:":
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


class KS_With_Errors_TestCase(KsvalidatorTest):
    def setUp(self):
        super(KS_With_Errors_TestCase, self).setUp()
        _handle, self._ks_path = tempfile.mkstemp(prefix="ks-", text=True)
        ks_content = """
firstb00t --enable
keyboard --vckeymap=cz --xlayoutz='cz'
unknown --foo='bar'
"""
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        # kickstart file contains 3 erroneous lines - 3 error messages should be present
        _retval, out, _err = self.run_tool(tool_params=[self._ks_path])
        errmsg_count = 0
        for line in out:
            if re.search("^Un[(expected)(known)].+:", line):
                errmsg_count += 1
        self.assertEqual(errmsg_count, 3)

    def tearDown(self):
        super(KS_With_Errors_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class Stop_On_First_Error_TestCase(KsvalidatorTest):
    def setUp(self):
        super(Stop_On_First_Error_TestCase, self).setUp()
        _handle, self._ks_path = tempfile.mkstemp(prefix="ks-", text=True)
        ks_content = """
firstb00t --enable
keyboard --vckeymap=cz --xlayoutz='cz'
unknown --foo='bar'
"""
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        # kickstart file contains 3 erroneous lines, but ksvalidator is run
        # with "-e" option, so only 1 error message should be present
        _retval, out, _err = self.run_tool(tool_params=[self._ks_path, "-e"])
        errmsg_count = 0
        for line in out:
            errmsg = re.search("^Un(expected|known).+:.+", line)
            if errmsg:
                last_errmsg = errmsg.group()
                errmsg_count += 1
        self.assertEqual(errmsg_count, 1)
        self.assertEqual("Unknown command: firstb00t", last_errmsg)

    def tearDown(self):
        super(Stop_On_First_Error_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class KS_With_Include_TestCase(KsvalidatorTest):
    def setUp(self):
        super(KS_With_Include_TestCase, self).setUp()
        self._include_path = mktempfile("unknown_command --foo=bar", prefix="ks-include")
        ks_content = "autopart --type=lvm\n%%include %s" % self._include_path
        self._ks_path = mktempfile(ks_content)

    def runTest(self):
        retval, out, _err = self.run_tool(tool_params=[self._ks_path])
        self.assertEqual(len(list(out)), 0) # no output should be present
        self.assertEqual(retval, 0)

        retval, out, _err = self.run_tool(tool_params=["-i", self._ks_path])
        errmsg_count = 0
        for line in out:
            errmsg = re.search("^Un(expected|known).+:.+", line)
            if errmsg:
                last_errmsg = errmsg.group()
                errmsg_count += 1
        self.assertEqual(errmsg_count, 1)
        self.assertEqual("Unknown command: unknown_command", last_errmsg)

    def tearDown(self):
        super(KS_With_Include_TestCase, self).tearDown()
        os.unlink(self._ks_path)
        os.unlink(self._include_path)


class Nonexistent_KS_File_TestCase(KsvalidatorTest):
    def runTest(self):
        retval, _out, _err = self.run_tool(tool_params=["/foo/bar/baz/ks.cfg"])
        self.assertEqual(retval, 1)


class KS_With_Wrong_Permissions_TestCase(KsvalidatorTest):
    def setUp(self):
        super(KS_With_Wrong_Permissions_TestCase, self).setUp()
        self._ks_path = mktempfile()
        # create IOError, which further results in KickstartError
        os.chmod(self._ks_path, 0o000)

    def runTest(self):
        retval, out, _err = self.run_tool(tool_params=[self._ks_path])
        read_error_seen = False
        for line in out:
            if re.search("Error reading %s.*" % self._ks_path, line):
                read_error_seen = True
        self.assertTrue(read_error_seen)
        self.assertEqual(retval, 1)

    def tearDown(self):
        super(KS_With_Wrong_Permissions_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class Wrong_KS_Version_TestCase(KsvalidatorTest):
    def setUp(self):
        super(Wrong_KS_Version_TestCase, self).setUp()
        self._ks_path = mktempfile()

    def runTest(self):
        # run ksvalidator with nonexistent KS version (FC42)
        retval, out, _err = self.run_tool(tool_params=[self._ks_path, "-v", "FC42"])
        self.assertEqual(retval, 1)
        self.assertEqual("The version FC42 is not supported by pykickstart", list(out)[0])

    def tearDown(self):
        super(Wrong_KS_Version_TestCase, self).tearDown()
        os.unlink(self._ks_path)


class List_Versions_TestCase(KsvalidatorTest):
    def setUp(self):
        self.versions_list = sorted(versionMap.keys())

    def runTest(self):
        retval, out, _err = self.run_tool(tool_params=["-l"])
        self.assertEqual(self.versions_list, out)
        self.assertEqual(retval, 1)
