import os
import sys
import unittest
import importlib
import unittest.mock as mock
from argparse import Namespace

from tests.baseclass import ParserTest
from pykickstart.parser import Script, KickstartParser
from pykickstart.version import F25
from pykickstart.handlers.f25 import F25Handler
from pykickstart.constants import KS_SCRIPT_POST
from pykickstart.errors import KickstartParseError
from pykickstart.commands.zfcp import F14_ZFCPData
from pykickstart.commands.autopart import F23_AutoPart
from pykickstart.commands.btrfs import F17_BTRFS, F23_BTRFS, F23_BTRFSData
from pykickstart.commands.cdrom import FC3_Cdrom
from pykickstart.base import BaseData, BaseHandler, DeprecatedCommand, KickstartCommand, \
    KickstartHandler


class KickstartCommandWithRemovals(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords + ["connect"]
    removedAttrs = KickstartCommand.removedAttrs + ["connect"]

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)

class KickstartCommandRemovedKeywords_TestCase(unittest.TestCase):
    @mock.patch('warnings.warn')
    def runTest(self, _warn):
        KickstartCommandWithRemovals(connect='test')
        self.assertEqual(_warn.call_count, 1)

        cmd = KickstartCommandWithRemovals()
        cmd.__call__(connect='test', missingAttr='test')
        self.assertFalse(hasattr(cmd, 'connect'))
        self.assertFalse(hasattr(cmd, 'missingAttr'))

class BaseDataWithRemovals(BaseData):
    removedKeywords = BaseData.removedKeywords + ["connect"]
    removedAttrs = BaseData.removedAttrs + ["connect"]

    def __init__(self, writePriority=0, *args, **kwargs):
        BaseData.__init__(self, writePriority, *args, **kwargs)

class BaseDataRemovedKeywords_TestCase(unittest.TestCase):
    @mock.patch('warnings.warn')
    def runTest(self, _warn):
        BaseDataWithRemovals(connect='test')
        self.assertEqual(_warn.call_count, 1)

        data = BaseDataWithRemovals()
        data.__call__(connect='test-me')
        self.assertFalse(hasattr(data, 'connect'))

class DeleteRemovedAttrs_TestCase(unittest.TestCase):
    """
        Test if self.deleteRemovedAttrs() has been called
        and that no removed attributes remain in the object.
    """
    def runTest(self):
        errors = []
        commands_dir = os.path.join(os.path.dirname(__file__), "..", "pykickstart", "commands")
        commands_dir = os.path.abspath(commands_dir)

        self.assertTrue(os.path.exists(commands_dir))
        if commands_dir not in sys.path:
            sys.path.append(commands_dir)

        for _dirpath, _dirnames, paths in os.walk(commands_dir):
            for path in paths:
                if path == '__init__.py' or not path.endswith('.py'):
                    continue

                # load the module defining all possible command implementations
                command_module = importlib.import_module(path.replace(".py", ""))

                for _impl_name, impl_class in command_module.__dict__.items():
                    # skip everything which isn't a class
                    if type(impl_class) is not type:
                        continue

                    # skip everything which doesn't inherit
                    # from KickstartCommand or BaseData
                    if not (issubclass(impl_class, KickstartCommand) or issubclass(impl_class, BaseData)):
                        continue

                    # skip base classes as well
                    if impl_class.__name__ in ['KickstartCommand', 'DeprecatedCommand']:
                        continue

                    if impl_class.removedAttrs:
                        cmd = impl_class()
                        for attr in cmd.removedAttrs:
                            if hasattr(cmd, attr):
                                errors.append("%s.%s not removed, execute self.deleteRemovedAttrs()!" %
                                              (impl_class.__name__, attr))

        self.assertEqual(errors, [])


class KickstartCommandNoParseMethod(KickstartCommand):
    """ The parse() method is not defined """

class TestDeprecatedCommand(DeprecatedCommand):
    pass

class TestBaseData(BaseData):
    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.testAttr = kwargs.get('testAttr', '')

class BaseClasses_TestCase(ParserTest):
    def runTest(self):
        # fail - can't instantiate these directly
        self.assertRaises(TypeError, KickstartCommand, (100, ))
        self.assertRaises(TypeError, DeprecatedCommand, (100, ))
        self.assertRaises(TypeError, BaseHandler, (100, ))
        self.assertRaises(TypeError, BaseData, (100, ))

        cmd = KickstartCommandNoParseMethod()
        self.assertEqual(cmd.dataList(), None)
        self.assertEqual(cmd.dataClass, None)
        with self.assertRaises(TypeError):
            cmd.parse(['test'])

        with mock.patch('warnings.warn') as _warn:
            cmd._setToSelf(Namespace())
            self.assertEqual(_warn.call_count, 1)

        with mock.patch('warnings.warn') as _warn:
            cmd._setToObj(Namespace(), cmd)
            self.assertEqual(_warn.call_count, 1)

        dep_cmd = TestDeprecatedCommand()
        self.assertEqual(dep_cmd.__str__(), '')
        with mock.patch('warnings.warn') as _warn:
            dep_cmd.parse(['test'])
            self.assertEqual(_warn.call_count, 1)


        self.assertEqual(TestBaseData().__str__(), '')

        data = TestBaseData()
        data.__call__(testAttr='test-me', missingAttr='missing')
        self.assertEqual(data.testAttr, 'test-me')
        self.assertFalse(hasattr(data, 'missingAttr'))

