import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart.version import RHEL6

class Packages_Contains_Comments_TestCase(ParserTest):
    ks = """
%packages
packageA    # this is an end-of-line comment
# this is a whole line comment
packageB
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that the packages are what we think they are.
        self.assertEqual(len(self.handler.packages.packageList), 2)
        self.assertEqual(self.handler.packages.packageList[0], "packageA")
        self.assertEqual(self.handler.packages.packageList[1], "packageB")

class Packages_Contains_Nobase_1_TestCase(ParserTest):
    ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[-1].message, DeprecationWarning)

class Packages_Contains_Nobase_2_TestCase(ParserTest):
    version = RHEL6

    ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 0)

if __name__ == "__main__":
    unittest.main()
