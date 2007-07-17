#
# parser.py:  Kickstart file parser.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
"""
Main kickstart file processing module.

This module exports several important classes:

    Script - Representation of a single %pre, %post, or %traceback script.

    Packages - Representation of the %packages section.

    KickstartParser - The kickstart file parser state machine.
"""

import os
import shlex
import sys
import string
import tempfile
from copy import copy
from optparse import *
from urlgrabber import urlopen
import urlgrabber.grabber as grabber

from constants import *
from errors import *
from options import *
from version import *

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

def _preprocessStateMachine (provideLineFn):
    l = None
    lineno = 0

    # Now open an output kickstart file that we are going to write to one
    # line at a time.
    (outF, outName) = tempfile.mkstemp("-ks.cfg", "", "/tmp")

    while True:
        try:
            l = provideLineFn()
        except StopIteration:
            break

        # At the end of the file?
        if l == "":
            break

        lineno += 1
        url = None

        ll = l.strip()
        if string.find(ll, "%ksappend") == -1:
            os.write(outF, l)
            continue

        # Try to pull down the remote file.
        try:
            ksurl = string.split(ll, ' ')[1]
        except:
            raise KickstartParseError, formatErrorMsg(lineno, msg=_("Illegal url for %%ksappend: %s") % ll)

        try:
            url = grabber.urlopen(ksurl)
        except grabber.URLGrabError, e:
            raise KickstartError, formatErrorMsg(lineno, msg=_("Unable to open %%ksappend file: ") % e.strerror)
        else:
            # Sanity check result.  Sometimes FTP doesn't catch a file
            # is missing.
            try:
                if url.info()["content-length"] < 1:
                    raise KickstartError, formatErrorMsg(lineno, msg=_("Unable to open %%ksappend file"))
            except:
                raise KickstartError, formatErrorMsg(lineno, msg=_("Unable to open %%ksappend file"))

        # If that worked, write the remote file to the output kickstart
        # file in one burst.  Then close everything up to get ready to
        # read ahead in the input file.  This allows multiple %ksappend
        # lines to exist.
        if url is not None:
            os.write(outF, url.read())
            url.close()

    # All done - close the temp file and return its location.
    os.close(outF)
    return outName

def preprocessFromString (str):
    """Preprocess the kickstart file, provided as the string str.  This
        method is currently only useful for handling %ksappend lines,
        which need to be fetched before the real kickstart parser can be
        run.  Returns the location of the complete kickstart file.
    """
    i = iter(str.splitlines(True))
    rc = _preprocessStateMachine (lambda: i.next())
    return rc

def preprocessKickstart (file):
    """Preprocess the kickstart file, given by the filename file.  This
        method is currently only useful for handling %ksappend lines,
        which need to be fetched before the real kickstart parser can be
        run.  Returns the location of the complete kickstart file.
    """
    fh = urlopen(file)
    rc = _preprocessStateMachine (lambda: fh.readline())
    fh.close()
    return rc

###
### SCRIPT HANDLING
###
class Script:
    """A class representing a single kickstart script.  If functionality beyond
       just a data representation is needed (for example, a run method in
       anaconda), Script may be subclassed.  Although a run method is not
       provided, most of the attributes of Script have to do with running the
       script.  Instances of Script are held in a list by the Version object.
    """
    def __init__(self, script, interp = "/bin/sh", inChroot = False,
                 logfile = None, errorOnFail = False, type = KS_SCRIPT_PRE):
        """Create a new Script instance.  Instance attributes:

           errorOnFail -- If execution of the script fails, should anaconda
                          stop, display an error, and then reboot without
                          running any other scripts?
           inChroot    -- Does the script execute in anaconda's chroot
                          environment or not?
           interp      -- The program that should be used to interpret this
                          script.
           logfile     -- Where all messages from the script should be logged.
           script      -- A string containing all the lines of the script.
           type        -- The type of the script, which can be KS_SCRIPT_* from
                          pykickstart.constants.
        """
        self.script = string.join(script, "")
        self.interp = interp
        self.inChroot = inChroot
        self.logfile = logfile
        self.errorOnFail = errorOnFail
        self.type = type

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        if self.type == KS_SCRIPT_PRE:
            retval = '\n%pre'
        elif self.type == KS_SCRIPT_POST:
            retval = '\n%post'
        elif self.type == KS_SCRIPT_TRACEBACK:
            retval = '\n%traceback'

        if self.interp != "/bin/sh" and self.interp != "":
            retval += " --interpreter=%s" % self.interp
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
class Group:
    """A class representing a single group in the %packages section."""
    def __init__(self, name="", include=GROUP_DEFAULT):
        """Create a new Group instance.  Instance attributes:

           name    -- The group's identifier
           include -- The level of how much of the group should be included.
                      Values can be GROUP_* from pykickstart.constants.
        """
        self.name = name
        self.include = include

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        if self.include == GROUP_REQUIRED:
            return "@%s --nodefaults" % self.name
        elif self.include == GROUP_ALL:
            return "@%s --optional" % self.name
        else:
            return "@%s" % self.name

