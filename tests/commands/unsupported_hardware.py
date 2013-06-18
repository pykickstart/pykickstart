import unittest
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.unsupported_hardware import *

class RHEL6_TestCase(CommandTest):
    command = "unsupported_hardware"

    def runTest(self):
        # pass
        self.assert_parse("unsupported_hardware")

        # fail
        self.assert_parse_error("unsupported_hardware --cheese")

if __name__ == "__main__":
    unittest.main()
