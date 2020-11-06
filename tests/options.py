from argparse import ArgumentTypeError
from tests.baseclass import ParserTest

from pykickstart.options import ksboolean, mountpoint, uid_gid

class Ksboolean_TestCase(ParserTest):
    def runTest(self):
        self.assertTrue(ksboolean("ON"))
        self.assertTrue(ksboolean("On"))
        self.assertTrue(ksboolean("YES"))
        self.assertTrue(ksboolean("Yes"))
        self.assertTrue(ksboolean("TRUE"))
        self.assertTrue(ksboolean("True"))
        self.assertTrue(ksboolean("1"))

        self.assertFalse(ksboolean("OFF"))
        self.assertFalse(ksboolean("Off"))
        self.assertFalse(ksboolean("NO"))
        self.assertFalse(ksboolean("No"))
        self.assertFalse(ksboolean("FALSE"))
        self.assertFalse(ksboolean("False"))
        self.assertFalse(ksboolean("0"))

        self.assertRaises(ArgumentTypeError, ksboolean, True)
        self.assertRaises(ArgumentTypeError, ksboolean, False)
        self.assertRaises(ArgumentTypeError, ksboolean, "YesSir")
        self.assertRaises(ArgumentTypeError, ksboolean, "NoWay")
        self.assertRaises(ArgumentTypeError, ksboolean, None)
        self.assertRaises(ArgumentTypeError, ksboolean, [])
        self.assertRaises(ArgumentTypeError, ksboolean, {})


class Mountpoint_TestCase(ParserTest):
    def runTest(self):
        self.assertEqual(mountpoint("none"), "none")
        self.assertEqual(mountpoint("swap"), "swap")
        self.assertEqual(mountpoint("/"), "/")
        self.assertEqual(mountpoint("/home"), "/home")
        self.assertEqual(mountpoint("/home/"), "/home")
        self.assertEqual(mountpoint("/var"), "/var")
        self.assertEqual(mountpoint("/var/"), "/var")


class Uid_gid_TestCase(ParserTest):
    def runTest(self):
        self.assertEqual(uid_gid("1"), 1)
        self.assertEqual(uid_gid("1000"), 1000)
        self.assertEqual(uid_gid("4294967295"), 4294967295)

        self.assertRaises(ArgumentTypeError, uid_gid, "-1")
        self.assertRaises(ArgumentTypeError, uid_gid, "0")
        self.assertRaises(ArgumentTypeError, uid_gid, "4294967296")

        self.assertRaises(ArgumentTypeError, uid_gid, "abc")
        self.assertRaises(ArgumentTypeError, uid_gid, "")
        self.assertRaises(ArgumentTypeError, uid_gid, None)
