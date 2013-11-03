import unittest, shlex
from tests.baseclass import *

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.version import *
from pykickstart.commands.volgroup import *

class FC3_TestCase(CommandTest):
    command = "volgroup"

    def runTest(self):
        # --noformat
        self.assert_parse("volgroup vg.01 --noformat",
                          "volgroup vg.01 --noformat --pesize=32768 --useexisting\n")
        # --useexisting
        self.assert_parse("volgroup vg.01 --useexisting",
                          "volgroup vg.01 --pesize=32768 --useexisting\n")

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

        # Pass - correct usage.
        self.assert_parse("volgroup vg.01 pv.01 --reserved-space=1000",
                          "volgroup vg.01 --pesize=32768 --reserved-space=1000 pv.01\n")
        self.assert_parse("volgroup vg.01 pv.01 --reserved-percent=50",
                          "volgroup vg.01 --pesize=32768 --reserved-percent=50 pv.01\n")

        # Fail - missing required argument.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space", KickstartParseError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent", KickstartParseError)

        # Fail - incorrect values.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space=-1", KickstartValueError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=0", KickstartValueError)
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=100", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
