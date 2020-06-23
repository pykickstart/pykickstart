#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
import warnings
from pykickstart.version import FC3, FC6, F18
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning
from pykickstart.options import KSOptionParser, commaSplit

from pykickstart.i18n import _

class FC3_Timezone(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.isUtc = kwargs.get("isUtc", False)
        self.timezone = kwargs.get("timezone", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.timezone:
            if self.isUtc:
                utc = "--utc"
            else:
                utc = ""

            retval += "# System timezone\ntimezone %s %s\n" % (utc, self.timezone)

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="timezone", description="""
                            This required command sets the system time zone to
                            which may be any of the time zones listed by
                            timeconfig.""", version=FC3)
        op.add_argument("--utc", dest="isUtc", action="store_true",
                        default=False, version=FC3, help="""
                        If present, the system assumes the hardware clock is set
                        to UTC (Greenwich Mean) time.

                       *To get the list of supported timezones, you can either
                        run this script:
                        http://vpodzime.fedorapeople.org/timezones_list.py or
                        look at this list:
                        http://vpodzime.fedorapeople.org/timezones_list.txt*
                        """)
        op.add_argument("timezone", metavar="<timezone>", nargs=1,
                        version=FC3, help="""
                        Timezone name, e.g. Europe/Sofia.""")
        return op

    # Caution: This method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        assert len(ns.timezone) == 1

        if extra:
            mapping = {"command": "timezone", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.timezone = ns.timezone[0]
        return self

class FC6_Timezone(FC3_Timezone):
    removedKeywords = FC3_Timezone.removedKeywords
    removedAttrs = FC3_Timezone.removedAttrs

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.timezone:
            if self.isUtc:
                utc = "--isUtc"
            else:
                utc = ""

            retval += "# System timezone\ntimezone %s %s\n" % (utc, self.timezone)

        return retval

    def _getParser(self):
        op = FC3_Timezone._getParser(self)
        op.add_argument("--utc", "--isUtc", dest="isUtc", action="store_true",
                        default=False, version=FC6, help="""
                        The ``--isUtc`` option was added.""")
        return op

class F18_Timezone(FC6_Timezone):
    def __init__(self, writePriority=0, *args, **kwargs):
        FC6_Timezone.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.nontp = kwargs.get("nontp", False)
        self.ntpservers = kwargs.get("ntpservers", set())

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.timezone:
            retval += "# System timezone\n"
            retval += "timezone " + self._getArgsAsStr() + "\n"

        return retval

    def _getArgsAsStr(self):
        retval = self.timezone

        if self.isUtc:
            retval += " --isUtc"

        if self.nontp:
            retval += " --nontp"

        if self.ntpservers:
            retval += " --ntpservers=" + ",".join(self.ntpservers)

        return retval

    def _getParser(self):
        op = FC6_Timezone._getParser(self)
        op.add_argument("--nontp", action="store_true", default=False,
                        version=F18, help="""
                        Disable automatic starting of NTP service.

                        ``--nontp`` and ``--ntpservers`` are mutually exclusive.
                        """)
        op.add_argument("--ntpservers", dest="ntpservers", type=commaSplit,
                        metavar="<server1>,<server2>,...,<serverN>",
                        version=F18, help="""
                        Specify a list of NTP servers to be used (comma-separated
                        list with no spaces). The chrony package is automatically
                        installed when this option is used. If you don't want the
                        package to be automatically installed then use ``-chrony``
                        in package selection. For example::

                        ``timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz Europe/Prague``
                        """)
        return op

    # Caution: The parse() method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def parse(self, args):
        FC6_Timezone.parse(self, args)

        # NTP servers can only be listed once in F18, so weed out the duplicates now.
        self.ntpservers = list(set(self.ntpservers))

        if self.ntpservers and self.nontp:
            msg = _("Options --nontp and --ntpservers are mutually exclusive")
            raise KickstartParseError(msg, lineno=self.lineno)

        return self

class F23_Timezone(F18_Timezone):
    def __init__(self, *args, **kwargs):
        F18_Timezone.__init__(self, *args, **kwargs)
        self.ntpservers = kwargs.get("ntpservers", list())

    # Caution: This method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def parse(self, args):
        FC6_Timezone.parse(self, args)

        if self.ntpservers and self.nontp:
            msg = _("Options --nontp and --ntpservers are mutually exclusive")
            raise KickstartParseError(msg, lineno=self.lineno)

        return self

# About the RHEL7_Timezone & F25_Timezone command classes
# =======================================================
#
# The F18_Timezone command class used in RHEL <=7.2 the F23_Timezone
# command class used in Fedora <=24 the always required a timezone
# specification to be provided.
#
# On the other hand the timezone command has also some commands that don't
# really need a timezone to be specified to work, like "--utc/--isutc".
#
# So if you for example wanted to set the hwclock to the UTC mode but still
# wanted the user to set a timezone manually in the UI (by not providing a
# timezone specification), you were out of luck - a timezone parsing error
# would be raised.
#
# To fix this we need to remove the requirement on always providing one
# argument to the timezone command. As the requirement is present
# quite deep in the class hierarchy (in the original FC3_Timezone class)
# we reimplement the parse() method in the RHEL7_Timezone and F25_Timezone
# classes and avoid calling the ancestors parse(), as it otherwise done in all
# other command child classes.

class RHEL7_Timezone(F18_Timezone):
    def __init__(self, writePriority=0, *args, **kwargs):
        F18_Timezone.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def _getParser(self):
        op = KSOptionParser(prog="timezone", description="""
                            This required command sets the system time zone to
                            which may be any of the time zones listed by
                            timeconfig.""", version=FC3)
        op.add_argument("timezone", metavar="<timezone>", nargs="*",
                        version=FC3, help="""
                        Timezone name, e.g. Europe/Sofia.
                        This is optional but at least one of the options needs
                        to be used if no timezone is specified.
                        """)
        op.add_argument("--utc", "--isUtc", dest="isUtc", action="store_true",
                        default=False, version=FC6, help="""
                        If present, the system assumes the hardware clock is set
                        to UTC (Greenwich Mean) time.

                       *To get the list of supported timezones, you can either
                        run this script:
                        http://vpodzime.fedorapeople.org/timezones_list.py or
                        look at this list:
                        http://vpodzime.fedorapeople.org/timezones_list.txt*
                        """)
        op.add_argument("--nontp", action="store_true", default=False,
                        version=F18, help="""
                        Disable automatic starting of NTP service.

                        ``--nontp`` and ``--ntpservers`` are mutually exclusive.
                        """)
        op.add_argument("--ntpservers", dest="ntpservers", type=commaSplit,
                        metavar="<server1>,<server2>,...,<serverN>",
                        version=F18, help="""
                        Specify a list of NTP servers to be used (comma-separated
                        list with no spaces). The chrony package is automatically
                        installed when this option is used. If you don't want the
                        package to be automatically installed then use ``-chrony``
                        in package selection. For example::

                        ``timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz Europe/Prague``
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        # just "timezone" without any arguments and timezone specification doesn't really make sense,
        # so throw an error when we see it (it might even be an indication of an incorrect machine generated kickstart)
        if not args:
            error_message = _("At least one option and/or an argument are expected for the %s command") % "timezone"
            raise KickstartParseError(error_message, lineno=self.lineno)

        # To be able to support the timezone command being used without
        # a timezone specification:
        # - we don't call the parse() method of the ancestors
        # -> due to the FC3 parse() method that would be eventually called,
        #    which throws an exception if no timezone specification is provided
        # - we implement the relevant functionality of the ancestor methods here

        if len(ns.timezone) == 1:
            self.timezone = ns.timezone[0]
        elif len(ns.timezone) > 1:
            error_message = _("One or zero arguments are expected for the %s command") % "timezone"
            raise KickstartParseError(error_message, lineno=self.lineno)

        if self.ntpservers and self.nontp:
            msg = _("Options --nontp and --ntpservers are mutually exclusive")
            raise KickstartParseError(msg, lineno=self.lineno)

        return self

class F25_Timezone(F23_Timezone):
    def __init__(self, writePriority=0, *args, **kwargs):
        F23_Timezone.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        args = self._getArgsAsStr()
        if args:
            retval += "# System timezone\n"
            retval += "timezone" + args + "\n"

        return retval

    def _getArgsAsStr(self):
        retval = ""

        if self.timezone:
            retval += " " + self.timezone

        if self.isUtc:
            retval += " --isUtc"

        if self.nontp:
            retval += " --nontp"

        if self.ntpservers:
            retval += " --ntpservers=" + ",".join(self.ntpservers)

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="timezone", description="""
                            This required command sets the system time zone to
                            which may be any of the time zones listed by
                            timeconfig.""", version=FC3)
        op.add_argument("timezone", metavar="<timezone>", nargs="*",
                        version=FC3, help="""
                        Timezone name, e.g. Europe/Sofia.
                        This is optional but at least one of the options needs
                        to be used if no timezone is specified.
                        """)
        op.add_argument("--utc", "--isUtc", dest="isUtc", action="store_true",
                        default=False, version=FC6, help="""
                        If present, the system assumes the hardware clock is set
                        to UTC (Greenwich Mean) time.

                       *To get the list of supported timezones, you can either
                        run this script:
                        http://vpodzime.fedorapeople.org/timezones_list.py or
                        look at this list:
                        http://vpodzime.fedorapeople.org/timezones_list.txt*
                        """)
        op.add_argument("--nontp", action="store_true", default=False,
                        version=F18, help="""
                        Disable automatic starting of NTP service.

                        ``--nontp`` and ``--ntpservers`` are mutually exclusive.
                        """)
        op.add_argument("--ntpservers", dest="ntpservers", type=commaSplit,
                        metavar="<server1>,<server2>,...,<serverN>",
                        version=F18, help="""
                        Specify a list of NTP servers to be used (comma-separated
                        list with no spaces). The chrony package is automatically
                        installed when this option is used. If you don't want the
                        package to be automatically installed then use ``-chrony``
                        in package selection. For example::

                        ``timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz Europe/Prague``
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        # just "timezone" without any arguments and timezone specification doesn't really make sense,
        # so throw an error when we see it (it might even be an indication of an incorrect machine generated kickstart)
        if not args:
            error_message = _("At least one option and/or an argument are expected for the %s command") % "timezone"
            raise KickstartParseError(error_message, lineno=self.lineno)

        # To be able to support the timezone command being used without
        # a timezone specification:
        # - we don't call the parse() method of the ancestors
        # -> due to the FC3 parse() method that would be eventually called,
        #    which throws an exception if no timezone specification is provided
        # - we implement the relevant functionality of the ancestor methods here

        if len(ns.timezone) == 1:
            self.timezone = ns.timezone[0]
        elif len(ns.timezone) > 1:
            error_message = _("One or zero arguments are expected for the %s command") % "timezone"
            raise KickstartParseError(error_message, lineno=self.lineno)

        if self.ntpservers and self.nontp:
            msg = _("Options --nontp and --ntpservers are mutually exclusive")
            raise KickstartParseError(msg, lineno=self.lineno)

        return self

class F32_Timezone(F25_Timezone):

    def __init__(self, writePriority=0, *args, **kwargs):
        F25_Timezone.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def _getArgsAsStr(self):
        retval = ""

        if self.timezone:
            retval += " " + self.timezone

        if self.isUtc:
            retval += " --utc"

        if self.nontp:
            retval += " --nontp"

        if self.ntpservers:
            retval += " --ntpservers=" + ",".join(self.ntpservers)

        return retval

    def parse(self, args):
        F25_Timezone.parse(self, args)

        if "--isUtc" in args:
            warnings.warn(_("The option --isUtc will be deprecated in future releases. Please "
                            "modify your kickstart file to replace this option with its preferred "
                            "alias --utc."),
                          KickstartDeprecationWarning)

        return self


class F33_Timezone(F32_Timezone):

    def __init__(self, writePriority=0, *args, **kwargs):
        F32_Timezone.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def parse(self, args):
        F32_Timezone.parse(self, args)

        if self.ntpservers:
            warnings.warn(_("The option --ntpservers will be deprecated in future releases. Please "
                            "modify your kickstart file to replace this option with "
                            "timesource --ntp-server <server hostname> command invocation, "
                            "one per NTP server."),
                          KickstartDeprecationWarning)
        if self.nontp:
            warnings.warn(_("The option --nontp will be deprecated in future releases. Please "
                            "modify your kickstart file to replace this option with "
                            "timesource --ntp-disable command invocation."),
                          KickstartDeprecationWarning)
        return self
