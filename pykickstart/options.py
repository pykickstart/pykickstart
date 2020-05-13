#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005-2016 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#
"""
Specialized option handling.

This module exports three classes:

    ExtendAction - A subclass of Action that appends a list of values to an
                   already existing list.  In this way, it's like the existing
                   "append" action except for lists instead of single values.

    ExtendConstAction - A subclass of Action that appends a list of constants
                        to an already existing list.  In this way, it's like the
                        existing "append_const" action except for lists instead
                        of single values.

    KSOptionParser - A specialized subclass of ArgumentParser to be used
                     in BaseHandler subclasses.

And it exports two functions:

    commaSplit - A function to be used as the type= argument to any arguments
                 that take a single string that may be split on commas, resulting
                 in a list of strings.

    ksboolean - A function to be used as the type= argument to any arguments
                that can take a boolean.
"""
import os
import warnings
import textwrap
from argparse import RawTextHelpFormatter, SUPPRESS
from argparse import Action, ArgumentParser, ArgumentTypeError

from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning
from pykickstart.version import versionToLongString

from pykickstart.i18n import _

def commaSplit(value):
    return list(filter(None, [v.strip() for v in value.split(',')]))

def ksboolean(value):
    try:
        if value.lower() in ("on", "yes", "true", "1"):
            return True
        elif value.lower() in ("off", "no", "false", "0"):
            return False
        else:
            raise ArgumentTypeError(_("invalid boolean value: %r") % value)
    except AttributeError:
        raise ArgumentTypeError(_("invalid boolean value: %r") % value)

def mountpoint(value):
    if value.startswith("/"):
        return os.path.normpath(value)

    return value

class KSHelpFormatter(RawTextHelpFormatter):
    """
        Used in generating documentation
    """

    def _format_usage(self, usage, actions, groups, prefix):
        return "::\n\n    %s" % super(KSHelpFormatter,
                                      self)._format_usage(usage,
                                                          actions,
                                                          groups,
                                                          "").strip()

    def _format_action(self, action):
        text = super(KSHelpFormatter, self)._format_action(action)
        parts = text.strip().split('\n')
        new_parts = []
        new_parts.append("\n``%s``\n" % parts[0].strip())
        for p in parts[1:]:
            if p:
                new_parts.append("    %s" % p.lstrip())
        return self._join_parts(new_parts)

    def _join_parts(self, part_strings):
        return '\n'.join([part.rstrip(' ')
                          for part in part_strings
                          if part and part is not SUPPRESS])


class ExtendAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            setattr(namespace, self.dest, getattr(namespace, self.dest) + values)
        else:
            setattr(namespace, self.dest, values)

class ExtendConstAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            setattr(namespace, self.dest, self.const + values)
        else:
            setattr(namespace, self.dest, self.const)

