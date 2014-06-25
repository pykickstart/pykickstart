import unittest
from tests.baseclass import ParserTest

from pykickstart.errors import *

class NoErrorMessage_TestCase(ParserTest):
    def runTest(self):
        # For now, just verify that calling formatErrorMsg with no message
        # returns something.  Digging in and checking what the message is
        # when we could be running "make check" in another language is hard.
        self.assertNotEqual(formatErrorMsg(47), "")

class ExceptionStr_TestCase(ParserTest):
    def runTest(self):
        # Yes, I am aware I'm just checking off boxes now.
        self.assertEqual(str(KickstartError("OH NO!")), "OH NO!")
        self.assertEqual(str(KickstartParseError("OH NO!")), "OH NO!")
        self.assertEqual(str(KickstartValueError("OH NO!")), "OH NO!")
        self.assertEqual(str(KickstartVersionError("OH NO!")), "OH NO!")

if __name__ == "__main__":
    unittest.main()
