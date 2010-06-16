import os
import sys
import unittest
import shlex
import imputil
import glob
import warnings
import re

from pykickstart.version import versionMap, returnClassForVersion
from pykickstart.errors import *
import gettext
gettext.textdomain("pykickstart")
_ = lambda x: gettext.ldgettext("pykickstart", x)

# Base class for any test case
class CommandTest(unittest.TestCase):
    def setUp(self):
        '''Perform any command setup'''
        unittest.TestCase.setUp(self)
        self.handler = None

        # ignore DeprecationWarning
        warnings.simplefilter("ignore", category=DeprecationWarning, append=0)

    def tearDown(self):
        '''Undo anything performed by setUp(self)'''
        # reset warnings
        warnings.filters = warnings.filters[1:]

        unittest.TestCase.tearDown(self)

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._options = []

    @property
    def optionList(self):
        if self._options:
            return self._options

        parser = self.getParser(self.command)._getParser()

        for opt in filter(lambda o: not o.deprecated, parser.option_list):
            self._options.append(opt.get_opt_string())

        return self._options

    def getParser(self, inputStr):
        '''Find a handler using the class name.  Return the requested command
        object.'''
        args = shlex.split(inputStr)
        cmd = args[0]

        if self.handler is None:
            version = self.__class__.__name__.split("_")[0]
            self.handler = returnClassForVersion(version)

        parser = self.handler().commands[cmd]
        parser.currentLine = inputStr
        parser.currentCmd = args[0]

        return parser

    def assert_parse(self, inputStr, expectedStr=None, ignoreComments=True):
        '''KickstartParseError is not raised and the resulting string matches
        supplied value'''
        parser = self.getParser(inputStr)
        args = shlex.split(inputStr)

        # If expectedStr supplied, we want to ensure the parsed result matches
        if expectedStr is not None:
            result = parser.parse(args[1:])

            # Strip any comment lines ... we only match on non-comments
            if ignoreComments:
                result = re.sub("^#[^\n]*\n", "", str(result))

            # Ensure we parsed as expected
            self.assertEqual(str(result), expectedStr)
        # No expectedStr supplied, just make sure it does not raise an
        # exception
        else:
            try:
                result = parser.parse(args[1:])
            except Exception, e:
                self.fail("Failed while parsing: %s" % e)

    def assert_parse_error(self, inputStr, exception=KickstartParseError):
        '''Assert that parsing the supplied string raises a
        KickstartParseError'''
        parser = self.getParser(inputStr)
        args = shlex.split(inputStr)

        self.assertRaises(exception, parser.parse, args[1:])

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
    moduleList = []
    lst = map(lambda x: os.path.splitext(os.path.basename(x))[0],
              glob.glob(moduleDir + "/*.py"))

    # Inspect each .py file found
    for module in lst:
        if module in skip_list:
            continue

        # Attempt to load the found module.
        try:
            found = imputil.imp.find_module(module)
            loaded = imputil.imp.load_module(module, found[0], found[1], found[2])
        except ImportError, e:
            print(_("Error loading module %s.") % module)

        # Find class names that match the supplied pattern (default: "_TestCase")
        beforeCount = len(tstList)
        for obj in loaded.__dict__.keys():
            if obj.endswith(cls_pattern):
                tstList.append(loaded.__dict__[obj])
        afterCount = len(tstList)

        # Warn if no tests found
        if beforeCount == afterCount:
            print(_("Module %s does not contain any test cases; skipping.") % module)
            continue

    return tstList

# Run the tests
if __name__ == "__main__":

    # Create a test suite
    PyKickstartTestSuite = unittest.TestSuite()

    # Find tests to add
    tstList = loadModules(os.path.join(os.environ.get("PWD"), "tests/"))
    tstList.extend(loadModules(os.path.join(os.environ.get("PWD"), "tests/commands")))
    for tst in tstList:
        PyKickstartTestSuite.addTest(tst())

    # Run tests
    unittest.main(defaultTest="PyKickstartTestSuite")
