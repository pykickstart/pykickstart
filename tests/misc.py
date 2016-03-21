import unittest

from tests.baseclass import ParserTest

class Platform_Comment_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
#platform=x86_64
autopart
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(self.handler.platform, "x86_64")

if __name__ == "__main__":
    unittest.main()
