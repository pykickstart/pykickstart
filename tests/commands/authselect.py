import unittest
from tests.baseclass import CommandTest


class F28_TestCase(CommandTest):
    command = "authselect"

    def runTest(self):
        # pass
        self.assert_parse("authselect")

        self.assert_parse("authselect select winbind",
                          "authselect select winbind\n")

        self.assert_parse("authselect select sssd with-mkhomedir",
                          "authselect select sssd with-mkhomedir\n")


if __name__ == "__main__":
    unittest.main()
