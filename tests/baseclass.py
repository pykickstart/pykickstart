import os
import sys
import unittest
import shlex
import glob
import warnings
import re
import tempfile
import shutil
import six

try:
    from imputil import imp
except ImportError: # Python 3
    import imp

from pykickstart.errors import *
from pykickstart.parser import preprocessFromString, KickstartParser
from pykickstart.version import *
from pykickstart.i18n import _

class ParserTest(unittest.TestCase):
    version = DEVEL

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self._handler = None
        self._parser = None
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Undo anything performed by setUp"""
        unittest.TestCase.tearDown(self)

    def get_parser(self):
        """This function can be overriden by subclasses,
        for example if the subclass wants to use a fresh
        parser for every test
        """
        if self._parser is None:
            self._parser = KickstartParser(self.handler)
        return self._parser

    @property
    def parser(self):
        return self.get_parser()

    @property
    def handler(self):
        if self._handler is None:
            self._handler = makeVersion(self.version)
        return self._handler

    def assert_parse_error(self, ks_string, exception=KickstartParseError, regex=r".*"):
        """Parsing of this command sequence is expected to raise an exception,
        exception type can be set by the exception keyword argument.

        By default the KickstartParseError is expected.
        """

        if not six.PY3:
            assert_function = 'assertRaisesRegexp'
        else:
            assert_function = 'assertRaisesRegex'
        with getattr(self, assert_function)(exception, regex):
            self.parser.readKickstartFromString(ks_string)

    def assert_parse(self, ks_string):
        """Parsing of his command sequence is expected to finish without
        raising an exception; if it raises an exception, the test failed
        """
        try:
            self.parser.readKickstartFromString(ks_string)
        except Exception as e:
            self.fail("Failed while parsing commands %s: %s" % (ks_string, e))


class CommandSequenceTest(ParserTest):
    """Kickstart command sequence testing

    Enables testing kickstart indepdent command sequences
    and checking if their parsing raises or doesn't raise
    a parsing exception.
    """

    def get_parser(self):
        """Command sequence tests need a fresh parser
        for each test"""
        handler = makeVersion(self.version)
        return KickstartParser(handler)


# Base class for any command test case
class CommandTest(unittest.TestCase):
    def setUp(self):
        '''Perform any command setup'''
        unittest.TestCase.setUp(self)

        # ignore DeprecationWarning
        warnings.simplefilter("error", category=UserWarning)
        warnings.simplefilter("ignore", category=DeprecationWarning, append=0)

    def tearDown(self):
        '''Undo anything performed by setUp(self)'''
        # reset warnings
        warnings.resetwarnings()

        unittest.TestCase.tearDown(self)

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._options = []

    @property
    def handler(self):
        version = self.__class__.__name__.split("_")[0]
        return returnClassForVersion(version)

    @property
    def optionList(self):
        if self._options:
            return self._options

        parser = self.getParser(self.command)._getParser()

        for opt in [o for o in parser.option_list if not o.deprecated]:
            self._options.append(opt.get_opt_string())

        return self._options

    def getParser(self, inputStr):
        '''Find a handler using the class name.  Return the requested command
        object.'''
        args = shlex.split(inputStr)
        cmd = args[0]

        parser = self.handler().commands[cmd]
        parser.currentLine = inputStr
        parser.currentCmd = args[0]
        parser.seen = True

        return parser

    def assert_parse(self, inputStr, expectedStr=None, ignoreComments=True):
        '''KickstartParseError is not raised and the resulting string matches
        supplied value'''
        parser = self.getParser(inputStr)
        args = shlex.split(inputStr)

        # If expectedStr supplied, we want to ensure the parsed result matches
        if expectedStr is not None:
            obj = parser.parse(args[1:])
            result = str(obj)

            # Strip any comment lines ... we only match on non-comments
            if ignoreComments:
                result = re.sub("^#[^\n]*\n", "", result)

            # Ensure we parsed as expected
            self.assertEqual(result, expectedStr)
        # No expectedStr supplied, just make sure it does not raise an
        # exception
        else:
            try:
                obj = parser.parse(args[1:])
            except Exception as e:
                self.fail("Failed while parsing: %s" % e)
        return obj

    def assert_parse_error(self, inputStr, exception=KickstartParseError, regex=r".*"):
        '''Assert that parsing the supplied string raises a
        KickstartParseError'''
        parser = self.getParser(inputStr)
        args = shlex.split(inputStr)

        with self.assertRaisesRegexp(exception, regex):
            parser.parse(args[1:])

    def assert_deprecated(self, cmd, opt):
        '''Ensure that the provided option is listed as deprecated'''
        parser = self.getParser(cmd)

        for op in parser.op.option_list:
            if op.get_opt_string() == opt:
                self.assert_(op.deprecated)

    def assert_removed(self, cmd, opt):
        '''Ensure that the provided option is not present in option_list'''
        parser = self.getParser(cmd)
        for op in parser.op.option_list:
            self.assertNotEqual(op.dest, opt)

    def assert_required(self, cmd, opt):
        '''Ensure that the provided option is labelled as required in
        option_list'''
        parser = self.getParser(cmd)
        for op in parser.op.option_list:
            if op.get_opt_string() == opt:
                self.assert_(op.required)

    def assert_type(self, cmd, opt, opt_type):
        '''Ensure that the provided option is of the requested type'''
        parser = self.getParser(cmd)
        for op in parser.op.option_list:
            if op.get_opt_string() == opt:
                self.assertEqual(op.type, opt_type)


def loadModules(moduleDir, cls_pattern="_TestCase", skip_list=["__init__", "baseclass"]):
    '''taken from firstboot/loader.py'''

    # Guaruntee that __init__ is skipped
    if skip_list.count("__init__") == 0:
        skip_list.append("__init__")

    tstList = list()

    # Make sure moduleDir is in the system path so imputil works.
    if not moduleDir in sys.path:
        sys.path.insert(0, moduleDir)

    # Get a list of all *.py files in moduleDir
    lst = [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(moduleDir + "/*.py")]

    # Inspect each .py file found
    for module in lst:
        if module in skip_list:
            continue

        # Attempt to load the found module.
        try:
            try:
                found = imp.find_module(module)
                loaded = imp.load_module(module, found[0], found[1], found[2])
            except ImportError as e:
                print(_("Error loading module %s: %s") % (module, e))
                continue

            # Find class names that match the supplied pattern (default: "_TestCase")
            beforeCount = len(tstList)
            for obj in list(loaded.__dict__.keys()):
                if obj.endswith(cls_pattern):
                    tstList.append(loaded.__dict__[obj])
            afterCount = len(tstList)

            # Warn if no tests found
            if beforeCount == afterCount:
                print(_("Module %s does not contain any test cases; skipping.") % module)
                continue
        finally: # Closing opened files in imp.load_module
            if found and len(found) > 0:
                found[0].close()

    return tstList

# Run the tests
if __name__ == "__main__":
    # Make sure PWD is in the path before the eggs, system paths, etc.
    sys.path.insert(0, os.environ.get("PWD"))

    # Create a test suite
    PyKickstartTestSuite = unittest.TestSuite()

    # Find tests to add
    tstList = loadModules(os.path.join(os.environ.get("PWD"), "tests/"))
    tstList.extend(loadModules(os.path.join(os.environ.get("PWD"), "tests/commands")))
    tstList.extend(loadModules(os.path.join(os.environ.get("PWD"), "tests/parser")))
    for tst in tstList:
        PyKickstartTestSuite.addTest(tst())

    # Run tests
    unittest.main(defaultTest="PyKickstartTestSuite")
