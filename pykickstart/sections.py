#
# sections.py:  Kickstart file sections.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2011-2016 Red Hat, Inc.
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
This module exports the classes that define a section of a kickstart file.  A
section is a chunk of the file starting with a %tag and ending with a %end.
Examples of sections include %packages, %pre, and %post.

You may use this module to define your own custom sections which will be
treated just the same as a predefined one by the kickstart parser.  All that
is necessary is to create a new subclass of Section and call
parser.registerSection with an instance of your new class.
"""
from pykickstart.constants import KS_SCRIPT_PRE, KS_SCRIPT_POST, KS_SCRIPT_TRACEBACK, \
                                  KS_SCRIPT_PREINSTALL, KS_SCRIPT_ONERROR, \
                                  KS_MISSING_IGNORE, KS_MISSING_PROMPT
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser
from pykickstart.version import FC4, F7, F9, F18, F21, F22, F24

from pykickstart.i18n import _

class Section(object):
    """The base class for defining kickstart sections.  You are free to
       subclass this as appropriate.

       Class attributes:

       allLines    -- Does this section require the parser to call handleLine
                      for every line in the section, even blanks and comments?
       sectionOpen -- The string that denotes the start of this section.  You
                      must start your tag with a percent sign.
       timesSeen   -- This attribute is for informational purposes only.  It is
                      incremented every time handleHeader is called to keep
                      track of the number of times a section of this type is
                      seen.
    """
    allLines = False
    sectionOpen = ""
    timesSeen = 0

    def __init__(self, handler, **kwargs):
        """Create a new Script instance.  At the least, you must pass in an
           instance of a baseHandler subclass.

           Valid kwargs:

           dataObj -- A class that should be populated by this Section.  It almost
                      always should be Script, or some subclass of it.
        """
        self.handler = handler
        self.version = self.handler.version

        self.dataObj = kwargs.get("dataObj", None)

    def finalize(self):
        """This method is called when the %end tag for a section is seen.  It
           is not required to be provided.
        """
        pass

    def handleLine(self, line):
        """This method is called for every line of a section.  Take whatever
           action is appropriate.  While this method is not required to be
           provided, not providing it does not make a whole lot of sense.

           Arguments:

           line -- The complete line, with any trailing newline.
        """
        pass

    # pylint: disable=unused-argument
    def handleHeader(self, lineno, args):
        """This method is called when the opening tag for a section is seen.
           Not all sections will need this method, though all provided with
           kickstart include one.

           Arguments:

           args -- A list of all strings passed as arguments to the section
                   opening tag.
        """
        self.timesSeen += 1
    # pylint: enable=unused-argument

    @property
    def seen(self):
        """This property is given for consistency with KickstartCommand objects
           only.  It simply returns whether timesSeen is non-zero.
        """
        return self.timesSeen > 0

class NullSection(Section):
    """This defines a section that pykickstart will recognize but do nothing
       with.  If the parser runs across a %section that has no object registered,
       it will raise an error.  Sometimes, you may want to simply ignore those
       sections instead.  This class is useful for that purpose.
    """
    def __init__(self, *args, **kwargs):
        """Create a new NullSection instance.  You must pass a sectionOpen
           parameter (including a leading '%') for the section you wish to
           ignore.
        """
        Section.__init__(self, *args, **kwargs)
        self.sectionOpen = kwargs.get("sectionOpen")

class ScriptSection(Section):
    allLines = True
    description = ""

    def __init__(self, *args, **kwargs):
        Section.__init__(self, *args, **kwargs)
        self._script = {}
        self._resetScript()

    def _getParser(self):
        op = KSOptionParser(prog=self.sectionOpen,
                            description=self.description,
                            version=self.version)
        op.add_argument("--erroronfail", dest="errorOnFail", action="store_true",
                        default=False, help="""
                        If the error script fails, this option will cause an
                        error dialog to be displayed and will halt installation.
                        The error message will direct you to where the cause of
                        the failure is logged.""", introduced=FC4)
        op.add_argument("--interpreter", dest="interpreter", default="/bin/sh",
                        introduced=FC4, help="""
                        Allows you to specify a different scripting language,
                        such as Python. Replace /usr/bin/python with the
                        scripting language of your choice.
                        """)
        op.add_argument("--log", "--logfile", dest="log", introduced=FC4,
                        help="""
                        Log all messages from the script to the given log file.
                        """)
        return op

    def _resetScript(self):
        self._script = {"interp": "/bin/sh", "log": None, "errorOnFail": False,
                        "lineno": None, "chroot": False, "body": []}

    def handleLine(self, line):
        self._script["body"].append(line)

    def finalize(self):
        if " ".join(self._script["body"]).strip() == "":
            return

        kwargs = {"interp": self._script["interp"],
                  "inChroot": self._script["chroot"],
                  "lineno": self._script["lineno"],
                  "logfile": self._script["log"],
                  "errorOnFail": self._script["errorOnFail"],
                  "type": self._script["type"]}

        if self.dataObj is not None:
            s = self.dataObj (self._script["body"], **kwargs)
            self._resetScript()
            self.handler.scripts.append(s)

    def handleHeader(self, lineno, args):
        """Process the arguments to a %pre/%post/%traceback header for later
           setting on a Script instance once the end of the script is found.
           This method may be overridden in a subclass if necessary.
        """
        Section.handleHeader(self, lineno, args)
        op = self._getParser()

        ns = op.parse_args(args=args[1:], lineno=lineno)

        self._script["interp"] = ns.interpreter
        self._script["lineno"] = lineno
        self._script["log"] = ns.log
        self._script["errorOnFail"] = ns.errorOnFail
        if hasattr(ns, "nochroot"):
            self._script["chroot"] = not ns.nochroot

class PreScriptSection(ScriptSection):
    sectionOpen = "%pre"

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_PRE

class PreInstallScriptSection(ScriptSection):
    sectionOpen = "%pre-install"

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_PREINSTALL

class PostScriptSection(ScriptSection):
    sectionOpen = "%post"

    def _getParser(self):
        op = ScriptSection._getParser(self)
        op.add_argument("--nochroot", dest="nochroot", action="store_true",
                        default=False, introduced=FC4, help="""
                        Allows you to specify commands that you would like to
                        run outside of the chroot environment.""")
        return op

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["chroot"] = True
        self._script["type"] = KS_SCRIPT_POST

class OnErrorScriptSection(ScriptSection):
    sectionOpen = "%onerror"

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_ONERROR

class TracebackScriptSection(OnErrorScriptSection):
    sectionOpen = "%traceback"

    def _resetScript(self):
        OnErrorScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_TRACEBACK

class PackageSection(Section):
    sectionOpen = "%packages"

    def handleLine(self, line):
        h = line.partition('#')[0]
        line = h.rstrip()
        self.handler.packages.add([line])

    def handleHeader(self, lineno, args):
        """Process the arguments to the %packages header and set attributes
           on the Version's Packages instance appropriate.  This method may be
           overridden in a subclass if necessary.
        """
        Section.handleHeader(self, lineno, args)
        op = KSOptionParser(prog=self.sectionOpen, description="""
                            Use the %packages command to begin a kickstart file
                            section that lists the packages you would like to
                            install.

                            Packages can be specified by group or by individual
                            package name. The installation program defines
                            several groups that contain related packages. Refer
                            to the repodata/*comps.xml file on the first CD-ROM
                            for a list of groups. Each group has an id, user
                            visibility value, name, description, and package
                            list. In the package list, the packages marked as
                            mandatory are always installed if the group is
                            selected, the packages marked default are selected
                            by default if the group is selected, and the packages
                            marked optional must be specifically selected even
                            if the group is selected to be installed.

                            In most cases, it is only necessary to list the
                            desired groups and not individual packages. Note
                            that the Core group is always selected by default,
                            so it is not necessary to specify it in the
                            %packages section.

                            The %packages section is required to be closed with
                            %end. Also, multiple %packages sections may be given.
                            This may be handy if the kickstart file is used as a
                            template and pulls in various other files with the
                            %include mechanism.

                            Here is an example %packages selection::

                                %packages
                                @X Window System
                                @GNOME Desktop Environment
                                @Graphical Internet
                                @Sound and Video
                                dhcp
                                %end

                            As you can see, groups are specified, one to a line,
                            starting with an ``@`` symbol followed by the full
                            group name as given in the comps.xml file. Groups
                            can also be specified using the id for the group,
                            such as gnome-desktop. Specify individual packages
                            with no additional characters (the dhcp line in the
                            example above is an individual package).

                            You can also specify environments using the ``@^``
                            prefix followed by full environment name as given in
                            the comps.xml file.  If multiple environments are
                            specified, only the last one specified will be used.
                            Environments can be mixed with both group
                            specifications (even if the given group is not part
                            of the specified environment) and package
                            specifications.

                            Here is an example of requesting the GNOME Desktop
                            environment to be selected for installation::

                                %packages
                                @^gnome-desktop-environment
                                %end

                            Additionally, individual packages may be specified
                            using globs. For instance::

                                %packages
                                vim*
                                kde-i18n-*
                                %end

                            This would install all packages whose names start
                            with "vim" or "kde-i18n-".

                            You can also specify which packages or groups not to
                            install from the default package list::

                                %packages
                                -autofs
                                -@Sound and Video
                                %end
                            """, epilog="""
                            Group-level options
                            -------------------

                            In addition, group lines in the %packages section
                            can take the following options:

                            ``--nodefaults``

                                Only install the group's mandatory packages, not
                                the default selections.

                            ``--optional``

                                In addition to the mandatory and default packages,
                                also install the optional packages. This means all
                                packages in the group will be installed.
                            """, version=self.version)
        op.add_argument("--excludedocs", action="store_true", default=False,
                        help="""
                        Do not install any of the documentation from any packages.
                        For the most part, this means files in /usr/share/doc*
                        will not get installed though it could mean other files
                        as well, depending on how the package was built.""",
                        introduced=FC4)
        op.add_argument("--ignoremissing", action="store_true", default=False,
                        help="""
                        Ignore any packages or groups specified in the packages
                        section that are not found in any configured repository.
                        The default behavior is to halt the installation and ask
                        the user if the installation should be aborted or
                        continued. This option allows fully automated
                        installation even in the error case.""",
                        introduced=FC4)
        op.add_argument("--nobase", action="store_true", default=False,
                        deprecated=F18, removed=F22, help="""
                        Do not install the @base group (installed by default,
                        otherwise).""")
        op.add_argument("--nocore", action="store_true", default=False,
                        introduced=F21, help="""
                        Do not install the @core group (installed by default,
                        otherwise).

                        **Omitting the core group can produce a system that is
                        not bootable or that cannot finish the install. Use
                        with caution.**""")
        op.add_argument("--ignoredeps", dest="resolveDeps", action="store_false",
                        deprecated=FC4, removed=F9, help="")
        op.add_argument("--resolvedeps", dest="resolveDeps", action="store_true",
                        deprecated=FC4, removed=F9, help="")
        op.add_argument("--default", dest="defaultPackages", action="store_true",
                        default=False, introduced=F7, help="""
                        Install the default package set. This corresponds to the
                        package set that would be installed if no other
                        selections were made on the package customization screen
                        during an interactive install.""")
        op.add_argument("--instLangs", default=None, introduced=F9, help="""
                        Specify the list of languages that should be installed.
                        This is different from the package group level
                        selections, though. This option does not specify what
                        package groups should be installed. Instead, it controls
                        which translation files from individual packages should
                        be installed by setting RPM macros.""")
        op.add_argument("--multilib", dest="multiLib", action="store_true",
                        default=False, introduced=F18, help="""
                        Enable yum's "all" multilib_policy as opposed to the
                        default of "best".""")
        op.add_argument("--excludeWeakdeps", dest="excludeWeakdeps",
                        action="store_true", default=False, introduced=F24,
                        help="""
                        Do not install packages from weak dependencies. These
                        are packages linked to the selected package set by
                        Recommends and Supplements flags. By default weak
                        dependencies will be installed.""")

        ns = op.parse_args(args=args[1:], lineno=lineno)

        if ns.defaultPackages and ns.nobase:
            raise KickstartParseError(formatErrorMsg(lineno, msg=_("--default and --nobase cannot be used together")))
        elif ns.defaultPackages and ns.nocore:
            raise KickstartParseError(formatErrorMsg(lineno, msg=_("--default and --nocore cannot be used together")))

        self.handler.packages.excludeDocs = ns.excludedocs
        self.handler.packages.addBase = not ns.nobase
        if ns.ignoremissing:
            self.handler.packages.handleMissing = KS_MISSING_IGNORE
        else:
            self.handler.packages.handleMissing = KS_MISSING_PROMPT

        if ns.defaultPackages:
            self.handler.packages.default = True

        if ns.instLangs is not None:
            self.handler.packages.instLangs = ns.instLangs

        self.handler.packages.nocore = ns.nocore
        self.handler.packages.multiLib = ns.multiLib
        self.handler.packages.excludeWeakdeps = ns.excludeWeakdeps
        self.handler.packages.seen = True
