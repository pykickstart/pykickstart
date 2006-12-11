#
# parser.py:  Kickstart file parser.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import shlex
import sys
import string
from copy import copy
from optparse import *

from constants import *
from errors import *
from options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

STATE_END = 0
STATE_COMMANDS = 1
STATE_PACKAGES = 2
STATE_SCRIPT_HDR = 3
STATE_PRE = 4
STATE_POST = 5
STATE_TRACEBACK = 6

###
### SCRIPT HANDLING
###

# You may make a subclass of Script if you need additional script handling
# besides just a data representation.  For instance, anaconda may subclass
# this to add a run method.
class Script:
    def __init__(self, script, interp = "/bin/sh", inChroot = False,
                 logfile = None, errorOnFail = False, type = KS_SCRIPT_PRE):
        self.script = string.join(script, "")
        self.interp = interp
        self.inChroot = inChroot
        self.logfile = logfile
        self.errorOnFail = errorOnFail
        self.type = type

    # Produce a string representation of the script suitable for writing
    # to a kickstart file.  Add this to the end of the %whatever header.
    def __str__(self):
        if self.type == KS_SCRIPT_PRE:
            retval = "%%pre"
        elif self.type == KS_SCRIPT_POST:
            retval = "%%post"
        elif self.type == KS_SCRIPT_TRACEBACK:
            retval = "%%traceback"

        if self.interp != "/bin/sh" and self.interp != "":
            retval += " --interp %s" % self.interp
        if self.type == KS_SCRIPT_POST and not self.inChroot:
            retval += " --nochroot"
        if self.logfile != None:
            retval += " --logfile %s" % self.logfile
        if self.errorOnFail:
            retval += " --erroronfail"

        return retval + "\n%s" % self.script


##
## PACKAGE HANDLING
##
class Packages:
    def __init__(self):
        self.groupList = []
        self.packageList = []
        self.excludedList = []
        self.excludeDocs = False
        self.addBase = True
        self.handleMissing = KS_MISSING_PROMPT

    def __str__(self):
        pkgs = ""

        for grp in self.groupList:
            pkgs += "@%s\n" % grp

        for pkg in self.packageList:
            pkgs += "%s\n" % pkg

        for pkg in self.excludedList:
            pkgs += "-%s\n" % pkg

        if pkgs == "":
            return ""

        retval = "\n%packages"

        if self.excludeDocs:
            retval += " --excludedocs"
        if not self.addBase:
            retval += " --nobase"
        if self.handleMissing == KS_MISSING_IGNORE:
            retval += " --ignoremissing"

        return retval + "\n" + pkgs


###
### PARSER
###

