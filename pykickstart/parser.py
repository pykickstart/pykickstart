#
# parser.py:  Kickstart file parser.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
Main kickstart file processing module.

This module exports several important classes:

    Script - Representation of a single %pre, %post, or %traceback script.

    Packages - Representation of the %packages section.

    KickstartParser - The kickstart file parser state machine.
"""

import os
import shlex
import sys
import tempfile
from copy import copy
from optparse import *
from urlgrabber import urlopen
import urlgrabber.grabber as grabber

from constants import *
from errors import *
from ko import *
from options import *
from version import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

STATE_END = 0
STATE_COMMANDS = 1
STATE_PACKAGES = 2
STATE_SCRIPT_HDR = 3
STATE_SCRIPT = 4

# FIXME:  This is a hack until I have time to think about making the parser
# itself support multiple syntax versions.  Yes, I know this means it will
# never be fixed.
ver = DEVEL

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
        if not ll.startswith("%ksappend"):
            os.write(outF, l)
            continue

        # Try to pull down the remote file.
        try:
            ksurl = ll.split(' ')[1]
        except:
            raise KickstartParseError, formatErrorMsg(lineno, msg=_("Illegal url for %%ksappend: %s") % ll)

        try:
            url = grabber.urlopen(ksurl)
        except grabber.URLGrabError, e:
            raise KickstartError, formatErrorMsg(lineno, msg=_("Unable to open %%ksappend file: %s") % e.strerror)
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

def preprocessFromString (s):
    """Preprocess the kickstart file, provided as the string str.  This
        method is currently only useful for handling %ksappend lines,
        which need to be fetched before the real kickstart parser can be
        run.  Returns the location of the complete kickstart file.
    """
    i = iter(s.splitlines(True) + [""])
    rc = _preprocessStateMachine (lambda: i.next())
    return rc

def preprocessKickstart (f):
    """Preprocess the kickstart file, given by the filename file.  This
        method is currently only useful for handling %ksappend lines,
        which need to be fetched before the real kickstart parser can be
        run.  Returns the location of the complete kickstart file.
    """
    try:
        fh = urlopen(f)
    except grabber.URLGrabError, e:
        raise KickstartError, formatErrorMsg(0, msg=_("Unable to open input kickstart file: %s") % e.strerror)

    rc = _preprocessStateMachine (lambda: fh.readline())
    fh.close()
    return rc

###
### SCRIPT HANDLING
###
class Script(KickstartObject):
    """A class representing a single kickstart script.  If functionality beyond
       just a data representation is needed (for example, a run method in
       anaconda), Script may be subclassed.  Although a run method is not
       provided, most of the attributes of Script have to do with running the
       script.  Instances of Script are held in a list by the Version object.
    """
    def __init__(self, script, *args , **kwargs):
        """Create a new Script instance.  Instance attributes:

           errorOnFail -- If execution of the script fails, should anaconda
                          stop, display an error, and then reboot without
                          running any other scripts?
           inChroot    -- Does the script execute in anaconda's chroot
                          environment or not?
           interp      -- The program that should be used to interpret this
                          script.
           lineno      -- The line number this script starts on.
           logfile     -- Where all messages from the script should be logged.
           script      -- A string containing all the lines of the script.
           type        -- The type of the script, which can be KS_SCRIPT_* from
                          pykickstart.constants.
        """
        KickstartObject.__init__(self, *args, **kwargs)
        self.script = "".join(script)

        self.interp = kwargs.get("interp", "/bin/sh")
        self.inChroot = kwargs.get("inChroot", False)
        self.lineno = kwargs.get("lineno", None)
        self.logfile = kwargs.get("logfile", None)
        self.errorOnFail = kwargs.get("errorOnFail", False)
        self.type = kwargs.get("type", KS_SCRIPT_PRE)

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        if self.preceededInclude is not None:
            retval = "\n%%include %s\n" % self.preceededInclude
        else:
            retval = ""

        if self.type == KS_SCRIPT_PRE:
            retval += '\n%pre'
        elif self.type == KS_SCRIPT_POST:
            retval += '\n%post'
        elif self.type == KS_SCRIPT_TRACEBACK:
            retval += '\n%traceback'

        if self.interp != "/bin/sh" and self.interp != "":
            retval += " --interpreter=%s" % self.interp
        if self.type == KS_SCRIPT_POST and not self.inChroot:
            retval += " --nochroot"
        if self.logfile != None:
            retval += " --logfile %s" % self.logfile
        if self.errorOnFail:
            retval += " --erroronfail"

        if self.script.endswith("\n"):
            if ver >= F8:
                return retval + "\n%s%%end\n" % self.script
            else:
                return retval + "\n%s\n" % self.script
        else:
            if ver >= F8:
                return retval + "\n%s\n%%end\n" % self.script
            else:
                return retval + "\n%s\n" % self.script


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

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name > other.name:
            return 1
        return 0

class Packages(KickstartObject):
    """A class representing the %packages section of the kickstart file."""
    def __init__(self, *args, **kwargs):
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
           excludedGroupList -- A list of Group objects representing all the
                                groups specified for removal in the %packages
                                section.  Names will be stripped of the leading
                                -@ symbols.
           handleMissing -- If unknown packages are specified in the %packages
                            section, should it be ignored or not?  Values can
                            be KS_MISSING_* from pykickstart.constants.
           packageList   -- A list of all the packages specified in the
                            %packages section.
           instLangs     -- A list of languages to install.
        """
        KickstartObject.__init__(self, *args, **kwargs)

        self.addBase = True
        self.default = False
        self.excludedList = []
        self.excludedGroupList = []
        self.excludeDocs = False
        self.groupList = []
        self.handleMissing = KS_MISSING_PROMPT
        self.packageList = []
        self.instLangs = None

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        pkgs = ""

        if not self.default:
            grps = self.groupList
            grps.sort()
            for grp in grps:
                pkgs += "%s\n" % grp.__str__()

            p = self.packageList
            p.sort()
            for pkg in p:
                pkgs += "%s\n" % pkg

            grps = self.excludedGroupList
            grps.sort()
            for grp in grps:
                pkgs += "-%s\n" % grp.__str__()

            p = self.excludedList
            p.sort()
            for pkg in p:
                pkgs += "-%s\n" % pkg

            if pkgs == "":
                return ""

        if self.preceededInclude is not None:
            retval = "\n%%include %s\n" % self.preceededInclude
        else:
            retval = ""

        retval += "\n%packages"

        if self.default:
            retval += " --default"
        if self.excludeDocs:
            retval += " --excludedocs"
        if not self.addBase:
            retval += " --nobase"
        if self.handleMissing == KS_MISSING_IGNORE:
            retval += " --ignoremissing"
        if self.instLangs:
            retval += " --instLangs=%s" % self.instLangs

        if ver >= F8:
            return retval + "\n" + pkgs + "\n%end\n"
        else:
            return retval + "\n" + pkgs + "\n"

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
        existingExcludedSet = set(self.excludedList)
        existingPackageSet = set(self.packageList)
        newExcludedSet = set()
        newPackageSet = set()

        excludedGroupList = []

        for pkg in pkgList:
            stripped = pkg.strip()

            if stripped[0] == "@":
                self._processGroup(stripped[1:])
            elif stripped[0] == "-":
                if stripped[1] == "@":
                    excludedGroupList.append(Group(name=stripped[2:]))
                else:
                    newExcludedSet.add(stripped[1:])
            else:
                newPackageSet.add(stripped)

        # Groups have to be excluded in two different ways (note: can't use
        # sets here because we have to store objects):
        excludedGroupNames = map(lambda g: g.name, excludedGroupList)

        # First, an excluded group may be cancelling out a previously given
        # one.  This is often the case when using %include.  So there we should
        # just remove the group from the list.
        self.groupList = filter(lambda g: g.name not in excludedGroupNames, self.groupList)

        # Second, the package list could have included globs which are not
        # processed by pykickstart.  In that case we need to preserve a list of
        # excluded groups so whatever tool doing package/group installation can
        # take appropriate action.
        self.excludedGroupList.extend(excludedGroupList)

        existingPackageSet = (existingPackageSet - newExcludedSet) | newPackageSet
        existingExcludedSet = (existingExcludedSet - existingPackageSet) | newExcludedSet

        self.packageList = list(existingPackageSet)
        self.excludedList = list(existingExcludedSet)


