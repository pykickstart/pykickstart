import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.selinux import *
#from pykickstart.base import *
#from pykickstart.options import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("selinux")
        self.assert_parse("selinux --permissive", "selinux --permissive\n")
        self.assert_parse("selinux --enforcing", "selinux --enforcing\n")
        self.assert_parse("selinux --disabled", "selinux --disabled\n")

        # fail
        self.assert_parse_error("selinux --cheese")
        self.assert_parse_error("selinux --crackers=CRUNCHY")

if __name__ == "__main__":
    unittest.main()
