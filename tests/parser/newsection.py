import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart import sections
from pykickstart import version

class RawSection(sections.Section):
    sectionOpen = "%raw"

    def __init__(self, handler, **kwargs):
        sections.Section.__init__(self, handler, **kwargs)
        self.handler.raw = ""

    def handleLine(self, line):
        if not self.handler:
            return

        self.handler.raw += line

class New_Section_TestCase(ParserTest):
    ks = """
%raw
1234
abcd
%end
"""

    def runTest(self):
        self.parser.registerSection(RawSection(self.parser.handler))
        self.parser.readKickstartFromString(self.ks)

        # Verify the contents of the custom section were saved.
        self.assertEqual(self.parser.handler.raw, "1234\nabcd\n")

if __name__ == "__main__":
    unittest.main()
