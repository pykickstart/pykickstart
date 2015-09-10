import unittest
import warnings
from tests.baseclass import ParserTest

from pykickstart.constants import KS_MISSING_IGNORE
from pykickstart.errors import KickstartParseError
from pykickstart.version import F21, RHEL6
from pykickstart.parser import Group

class GroupsAreHashable_TestCase(ParserTest):
    def runTest(self):
        hash(Group(name="groupA"))

class Packages_Options_TestCase(ParserTest):
    ks = """
%packages --ignoremissing --default --instLangs="bg_BG"
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that the options are parsed as expected
        self.assertTrue(self.handler.packages.default)
        self.assertEqual(self.handler.packages.handleMissing, KS_MISSING_IGNORE)
        self.assertEqual(self.handler.packages.instLangs, "bg_BG")

        # extra test coverage
        self.assertTrue(self.parser._sections['%packages'].seen)

class Packages_Options_Empty_InstLangs_TestCase(ParserTest):
    ks = """
%packages --instLangs=
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that instLangs is an empty string
        self.assertEqual(self.handler.packages.instLangs, "")

        # Verify that the empty instLangs comes back out
        self.assertEqual(str(self.handler.packages).strip(), "%packages --instLangs=\n\n%end")

class Packages_Options_No_InstLangs_TestCase(ParserTest):
    ks = """
%packages
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that instLangs is None
        self.assertIsNone(self.handler.packages.instLangs)

        # Verify that --instLangs is not displayed
        self.assertEqual(str(self.handler.packages).strip(), "%packages\n\n%end")

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

# An empty %packages section is allowed, and means something different from %packages --default.
# An empty section means to install the minimum amount of stuff, while --default means to install
# whatever would have been installed had this been a graphical installation and the user just
# accepted whatever was offered.
class Packages_Empty_TestCase(ParserTest):
    ks = """
%packages
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertTrue(self.handler.packages.seen)
            self.assertEqual(str(self.handler.packages).strip(), "%packages\n\n%end")

if __name__ == "__main__":
    unittest.main()
