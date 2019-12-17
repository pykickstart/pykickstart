import unittest
import warnings

from tests.baseclass import ParserTest

from pykickstart import sections
from pykickstart.errors import KickstartParseError, KickstartParseWarning


class RawSection(sections.Section):
    def __init__(self, handler, **kwargs):
        sections.Section.__init__(self, handler, **kwargs)
        self.handler.raw = ""
        self.sectionOpen = "%raw"

    def handleLine(self, line):
        if not self.handler:
            return

        self.handler.raw += line

class New_Section_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
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

class Unknown_New_Section_1_TestCase(New_Section_TestCase):
    def runTest(self):
        # pykickstart doesn't understand the %raw section, and we've not
        # told it to ignore these errors.
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Unknown_New_Section_2_TestCase(New_Section_TestCase):
    def runTest(self):
        # pykickstart doesn't understand the %raw section, but we've told
        # it to ignore that.  There's not an "assertDoesntRaise" function,
        # so we just call it and if anything goes wrong it'll FAIL.
        self.parser.unknownSectionIsFatal = False
        self.assertWarns(KickstartParseWarning, self.parser.readKickstartFromString, self.ks)

class Ignored_Section_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%addon
whatever
%end

%anaconda
whatever2
%end
"""

    def runTest(self):
        # pykickstart recognizes these sections, but doesn't do anything with them.
        # Be as strict as possible by turning warnings into errors, to make sure we
        # don't even warn about them.
        warnings.simplefilter("error", category=KickstartParseWarning)
        self.parser.readKickstartFromString(self.ks)
        warnings.resetwarnings()

if __name__ == "__main__":
    unittest.main()
