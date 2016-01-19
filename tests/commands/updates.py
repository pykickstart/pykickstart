import unittest
from tests.baseclass import CommandTest

class F7_TestCase(CommandTest):
    command = "updates"

    def runTest(self):
        # pass
        self.assert_parse("updates", "updates\n")
        self.assert_parse("updates deliciouscheeses", "updates deliciouscheeses\n")

        # fail
        self.assert_parse_error("updates cheese crackers")
        self.assert_parse_error("updates --bogus-option")

if __name__ == "__main__":
    unittest.main()
