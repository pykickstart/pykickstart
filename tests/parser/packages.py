import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart.version import F21, RHEL6

class Packages_Contains_Comments_TestCase(ParserTest):
    ks = """
%packages
packageA    # this is an end-of-line comment
# this is a whole line comment
packageB
packageC
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that the packages are what we think they are.
        self.assertEqual(len(self.handler.packages.packageList), 3)
        self.assertEqual(self.handler.packages.packageList[0], "packageA")
        self.assertEqual(self.handler.packages.packageList[1], "packageB")
        self.assertEqual(self.handler.packages.packageList[2], "packageC")

class Packages_Contains_Nobase_1_TestCase(ParserTest):
    version = F21

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

class Packages_Contains_Nobase_3_TestCase(ParserTest):
    ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Nobase_Default_TestCase(ParserTest):
    version = F21

    ks = """
%packages --nobase --default
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Nocore_Default_TestCase(ParserTest):
    ks = """
%packages --nocore --default
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Environment_1_TestCase(ParserTest):
    ks = """
%packages
@^whatever-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "whatever-environment")

class Packages_Contains_Environment_2_TestCase(ParserTest):
    ks = """
%packages
@^whatever-environment
@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "another-environment")

class Packages_Contains_Environment_3_TestCase(ParserTest):
    ks = """
%packages
@^whatever-environment
-@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "whatever-environment")

class Packages_Contains_Environment_4_TestCase(ParserTest):
    ks = """
%packages
@^whatever-environment
-@^whatever-environment
@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "another-environment")

if __name__ == "__main__":
    unittest.main()
