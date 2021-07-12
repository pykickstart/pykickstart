import unittest

from pykickstart.base import RemovedCommand
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


class F35_TestCase(F28_TestCase):

    def runTest(self):
        # make sure that auth is removed
        cmd = self.handler().commands["auth"]
        self.assertTrue(issubclass(cmd.__class__, RemovedCommand))

        # make sure that authconfig is removed
        cmd = self.handler().commands["authconfig"]
        self.assertTrue(issubclass(cmd.__class__, RemovedCommand))


if __name__ == "__main__":
    unittest.main()
