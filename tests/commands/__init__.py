import os
import sys
import unittest
import importlib
from pykickstart.base import KickstartCommand, BaseData

class ClassDefinitionTestCase(unittest.TestCase):
    """
        Search for command and data classes defined like so:

        RHEL7_AutoPart = F21_AutoPart.

        This kind of definitions makes it possible for other
        tests to omit possible errors and we don't like to have
        them. Either we use the existing class name if we haven't
        redefined anything or provide a boilerplate definition:

        class RHEL7_Autopart(F21_Autopart):
            pass
    """
    def runTest(self):
        errors = 0
        commands_dir = os.path.join(os.path.dirname(__file__), "..", "..", "pykickstart", "commands")
        commands_dir = os.path.abspath(commands_dir)

        self.assertTrue(os.path.exists(commands_dir))
        if commands_dir not in sys.path:
            sys.path.append(commands_dir)

        for dirpath, _dirnames, paths in os.walk(commands_dir):
            for path in paths:
                if path == '__init__.py' or not path.endswith('.py'):
                    continue

                # load the module defining all possible command implementations
                command_module = importlib.import_module(path.replace(".py", ""))
                module_commands = [] # a list of already checked commands

                for impl_name, impl_class in command_module.__dict__.items():
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

                    if impl_class not in module_commands and \
                        impl_class.__name__ == impl_name:
                        module_commands.append(impl_class)
                    else:
                        errors += 1
                        message = "ERROR: In `commands/%s` %s = %s" % (path, impl_name, impl_class.__name__)
                        print(message)


        # assert for errors presence
        self.assertEqual(0, errors)

if __name__ == "__main__":
    unittest.main()
