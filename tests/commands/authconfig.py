import unittest

from pykickstart.errors import KickstartDeprecationWarning
from tests.baseclass import CommandTest


class FC3_TestCase(CommandTest):
    command = "authconfig"

    def runTest(self):
        # pass
        self.assert_parse("authconfig")
        self.assert_parse("authconfig --cheese", "auth --cheese\n")
        self.assert_parse("authconfig --cracker=CRUNCHY", "auth --cracker=CRUNCHY\n")
        self.assert_parse("auth")
        self.assert_parse("auth --cheese", "auth --cheese\n")
        self.assert_parse("auth --cracker=CRUNCHY", "auth --cracker=CRUNCHY\n")


class F28_TestCase(FC3_TestCase):

    def runTest(self):
        super().runTest()

        with self.assertWarns(KickstartDeprecationWarning):
            self.assert_parse("authconfig")

        with self.assertWarns(KickstartDeprecationWarning):
            self.assert_parse("auth")


if __name__ == "__main__":
    unittest.main()
