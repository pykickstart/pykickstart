import warnings

from tests.baseclass import ParserTest

from pykickstart.errors import KickstartDeprecationWarning
from pykickstart.parser import KickstartParser
from pykickstart.version import makeVersion, F33


class TracebackScriptSection_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = "\n%traceback\n%end\n"

    def runTest(self):

        # F33 has no warnings
        handler = makeVersion(version=F33)
        parser = KickstartParser(handler)
        with warnings.catch_warnings(record=True) as w:
            parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 0)

        # F34 warns about deprecation
        with self.assertWarns(KickstartDeprecationWarning):
            self.parser.readKickstartFromString(self.ks)
