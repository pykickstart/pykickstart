import unittest
import warnings

from pykickstart.parser import KickstartParser
from pykickstart.version import makeVersion
from tests.baseclass import ParserTest
from pykickstart.handlers import control
from pykickstart.base import DeprecatedCommand, RemovedCommand
from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning


class Platform_Comment_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
#platform=x86_64
autopart
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(self.handler.platform, "x86_64")

class WritePriority_TestCase(unittest.TestCase):
    def runTest(self):
        for _version, _map in control.commandMap.items():
            for _name, command_class in _map.items():
                cmd = command_class()
                if issubclass(cmd.__class__, DeprecatedCommand):
                    self.assertEqual(None, cmd.writePriority, command_class)
                elif issubclass(cmd.__class__, RemovedCommand):
                    self.assertEqual(None, cmd.writePriority, command_class)
                elif _name in ['bootloader', 'lilo', 'zipl']:
                    self.assertEqual(10, cmd.writePriority, command_class)
                elif _name in ['multipath']:
                    self.assertEqual(50, cmd.writePriority, command_class)
                elif _name in ['dmraid']:
                    self.assertEqual(60, cmd.writePriority, command_class)
                elif _name in ['iscsiname']:
                    self.assertEqual(70, cmd.writePriority, command_class)
                elif _name in ['fcoe', 'zfcp', 'iscsi']:
                    self.assertEqual(71, cmd.writePriority, command_class)
                elif _name in ['nvdimm']:
                    self.assertEqual(80, cmd.writePriority, command_class)
                elif _name in ['autopart', 'reqpart']:
                    self.assertEqual(100, cmd.writePriority, command_class)
                elif _name in ['zerombr']:
                    self.assertEqual(110, cmd.writePriority, command_class)
                elif _name in ['clearpart']:
                    self.assertEqual(120, cmd.writePriority, command_class)
                elif _name in ['partition', 'part']:
                    self.assertEqual(130, cmd.writePriority, command_class)
                elif _name in ['raid']:
                    self.assertEqual(131, cmd.writePriority, command_class)
                elif _name in ['volgroup', 'btrfs', 'stratispool']:
                    self.assertEqual(132, cmd.writePriority, command_class)
                elif _name in ['logvol', 'stratisfs']:
                    self.assertEqual(133, cmd.writePriority, command_class)
                elif _name in ['snapshot']:
                    self.assertEqual(140, cmd.writePriority, command_class)
                else:
                    self.assertEqual(0, cmd.writePriority, command_class)

class DeprecatedCommandsParsing_TestCase(unittest.TestCase):
    def runTest(self):
        for version, command_map in control.commandMap.items():

            handler = makeVersion(version)
            parser = KickstartParser(handler)

            for command_name, command_class in command_map.items():
                if not issubclass(command_class, DeprecatedCommand):
                    continue
                if issubclass(command_class, RemovedCommand):
                    continue

                with warnings.catch_warnings(record=True):
                    # The deprecated commands should be ignored with
                    # a warning when they are parsed. Make sure that
                    # they will not cause any errors.
                    with self.assertWarns(KickstartDeprecationWarning) as cm:
                        parser.readKickstartFromString(command_name)

                    # Check the warning message.
                    expected = " {} command has been deprecated ".format(command_name)
                    self.assertIn(expected, str(cm.warning))

class RemovedCommandsParsing_TestCase(unittest.TestCase):
    def runTest(self):
        for version, command_map in control.commandMap.items():

            handler = makeVersion(version)
            parser = KickstartParser(handler)

            for command_name, command_class in command_map.items():
                if not issubclass(command_class, RemovedCommand):
                    continue

                # Make sure that using the removed command raises an error
                with self.assertRaises(KickstartParseError):
                    parser.readKickstartFromString(command_name)

class ClosingQuote_TestCase(ParserTest):
    """Missing closing quotes should raise a ValueError"""
    def runTest(self):
        self.assert_parse_error('autopart --passphrase="lots of words', ValueError)


if __name__ == "__main__":
    unittest.main()
