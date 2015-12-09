import unittest, shlex
from tests.baseclass import *

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.version import *
from pykickstart.commands.volgroup import *

class FC3_TestCase(CommandTest):
    command = "volgroup"

    def runTest(self):
        if self.__class__ in (FC3_TestCase, F16_TestCase, RHEL6_TestCase):
            def_pesize_str = " --pesize=32768"
        else:
            def_pesize_str = ""

        # --noformat
        self.assert_parse("volgroup vg.01 --noformat",
                          "volgroup vg.01 --noformat%s --useexisting\n" % def_pesize_str)
        # --useexisting
        self.assert_parse("volgroup vg.01 --useexisting",
                          "volgroup vg.01%s --useexisting\n" % def_pesize_str)

        # --pesize
        self.assert_parse("volgroup vg.01 pv.01 --pesize=70000",
                          "volgroup vg.01 --pesize=70000 pv.01\n")

        # assert data types
        self.assert_type("volgroup", "pesize", "int")
        self.assert_type("volgroup", "format", "boolean")
        self.assert_type("volgroup", "preexist", "boolean")

        # fail - incorrect type
        self.assert_parse_error("volgroup vg.01 pv.01 --pesize=SIZE", KickstartParseError)

        # fail - missing name
        self.assert_parse_error("volgroup", KickstartParseError)

        # fail - missing list of partitions
        self.assert_parse_error("volgroup vg01", KickstartValueError)

        # fail - both members and useexisting specified
        self.assert_parse_error("volgroup vg.01 --useexisting pv.01 pv.02", KickstartValueError)

class F16_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        if self.__class__ in (FC3_TestCase, F16_TestCase, RHEL6_TestCase):
            def_pesize_str = " --pesize=32768"
        else:
            def_pesize_str = ""

        # Pass - correct usage.
        self.assert_parse("volgroup vg.01 pv.01 --reserved-space=1000",
                          "volgroup vg.01%s --reserved-space=1000 pv.01\n" % def_pesize_str)
        self.assert_parse("volgroup vg.01 pv.01 --reserved-percent=50",
                          "volgroup vg.01%s --reserved-percent=50 pv.01\n" % def_pesize_str)

        # Fail - missing required argument.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space", KickstartParseError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent", KickstartParseError)

        # Fail - incorrect values.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space=-1", KickstartValueError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=0", KickstartValueError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=100", KickstartValueError)


class RHEL6_TestCase(F16_TestCase):
    def runTest(self):
        F16_TestCase.runTest(self)
        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.parse(["volgroup", "vg.02", "pv.01"])
        self.assertEqual(cmd.__str__(), "")
        cmd.handler.autopart.seen = True
        with self.assertRaises(KickstartParseError):
            cmd.parse(["volgroup", "vg.02", "pv.01"])
        cmd.handler.autopart.seen = False


class F21_TestCase(F16_TestCase):
    def runTest(self):
        # just run all the old tests with the new class (different PE size
        # default)
        F16_TestCase.runTest(self)

RHEL7_TestCase = F16_TestCase

if __name__ == "__main__":
    unittest.main()
