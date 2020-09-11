from tools import ksshell
import unittest.mock as mock
from unittest import TestCase

from pykickstart.version import DEVEL, makeVersion


class InvalidKSVersion_Test(TestCase):
    @mock.patch('tools.ksshell.print')
    def runTest(self, _print):
        retval = ksshell.main(['-v', 'INVALID'])
        self.assertEqual(retval, 1)
        _print.assert_called_with('The version INVALID is not supported by pykickstart')

class KickstartCompleter_Test(TestCase):
    def runTest(self):
        kshandler = makeVersion(DEVEL)
        self.assertIsNotNone(kshandler)

        # Did it add the commands, and is there at least one (part) that should be present?
        ksc = ksshell.KickstartCompleter(kshandler, {})
        self.assertTrue(len(ksc.commands) > 0)
        self.assertIn("part", ksc.commands)

        # Test tab completion on 'part [TAB]'
        # Initialize the matches with a mocked input line
        ksc._init_matches("part ", 5, 5)
        self.assertEqual(ksc.complete("", 1), "--fstype")

        # Test tab completion on 'auth[TAB]'
        ksc._init_matches("auth", 0, 5)

        # Python 3.5 returns things in a different order, just make sure they are there and different
        self.assertIn(ksc.complete("", 1), ["auth", "authconfig", "authselect"])
        self.assertIn(ksc.complete("", 2), ["auth", "authconfig", "authselect"])
        self.assertNotEqual(ksc.complete("", 1), ksc.complete("", 2))
