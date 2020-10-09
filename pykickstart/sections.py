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
import warnings
from pykickstart.constants import KS_SCRIPT_PRE, KS_SCRIPT_POST, KS_SCRIPT_TRACEBACK, \
                                  KS_SCRIPT_PREINSTALL, KS_SCRIPT_ONERROR, \
                                  KS_MISSING_IGNORE, KS_MISSING_PROMPT, \
                                  KS_BROKEN_IGNORE, KS_BROKEN_REPORT
from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning
from pykickstart.options import KSOptionParser
from pykickstart.version import FC4, F7, F9, F18, F21, F22, F24, F32, RHEL6, RHEL7
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

    def handleLine(self, line):
        """This method is called for every line of a section.  Take whatever
           action is appropriate.  While this method is not required to be
           provided, not providing it does not make a whole lot of sense.

           Arguments:

           line -- The complete line, with any trailing newline.
        """

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
    allLines = True

    def __init__(self, *args, **kwargs):
        """Create a new NullSection instance.  You must pass a sectionOpen
           parameter (including a leading '%') for the section you wish to
           ignore.
        """
        Section.__init__(self, *args, **kwargs)
        self.sectionOpen = kwargs.get("sectionOpen")
        self._args = []
        self._body = []

    def handleHeader(self, lineno, args):
        self._args = args

    def handleLine(self, line):
        self._body.append(line)

    def finalize(self):
        body = "\n".join(self._body)
        if body:
            s = "%s\n%s\n%%end" % (" ".join(self._args), body)
        else:
            s = "%s\n%%end" % " ".join(self._args)

        self.handler._null_section_strings.append(s)

        self._args = []
        self._body = []

