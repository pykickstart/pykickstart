import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart import version

class Packages_Seen_TestCase(ParserTest):
    ks = """
%packages
packageA
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertTrue(self.handler.packages.seen)

class Packages_Not_Seen_TestCase(ParserTest):
    ks = """
autopart
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertFalse(self.handler.packages.seen)

class Commands_Seen_TestCase(ParserTest):
    ks = """
bootloader --location=none
part / --size=10000 --fstype=ext4
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertFalse(self.handler.autopart.seen)
        self.assertTrue(self.handler.bootloader.seen)
        self.assertTrue(self.handler.partition.seen)

if __name__ == "__main__":
    unittest.main()