# The kickstart file parser.  This only transitions between states and calls
# handlers at certain points.  To create a specialized parser, make a subclass
# of this and override the methods you care about.  Methods that don't need to
# do anything may just pass.
#
# Passing None for kshandlers is valid just in case you don't care about
# handling any commands.
class KickstartParser:
    def __init__ (self, kshandlers, followIncludes=True,
                  errorsAreFatal=True, missingIncludeIsFatal=True):
        self.handler = kshandlers
        self.followIncludes = followIncludes
        self.missingIncludeIsFatal = missingIncludeIsFatal
        self.state = STATE_COMMANDS
        self.script = None
        self.includeDepth = 0
        self.errorsAreFatal = errorsAreFatal

    # Functions to be called when we are at certain points in the
    # kickstart file parsing.  Override these if you need special
    # behavior.
    def addScript (self):
        if string.join(self.script["body"]).strip() == "":
            return

        s = Script (self.script["body"], self.script["interp"],
                    self.script["chroot"], self.script["log"],
                    self.script["errorOnFail"], self.script["type"])

        self.handler.scripts.append(s)

    def addPackages (self, line):
        stripped = line.strip()

        if stripped[0] == '@':
            self.handler.packages.groupList.append(stripped[1:].lstrip())
        elif stripped[0] == '-':
            self.handler.packages.excludedList.append(stripped[1:].lstrip())
        else:
            self.handler.packages.packageList.append(stripped)

    def handleCommand (self, lineno, args):
        if self.handler:
            self.handler.dispatcher(args[0], args[1:], lineno)

    def handlePackageHdr (self, lineno, args):
        op = KSOptionParser(lineno=lineno)
        op.add_option("--excludedocs", dest="excludedocs", action="store_true",
                      default=False)
        op.add_option("--ignoremissing", dest="ignoremissing",
                      action="store_true", default=False)
        op.add_option("--nobase", dest="nobase", action="store_true",
                      default=False)
        op.add_option("--ignoredeps", dest="resolveDeps", action="store_false",
                      deprecated=1)
        op.add_option("--resolvedeps", dest="resolveDeps", action="store_true",
                      deprecated=1)

        (opts, extra) = op.parse_args(args=args[1:])

        self.handler.packages.excludeDocs = opts.excludedocs
        self.handler.packages.addBase = not opts.nobase
        if opts.ignoremissing:
            self.handler.packages.handleMissing = KS_MISSING_IGNORE
        else:
            self.handler.packages.handleMissing = KS_MISSING_PROMPT

    def handleScriptHdr (self, lineno, args):
        op = KSOptionParser(lineno=lineno)
        op.add_option("--erroronfail", dest="errorOnFail", action="store_true",
                      default=False)
        op.add_option("--interpreter", dest="interpreter", default="/bin/sh")
        op.add_option("--log", "--logfile", dest="log")

        if args[0] == "%pre" or args[0] == "%traceback":
            self.script["chroot"] = False
        elif args[0] == "%post":
            self.script["chroot"] = True
            op.add_option("--nochroot", dest="nochroot", action="store_true",
                          default=False)

        (opts, extra) = op.parse_args(args=args[1:])

        self.script["interp"] = opts.interpreter
        self.script["log"] = opts.log
        self.script["errorOnFail"] = opts.errorOnFail
        if hasattr(opts, "nochroot"):
            self.script["chroot"] = not opts.nochroot

    # Parser state machine.  Don't override this in a subclass.
    def readKickstart (self, file):
        # For error reporting.
        lineno = 0

        fh = open(file)
        needLine = True

        while True:
            if needLine:
                line = fh.readline()
                lineno += 1
                needLine = False

            # At the end of an included file
            if line == "" and self.includeDepth > 0:
                fh.close()
                break

            # Don't eliminate whitespace or comments from scripts.
            if line.isspace() or (line != "" and line.lstrip()[0] == '#'):
                # Save the platform for s-c-kickstart, though.
                if line[:10] == "#platform=" and self.state == STATE_COMMANDS:
                    self.handler.platform = line[11:]

                if self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                    self.script["body"].append(line)

                needLine = True
                continue

            # We only want to split the line if we're outside of a script,
            # as inside the script might involve some pretty weird quoting
            # that shlex doesn't understand.
            if self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                # Have we found a state transition?  If so, we still want
                # to split.  Otherwise, args won't be set but we'll fall through
                # all the way to the last case.
                if line != "" and string.split(line.lstrip())[0] in \
                   ["%post", "%pre", "%traceback", "%include", "%packages"]:
                    args = shlex.split(line)
                else:
                    args = None
            else:
                args = shlex.split(line)

            if args and args[0] == "%include":
                # This case comes up primarily in ksvalidator.
                if not self.followIncludes:
                    needLine = True
                    continue

                if not args[1]:
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    self.includeDepth += 1

                    try:
                        self.readKickstart (args[1])
                    except IOError:
                        # Handle the include file being provided over the
                        # network in a %pre script.  This case comes up in the
                        # early parsing in anaconda.
                        if self.missingIncludeIsFatal:
                            raise

                    self.includeDepth -= 1
                    needLine = True
                    continue

            if self.state == STATE_COMMANDS:
                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self.state = STATE_SCRIPT_HDR
                elif args[0] == "%packages":
                    self.state = STATE_PACKAGES
                elif args[0][0] == '%':
                    # This error is too difficult to continue from, without
                    # lots of resync code.  So just print this one and quit.
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    needLine = True

                    if self.errorsAreFatal:
                        self.handleCommand(lineno, args)
                    else:
                        try:
                            self.handleCommand(lineno, args)
                        except Exception, msg:
                            print msg

            elif self.state == STATE_PACKAGES:
                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self.state = STATE_SCRIPT_HDR
                elif args[0] == "%packages":
                    needLine = True

                    if self.errorsAreFatal:
                        self.handlePackageHdr (lineno, args)
                    else:
                        try:
                            self.handlePackageHdr (lineno, args)
                        except Exception, msg:
                            print msg
                elif args[0][0] == '%':
                    # This error is too difficult to continue from, without
                    # lots of resync code.  So just print this one and quit.
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    needLine = True
                    self.addPackages (string.rstrip(line))

            elif self.state == STATE_SCRIPT_HDR:
                needLine = True
                self.script = {"body": [], "interp": "/bin/sh", "log": None,
                               "errorOnFail": False}

                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] == "%pre":
                    self.state = STATE_PRE
                    self.script["type"] = KS_SCRIPT_PRE
                elif args[0] == "%post":
                    self.state = STATE_POST
                    self.script["type"] = KS_SCRIPT_POST
                elif args[0] == "%traceback":
                    self.state = STATE_TRACEBACK
                    self.script["type"] = KS_SCRIPT_TRACEBACK
                elif args[0][0] == '%':
                    # This error is too difficult to continue from, without
                    # lots of resync code.  So just print this one and quit.
                    raise KickstartParseError, formatErrorMsg(lineno)

                if self.errorsAreFatal:
                    self.handleScriptHdr (lineno, args)
                else:
                    try:
                        self.handleScriptHdr (lineno, args)
                    except Exception, msg:
                        print msg

            elif self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                if line == "" and self.includeDepth == 0:
                    # If we're at the end of the kickstart file, add the script.
                    self.addScript()
                    self.state = STATE_END
                elif args and args[0] in ["%pre", "%post", "%traceback", "%packages"]:
                    # Otherwise we're now at the start of the next section.
                    # Figure out what kind of a script we just finished
                    # reading, add it to the list, and switch to the initial
                    # state.
                    self.addScript()
                    self.state = STATE_COMMANDS
                else:
                    # Otherwise just add to the current script body.
                    self.script["body"].append(line)
                    needLine = True

            elif self.state == STATE_END:
                break
