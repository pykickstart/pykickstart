import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.updates import *
#from pykickstart.base import *
#from pykickstart.options import *

class F7_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("updates", "updates\n")
        self.assert_parse("updates deliciouscheeses", "updates deliciouscheeses\n")

	# fail
	self.assert_parse_error("updates cheese crackers", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