class ScriptSection(Section):
    allLines = True
    _description = ""
    _epilog = ""
    _title = ""

    def __init__(self, *args, **kwargs):
        Section.__init__(self, *args, **kwargs)
        self._script = {}
        self._resetScript()

    def _getParser(self):
        op = KSOptionParser(prog=self.sectionOpen,
                            description=self._description,
                            epilog=self._epilog,
                            version=FC4)

        op.add_argument("--erroronfail", dest="errorOnFail", action="store_true",
                        default=False, help="""
                        If the error script fails, this option will cause an
                        error dialog to be displayed and will halt installation.
                        The error message will direct you to where the cause of
                        the failure is logged.""", version=FC4)
        op.add_argument("--interpreter", dest="interpreter", default="/bin/sh",
                        version=FC4, metavar="/usr/bin/python", help="""
                        Allows you to specify a different scripting language,
                        such as Python. Replace /usr/bin/python with the
                        scripting language of your choice.
                        """)
        op.add_argument("--log", "--logfile", dest="log", version=FC4,
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
            s = self.dataObj(self._script["body"], **kwargs)
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
    _title = "Pre-installation script"
    _description = """
        You can add commands to run on the system immediately after the ks.cfg
        has been parsed and the lang, keyboard, and url options have been
        processed. This section must be at the end of the kickstart file (after
        the commands) and must start with the %pre command. You can access the
        network in the %pre section; however, name service has not been
        configured at this point, so only IP addresses will work.

        Preinstallation scripts are required to be closed with %end.

        If your script spawns a daemon process, you must make sure to close
        ``stdout`` and ``stderr``. Doing so is standard procedure for creating
        daemons. If you do not close these file descriptors, the installation
        will appear hung as anaconda waits for an EOF from the script.

        .. note::

            The pre-install script is not run in the chroot environment.
    """
    _epilog = """
    Example
    -------

    Here is an example %pre section::

        %pre
        #!/bin/bash
        hds=""
        mymedia=""

        for file in /sys/block/sd*; do
        hds="$hds $(basename $file)"
        done

        set $hds
        numhd=$(echo $#)

        drive1=$(echo $hds | cut -d' ' -f1)
        drive2=$(echo $hds | cut -d' ' -f2)


        if [ $numhd == "2" ]  ; then
            echo "#partitioning scheme generated in %pre for 2 drives" > /tmp/part-include
            echo "clearpart --all" >> /tmp/part-include
            echo "part /boot --fstype ext4 --size 512 --ondisk sda" >> /tmp/part-include
            echo "part / --fstype ext4 --size 10000 --grow --ondisk sda" >> /tmp/part-include
            echo "part swap --recommended --ondisk $drive1" >> /tmp/part-include
            echo "part /home --fstype ext4 --size 10000 --grow --ondisk sdb" >> /tmp/part-include
        else
            echo "#partitioning scheme generated in %pre for 1 drive" > /tmp/part-include
            echo "clearpart --all" >> /tmp/part-include
            echo "part /boot --fstype ext4 --size 521" >> /tmp/part-include
            echo "part swap --recommended" >> /tmp/part-include
            echo "part / --fstype ext4 --size 2048" >> /tmp/part-include
            echo "part /home --fstype ext4 --size 2048 --grow" >> /tmp/part-include
        fi
        %end

    This script determines the number of hard drives in the system and
    writes a text file with a different partitioning scheme depending on
    whether it has one or two drives. Instead of having a set of
    partitioning commands in the kickstart file, include the line:

    ``%include /tmp/part-include``

    The partitioning commands selected in the script will be used.
    """

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_PRE

class PreInstallScriptSection(ScriptSection):
    sectionOpen = "%pre-install"
    _title = "Pre-install Script"
    _description="""
    You can use the %pre-install section to run commands after the system has been
    partitioned, filesystems created, and everything is mounted under /mnt/sysimage
    Like %pre these scripts do not run in the chrooted environment.

    Each %pre-install section is required to be closed with a corresponding %end.
    """

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_PREINSTALL

class PostScriptSection(ScriptSection):
    sectionOpen = "%post"
    _title = "Post-installation Script"
    _description="""
    You have the option of adding commands to run on the system once the
    installation is complete. This section must be at the end of the
    kickstart file and must start with the %post command. This section is
    useful for functions such as installing additional software and
    configuring an additional nameserver.

    You may have more than one %post section, which can be useful for cases
    where some post-installation scripts need to be run in the chroot and
    others that need access outside the chroot.

    Each %post section is required to be closed with a corresponding %end.

    If you configured the network with static IP information, including a
    nameserver, you can access the network and resolve IP addresses in the %post
    section.  If you configured the network for DHCP, the /etc/resolv.conf file
    has not been completed when the installation executes the %post section. You
    can access the network, but you can not resolve IP addresses. Thus, if you
    are using DHCP, you must specify IP addresses in the %post section.

    If your script spawns a daemon process, you must make sure to close stdout
    and stderr.  Doing so is standard procedure for creating daemons.  If you do
    not close these file descriptors, the installation will appear hung as
    anaconda waits for an EOF from the script.

    The post-install script is run in a chroot environment; therefore, performing
    tasks such as copying scripts or RPMs from the installation media will not
    work.
    """

    _epilog="""
    Examples
    --------

    Run a script named ``runme`` from an NFS share::

        %post
        mkdir /mnt/temp
        mount 10.10.0.2:/usr/new-machines /mnt/temp
        open -s -w -- /mnt/temp/runme
        umount /mnt/temp
        %end

    Copy the file /etc/resolv.conf to the file system that was just
    installed::

        %post --nochroot
        cp /etc/resolv.conf /mnt/sysimage/etc/resolv.conf
        %end

    **If your kickstart is being interpreted by the livecd-creator tool, you should
    replace /mnt/sysimage above with $INSTALL_ROOT.**
    """

    def _getParser(self):
        op = ScriptSection._getParser(self)
        op.add_argument("--nochroot", dest="nochroot", action="store_true",
                        default=False, version=FC4, help="""
                        Allows you to specify commands that you would like to
                        run outside of the chroot environment.""")
        return op

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["chroot"] = True
        self._script["type"] = KS_SCRIPT_POST

class OnErrorScriptSection(ScriptSection):
    sectionOpen = "%onerror"
    _title = "Handling Errors"
    _description="""
    These scripts run when the installer hits a fatal error, but not necessarily
    a bug in the installer.  Some examples of these situations include errors in
    packages that have been requested to be installed, failures when starting VNC
    when requested, and error when scanning storage.  When these situations happen,
    installaton cannot continue.  The installer will run all %onerror scripts in
    the order they are provided in the kickstart file.

    In addition, %onerror scripts will be run on a traceback as well.  To be exact,
    all %onerror scripts will be run and then all %traceback scripts will be run
    afterwards.

    Each %onerror script is required to be closed with a corresponding %end.

    .. note::

        These scripts could potentially run at
        any stage in installation - early on, between making filesystems and installing
        packages, before the bootloader is installed, when attempting to reboot, and
        so on.  For this reason, these scripts cannot be run in the chroot environment
        and you should not trust anything in the installed system.  These scripts are
        primarily for testing and error reporting purposes.
    """

    def _resetScript(self):
        ScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_ONERROR

class TracebackScriptSection(OnErrorScriptSection):
    sectionOpen = "%traceback"
    _title = "Handling Tracebacks"
    _description="""
    These scripts run when the installer hits an internal error (a traceback, as
    they are called in Python) and cannot continue.  When this situation happens,
    the installer will display an error dialog to the screen that prompts the user
    to file a bug or reboot.  At the same time, it will run all %traceback scripts
    in the order they are provided in the kickstart file.

    Each %traceback script is required to be closed with a corresponding %end.

    .. note::

        These scripts could potentially run at
        any stage in installation - early on, between making filesystems and installing
        packages, before the bootloader is installed, when attempting to reboot, and
        so on.  For this reason, these scripts cannot be run in the chroot environment
        and you should not trust anything in the installed system.  These scripts are
        primarily for testing and error reporting purposes.
    """

    def _resetScript(self):
        OnErrorScriptSection._resetScript(self)
        self._script["type"] = KS_SCRIPT_TRACEBACK

class PackageSection(Section):
    sectionOpen = "%packages"
    _title = "Package Selection"

    def handleLine(self, line):
        h = line.partition('#')[0]
        line = h.rstrip()
        self.handler.packages.add([line])

    def _getParser(self):
        op = KSOptionParser(prog=self.sectionOpen, description="""
                            Use the %packages command to begin a kickstart file
                            section that lists the packages you would like to
                            install.

                            Packages can be specified by group or by individual
                            package name. The installation program defines
                            several groups that contain related packages. Refer
                            to the repodata/\\*comps\\*.xml file on the
                            installation media or in installation repository
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

                            The ``@`` prefix is also used to request installation
                            of module streams in the following format::

                                @<module name>:<stream name>/<profile name>

                            Profile name is optional and multiple profiles can be
                            installed by using multiple lines, one per profile.
                            Stream name is only optional only if the given module
                            has a default stream.

                            If there are a module and a group named the same,
                            and no stream name and profile are specified,
                            module will be selected instead of a group.

                            Requesting one module more than once with different
                            streams or not specifying a stream name for a module
                            without a default stream will result in an error.

                            Here is an example %packages selection with modules::

                                %packages
                                @^Fedora Server Edition
                                @nodejs:10
                                @django:1.6
                                @postgresql:9.6/server
                                @mariadb:10.1/server
                                @mysql:5.7/default
                                @scala:2.10/default
                                @gimp:2.10/devel
                                vim
                                %end

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
                            """, version=FC4)

        op.add_argument("--excludedocs", action="store_true", default=False,
                        help="""
                        Do not install any of the documentation from any packages.
                        For the most part, this means files in /usr/share/doc*
                        will not get installed though it could mean other files
                        as well, depending on how the package was built.""",
                        version=FC4)
        op.add_argument("--ignoremissing", action="store_true", default=False,
                        help="""
                        Ignore any packages, groups or module streams specified in the
                        packages section that are not found in any configured repository.
                        The default behavior is to halt the installation and ask
                        the user if the installation should be aborted or
                        continued. This option allows fully automated
                        installation even in the error case.""",
                        version=FC4)
        op.add_argument("--ignoredeps", dest="resolveDeps", action="store_false",
                        deprecated=FC4, help="")
        op.add_argument("--resolvedeps", dest="resolveDeps", action="store_true",
                        deprecated=FC4, help="")

        if self.version < F7:
            return op

        op.add_argument("--default", dest="defaultPackages", action="store_true",
                        default=False, version=F7, help="""
                        Install the default environment. This corresponds to the
                        package set that would be installed if no other
                        selections were made on the package customization screen
                        during an interactive install.""")

        if self.version < F9:
            return op

        op.remove_argument("--ignoredeps", version=F9)
        op.remove_argument("--resolvedeps", version=F9)
        op.add_argument("--instLangs", "--inst-langs", default=None, version=F9, help="""
                        Specify the list of languages that should be installed.
                        This is different from the package group level
                        selections, though. This option does not specify what
                        package groups should be installed. Instead, it controls
                        which translation files from individual packages should
                        be installed by setting RPM macros.""")

        if self.version < RHEL6:
            return op

        op.add_argument("--nobase", action="store_true", default=False,
                        version=RHEL6, help="""
                        Do not install the @base group (installed by default,
                        otherwise).""")

        if self.version < F18:
            return op

        op.add_argument("--nobase", action="store_true", default=False,
                        deprecated=F18)
        op.add_argument("--multilib", dest="multiLib", action="store_true",
                        default=False, version=F18, help="""
                        Enable yum's "all" multilib_policy as opposed to the
                        default of "best".""")

        if self.version < F21:
            return op

        op.add_argument("--nocore", action="store_true", default=False,
                        version=F21, help="""
                        Do not install the @core group (installed by default,
                        otherwise).

                        **Omitting the core group can produce a system that is
                        not bootable or that cannot finish the install. Use
                        with caution.**""")

        if self.version < RHEL7:
            return op

        op.add_argument("--timeout", dest="timeout", type=int,
                        default=None, version=RHEL7, help="""
                        Set up yum's or dnf's timeout. It is a number of seconds
                        to wait for a connection before timing out.""")
        op.add_argument("--retries", dest="retries", type=int,
                        default=None, version=RHEL7, help="""
                        Set up yum's or dnf's retries. It is a number of times
                        any attempt to retrieve a file should retry before
                        returning an error.""")

        if self.version < F22:
            return op

        op.remove_argument("--nobase", version=F22)

        if self.version < F24:
            return op

        op.add_argument("--excludeWeakdeps", "--exclude-weakdeps", dest="excludeWeakdeps",
                        action="store_true", default=False, version=F24,
                        help="""
                        Do not install packages from weak dependencies. These
                        are packages linked to the selected package set by
                        Recommends and Supplements flags. By default weak
                        dependencies will be installed.""")

        if self.version < F32:
            return op

        op.add_argument("--ignorebroken", action="store_true", default=False, version=F32,
                        help="""
                        Ignore any packages, groups or modules with conflicting files.
                        This issue will disable the DNF `strict` option. The default behavior
                        is to abort the installation with error message describing the
                        conflicting files.

                        **WARNING: Usage of this parameter is DISCOURAGED! The DNF
                        strict option will NOT log any information about what packages
                        were skipped. Using this option may result in an unusable system.**
                        """)

        return op

    def handleHeader(self, lineno, args):
        """Process the arguments to the %packages header and set attributes
           on the Version's Packages instance appropriate.  This method may be
           overridden in a subclass if necessary.
        """
        Section.handleHeader(self, lineno, args)
        op = self._getParser()
        ns = op.parse_args(args=args[1:], lineno=lineno)

        self.handler.packages.seen = True
        self.handler.packages.excludeDocs = ns.excludedocs
        if ns.ignoremissing:
            self.handler.packages.handleMissing = KS_MISSING_IGNORE
        else:
            self.handler.packages.handleMissing = KS_MISSING_PROMPT

        if self.version < F7:
            return

        if ns.defaultPackages:
            self.handler.packages.default = True

        if self.version < F9:
            return

        if ns.instLangs is not None:
            self.handler.packages.instLangs = ns.instLangs

        if self.version < RHEL6:
            return

        if ns.defaultPackages and getattr(ns, "nobase", False):
            raise KickstartParseError(_("--default and --nobase cannot be used together"), lineno=lineno)

        self.handler.packages.addBase = not getattr(ns, "nobase", False)

        if self.version < F18:
            return

        self.handler.packages.multiLib = ns.multiLib

        if self.version < F21:
            return

        if ns.defaultPackages and ns.nocore:
            raise KickstartParseError(_("--default and --nocore cannot be used together"), lineno=lineno)

        self.handler.packages.nocore = ns.nocore

        if self.version < RHEL7:
            return

        self.handler.packages.timeout = ns.timeout
        self.handler.packages.retries = ns.retries

        if self.version < F24:
            return

        self.handler.packages.excludeWeakdeps = ns.excludeWeakdeps

        if self.version < F32:
            return

        if ns.ignorebroken:
            self.handler.packages.handleBroken = KS_BROKEN_IGNORE
        else:
            self.handler.packages.handleBroken = KS_BROKEN_REPORT

        for option, new_option in \
                {"--instLangs": "--inst-langs", "--excludeWeakdeps": "--exclude-weakdeps"}.items():
            if option in args:
                warnings.warn(_("The %(option)s option on line %(lineno)s will be deprecated in "
                                "future releases. Please modify your kickstart file to replace "
                                "this option with its preferred alias %(new_option)s.")
                              % {"option": option, "lineno": lineno, "new_option": new_option},
                              KickstartDeprecationWarning)