class Packages:
    """A class representing the %packages section of the kickstart file."""
    def __init__(self):
        """Create a new Packages instance.  Instance attributes:

           addBase       -- Should the Base group be installed even if it is
                            not specified?
           default       -- Should the default package set be selected?
           excludedList  -- A list of all the packages marked for exclusion in
                            the %packages section, without the leading minus
                            symbol.
           excludeDocs   -- Should documentation in each package be excluded?
           groupList     -- A list of Group objects representing all the groups
                            specified in the %packages section.  Names will be
                            stripped of the leading @ symbol.
           handleMissing -- If unknown packages are specified in the %packages
                            section, should it be ignored or not?  Values can
                            be KS_MISSING_* from pykickstart.constants.
           packageList   -- A list of all the packages specified in the
                            %packages section.
        """
        self.addBase = True
        self.default = False
        self.excludedList = []
        self.excludeDocs = False
        self.groupList = []
        self.handleMissing = KS_MISSING_PROMPT
        self.packageList = []

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        pkgs = ""

        if not self.default:
            for grp in self.groupList:
                pkgs += "%s\n" % grp.__str__()

            for pkg in self.packageList:
                pkgs += "%s\n" % pkg

            for pkg in self.excludedList:
                pkgs += "-%s\n" % pkg

            if pkgs == "":
                return ""

        retval = "\n%packages"

        if self.default:
            retval += " --default"
        if self.excludeDocs:
            retval += " --excludedocs"
        if not self.addBase:
            retval += " --nobase"
        if self.handleMissing == KS_MISSING_IGNORE:
            retval += " --ignoremissing"

        return retval + "\n" + pkgs

    def _processGroup (self, line):
        op = OptionParser()
        op.add_option("--nodefaults", action="store_true", default=False)
        op.add_option("--optional", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=line.split())

        if opts.nodefaults and opts.optional:
            raise KickstartValueError, _("Group cannot specify both --nodefaults and --optional")

        # If the group name has spaces in it, we have to put it back together
        # now.
        grp = " ".join(extra)

        if opts.nodefaults:
            self.groupList.append(Group(name=grp, include=GROUP_REQUIRED))
        elif opts.optional:
            self.groupList.append(Group(name=grp, include=GROUP_ALL))
        else:
            self.groupList.append(Group(name=grp, include=GROUP_DEFAULT))

    def add (self, pkgList):
        """Given a list of lines from the input file, strip off any leading
           symbols and add the result to the appropriate list.
        """
        for pkg in pkgList:
            stripped = pkg.strip()

            if stripped[0] == "@":
                self._processGroup(stripped[1:])
            elif stripped[0] == "-":
                self.excludedList.append(stripped[1:])
            else:
                self.packageList.append(stripped)


