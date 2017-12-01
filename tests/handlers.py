import unittest
import importlib
from textwrap import dedent

from pykickstart.version import *           # pylint: disable=wildcard-import
from pykickstart.handlers import control
from pykickstart.base import KickstartCommand, BaseData, BaseHandler


class HandlerMappingTestCase(unittest.TestCase):
    """
        Verify that command handlers actually map to the
        latest possible commands implementations. See:
        https://github.com/rhinstaller/pykickstart/issues/28
    """
    def runTest(self):
        errors = 0
        for handler_version in control.commandMap:
            # test for commands
            for command_name, command_class in control.commandMap[handler_version].items():
                command_version = getVersionFromCommandClass(command_class)

                # skip commands with the same version as their handler
                # b/c they are obviously the latest possible version
                if command_version == handler_version:
                    continue

                # load the module defining all possible command implementations
                command_module = importlib.import_module(command_class.__module__)

                for impl_class in command_module.__dict__.values():
                    # skip everything which isn't a class
                    if type(impl_class) is not type:
                        continue

                    # skip everything which doesn't inherit from KickstartCommand
                    if not issubclass(impl_class, KickstartCommand):
                        continue

                    # skip base classes as well
                    if impl_class.__name__ in ['KickstartCommand', 'DeprecatedCommand']:
                        continue

                    # version of this particular implementation
                    impl_version = getVersionFromCommandClass(impl_class)

                    # skip older implementations of the same command
                    if impl_version <= command_version:
                        continue

                    # if there is a newer implementation, which isn't newer than the
                    # handler version this means our commandMap doesn't contain the
                    # latest possible version for this command. For example we're testing
                    # the f23.py handler so handler_version == F23, command_version == F20
                    # and impl_version == F21 or later. This is a bug!
                    if command_version < impl_version and impl_version <= handler_version:
                        s_handler_version = versionToString(handler_version, True)
                        s_impl_version = versionToString(impl_version, True)
                        # skip newer RHEL implementations if testing a Fedora handler
                        # or vice versa
                        if (s_handler_version.startswith('F') and \
                            s_impl_version.startswith('RHEL')) or \
                            (s_handler_version.startswith('RHEL') and \
                            s_impl_version.startswith('F')):
                            continue

                        errors += 1
                        message = dedent("""
                            ERROR: In `handlers/%s.py` the "%s" command maps to "%s" while in
                            `%s` there is newer implementation: "%s".
                        """ % (versionToString(handler_version, True).lower(),
                               command_name, command_class.__name__,
                               command_class.__module__, impl_class.__name__))
                        print(message)

            # test for data
            for data_name, data_class in control.dataMap[handler_version].items():
                data_version = getVersionFromCommandClass(data_class)

                # skip data with the same version as their handler
                # b/c they are obviously the latest possible version
                if data_version == handler_version:
                    continue

                # load the module defining all possible data implementations
                data_module = importlib.import_module(data_class.__module__)

                for impl_class in data_module.__dict__.values():
                    # skip everything which isn't a class
                    if type(impl_class) is not type:
                        continue

                    # skip everything which doesn't inherit from BaseData
                    if not issubclass(impl_class, BaseData):
                        continue

                    # skip base classes as well
                    if impl_class.__name__ == 'BaseData':
                        continue

                    # version of this particular implementation
                    impl_version = getVersionFromCommandClass(impl_class)

                    # skip older implementations of the same data
                    if impl_version <= data_version:
                        continue

                    # if there is a newer implementation, which isn't newer than the
                    # handler version this means our dataMap doesn't contain the
                    # latest possible version for this data.
                    if data_version < impl_version and impl_version <= handler_version:
                        s_handler_version = versionToString(handler_version, True)
                        s_impl_version = versionToString(impl_version, True)
                        # skip newer RHEL implementations if testing a Fedora handler
                        # or vice versa
                        if (s_handler_version.startswith('F') and \
                            s_impl_version.startswith('RHEL')) or \
                            (s_handler_version.startswith('RHEL') and \
                            s_impl_version.startswith('F')):
                            continue

                        errors += 1
                        message = dedent("""
                            ERROR: In `handlers/%s.py` "%s" maps to "%s" while in
                            `%s` there is newer implementation: "%s".
                        """ % (versionToString(handler_version, True).lower(),
                               data_name, data_class.__name__,
                               data_class.__module__, impl_class.__name__))
                        print(message)

        # assert for errors presence
        self.assertEqual(0, errors)


class HandlerUpdateTestCase(unittest.TestCase):

    class TestHandler(BaseHandler):
        version = F27

    class TestCommand1(KickstartCommand):
        pass

    class TestCommand2(KickstartCommand):
        pass

    class TestData1(BaseData):
        pass

    class TestData2(BaseData):
        pass

    def setUp(self):
        version_cls = self._get_version_cls()
        self.command_map = dict(version_cls.commandMap)
        self.data_map = dict(version_cls.dataMap)

    def assertEmpty(self, tested_set):
        self.assertEqual(len(tested_set), 0, msg="The set is not empty.")

    def _get_version_cls(self):
        version = self.TestHandler.version
        return returnClassForVersion(version)

    def _test_handler(self, command_updates, data_updates):
        # Create a new handler
        handler = self.TestHandler(commandUpdates=command_updates,
                                   dataUpdates=data_updates)

        # Check that the specified version has not changed its maps.
        version_cls = self._get_version_cls()
        self.assertEqual(self.command_map, version_cls.commandMap)
        self.assertEqual(self.data_map, version_cls.dataMap)

        # Check that the handler knows all commands from the specified version.
        self.assertEmpty(set(self.command_map)
                         - set(handler.commands))

        # Check that the handler knows all commands from updates.
        self.assertEmpty(set(command_updates)
                         - set(handler.commands))

        # Check that the handler doesn't know anything else.
        self.assertEmpty(set(handler.commands)
                         - set(self.command_map)
                         - set(handler.commands))

        # Check parents of the commands in the handler.
        command_map = dict(self.command_map)
        command_map.update(command_updates)

        for name, obj in handler.commands.items():
            self.assertTrue(isinstance(obj, command_map[name]))

        # Check the data.
        data_map = dict(self.data_map)
        data_map.update(data_updates)

        for name, cls in data_map.items():
            self.assertEqual(getattr(handler, name), cls)

    def test_no_updates(self):
        """Test handler with no updates."""
        self._test_handler(dict(), dict())

    def test_command_updates(self):
        """Test handler with command updates."""
        command_updates = {
            "autopart": self.TestCommand1,
            "nonexistent": self.TestCommand2
        }

        self._test_handler(command_updates, dict())
        self._test_handler(dict(), dict())

    def test_data_updates(self):
        """Test handler with data updates."""
        data_updates = {
            "UserData": self.TestData1,
            "NonExistent": self.TestData2
        }

        self._test_handler(dict(), data_updates)
        self._test_handler(dict(), dict())

    def test_all_updates(self):
        """Test handler with command and data updates."""
        command_updates = {
            "bootloader": self.TestCommand1,
            "user": self.TestCommand2,
            "imaginary": self.TestCommand1
        }

        data_updates = {
            "RepoData": self.TestData1,
            "Imaginary": self.TestData2,
            "FakeData": self.TestData2
        }

        self._test_handler(command_updates, data_updates)
        self._test_handler(dict(), dict())

if __name__ == "__main__":
    unittest.main()