###
### PARSER
###
class KickstartParser:
    """The kickstart file parser class as represented by a basic state
       machine.  To create a specialized parser, make a subclass and override
       any of the methods you care about.  Methods that don't need to do
       anything may just pass.  However, _stateMachine should never be
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
        self.currentdir = {}
        self.missingIncludeIsFatal = missingIncludeIsFatal
        self._reset()

        self._line = ""

        self.version = self.handler.version

        global ver
        ver = self.version

    def _reset(self):
        """Reset the internal variables of the state machine for a new kickstart file."""
        self._state = STATE_COMMANDS
        self._script = None
        self._includeDepth = 0
        self._preceededInclude = None

    def addScript (self):
        """Create a new Script instance and add it to the Version object.  This
           is called when the end of a script section is seen and may be
           overridden in a subclass if necessary.
        """
        if " ".join(self._script["body"]).strip() == "":
            return

        kwargs = {"interp": self._script["interp"],
                  "inChroot": self._script["chroot"],
                  "lineno": self._script["lineno"],
                  "logfile": self._script["log"],
                  "errorOnFail": self._script["errorOnFail"],
                  "type": self._script["type"]}

        if self._preceededInclude is not None:
            kwargs["preceededInclude"] = self._preceededInclude
            self._preceededInclude = None

        s = Script (self._script["body"], **kwargs)

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
           dispatcher method to handle the command.  Returns the command or
           data object returned by the dispatcher.  This method may be
           overridden in a subclass if necessary.
        """
        if self.handler:
            self.handler.currentCmd = args[0]
            self.handler.currentLine = self._line
            retval = self.handler.dispatcher(args, lineno, self._preceededInclude)
            self._preceededInclude = None

            return retval

    def handlePackageHdr (self, lineno, args):
        """Process the arguments to the %packages header and set attributes
           on the Version's Packages instance appropriate.  This method may be
           overridden in a subclass if necessary.
        """
        op = KSOptionParser(version=self.version)
        op.add_option("--excludedocs", dest="excludedocs", action="store_true",
                      default=False)
        op.add_option("--ignoremissing", dest="ignoremissing",
                      action="store_true", default=False)
        op.add_option("--nobase", dest="nobase", action="store_true",
                      default=False)
        op.add_option("--ignoredeps", dest="resolveDeps", action="store_false",
                      deprecated=FC4, removed=F9)
        op.add_option("--resolvedeps", dest="resolveDeps", action="store_true",
                      deprecated=FC4, removed=F9)
        op.add_option("--default", dest="defaultPackages", action="store_true",
                      default=False, introduced=F7)
        op.add_option("--instLangs", dest="instLangs", type="string",
                      default="", introduced=F9)

        (opts, extra) = op.parse_args(args=args[1:], lineno=lineno)

        self.handler.packages.excludeDocs = opts.excludedocs
        self.handler.packages.addBase = not opts.nobase
        if opts.ignoremissing:
            self.handler.packages.handleMissing = KS_MISSING_IGNORE
        else:
            self.handler.packages.handleMissing = KS_MISSING_PROMPT

        if opts.defaultPackages:
            self.handler.packages.default = True

        if opts.instLangs:
            self.handler.packages.instLangs = opts.instLangs

        if self._preceededInclude is not None:
            self.handler.packages.preceededInclude = self._preceededInclude
            self._preceededInclude = None

    def handleScriptHdr (self, lineno, args):
        """Process the arguments to a %pre/%post/%traceback header for later
           setting on a Script instance once the end of the script is found.
           This method may be overridden in a subclass if necessary.
        """
        op = KSOptionParser(version=self.version)
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

        (opts, extra) = op.parse_args(args=args[1:], lineno=lineno)

        self._script["interp"] = opts.interpreter
        self._script["lineno"] = lineno
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

                if self._state == STATE_SCRIPT:
                    self._script["body"].append(self._line)

                needLine = True
                continue

            # We only want to split the line if we're outside of a script,
            # as inside the script might involve some pretty weird quoting
            # that shlex doesn't understand.
            if self._state == STATE_SCRIPT:
                # Have we found a state transition?  If so, we still want
                # to split.  Otherwise, args won't be set but we'll fall through
                # all the way to the last case.
                if self._line != "" and self._line.lstrip().split()[0] in \
                   ["%end", "%post", "%pre", "%traceback", "%include", "%packages", "%ksappend"]:
                    args = shlex.split(self._line)
                else:
                    args = None
            else:
                # Remove any end-of-line comments.
                ind = self._line.find("#")
                if (ind > -1):
                    h = self._line[:ind]
                else:
                    h = self._line

                self._line = h.rstrip()
                args = shlex.split(self._line)

            if args and args[0] == "%include":
                self._preceededInclude = args[1]

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
                    except KickstartError:
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
                    if self.version >= F8:
                        raise KickstartParseError, formatErrorMsg(lineno, msg=_("Section does not end with %%end."))

                    self._state = STATE_END
                elif args[0] == "%end":
                    self._state = STATE_COMMANDS
                    needLine = True
                elif args[0] == "%ksappend":
                    needLine = True
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
                    self.addPackages(self._line.rstrip())

            elif self._state == STATE_SCRIPT_HDR:
                needLine = True
                self._script = {"body": [], "interp": "/bin/sh", "log": None,
                                "errorOnFail": False, lineno: None}

                if not args and self._includeDepth == 0:
                    self._state = STATE_END
                elif args[0] == "%pre":
                    self._state = STATE_SCRIPT
                    self._script["type"] = KS_SCRIPT_PRE
                elif args[0] == "%post":
                    self._state = STATE_SCRIPT
                    self._script["type"] = KS_SCRIPT_POST
                elif args[0] == "%traceback":
                    self._state = STATE_SCRIPT
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

            elif self._state == STATE_SCRIPT:
                if self._line in ["%end", ""] and self._includeDepth == 0:
                    if self._line == "" and self.version >= F8:
                        raise KickstartParseError, formatErrorMsg(lineno, msg=_("Section does not end with %%end."))

                    # If we're at the end of the kickstart file, add the script.
                    self.addScript()
                    self._state = STATE_END
                elif args and args[0] in ["%end", "%pre", "%post", "%traceback", "%packages", "%ksappend"]:
                    # Otherwise we're now at the start of the next section.
                    # Figure out what kind of a script we just finished
                    # reading, add it to the list, and switch to the initial
                    # state.
                    self.addScript()
                    self._state = STATE_COMMANDS

                    if args[0] == "%end":
                        needLine = True
                else:
                    # Otherwise just add to the current script body.
                    self._script["body"].append(self._line)
                    needLine = True

            elif self._state == STATE_END:
                break

    def readKickstartFromString (self, s, reset=True):
        """Process a kickstart file, provided as the string str."""
        if reset:
            self._reset()

        # Add a "" to the end of the list so the string reader acts like the
        # file reader and we only get StopIteration when we're after the final
        # line of input.
        i = iter(s.splitlines(True) + [""])
        self._stateMachine (lambda: i.next())

    def readKickstart(self, f, reset=True):
        """Process a kickstart file, given by the filename f."""
        if reset:
            self._reset()

        # an %include might not specify a full path.  if we don't try to figure
        # out what the path should have been, then we're unable to find it
        # requiring full path specification, though, sucks.  so let's make
        # the reading "smart" by keeping track of what the path is at each
        # include depth.
        if not os.path.exists(f):
            if self.currentdir.has_key(self._includeDepth - 1):
                if os.path.exists(os.path.join(self.currentdir[self._includeDepth - 1], f)):
                    f = os.path.join(self.currentdir[self._includeDepth - 1], f)

        cd = os.path.dirname(f)
        if not cd.startswith("/"):
            cd = os.path.abspath(cd)
        self.currentdir[self._includeDepth] = cd

        try:
            fh = urlopen(f)
        except grabber.URLGrabError, e:
            raise KickstartError, formatErrorMsg(0, msg=_("Unable to open input kickstart file: %s") % e.strerror)

        self._stateMachine (lambda: fh.readline())
        fh.close()
