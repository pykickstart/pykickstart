import unittest
from tests.baseclass import CommandTest
from pykickstart.commands.lang import FC3_Lang, F19_Lang

class Lang_TestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(FC3_Lang().__str__(), '')
        self.assertEqual(F19_Lang().__str__(), '')


class FC3_TestCase(CommandTest):
    command = "lang"

    def runTest(self):
        # pass
        self.assert_parse("lang en_US", "lang en_US\n")

        # fail
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang")
        self.assert_parse_error("lang en_US en_CA")
        self.assert_parse_error("lang --whatever")


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
        self.assert_parse_error("lang --bogus-option")
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang")
        self.assert_parse_error("lang en_US en_CA")
        self.assert_parse_error("lang --addsupport=en_US")
        self.assert_parse_error("lang --addsupport=,bg_BG")

if __name__ == "__main__":
    unittest.main()
