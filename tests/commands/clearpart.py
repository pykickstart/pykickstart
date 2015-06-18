import unittest
from tests.baseclass import CommandTest
from pykickstart.commands.clearpart import FC3_ClearPart

class FC3_TestCase(CommandTest):
    command = "clearpart"

    def runTest(self):
        cmd = FC3_ClearPart()
        self.assertFalse(cmd.initAll)

        cmd.type = -1 # invalid value, don't know what partitions to clear
        self.assertEqual(cmd.__str__(), "# Partition clearing information\nclearpart\n")

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

class F28_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)
        self.assert_parse("clearpart --all --cdl",
                          "clearpart --all --cdl\n")

        self.assert_parse("clearpart --all --drives=dasda,dasdb,dasdc --cdl",
                          "clearpart --all --drives=dasda,dasdb,dasdc --cdl\n")

        # cdl should not take a value
        self.assert_parse_error("clearpart --cdl=foo")

class RHEL7_TestCase(F28_TestCase):
    def runTest(self):
        F28_TestCase.runTest(self)


if __name__ == "__main__":
    unittest.main()
