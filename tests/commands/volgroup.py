import unittest
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.volgroup import FC3_VolGroupData, F21_VolGroupData
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.version import FC3

class VolGroup_TestCase(unittest.TestCase):
    def runTest(self):
        data1 = FC3_VolGroupData()
        data2 = FC3_VolGroupData()

        # test default object values
        self.assertEqual(data1.format, True)
        self.assertEqual(data1.pesize, 32768)
        self.assertEqual(data1.preexist, False)

        self.assertEqual(F21_VolGroupData().pesize, 0)

        # test that new objects are always equal
        self.assertEqual(data1, data2)
        self.assertNotEqual(data1, None)

        # test for objects difference
        for atr in ['vgname']:
            setattr(data1, atr, '')
            setattr(data2, atr, 'test')
            # objects that differ in only one attribute
            # are not equal
            self.assertNotEqual(data1, data2)
            self.assertNotEqual(data2, data1)
            setattr(data1, atr, '')
            setattr(data2, atr, '')


class FC3_TestCase(CommandTest):
    command = "volgroup"

    def runTest(self):
        if self.__class__ in (FC3_TestCase, F16_TestCase, RHEL6_TestCase):
            def_pesize_str = " --pesize=32768"
        else:
            def_pesize_str = ""

        # --noformat
        self.assert_parse("volgroup vg.01 --noformat",
                          "volgroup vg.01 --noformat%s --useexisting\n" % def_pesize_str)
        # --useexisting
        self.assert_parse("volgroup vg.01 --useexisting",
                          "volgroup vg.01%s --useexisting\n" % def_pesize_str)

        # --pesize
        self.assert_parse("volgroup vg.01 pv.01 --pesize=70000",
                          "volgroup vg.01 --pesize=70000 pv.01\n")

        # assert data types
        self.assert_type("volgroup", "pesize", "int")
        self.assert_type("volgroup", "format", "boolean")
        self.assert_type("volgroup", "preexist", "boolean")

        self.assertFalse(self.assert_parse("volgroup vg.01 pv.01") is None)
        self.assertTrue(self.assert_parse("volgroup vg.01 pv.01") !=
                        self.assert_parse("volgroup vg.02 pv.01"))
        self.assertFalse(self.assert_parse("volgroup vg.01 pv.01") ==
                         self.assert_parse("volgroup vg.02 pv.01"))

        # fail - incorrect type
        self.assert_parse_error("volgroup vg.01 pv.01 --pesize=SIZE")

        # fail - missing name
        self.assert_parse_error("volgroup")

        # fail - missing list of partitions
        self.assert_parse_error("volgroup vg01")

        # fail - both members and useexisting specified
        self.assert_parse_error("volgroup vg.01 pv.01 pv.02 --useexisting")
        self.assert_parse_error("volgroup vg.01 --useexisting pv.01 pv.02")

        # fail - invalid argument
        self.assert_parse_error("volgroup --bogus-option")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.vgList = ["vg.01"]
        self.assertEqual(cmd.__str__(), "vg.01")

class FC3_Duplicate_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = FC3

    def runTest(self):
        self.assert_parse("""
volgroup vg.01 pv.01
volgroup vg.02 pv.01""")

        self.assert_parse_error("""
volgroup vg.01 pv.01
volgroup vg.01 pv.02""", KickstartParseWarning)

class F16_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        if self.__class__ in (FC3_TestCase, F16_TestCase, RHEL6_TestCase):
            def_pesize_str = " --pesize=32768"
        else:
            def_pesize_str = ""

        # Pass - correct usage.
        self.assert_parse("volgroup vg.01 pv.01 --reserved-space=1000",
                          "volgroup vg.01%s --reserved-space=1000 pv.01\n" % def_pesize_str)
        self.assert_parse("volgroup vg.01 pv.01 --reserved-percent=50",
                          "volgroup vg.01%s --reserved-percent=50 pv.01\n" % def_pesize_str)

        # Fail - missing required argument.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space")
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent")

        # Fail - incorrect values.
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-space=-1")
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=0")
        self.assert_parse_error("volgroup vg.01 pv.01 --reserved-percent=100")

class RHEL6_TestCase(F16_TestCase):
    def runTest(self):
        F16_TestCase.runTest(self)
        # extra test coverage
        cmd = self.handler().commands[self.command]
        cmd.parse(["volgroup", "vg.02", "pv.01"])
        self.assertEqual(cmd.__str__(), "")
        cmd.handler.autopart.seen = True
        with self.assertRaises(KickstartParseError):
            cmd.parse(["volgroup", "vg.02", "pv.01"])
        cmd.handler.autopart.seen = False

class F21_TestCase(F16_TestCase):
    def runTest(self):
        # just run all the old tests with the new class (different PE size
        # default)
        F16_TestCase.runTest(self)

class RHEL7_TestCase(F16_TestCase):
    def runTest(self):
        F16_TestCase.runTest(self)

if __name__ == "__main__":
    unittest.main()
