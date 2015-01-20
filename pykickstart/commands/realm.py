#
# Stef Walter <stefw@redhat.com>
#
# Copyright 2013 Red Hat, Inc.
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

from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartValueError, formatErrorMsg

import getopt
import pipes
import shlex

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class F19_Realm(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.join_realm = None
        self.join_args = []
        self.discover_options = []

    def _parseArguments(self, string):
        if self.join_realm:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_(
                "The realm command 'join' should only be specified once")))
        args = shlex.split(string)
        if not args:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_(
                "Missing realm command arguments")))
        command = args.pop(0)
        if command == "join":
            self._parseJoin(args)
        else:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_(
                "Unsupported realm '%s' command" % command)))

    def _parseJoin(self, args):
        try:
            # We only support these args
            opts, remaining = getopt.getopt(args, "", ("client-software=",
                                                       "server-software=",
                                                       "membership-software=",
                                                       "one-time-password=",
                                                       "no-password",
                                                       "computer-ou="))
        except getopt.GetoptError as ex:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_(
                "Invalid realm arguments: %s") % ex))

        if len(remaining) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_(
                "Specify only one realm to join")))

        # Parse successful, just use this as the join command
        self.join_realm = remaining[0]
        self.join_args = args

        # Build a discovery command
        self.discover_options = []
        supported_discover_options = ("--client-software",
                                      "--server-software",
                                      "--membership-software")
        for (o, a) in opts:
            if o in supported_discover_options:
                self.discover_options.append("%s=%s" % (o, a))

    def _getCommandsAsStrings(self):
        commands = []
        if self.join_args:
            args = [pipes.quote(arg) for arg in self.join_args]
            commands.append("realm join " + " ".join(args))
        return commands

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        commands = self._getCommandsAsStrings()
        if commands:
            retval += "# Realm or domain membership\n"
            retval += "\n".join(commands)
            retval += "\n"

        return retval

    def parse(self, args):
        self._parseArguments(self.currentLine[len(self.currentCmd):].strip())
        return self
