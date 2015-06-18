from tests.baseclass import *

class FC3_TestCase(CommandTest):
    command = "clearpart"

    def runTest(self):
        # pass
        self.assert_parse("clearpart")
        self.assert_parse("clearpart --all", "clearpart --all\n")
        self.assert_parse("clearpart --none", "clearpart --none\n")
        # Passing multiple competing type options should accept only the last one
        self.assert_parse("clearpart --linux --none --all", "clearpart --all\n")
        # Setting --initlabel or --drives without a type option should 'fail'
        self.assert_parse("clearpart --initlabel", "")
        self.assert_parse("clearpart --drives sda", "")

        self.assert_parse("clearpart --all --initlabel", "clearpart --all --initlabel\n")
        self.assert_parse("clearpart --all --drives sda", "clearpart --all --drives=sda\n")
        self.assert_parse("clearpart --all --drives sda,sdb", "clearpart --all --drives=sda,sdb\n")
        self.assert_parse("clearpart --all --drives=sda", "clearpart --all --drives=sda\n")
        self.assert_parse("clearpart --all --drives=sda,sdb", "clearpart --all --drives=sda,sdb\n")
        # Big Everything Test
        self.assert_parse("clearpart --drives=sda,sdb --all --linux --initlabel", "clearpart --linux --initlabel --drives=sda,sdb\n")

        # fail
        # initlabel should not take a value
        self.assert_parse_error("clearpart --initlabel=foo")
        # drives must take a value
        self.assert_parse_error("clearpart --all --drives")
        # nonsensical parameter test
        self.assert_parse_error("clearpart --cheese")

class F17_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)
        self.assert_parse("clearpart --list=sda2,sda3,disk/by-label/foo",
                          "clearpart --list=sda2,sda3,disk/by-label/foo\n")

class F21_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)
        self.assert_parse("clearpart --all --initlabel --disklabel=gpt",
                          "clearpart --all --initlabel --disklabel=gpt\n")
        self.assert_parse_error("clearpart --all --disklabel")

        self.assert_parse("clearpart --all --cdl", "clearpart --all --cdl  \n")
        self.assert_parse("clearpart --all --cdl --drives=dasda,dasdb,dasdc", "clearpart --all --cdl --drives=dasda,dasdb,dasdc \n")

        # cdl should not take a value
        self.assert_parse_error("clearpart --cdl=foo")

if __name__ == "__main__":
    unittest.main()
