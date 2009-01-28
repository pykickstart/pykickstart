import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.authconfig import *
#from pykickstart.base import *
#from pykickstart.options import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("lang en_US", "lang en_US\n")

        # fail
        # Fail if less than or more than one argument is specified
        self.assert_parse_error("lang", KickstartValueError)
        self.assert_parse_error("lang en_US en_CA", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