class KickstartHandler_TestCase(unittest.TestCase):
    def runTest(self):
        handler = KickstartHandler()
        self.assertEqual(str(handler), "")

        handler = KickstartHandler()
        handler.registerCommand('autopart', F23_AutoPart)
        handler.registerCommand('btrfs', F17_BTRFS)
        handler.registerData('BTRFSData', F23_BTRFSData)
        handler.registerData('ZFCPData', F14_ZFCPData)

        self.assertEqual(len(handler.commands.keys()), 2)
        self.assertTrue(isinstance(handler.commands['autopart'], F23_AutoPart))
        self.assertTrue(isinstance(handler.commands['btrfs'], F17_BTRFS))

        self.assertTrue(hasattr(handler, 'BTRFSData'))
        self.assertEqual(getattr(handler, 'BTRFSData'), F23_BTRFSData)
        self.assertTrue(hasattr(handler, 'ZFCPData'))
        self.assertEqual(getattr(handler, 'ZFCPData'), F14_ZFCPData)

        handler = KickstartHandler()
        handler.registerCommand('cdrom', FC3_Cdrom)
        handler.version = F25

        parser = KickstartParser(handler)
        parser.readKickstartFromString("cdrom")
        self.assertEqual(str(handler), "# Use CDROM installation media\ncdrom\n")

class HandlerRegisterCommands_TestCase(unittest.TestCase):
    def runTest(self):
        handler = F25Handler(mapping={
                                'autopart': F23_AutoPart,
                                'btrfs': F23_BTRFS,
                             },
                             dataMapping={
                                'BTRFSData': F23_BTRFSData,
                                'ZFCPData': None,
                             },
                             commandUpdates={
                                'btrfs': F17_BTRFS,
                             },
                             dataUpdates={
                                'ZFCPData': F14_ZFCPData,
                             })
        self.assertEqual(len(handler.commands.keys()), 2)
        self.assertTrue(isinstance(handler.commands['autopart'], F23_AutoPart))
        self.assertTrue(isinstance(handler.commands['btrfs'], F17_BTRFS))

        self.assertTrue(hasattr(handler, 'BTRFSData'))
        self.assertEqual(getattr(handler, 'BTRFSData'), F23_BTRFSData)
        self.assertTrue(hasattr(handler, 'ZFCPData'))
        self.assertEqual(getattr(handler, 'ZFCPData'), F14_ZFCPData)


class HandlerString_TestCase(ParserTest):
    def runTest(self):
        self.handler.platform = "x86_64"
        self.assertIn("#platform=x86_64", str(self.handler))

        self.handler.platform = ""
        self.assertNotIn("#platform", str(self.handler))

        self.handler.scripts.append(Script("echo Hello", type=KS_SCRIPT_POST))
        self.assertIn("echo Hello", str(self.handler))

class HandlerResetCommand_TestCase(ParserTest):
    def runTest(self):
        # fail - tried to reset a command that doesn't exist
        self.assertRaises(KeyError, self.handler.resetCommand, "fakecommand")

        # might as well test this way of getting the same information, while we're at it
        self.assertFalse(self.handler.hasCommand("fakecommand"))

        # Set some attributes on a command (both by calling the command and by setting them
        # directly), verify they're set, then reset it and verify they're gone.
        self.handler.autopart(autopart=True, encrypted=True, passphrase="something")
        self.handler.autopart.cipher = "whatever"
        self.handler.autopart.bogus = True

        self.assertTrue(self.handler.autopart.autopart)
        self.assertEqual(self.handler.autopart.cipher, "whatever")
        self.assertTrue(self.handler.autopart.encrypted)
        self.assertEqual(self.handler.autopart.passphrase, "something")
        self.assertTrue(self.handler.autopart.bogus)
        self.assertTrue("autopart" in str(self.handler))

        self.handler.resetCommand("autopart")
        self.assertFalse(self.handler.autopart.autopart)
        self.assertEqual(self.handler.autopart.cipher, "")
        self.assertFalse(self.handler.autopart.encrypted)
        self.assertEqual(self.handler.autopart.passphrase, "")
        self.assertNotIn("bogus", self.handler.autopart.__dict__)
        self.assertFalse("autopart" in str(self.handler))

class HandlerDispatch_TestCase(ParserTest):
    def runTest(self):
        # fail - no such command
        self.assertRaises(KickstartParseError, self.handler.dispatcher, ["fakecommand"], 1)

        # pass - parses a valid kickstart
        self.handler.dispatcher(['autopart'], 1)
        self.assertTrue(self.handler.autopart.seen)

        self.handler.dispatcher(['network', '--device', 'eth0'], 1)
        self.assertEqual(self.handler.network.dataList()[0].device, 'eth0')


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
