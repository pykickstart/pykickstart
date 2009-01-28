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
        self.assert_parse("clearpart")
        self.assert_parse("clearpart --all", "clearpart --all  \n")
        # Passing multiple competing type options should accept only the last one
        self.assert_parse("clearpart --linux --none --all", "clearpart --all  \n")
        # Setting --initlabel or --drives without a type option should 'fail'
        self.assert_parse("clearpart --initlabel", "")
        self.assert_parse("clearpart --drives sda", "")

        self.assert_parse("clearpart --all --initlabel", "clearpart --all --initlabel \n")
        self.assert_parse("clearpart --all --drives sda", "clearpart --all  --drives=sda\n")
        self.assert_parse("clearpart --all --drives sda,sdb", "clearpart --all  --drives=sda,sdb\n")
        self.assert_parse("clearpart --all --drives=sda", "clearpart --all  --drives=sda\n")
        self.assert_parse("clearpart --all --drives=sda,sdb", "clearpart --all  --drives=sda,sdb\n")
        # Big Everything Test
        self.assert_parse("clearpart --drives=sda,sdb --all --linux --initlabel", "clearpart --linux --initlabel --drives=sda,sdb\n")

        # fail
        # initlabel should not take a value
        self.assert_parse_error("clearpart --initlabel=foo")
        # drives must take a value
        self.assert_parse_error("clearpart --all --drives")
        # nonsensical parameter test
        self.assert_parse_error("clearpart --cheese")

if __name__ == "__main__":
    unittest.main()