class KSOptionParser(ArgumentParser):
    """A specialized subclass of argparse.ArgumentParser to handle extra option
       attribute checking, work error reporting into the KickstartParseError
       framework, and to turn off the default help.
    """
    def __init__(self, *args, **kwargs):
        """Create a new KSOptionParser instance.  Each KickstartCommand
           subclass should create one instance of KSOptionParser, providing
           at least the lineno attribute.  version is not required.

           Instance attributes:

           version -- The version when the kickstart command was introduced.

        """
        # Overridden to allow for the version kwargs, to skip help option generation,
        # and to resolve conflicts instead of override earlier options.
        int_version = kwargs.pop("version")  # fail fast if no version is specified
        version = versionToLongString(int_version)

        # always document the version
        if "addVersion" in kwargs:
            warnings.warn("The option 'addVersion' will be removed in a future release.",
                          PendingDeprecationWarning)

        addVersion = kwargs.pop('addVersion', True)

        # remove leading spaced from description and epilog.
        # fail fast if we forgot to add description
        kwargs['description'] = textwrap.dedent(kwargs.pop("description"))
        if addVersion:
            kwargs['description'] = "\n.. versionadded:: %s\n\n%s" % (version,
                                                                    kwargs['description'])
        kwargs['epilog'] = textwrap.dedent(kwargs.pop("epilog", ""))

        # fail fast if we forgot to add prog
        kwargs['prog'] = kwargs.pop("prog")

        # remove leading spaced from description and epilog.
        # fail fast if we forgot to add description
        kwargs['description'] = textwrap.dedent(kwargs.pop("description"))
        kwargs['epilog'] = textwrap.dedent(kwargs.pop("epilog", ""))

        # fail fast if we forgot to add prog
        kwargs['prog'] = kwargs.pop("prog")

        ArgumentParser.__init__(self, add_help=False, conflict_handler="resolve",
                                formatter_class=KSHelpFormatter, *args, **kwargs)
        # NOTE: On Python 2.7 ArgumentParser has a deprecated version parameter
        # which always defaults to self.version = None which breaks deprecation
        # warnings in pykickstart. That's why we always set this value after
        # ArgumentParser.__init__ has been executed
        self.version = int_version
        self.lineno = None

    def _parse_optional(self, arg_string):
        option_tuple = ArgumentParser._parse_optional(self, arg_string)
        if option_tuple is None or option_tuple[0] is None:
            return option_tuple

        action = option_tuple[0]
        option = action.option_strings[0]

        if action.deprecated:
            warnings.warn(_("Ignoring deprecated option on line %(lineno)s: The %(option)s option "
                            "has been deprecated and no longer has any effect. It may be removed "
                            "from future releases, which will result in a fatal error from "
                            "kickstart. Please modify your kickstart file to remove this option.")
                          % {"lineno": self.lineno, "option": option}, KickstartDeprecationWarning)

        return option_tuple

    def add_argument(self, *args, **kwargs):
        if "introduced" in kwargs:
            warnings.warn("The option 'introduced' will be removed in a future release. "
                          "Use 'version' instead.", PendingDeprecationWarning)

        if "removed" in kwargs:
            warnings.warn("The option 'removed' will be removed in a future release. "
                          "Use 'remove_argument' instead.", PendingDeprecationWarning)

        introduced = kwargs.pop("introduced", None)
        deprecated = kwargs.pop("deprecated", False)

        if deprecated:
            version = versionToLongString(deprecated)
        else:
            # fail fast if version is missing
            version = versionToLongString(introduced or kwargs.pop("version"))

        candidate = None
        for action in self._actions:
            for arg in args:
                if arg in action.option_strings:
                    candidate = action
                    break

        if candidate:
            if deprecated:
                _help = candidate.help or ""
                _help += "\n\n    .. deprecated:: %s" % version
                kwargs["help"] = _help
            else:
                # this is a modified argument, which is already present
                _help = candidate.help or ""
                _help += "\n\n    .. versionchanged:: %s\n\n%s" % (version, kwargs.pop("help"))
                kwargs["help"] = _help
        else:
            # this is a new argument which is added for the first time
            _help = kwargs.pop("help")
            _help += "\n\n    .. versionadded:: %s" % version
            # there are some argumets which are deprecated on first declaration
            if deprecated:
                _help += "\n\n    .. deprecated:: %s" % version
            kwargs["help"] = _help

        notest = kwargs.pop("notest", False)
        removed = kwargs.pop("removed", None)

        action = ArgumentParser.add_argument(self, *args, **kwargs)
        action.deprecated = deprecated
        action.introduced = introduced
        action.notest = notest
        action.removed = removed
        return action

    def remove_argument(self, arg, **kwargs):
        candidate = None

        for action in self._actions:
            if arg in action.option_strings:
                candidate = action
                break

        if candidate:
            if not candidate.help:
                candidate.help = ""
            candidate.help += "\n\n    .. versionremoved:: %s" % versionToLongString(kwargs.pop("version"))
            self._remove_action(candidate)
            self._option_string_actions.pop(arg)

    def error(self, message):
        # Overridden to turn errors into KickstartParseErrors.
        if self.lineno is not None:
            raise KickstartParseError(message, lineno=self.lineno)
        else:
            raise KickstartParseError(message)

    def exit(self, status=0, message=None):
        # Overridden because this is a library, and libraries shouldn't just
        # exit.  That's what raising exceptions is for.
        pass

    def parse_args(self, *args, **kwargs):  # pylint: disable=arguments-differ,signature-differs
        if "lineno" in kwargs:
            self.lineno = kwargs.pop("lineno")

        return ArgumentParser.parse_args(self, *args, **kwargs)

    def parse_known_args(self, *args, **kwargs):  # pylint: disable=arguments-differ,signature-differs
        if "lineno" in kwargs:
            self.lineno = kwargs.pop("lineno")

        return ArgumentParser.parse_known_args(self, *args, **kwargs)
