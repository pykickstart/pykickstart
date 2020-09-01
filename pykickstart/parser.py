#
# parser.py:  Kickstart file parser.
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
Main kickstart file processing module.

This module exports several important classes:

    Script - Representation of a single %pre, %pre-install, %post, or %traceback script.

    Packages - Representation of the %packages section.

    KickstartParser - The kickstart file parser state machine.
"""

from __future__ import print_function

try:
    from collections.abc import Iterator
except ImportError:  # python2 compatibility
    from collections import Iterator

import os
import six
import shlex
import sys
import warnings

from pykickstart import constants, version
from pykickstart.errors import KickstartError, KickstartParseError, KickstartParseWarning
from pykickstart.ko import KickstartObject
from pykickstart.load import load_to_str
from pykickstart.options import KSOptionParser
from pykickstart.sections import PackageSection, PreScriptSection, PreInstallScriptSection, \
                                 PostScriptSection, TracebackScriptSection, OnErrorScriptSection, \
                                 NullSection

from pykickstart.i18n import _

STATE_END = "end"
STATE_COMMANDS = "commands"

def _preprocessStateMachine(lineIter):
    l = None
    lineno = 0
    retval = ""

    if six.PY3:
        retval = retval.encode(sys.getdefaultencoding())

    while True:
        try:
            l = next(lineIter)
        except StopIteration:
            break

        # At the end of the file?
        if l == "":
            break

        lineno += 1
        ksurl = None

        ll = l.strip()
        if not ll.startswith("%ksappend"):
            if six.PY3:
                l = l.encode(sys.getdefaultencoding())
            retval += l
            continue

        # Try to pull down the remote file.
        try:
            ksurl = ll.split(' ')[1]
        except:
            raise KickstartParseError(_("Illegal url for %%ksappend: %s") % ll, lineno=lineno)

        try:
            contents = load_to_str(ksurl)
        except KickstartError as e:
            raise KickstartError(_("Unable to open %%ksappend file: %s") % str(e), lineno=lineno)

        # If that worked, write the remote file to the output kickstart
        # file in one burst.  This allows multiple %ksappend lines to
        # exist.
        if contents is not None:
            retval += contents.encode(sys.getdefaultencoding())

    return retval

def preprocessFromStringToString(s):
    """Preprocess the kickstart file, provided as the string s.  This
       method is currently only useful for handling %ksappend lines, which
       need to be fetched before the real kickstart parser can be run.
       Returns the complete kickstart file as a string.
    """
    i = iter(s.splitlines(True) + [""])
    return _preprocessStateMachine(i)

def preprocessKickstartToString(f):
    """Preprocess the kickstart file, given by the filename f.  This
       method is currently only useful for handling %ksappend lines,
       which need to be fetched before the real kickstart parser can be
       run.  Returns the complete kickstart file as a string.
    """
    try:
        contents = load_to_str(f)
    except KickstartError as e:
        raise KickstartError(_("Unable to open input kickstart file: %s") % str(e), lineno=0)

    return _preprocessStateMachine(iter(contents.splitlines(True)))

def preprocessFromString(s):
    """Preprocess the kickstart file, provided as the string s.  This
       method is currently only useful for handling %ksappend lines,
       which need to be fetched before the real kickstart parser can be
       run.  Returns the location of the complete kickstart file.
    """
    s = preprocessFromStringToString(s)
    if s:
        import tempfile
        (outF, outName) = tempfile.mkstemp(suffix="-ks.cfg")

        os.write(outF, s)
        os.close(outF)
        return outName

    return None

def preprocessKickstart(f):
    """Preprocess the kickstart file, given by the filename f.  This
       method is currently only useful for handling %ksappend lines,
       which need to be fetched before the real kickstart parser can be
       run.  Returns the location of the complete kickstart file.
    """
    s = preprocessKickstartToString(f)
    if s:
        import tempfile
        (outF, outName) = tempfile.mkstemp(suffix="-ks.cfg")

        os.write(outF, s)
        os.close(outF)
        return outName

    return None

class PutBackIterator(Iterator):
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._buf = None

    def __iter__(self):
        return self

    def put(self, s):
        self._buf = s

    def next(self):
        if self._buf:
            retval = self._buf
            self._buf = None
            return retval
        else:
            return next(self._iterable)

    def __next__(self):
        return self.next()                          # pylint: disable=not-callable

###
### SCRIPT HANDLING
###
class Script(KickstartObject):
    _ver = version.DEVEL

    """A class representing a single kickstart script.  If functionality beyond
       just a data representation is needed (for example, a run method in
       anaconda), Script may be subclassed.  Although a run method is not
       provided, most of the attributes of Script have to do with running the
       script.  Instances of Script are held in a list by the Version object.
    """
    def __init__(self, script, *args, **kwargs):
        """Create a new Script instance.  Instance attributes:

           :keyword errorOnFail: If execution of the script fails, should anaconda
                                 stop, display an error, and then reboot without
                                 running any other scripts?

           :keyword inChroot: Does the script execute in anaconda's chroot
                              environment or not?

           :keyword interp: The program that should be used to interpret this
                            script.

           :keyword lineno: The line number this script starts on.

           :keyword logfile: Where all messages from the script should be logged.

           :keyword script: A string containing all the lines of the script.

           :keyword type: The type of the script, which can be KS_SCRIPT_* from
                          :mod:`pykickstart.constants`.
        """
        KickstartObject.__init__(self, *args, **kwargs)
        self.script = "".join(script)

        self.interp = kwargs.get("interp", "/bin/sh")
        self.inChroot = kwargs.get("inChroot", False)
        self.lineno = kwargs.get("lineno", None)
        self.logfile = kwargs.get("logfile", None)
        self.errorOnFail = kwargs.get("errorOnFail", False)
        self.type = kwargs.get("type", constants.KS_SCRIPT_PRE)

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        retval = ""

        if self.type == constants.KS_SCRIPT_PRE:
            retval += '\n%pre'
        elif self.type == constants.KS_SCRIPT_POST:
            retval += '\n%post'
        elif self.type == constants.KS_SCRIPT_TRACEBACK:
            retval += '\n%traceback'
        elif self.type == constants.KS_SCRIPT_PREINSTALL:
            retval += '\n%pre-install'
        elif self.type == constants.KS_SCRIPT_ONERROR:
            retval += '\n%onerror'

        if self.interp != "/bin/sh" and self.interp:
            retval += " --interpreter=%s" % self.interp
        if self.type == constants.KS_SCRIPT_POST and not self.inChroot:
            retval += " --nochroot"
        if self.logfile is not None:
            retval += " --logfile=%s" % self.logfile
        if self.errorOnFail:
            retval += " --erroronfail"

        if self.script.endswith("\n"):
            if self._ver >= version.F8:
                return retval + "\n%s%%end\n" % self.script
            else:
                return retval + "\n%s" % self.script
        else:
            if self._ver >= version.F8:
                return retval + "\n%s\n%%end\n" % self.script
            else:
                return retval + "\n%s\n" % self.script

##
## PACKAGE HANDLING
##
class Group(KickstartObject):
    """A class representing a single group in the %packages section."""
    def __init__(self, name="", include=constants.GROUP_DEFAULT):
        """Create a new Group instance.  Instance attributes:

           name    -- The group's identifier
           include -- The level of how much of the group should be included.
                      Values can be GROUP_* from pykickstart.constants.
        """
        KickstartObject.__init__(self)
        self.name = name
        self.include = include

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        if self.include == constants.GROUP_REQUIRED:
            return "@%s --nodefaults" % self.name
        elif self.include == constants.GROUP_ALL:
            return "@%s --optional" % self.name
        else:
            return "@%s" % self.name

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __gt__(self, other):
        return self.name > other.name

    def __ge__(self, other):
        return self.name >= other.name

    __hash__ = KickstartObject.__hash__

class Packages(KickstartObject):
    _ver = version.DEVEL

    """A class representing the %packages section of the kickstart file."""
    def __init__(self, *args, **kwargs):
        """Create a new Packages instance.  Instance attributes:

           addBase       -- Should the Base group be installed even if it is
                            not specified?
           nocore        -- Should the Core group be skipped?  This results in
                            a %packages section that basically only installs the
                            packages you list, and may not be a usable system.
           default       -- Should the default package set be selected?
           environment   -- What base environment should be selected?  Only one
                            may be chosen at a time.
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
           handleBroken  -- If packages with conflicts are specified in the
                            %packages section, should it be ignored or not?
                            Values can be KS_BROKEN_* from pykickstart.constants.
           packageList   -- A list of all the packages specified in the
                            %packages section.
           instLangs     -- A list of languages to install.
           multiLib      -- Whether to use yum's "all" multilib policy.
           excludeWeakdeps -- Whether to exclude weak dependencies.
           timeout       -- Number of seconds to wait for a connection before
                            yum's or dnf's timing out or None.
           retries       -- Number of times yum's or dnf's attempt to retrieve
                            a file should retry before returning an error.
           seen          -- If %packages was ever used in the kickstart file,
                            this attribute will be set to True.

        """
        KickstartObject.__init__(self, *args, **kwargs)

        self.addBase = True
        self.nocore = False
        self.default = False
        self.environment = None
        self.excludedList = []
        self.excludedGroupList = []
        self.excludeDocs = False
        self.groupList = []
        self.handleMissing = constants.KS_MISSING_PROMPT
        self.handleBroken = constants.KS_BROKEN_REPORT
        self.packageList = []
        self.instLangs = None
        self.multiLib = False
        self.excludeWeakdeps = False
        self.timeout = None
        self.retries = None
        self.seen = False

    def __str__(self):
        """Return a string formatted for output to a kickstart file."""
        pkgs = self._processPackagesContent()
        retval = ""

        if self.default:
            retval += " --default"
        if self.excludeDocs:
            retval += " --excludedocs"
        if not self.addBase:
            retval += " --nobase"
        if self.nocore:
            retval += " --nocore"
        if self.handleMissing == constants.KS_MISSING_IGNORE:
            retval += " --ignoremissing"
        if self.handleBroken == constants.KS_BROKEN_IGNORE:
            retval += " --ignorebroken"
        if self.instLangs is not None:
            retval += " --inst-langs=%s" % self.instLangs
        if self.multiLib:
            retval += " --multilib"
        if self.excludeWeakdeps:
            retval += " --exclude-weakdeps"
        if self.timeout is not None:
            retval += " --timeout=%d" % self.timeout
        if self.retries is not None:
            retval += " --retries=%d" % self.retries

        if retval == "" and pkgs == "" and not self.seen:
            return ""

        if self._ver >= version.F8:
            return "\n%packages" + retval + "\n" + pkgs + "\n%end\n"
        else:
            return "\n%packages" + retval + "\n" + pkgs + "\n"

    def _processPackagesContent(self):
        pkgs = ""

        if not self.default:
            if self.environment:
                pkgs += "@^%s\n" % self.environment

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

        return pkgs

    def _processGroup(self, line):
        op = KSOptionParser(prog="", description="", version=version.DEVEL)
        op.add_argument("--nodefaults", action="store_true", default=False,
                        help="", version=version.DEVEL)
        op.add_argument("--optional", action="store_true", default=False,
                        help="", version=version.DEVEL)

        (ns, extra) = op.parse_known_args(args=line.split())

        if ns.nodefaults and ns.optional:
            raise KickstartParseError(_("Group cannot specify both --nodefaults and --optional"))

        # If the group name has spaces in it, we have to put it back together
        # now.
        grp = " ".join(extra)

        if grp in [g.name for g in self.groupList]:
            return

        if ns.nodefaults:
            self.groupList.append(Group(name=grp, include=constants.GROUP_REQUIRED))
        elif ns.optional:
            self.groupList.append(Group(name=grp, include=constants.GROUP_ALL))
        else:
            self.groupList.append(Group(name=grp, include=constants.GROUP_DEFAULT))

    def add(self, pkgList):
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

            if stripped[0:2] == "@^":
                self.environment = stripped[2:]
            elif stripped[0] == "@":
                self._processGroup(stripped[1:])
            elif stripped[0] == "-":
                if stripped[1:3] == "@^" and self.environment == stripped[3:]:
                    self.environment = None
                elif stripped[1] == "@":
                    excludedGroupList.append(Group(name=stripped[2:]))
                else:
                    newExcludedSet.add(stripped[1:])
            else:
                newPackageSet.add(stripped)

        # Groups have to be excluded in two different ways (note: can't use
        # sets here because we have to store objects):
        excludedGroupNames = [g.name for g in excludedGroupList]

        # First, an excluded group may be cancelling out a previously given
        # one.  This is often the case when using %include.  So there we should
        # just remove the group from the list.
        self.groupList = [g for g in self.groupList if g.name not in excludedGroupNames]

        # Second, the package list could have included globs which are not
        # processed by pykickstart.  In that case we need to preserve a list of
        # excluded groups so whatever tool doing package/group installation can
        # take appropriate action.
        self.excludedGroupList.extend(excludedGroupList)

        existingPackageSet = (existingPackageSet - newExcludedSet) | newPackageSet
        existingExcludedSet = (existingExcludedSet - existingPackageSet) | newExcludedSet

        # FIXME: figure these types out
        self.packageList = sorted(existingPackageSet)
        self.excludedList = sorted(existingExcludedSet)

###
### PARSER
###
class KickstartParser(object):
    """The kickstart file parser class as represented by a basic state
       machine.  To create a specialized parser, make a subclass and override
       any of the methods you care about.  Methods that don't need to do
       anything may just pass.  However, _stateMachine should never be
       overridden.
    """
    def __init__(self, handler, followIncludes=True, errorsAreFatal=True,
                 missingIncludeIsFatal=True, unknownSectionIsFatal=True):
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
           unknownSectionIsFatal -- Should an unknown %section be fatal?  Not all
                                    sections are handled by pykickstart.  Some are
                                    user-defined, so there should be a way to have
                                    pykickstart ignore them.
        """
        self.errorsAreFatal = errorsAreFatal
        self.errorsCount = 0
        self.followIncludes = followIncludes
        self.handler = handler
        self.currentdir = {}
        self.missingIncludeIsFatal = missingIncludeIsFatal
        self.unknownSectionIsFatal = unknownSectionIsFatal

        self._state = STATE_COMMANDS
        self._includeDepth = 0
        self._line = ""

        self.version = self.handler.version
        Script._ver = self.version
        Packages._ver = self.version

        self._sections = {}
        self.setupSections()

    def _reset(self):
        """Reset the internal variables of the state machine for a new kickstart file."""
        self._state = STATE_COMMANDS
        self._includeDepth = 0

    def getSection(self, s):
        """Return a reference to the requested section (s must start with '%'s),
           or raise KeyError if not found.
        """
        return self._sections[s]

    def handleCommand(self, lineno, args):
        """Given the list of command and arguments, call the Version's
           dispatcher method to handle the command.  Returns the command or
           data object returned by the dispatcher.  This method may be
           overridden in a subclass if necessary.
        """
        if self.handler:
            self.handler.currentLine = self._line
            retval = self.handler.dispatcher(args, lineno)
            return retval

    def registerSection(self, obj):
        """Given an instance of a Section subclass, register the new section
           with the parser.  Calling this method means the parser will
           recognize your new section and dispatch into the given object to
           handle it.
        """
        if not obj.sectionOpen:
            raise TypeError("no sectionOpen given for section %s" % obj)

        if not obj.sectionOpen.startswith("%"):
            raise TypeError("section %s tag does not start with a %%" % obj.sectionOpen)

        self._sections[obj.sectionOpen] = obj

    def _finalize(self, obj):
        """Called at the close of a kickstart section to take any required
           actions.  Internally, this is used to add scripts once we have the
           whole body read.
        """
        obj.finalize()
        self._state = STATE_COMMANDS

    def _handleSpecialComments(self, line):
        """Kickstart recognizes a couple special comments."""
        if self._state != STATE_COMMANDS:
            return

        # Save the platform for s-c-kickstart.
        if line[:10] == "#platform=":
            self.handler.platform = self._line[10:].strip()

    def _readSection(self, lineIter, lineno):
        obj = self._sections[self._state]

        while True:
            try:
                line = next(lineIter)
                if line == "" and self._includeDepth == 0:
                    # This section ends at the end of the file.
                    if self.version >= version.F8:
                        raise KickstartParseError(_("Section %s does not end with %%end.") % obj.sectionOpen, lineno=lineno)

                    self._finalize(obj)
            except StopIteration:
                break

            lineno += 1

            # Throw away blank lines and comments, unless the section wants all
            # lines.
            if self._isBlankOrComment(line) and not obj.allLines:
                continue

            if line.lstrip().startswith("%"):
                # If we're in a script, the line may begin with "%something"
                # that's not the start of any section we recognize, but still
                # valid for that script.  So, don't do the split below unless
                # we're sure.
                possibleSectionStart = line.split()[0]
                if not self._validState(possibleSectionStart) \
                   and possibleSectionStart not in ("%end", "%include"):
                    obj.handleLine(line)
                    continue

                args = shlex.split(line)

                if args and args[0] == "%end":
                    # This is a properly terminated section.
                    self._finalize(obj)
                    break
                elif args and args[0] == "%include":
                    if len(args) == 1 or not args[1]:
                        raise KickstartParseError(lineno=lineno)

                    self._handleInclude(args[1])
                    continue
                elif args and args[0] == "%ksappend":
                    continue
                elif args and self._validState(args[0]):
                    # This is an unterminated section.
                    if self.version >= version.F8:
                        raise KickstartParseError(_("Section %s does not end with %%end.") % obj.sectionOpen, lineno=lineno)

                    # Finish up.  We do not process the header here because
                    # kicking back out to STATE_COMMANDS will ensure that happens.
                    lineIter.put(line)
                    lineno -= 1
                    self._finalize(obj)
                    break
            else:
                # This is just a line within a section.  Pass it off to whatever
                # section handles it.
                obj.handleLine(line)

        return lineno

    def _validState(self, st):
        """Is the given section tag one that has been registered with the parser?"""
        return st in list(self._sections.keys())

    def _tryFunc(self, fn):
        """Call the provided function (which doesn't take any arguments) and
           do the appropriate error handling.  If errorsAreFatal is False, this
           function will just print the exception and keep going.
        """
        try:
            fn()
        except Exception as msg:    # pylint: disable=broad-except
            self.errorsCount += 1
            if self.errorsAreFatal:
                raise
            else:
                print(msg, file=sys.stderr)

    def _isBlankOrComment(self, line):
        return line.isspace() or line == "" or line.lstrip()[0] == '#'

    def _handleInclude(self, f):
        # This case comes up primarily in ksvalidator.
        if not self.followIncludes:
            return

        self._includeDepth += 1

        try:
            self.readKickstart(f, reset=False)
        except KickstartError:
            # Handle the include file being provided over the
            # network in a %pre script.  This case comes up in the
            # early parsing in anaconda.
            if self.missingIncludeIsFatal:
                raise

        self._includeDepth -= 1

    def _stateMachine(self, lineIter):
        # For error reporting.
        lineno = 0

        while True:
            # Get the next line out of the file, quitting if this is the last line.
            try:
                self._line = next(lineIter)
                if self._line == "":
                    break
            except StopIteration:
                break

            lineno += 1

            # Eliminate blank lines, whitespace-only lines, and comments.
            if self._isBlankOrComment(self._line):
                self._handleSpecialComments(self._line)
                continue

            # Split the line, discarding comments.
            args = shlex.split(self._line, comments=True)

            if args[0] == "%include":
                if len(args) == 1 or not args[1]:
                    raise KickstartParseError(lineno=lineno)

                self._handleInclude(args[1])
                continue

            # Now on to the main event.
            if self._state == STATE_COMMANDS:
                if args[0] == "%ksappend":
                    # This is handled by the preprocess* functions, so continue.
                    continue
                elif args[0][0] == '%':
                    # This is the beginning of a new section.  Handle its header
                    # here.
                    newSection = args[0]
                    if not self._validState(newSection):
                        if self.unknownSectionIsFatal:
                            raise KickstartParseError(_("Unknown kickstart section: %s") % newSection, lineno=lineno)
                        else:
                            # If we are ignoring unknown section errors, just create a new
                            # NullSection for the header we just saw.  Then nothing else
                            # needs to change.  You can turn this warning into an error via
                            # ksvalidator, or the warnings module.
                            warnings.warn(_("Potentially unknown section seen at line %(lineno)s: %(sectionName)s") % {"lineno": lineno, "sectionName": newSection}, KickstartParseWarning)
                            self.registerSection(NullSection(self.handler, sectionOpen=newSection))

                    self._state = newSection
                    obj = self._sections[self._state]
                    self._tryFunc(lambda: obj.handleHeader(lineno, args))

                    # This will handle all section processing, kicking us back
                    # out to STATE_COMMANDS at the end with the current line
                    # being the next section header, etc.
                    lineno = self._readSection(lineIter, lineno)
                else:
                    # This is a command in the command section.  Dispatch to it.
                    self._tryFunc(lambda: self.handleCommand(lineno, args))
            elif self._state == STATE_END:
                break
            elif self._includeDepth > 0:
                lineIter.put(self._line)
                lineno -= 1
                lineno = self._readSection(lineIter, lineno)

    def readKickstartFromString(self, s, reset=True):
        """Process a kickstart file, provided as the string str."""
        if reset:
            self._reset()

        # Add a "" to the end of the list so the string reader acts like the
        # file reader and we only get StopIteration when we're after the final
        # line of input.
        i = PutBackIterator(s.splitlines(True) + [""])
        self._stateMachine(i)

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
            if self._includeDepth - 1 in self.currentdir:
                if os.path.exists(os.path.join(self.currentdir[self._includeDepth - 1], f)):
                    f = os.path.join(self.currentdir[self._includeDepth - 1], f)

        cd = os.path.dirname(f)
        if not cd.startswith("/"):
            cd = os.path.abspath(cd)
        self.currentdir[self._includeDepth] = cd

        try:
            s = load_to_str(f)
        except KickstartError as e:
            raise KickstartError(_("Unable to open input kickstart file: %s") % str(e), lineno=0)

        self.readKickstartFromString(s, reset=False)

    def setupSections(self):
        """Install the sections all kickstart files support.  You may override
           this method in a subclass, but should avoid doing so unless you know
           what you're doing.
        """
        self._sections = {}

        # Install the sections all kickstart files support.
        self.registerSection(PreScriptSection(self.handler, dataObj=Script))
        self.registerSection(PreInstallScriptSection(self.handler, dataObj=Script))
        self.registerSection(PostScriptSection(self.handler, dataObj=Script))
        self.registerSection(OnErrorScriptSection(self.handler, dataObj=Script))
        self.registerSection(TracebackScriptSection(self.handler, dataObj=Script))
        self.registerSection(PackageSection(self.handler))

        # Whitelist well-known sections that pykickstart does not understand,
        # but shouldn't error on.
        self.registerSection(NullSection(self.handler, sectionOpen="%addon"))
        self.registerSection(NullSection(self.handler, sectionOpen="%anaconda"))