###
### PARSER
###
class KickstartParser:
    """The kickstart file parser class as represented by a basic state
       machine.  To create a specialized parser, make a subclass and override
       any of the methods you care about.  Methods that don't need to do
       anything may just pass.  However, readKickstart should never be
       overridden.
    """
    def __init__ (self, handler, followIncludes=True, errorsAreFatal=True,
                  missingIncludeIsFatal=True):
        """Create a new KickstartParser instance.  Instance attributes:

           errorsAreFatal        -- Should errors cause processing to halt, or
                                    just print a message to the screen?  This
                                    is most useful for writing syntax checkers
                                    that may want to continue after an error is
                                    encountered.
           followIncludes        -- If %include is seen, should the included
                                    file be checked as well or skipped?
           handler               -- An instance of a BaseHandler subclass.  If
                                    None, the input file will still be parsed
                                    but no data will be saved and no commands
                                    will be executed.
           missingIncludeIsFatal -- Should missing include files be fatal, even
                                    if errorsAreFatal is False?
        """
        self.errorsAreFatal = errorsAreFatal
        self.followIncludes = followIncludes
        self.handler = handler
        self.missingIncludeIsFatal = missingIncludeIsFatal
        self._reset()

        self._line = ""

        self.version = self.handler.version

    def _reset(self):
        """Reset the internal variables of the state machine for a new kickstart file."""
        self._state = STATE_COMMANDS
        self._script = None
        self._includeDepth = 0

    def addScript (self):
        """Create a new Script instance and add it to the Version object.  This
           is called when the end of a script section is seen and may be
           overridden in a subclass if necessary.
        """
        if string.join(self._script["body"]).strip() == "":
            return

        s = Script (self._script["body"], self._script["interp"],
                    self._script["chroot"], self._script["log"],
                    self._script["errorOnFail"], self._script["type"])

        if self.handler:
            self.handler.scripts.append(s)

    def addPackages (self, line):
        """Add the single package, exclude, or group into the Version's
           Packages instance.  This method may be overridden in a subclass
           if necessary.
        """
        if self.handler:
            self.handler.packages.add([line])

    def handleCommand (self, lineno, args):
        """Given the list of command and arguments, call the Version's
           dispatcher method to handle the command.  This method may be
           overridden in a subclass if necessary.
        """
        if self.handler:
            self.handler.currentCmd = args[0]
            self.handler.currentLine = self._line
            self.handler.dispatcher(args, lineno)

    def handlePackageHdr (self, lineno, args):
        """Process the arguments to the %packages header and set attributes
           on the Version's Packages instance appropriate.  This method may be
           overridden in a subclass if necessary.
        """
        op = KSOptionParser(lineno=lineno, version=self.version)
        op.add_option("--excludedocs", dest="excludedocs", action="store_true",
                      default=False, deprecated=FC6)
        op.add_option("--ignoremissing", dest="ignoremissing",
                      action="store_true", default=False)
        op.add_option("--nobase", dest="nobase", action="store_true",
                      default=False)
        op.add_option("--ignoredeps", dest="resolveDeps", action="store_false",
                      deprecated=FC4)
        op.add_option("--resolvedeps", dest="resolveDeps", action="store_true",
                      deprecated=FC4)
        op.add_option("--default", dest="defaultPackages", action="store_true",
                      default=False, introduced=F7)

        (opts, extra) = op.parse_args(args=args[1:])

        self.handler.packages.excludeDocs = opts.excludedocs
        self.handler.packages.addBase = not opts.nobase
        if opts.ignoremissing:
            self.handler.packages.handleMissing = KS_MISSING_IGNORE
        else:
            self.handler.packages.handleMissing = KS_MISSING_PROMPT

        if opts.defaultPackages:
            self.handler.packages.default = True

    def handleScriptHdr (self, lineno, args):
        """Process the arguments to a %pre/%post/%traceback header for later
           setting on a Script instance once the end of the script is found.
           This method may be overridden in a subclass if necessary.
        """
        op = KSOptionParser(lineno=lineno, version=self.version)
        op.add_option("--erroronfail", dest="errorOnFail", action="store_true",
                      default=False)
        op.add_option("--interpreter", dest="interpreter", default="/bin/sh")
        op.add_option("--log", "--logfile", dest="log")

        if args[0] == "%pre" or args[0] == "%traceback":
            self._script["chroot"] = False
        elif args[0] == "%post":
            self._script["chroot"] = True
            op.add_option("--nochroot", dest="nochroot", action="store_true",
                          default=False)

        (opts, extra) = op.parse_args(args=args[1:])

        self._script["interp"] = opts.interpreter
        self._script["log"] = opts.log
        self._script["errorOnFail"] = opts.errorOnFail
        if hasattr(opts, "nochroot"):
            self._script["chroot"] = not opts.nochroot

    def _stateMachine (self, provideLineFn):
        # For error reporting.
        lineno = 0
        needLine = True

        while True:
            if needLine:
                try:
                    self._line = provideLineFn()
                except StopIteration:
                    break

                lineno += 1
                needLine = False

            # At the end of an included file
            if self._line == "" and self._includeDepth > 0:
                break

            # Don't eliminate whitespace or comments from scripts.
            if self._line.isspace() or (self._line != "" and self._line.lstrip()[0] == '#'):
                # Save the platform for s-c-kickstart, though.
                if self._line[:10] == "#platform=" and self._state == STATE_COMMANDS:
                    self.handler.platform = self._line[11:]

                if self._state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                    self._script["body"].append(self._line)

                needLine = True
                continue

            # We only want to split the line if we're outside of a script,
            # as inside the script might involve some pretty weird quoting
            # that shlex doesn't understand.
            if self._state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                # Have we found a state transition?  If so, we still want
                # to split.  Otherwise, args won't be set but we'll fall through
                # all the way to the last case.
                if self._line != "" and string.split(self._line.lstrip())[0] in \
                   ["%post", "%pre", "%traceback", "%include", "%packages", "%ksappend"]:
                    args = shlex.split(self._line)
                else:
                    args = None
            else:
                args = shlex.split(self._line)

            if args and args[0] == "%include":
                # This case comes up primarily in ksvalidator.
                if not self.followIncludes:
                    needLine = True
                    continue

                if not args[1]:
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    self._includeDepth += 1

                    try:
                        self.readKickstart (args[1], reset=False)
                    except IOError:
                        # Handle the include file being provided over the
                        # network in a %pre script.  This case comes up in the
                        # early parsing in anaconda.
                        if self.missingIncludeIsFatal:
                            raise

                    self._includeDepth -= 1
                    needLine = True
                    continue

            if self._state == STATE_COMMANDS:
                if not args and self._includeDepth == 0:
                    self._state = STATE_END
                elif args[0] == "%ksappend":
                    needLine = True
                    continue
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self._state = STATE_SCRIPT_HDR
                elif args[0] == "%packages":
                    self._state = STATE_PACKAGES
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

            elif self._state == STATE_PACKAGES:
                if not args and self._includeDepth == 0:
                    self._state = STATE_END
                elif args[0] == "%ksappend":
                    needLine = True
                    continue
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self._state = STATE_SCRIPT_HDR
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
                    self.addPackages (string.rstrip(self._line))

            elif self._state == STATE_SCRIPT_HDR:
                needLine = True
                self._script = {"body": [], "interp": "/bin/sh", "log": None,
                                "errorOnFail": False}

                if not args and self._includeDepth == 0:
                    self._state = STATE_END
                elif args[0] == "%pre":
                    self._state = STATE_PRE
                    self._script["type"] = KS_SCRIPT_PRE
                elif args[0] == "%post":
                    self._state = STATE_POST
                    self._script["type"] = KS_SCRIPT_POST
                elif args[0] == "%traceback":
                    self._state = STATE_TRACEBACK
                    self._script["type"] = KS_SCRIPT_TRACEBACK
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

            elif self._state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                if self._line == "" and self._includeDepth == 0:
                    # If we're at the end of the kickstart file, add the script.
                    self.addScript()
                    self._state = STATE_END
                elif args and args[0] in ["%pre", "%post", "%traceback", "%packages", "%ksappend"]:
                    # Otherwise we're now at the start of the next section.
                    # Figure out what kind of a script we just finished
                    # reading, add it to the list, and switch to the initial
                    # state.
                    self.addScript()
                    self._state = STATE_COMMANDS
                else:
                    # Otherwise just add to the current script body.
                    self._script["body"].append(self._line)
                    needLine = True

            elif self._state == STATE_END:
                break

    def readKickstartFromString (self, str, reset=True):
        """Process a kickstart file, provided as the string str."""
        if reset:
            self._reset()

        i = iter(str.splitlines(True))
        self._stateMachine (lambda: i.next())

    def readKickstart (self, file, reset=True):
        """Process a kickstart file, given by the filename file."""
        if reset:
            self._reset()

        fh = urlopen(file)
        self._stateMachine (lambda: fh.readline())
        fh.close()
