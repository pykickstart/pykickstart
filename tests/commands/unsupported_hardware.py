import unittest
from tests.baseclass import CommandTest
from pykickstart.commands.unsupported_hardware import RHEL6_UnsupportedHardware

class RHEL6_TestCase(CommandTest):
    command = "unsupported_hardware"

    def runTest(self):
        # pass
        self.assert_parse("unsupported_hardware",
                          "unsupported_hardware\n")

        # fail
        self.assert_parse_error("unsupported_hardware --cheese")
        self.assert_parse_error("unsupported_hardware cheese")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.unsupported_hardware = False
        self.assertEqual(cmd.__str__(), "")

class Unsupported_Hardware_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = RHEL6_UnsupportedHardware()
        self.assertEqual(cmd.unsupported_hardware, False)

if __name__ == "__main__":
    unittest.main()
