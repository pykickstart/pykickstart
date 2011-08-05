import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart import version

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

if __name__ == "__main__":
    unittest.main()
