import unittest
import shlex
import re

from pykickstart.parser import KickstartParser
from pykickstart.sections import NullSection
from pykickstart.version import makeVersion

VALID_KICKSTART_OPTION_PATTERN = r"--[a-z0-9\-]+"


class ArgumentNamesStatic_TestCase(unittest.TestCase):

    def setUp(self):
        self._bad_options = []
        self._reg_name_checker = re.compile(VALID_KICKSTART_OPTION_PATTERN)
        self._handler = makeVersion()

    def runTest(self):
        self._check_commands()
        self._check_sections()
        self._report()

    def _check_sections(self):

        tmp_parser = KickstartParser(self._handler)
        # KickstartParser registers internally all sections, so it is possible to get the names and
        # instances from there. However, it handles some known sections implemented outside
        # pykickstart by using NullSection instead of the actual class.

        for section, instance in tmp_parser._sections.items():
            if not isinstance(instance, NullSection):
                arg_parser = instance._getParser()
                self._check_parser_actions(arg_parser, section)

    def _check_commands(self):

        for command, cmdClass in self._handler.commandMap.items():

            if command == "method":
                continue

            args = shlex.split(command, comments=True)
            cmd = args[0]

            ks_parser = self._handler.commands[cmd]
            ks_parser.currentLine = command
            ks_parser.currentCmd = args[0]
            ks_parser.seen = True
            arg_parser = ks_parser._getParser()

            self._check_parser_actions(arg_parser, command, cmd_class=cmdClass)

    def _check_parser_actions(self, arg_parser, cmd_name, cmd_class=None):

        for action in arg_parser._get_optional_actions():
            if action.deprecated:
                continue

            found_any_good = False
            for option in action.option_strings:
                if cmd_class and option.lstrip("-") in cmd_class.removedAttrs:
                    # caution removedAttrs does not include leading dashes
                    continue
                is_good = self._reg_name_checker.fullmatch(option) is not None
                found_any_good = found_any_good or is_good
                if not is_good:
                    print("Found option with uppercase letters: %s for command %s." % (option, cmd_name))

            if not found_any_good:
                self._bad_options.append(tuple((cmd_name, action.option_strings)))

    def _report(self):
        if self._bad_options:
            print("The following kickstart option sets do not include a lowercase only variant:")
            for option_set in self._bad_options:
                print("%s: %s" % (option_set[0], ", ".join(option_set[1])))

            self.fail("Some options use uppercase letters and do not have a lowercase-only alias.")
