import unittest
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.authconfig import *

class FC3_TestCase(CommandTest):
    command = "lang"

    def runTest(self):
        # pass
        self.assert_parse("lang en_US", "lang en_US\n")

        # fail
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang", KickstartValueError)
        self.assert_parse_error("lang en_US en_CA", KickstartValueError)

class F19_TestCase(FC3_TestCase):
    command = "lang"

    def runTest(self):

        # pass
        self.assert_parse("lang en_US")
        self.assert_parse("lang en_US --addsupport=cs_CZ")
        self.assert_parse("lang en_US --addsupport=sr_RS.UTF-8@latin")
        self.assert_parse("lang en_US --addsupport=cs_CZ,fr_FR")

        # fail
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang", KickstartValueError)
        self.assert_parse_error("lang en_US en_CA", KickstartValueError)
        self.assert_parse_error("lang --addsupport=en_US", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
