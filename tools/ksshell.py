#!/usr/bin/env python3
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2013-2014 Red Hat, Inc.
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

# This script takes as input an optional input kickstart file and an optional
# kickstart syntax version (the latest is assumed, if none specified).  It
# then provides an interactive shell for the user to manipulate the state of
# the input kickstart file and either prints the final results on stdout or to
# a designated output file when the program quits.

# TODO:
# - error reporting always says you are on line 1
# - handle sections like %packages
# - some meta-commands might be nice:
#   - .delete (a previous line)
#   - .help (requires moving help text into each optionparser object?)
#   - .save

# pylint: disable=found-_-in-module-class

import readline
import argparse
import os, six, sys

from pykickstart.i18n import _
from pykickstart.errors import KickstartError, KickstartVersionError
from pykickstart.parser import KickstartParser, preprocessKickstart
from pykickstart.version import DEVEL, makeVersion

##
## INTERNAL COMMANDS
## These are commands that control operation of the kickstart shell and are
## handled by this program.  They are not recognized kickstart commands.
##

class InternalCommand(object):
    def __init__(self):
        self.op = argparse.ArgumentParser()

    def execute(self, parser):
        pass

class ClearCommand(InternalCommand):
    def execute(self, parser):
        version = parser.version
        parser.handler = makeVersion(version)

class QuitCommand(InternalCommand):
    def execute(self, parser):
        raise EOFError

class ShowCommand(InternalCommand):
    def execute(self, parser):
        print(parser.handler)

##
## COMMAND COMPLETION
##

class KickstartCompleter(object):
    def __init__(self, handler, internal):
        # Build up a dict of kickstart commands and their valid options:
        # { command_name: [options] }
        self.commands = {}

        for (cStr, cObj) in handler.commands.items():
            self._add_command(cStr, cObj)

        for (cStr, cObj) in internal.items():
            self._add_command(cStr, cObj)

        self.currentCandidates = []

    def _add_command(self, cStr, cObj):
        self.commands[cStr] = []

        # Internal and simple commands don't have any optparse crud.
        if cStr.startswith(".") or not hasattr(cObj, "op"):
            return

        for opt in cObj.op.option_list:
            self.commands[cStr] += opt._short_opts + opt._long_opts

    def complete(self, _text, state):
        response = None

        # This is the first time Tab has been pressed, so build up a list of matches.
        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()

            beingCompleted = origline[begin:end]
            parts = origline.split()

            if not parts:
                # Everything's a match for an empty string.
                self.currentCandidates = sorted(self.commands.keys())
            else:
                try:
                    # Ignore leading whitespace when trying to figure out
                    # completions for a kickstart command.
                    if begin == 0 or origline[:begin].strip() == "":
                        # first word
                        candidates = self.commands.keys()
                    else:
                        # later word
                        candidates = self.commands[parts[0]]

                    if beingCompleted:
                        self.currentCandidates = [w for w in candidates if w.startswith(beingCompleted)]
                    else:
                        self.currentCandidates = list(candidates)
                except (KeyError, IndexError):
                    self.currentCandidates = []

        try:
            response = self.currentCandidates[state]
        except IndexError:
            response = None

        return response

##
## OPTION PROCESSING
##

op = argparse.ArgumentParser()
op.add_argument("-i", "--input", dest="input",
                help=_("a basis file to use for seeding the kickstart data (optional)"))
op.add_argument("-o", "--output", dest="output",
                help=_("the location to write the finished kickstart file, or stdout if not given"))
op.add_argument("-v", "--version", dest="version", default=DEVEL,
                help=_("version of kickstart syntax to validate against"))

opts = op.parse_args(sys.argv[1:])

##
## SETTING UP PYKICKSTART
##

try:
    kshandler = makeVersion(opts.version)
except KickstartVersionError:
    print(_("The version %s is not supported by pykickstart") % opts.version)
    sys.exit(1)

ksparser = KickstartParser(kshandler, followIncludes=True, errorsAreFatal=False)

if opts.input:
    try:
        processedFile = preprocessKickstart(opts.input)
        ksparser.readKickstart(processedFile)
        os.remove(processedFile)
    except KickstartError as e:
        # Errors should just dump you to the prompt anyway.
        print(_("Warning:  The following error occurred when processing the input file:\n%s\n") % e)

internalCommands = {".clear": ClearCommand(),
                    ".show": ShowCommand(),
                    ".quit": QuitCommand()}

##
## SETTING UP READLINE
##

readline.parse_and_bind("tab: complete")
readline.set_completer(KickstartCompleter(kshandler, internalCommands).complete)

# Since everything in kickstart looks like a command line arg, we need to
# remove '-' from the delimiter string.
delims = readline.get_completer_delims()
readline.set_completer_delims(delims.replace('-', ''))

##
## REPL
##

print("Press ^D to exit.")

while True:
    try:
        line = six.moves.input("ks> ")  # pylint: disable=no-member
    except EOFError:
        # ^D was hit, time to quit.
        break
    except KeyboardInterrupt:
        # ^C was hit, time to quit.  Don't be like other programs.
        break

    # All internal commands start with a ., so if that's the beginning of the
    # line, we need to dispatch ourselves.
    if line.startswith("."):
        words = line.split()
        if words[0] in internalCommands:
            try:
                internalCommands[words[0]].execute(ksparser)
            except EOFError:
                # ".quit" was typed, time to quit.
                break
        else:
            print(_("Internal command %s not recognized.") % words[0])

        continue

    # Now process the line of input as if it were a kickstart file - just an
    # extremely short one.
    try:
        ksparser.readKickstartFromString(line)
    except KickstartError as e:
        print(e)

# And finally, print the output kickstart file.
if opts.output:
    with open(opts.output, "w") as fd:
        fd.write(str(ksparser.handler))
else:
    print("\n" + str(ksparser.handler))
