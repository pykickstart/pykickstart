import unittest
from tests.baseclass import CommandTest
from pykickstart.commands.vnc import FC3_Vnc

class Vnc_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = FC3_Vnc()
        self.assertEqual(cmd.enabled, False)

class FC3_TestCase(CommandTest):
    command = "vnc"

    def runTest(self):
        obj = self.assert_parse("vnc", "vnc\n")
        obj.enabled = False
        self.assertEqual(str(obj), "")

        # pass
        self.assert_parse("vnc --connect=HOSTNAME", "vnc --connect=HOSTNAME\n")
        self.assert_parse("vnc --connect=HOSTNAME:PORT", "vnc --connect=HOSTNAME:PORT\n")
        self.assert_parse("vnc --password=PASSWORD", "vnc --password=PASSWORD\n")
        self.assert_parse("vnc --connect=HOSTNAME --password=PASSWORD", "vnc --connect=HOSTNAME --password=PASSWORD\n")

        # fail
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

class FC6_TestCase(CommandTest):
    command = "vnc"

    def runTest(self):
        # pass
        self.assert_parse("vnc", "vnc\n")
        self.assert_parse("vnc --host=HOSTNAME", "vnc --host=HOSTNAME\n")
        self.assert_parse("vnc --port=PORT", "vnc\n")
        self.assert_parse("vnc --password=PASSWORD", "vnc --password=PASSWORD\n")

        if "--connect" in self.optionList:
            self.assert_parse("vnc --connect=HOSTNAME", "vnc --host=HOSTNAME\n")
            self.assert_parse("vnc --connect=HOSTNAME:PORT", "vnc --host=HOSTNAME --port=PORT\n")
            self.assert_parse("vnc --connect=HOSTNAME --password=PASSWORD", "vnc --host=HOSTNAME --password=PASSWORD\n")
            self.assert_parse("vnc --connect=HOSTNAME:PORT --password=PASSWORD", "vnc --host=HOSTNAME --port=PORT --password=PASSWORD\n")

        # Ensure --connect has been deprecated
        self.assert_deprecated("vnc", "connect")

        # fail
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

class F9_TestCase(FC6_TestCase):
    def runTest(self):
        FC6_TestCase.runTest(self)

        # Ensure --connect has been removed
        self.assert_removed("vnc", "connect")

        # Any --connect use should raise KickstartParseError
        self.assert_parse_error("vnc --host=HOSTNAME --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --host=HOSTNAME --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --connect=HOSTNAME")
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

if __name__ == "__main__":
    unittest.main()
