import os
import sys
import unittest
import importlib
from unittest import mock
from pykickstart.options import KSOptionParser
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

        for _dirpath, _dirnames, paths in os.walk(commands_dir):
            for path in paths:
                if path == '__init__.py' or not path.endswith('.py'):
                    continue

                # load the module defining all possible command implementations
                command_module = importlib.import_module(path.replace(".py", ""))
                module_commands = []  # a list of already checked commands

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

class TestKSOptionParser(KSOptionParser):
    """
        Wrapper class that will raise exception if some of the
        help attributes are empty.
    """
    def __init__(self, *args, **kwargs):
        self._test_errors = []
        for arg_name in ['prog', 'version', 'description']:
            if not kwargs.get(arg_name) and not kwargs.get("deprecated"):
                self._test_errors.append("%s: %s can't be blank" % (args[0], arg_name))

        super(TestKSOptionParser, self).__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        for arg_name in ['help', 'version']:
            if not kwargs.get(arg_name) and not kwargs.get("deprecated"):
                self._test_errors.append("%s: %s can't be blank" % (args[0], arg_name))
        return super(TestKSOptionParser, self).add_argument(*args, **kwargs)


class HelpAndDescription_TestCase(unittest.TestCase):
    """
        Check that all commands and their options have some description text.
    """

    def runTest(self):
        errors = 0
        commands_dir = os.path.join(os.path.dirname(__file__), "..", "..", "pykickstart", "commands")
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

                for _, impl_class in command_module.__dict__.items():
                    # skip everything which isn't a class
                    if type(impl_class) is not type:
                        continue

                    # skip everything which doesn't inherit from KickstartCommand
                    if not issubclass(impl_class, KickstartCommand):
                        continue

                    # skip base classes as well
                    if impl_class.__name__ in ['KickstartCommand', 'DeprecatedCommand']:
                        continue

                    # In order for patch to locate the function to be patched, it must be
                    # specified using its fully qualified name, which may not be what you expect.
                    # For example, if a class is imported in the module my_module.py as follows:
                    # from module import ClassA
                    # It must be patched as patch(my_module.ClassA), rather than patch(module.ClassA),
                    # due to the semantics of the from ... import ... statement, which imports
                    # classes and functions into the current namespace.
                    command_module_name = command_module.__name__
                    # the install.py command inherits from upgrade.py and doesn't import
                    # KSOptionParser on its own
                    if command_module_name == 'install':
                        command_module_name = 'upgrade'
                    with mock.patch('%s.KSOptionParser' % command_module_name, new=TestKSOptionParser):
                        # just construct the option parser
                        # the wrapper class will raise an exception in case
                        # there are empty help strings
                        klass = impl_class()
                        op = klass._getParser()

                        if hasattr(op, "_test_errors") and len(op._test_errors) > 0:
                            errors += len(op._test_errors)
                            print("ERROR: In `%s`" % impl_class)
                            for err in op._test_errors:
                                print(err)

        # assert for errors presence
        self.assertEqual(0, errors)

if __name__ == "__main__":
    unittest.main()
