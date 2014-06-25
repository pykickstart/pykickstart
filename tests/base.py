import unittest
from tests.baseclass import ParserTest

from pykickstart.base import *
from pykickstart.version import *

class BaseClasses_TestCase(ParserTest):
    def runTest(self):
        # fail - can't instantiate these directly
        self.assertRaises(TypeError, KickstartCommand, (100, ))
        self.assertRaises(TypeError, DeprecatedCommand, (100, ))
        self.assertRaises(TypeError, BaseHandler, (100, ))
        self.assertRaises(TypeError, BaseData, (100, ))

class HandlerString_TestCase(ParserTest):
    def runTest(self):
        self.handler.platform = "x86_64"
        self.assertIn("#platform=x86_64", str(self.handler))

class HandlerResetCommand_TestCase(ParserTest):
    def runTest(self):
        # fail - tried to reset a command that doesn't exist
        self.assertRaises(KeyError, self.handler.resetCommand, "fakecommand")

        # might as well test this way of getting the same information, while we're at it
        self.assertFalse(self.handler.hasCommand("fakecommand"))

        # Set some attributes on a command, then reset it and verify they're gone.
        self.handler.autopart.autopart = True
        self.handler.autopart.cipher = "whatever"
        self.handler.autopart.encrypted = True
        self.handler.autopart.passphrase = "something"
        self.handler.autopart.bogus = True

        self.handler.resetCommand("autopart")
        self.assertFalse(self.handler.autopart.autopart)
        self.assertEqual(self.handler.autopart.cipher, "")
        self.assertFalse(self.handler.autopart.encrypted)
        self.assertEqual(self.handler.autopart.passphrase, "")
        self.assertNotIn("bogus", self.handler.autopart.__dict__)

class HandlerDispatch_TestCase(ParserTest):
    def runTest(self):
        # fail - no such command
        self.assertRaises(KickstartParseError, self.handler.dispatcher, ["fakecommand"], 1)

class HandlerMask_TestCase(ParserTest):
    def runTest(self):
        # First, verify all commands are set to something other than None.  This means
        # the command can be called.
        for cmd in self.handler.commands:
            self.assertIsNotNone(self.handler.commands[cmd])

        # Now blank out most commands except the one or two we're actually interested
        # in.  This has the effect of making the other commands recognized, but calling
        # them will have no effect on data.
        lst = ["rootpw", "user", "group"]

        self.handler.maskAllExcept(lst)
        for cmd in self.handler.commands:
            if cmd in lst:
                self.assertIsNotNone(self.handler.commands[cmd])
            else:
                self.assertIsNone(self.handler.commands[cmd])

        # These attributes should still be set to their defaults.
        self.handler.dispatcher(["autopart", "--encrypted", "--passphrase", "something"], 1)
        self.assertFalse(self.handler.autopart.encrypted)
        self.assertEqual(self.handler.autopart.passphrase, "")

if __name__ == "__main__":
    unittest.main()
