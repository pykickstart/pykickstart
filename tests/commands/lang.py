import unittest
from tests.baseclass import CommandTest

from pykickstart.errors import KickstartValueError

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
    def runTest(self):

        # pass
        self.assert_parse("lang en_US")
        self.assert_parse("lang en_US --addsupport=cs_CZ",
                          "lang en_US --addsupport=cs_CZ\n")
        self.assert_parse("lang en_US --addsupport=sr_RS.UTF-8@latin",
                          "lang en_US --addsupport=sr_RS.UTF-8@latin\n")
        self.assert_parse("lang en_US --addsupport=cs_CZ,fr_FR",
                          "lang en_US --addsupport=cs_CZ,fr_FR\n")

        # fail
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang", KickstartValueError)
        self.assert_parse_error("lang en_US en_CA", KickstartValueError)
        self.assert_parse_error("lang --addsupport=en_US", KickstartValueError)
        self.assert_parse_error("lang --addsupport=,bg_BG", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
