import unittest
from tests.baseclass import ParserTest
from pykickstart.handlers import control
from pykickstart.base import DeprecatedCommand

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
                elif _name in ['installclass']:
                    self.assertEqual(-1, cmd.writePriority, command_class)
                elif _name in ['rescue', 'upgrade', 'group', 'driverdisk', 'xconfig',
                    'keyboard', 'rootpw', 'url', 'lang', 'liveimg', 'method', 'realm',
                    'user', 'eula', 'firewall', 'ostreesetup', 'repo', 'sshkey', 'reboot',
                    'timezone', 'network', 'sshpw', 'updates', 'device', 'vnc', 'authconfig',
                    'autostep', 'cdrom', 'deviceprobe', 'text', 'graphical', 'firstboot', 'harddrive',
                    'selinux', 'skipx', 'mediacheck', 'logging', 'nfs', 'services', 'ignoredisk',
                    'interactive', 'cmdline', 'monitor', 'install', 'shutdown', 'halt',
                    'auth', 'poweroff', 'lilocheck', 'langsupport', 'mouse', 'key',
                    'unsupported_hardware']:
                    self.assertEqual(0, cmd.writePriority, command_class)
                elif _name in ['bootloader', 'lilo']:
                    self.assertEqual(10, cmd.writePriority, command_class)
                elif _name in ['multipath']:
                    self.assertEqual(50, cmd.writePriority, command_class)
                elif _name in ['dmraid']:
                    self.assertEqual(60, cmd.writePriority, command_class)
                elif _name in ['iscsiname']:
                    self.assertEqual(70, cmd.writePriority, command_class)
                elif _name in ['fcoe', 'zfcp', 'iscsi']:
                    self.assertEqual(71, cmd.writePriority, command_class)
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
                elif _name in ['volgroup', 'btrfs']:
                    self.assertEqual(132, cmd.writePriority, command_class)
                elif _name in ['logvol']:
                    self.assertEqual(133, cmd.writePriority, command_class)
                elif _name in ['snapshot']:
                    self.assertEqual(140, cmd.writePriority, command_class)
                else:
                    self.fail("Unknown writePriority for %s:%s" % (_name, command_class))

if __name__ == "__main__":
    unittest.main()
