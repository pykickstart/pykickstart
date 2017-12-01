import unittest

from pykickstart.version import *           # pylint: disable=wildcard-import
from pykickstart.base import KickstartCommand, BaseData, BaseHandler


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
