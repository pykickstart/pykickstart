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
from pykickstart.version import FC3, FC6, F18
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
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

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if len(ns.timezone) != 1:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone"))
        elif len(extra) > 0:
            mapping = {"command": "timezone", "options": extra}
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

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

    def parse(self, args):
        FC6_Timezone.parse(self, args)

        # NTP servers can only be listed once in F18, so weed out the duplicates now.
        self.ntpservers = list(set(self.ntpservers))

        if self.ntpservers and self.nontp:
            msg = formatErrorMsg(self.lineno, msg=_("Options --nontp and --ntpservers are mutually exclusive"))
            raise KickstartParseError(msg)

        return self

class F23_Timezone(F18_Timezone):
    def __init__(self, *args, **kwargs):
        F18_Timezone.__init__(self, *args, **kwargs)
        self.ntpservers = kwargs.get("ntpservers", list())

    def parse(self, args):
        FC6_Timezone.parse(self, args)

        if self.ntpservers and self.nontp:
            msg = formatErrorMsg(self.lineno, msg=_("Options --nontp and --ntpservers are mutually exclusive"))
            raise KickstartParseError(msg)

        return self
