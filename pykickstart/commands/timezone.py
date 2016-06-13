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
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

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
        op = KSOptionParser()
        op.add_option("--utc", dest="isUtc", action="store_true", default=False)
        return op

    # Caution: This method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(self.op, opts)

        if len(extra) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone"))

        self.timezone = extra[0]
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
        op.add_option("--utc", "--isUtc", dest="isUtc", action="store_true", default=False)
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
        def servers_cb(option, opt_str, value, parser):
            for server in value.split(","):
                if server:
                    parser.values.ensure_value(option.dest, set()).add(server)


        op = FC6_Timezone._getParser(self)
        op.add_option("--nontp", dest="nontp", action="store_true", default=False)
        op.add_option("--ntpservers", dest="ntpservers", action="callback",
                      callback=servers_cb, nargs=1, type="string")

        return op

    # Caution: The parse() method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def parse(self, args):
        FC6_Timezone.parse(self, args)

        if self.ntpservers and self.nontp:
            msg = formatErrorMsg(self.lineno, msg=_("Options --nontp and --ntpservers are mutually exclusive"))
            raise KickstartParseError(msg)

        return self

class F23_Timezone(F18_Timezone):
    def __init__(self, *args, **kwargs):
        F18_Timezone.__init__(self, *args, **kwargs)
        self.ntpservers = kwargs.get("ntpservers", list())

    # Caution: The parse() method is overridden in the RHEL7_Timezone & F25_Timezone classes
    # by a new implementation not calling this method.
    def _getParser(self):
        def servers_cb(option, opt_str, value, parser):
            for server in value.split(","):
                if server:
                    parser.values.ensure_value(option.dest, list()).append(server)

        op = FC6_Timezone._getParser(self)
        op.add_option("--nontp", dest="nontp", action="store_true", default=False)
        op.add_option("--ntpservers", dest="ntpservers", action="callback",
                      callback=servers_cb, nargs=1, type="string")

        return op

# About the RHEL7_Timezone & F25_Timezone command classes
# =======================================================
#
# The F18_Timezone command class used in RHEL <=7.2 and Fedora <=24 the
# timezone command always required a ti,ezone specification to be provided.
#
# On the other hand the timezone command has also some commands that don't
# really need a timezone to be specicifed to work, like "--utc/--isutc".
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

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        # just "timezone" without any arguments and timezone specification doesn't really make sense,
        # so throw an error when we see it (it might even be an indication of an incorrect machine generated kickstart)
        if not args:
            error_message = _("At least one option and/or an argument are expected for the  %s command") % "timezone"
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=error_message))

        # To be able to support the timezone command being used without
        # a timezone specification:
        # - we don't call the parse() method of the ancestors
        # -> due to the FC3 parse() method that would be eventually called,
        #    which throws an exception if no timezone specification is provided
        # - we implement the relevant functionality of the ancestor methods here

        if len(extra) > 1:
            error_message = _("One or zero arguments are expected for the %s command") % "timezone"
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=error_message))

        if len(extra) > 0:
            self.timezone = extra[0]

        if self.ntpservers and self.nontp:
            msg = formatErrorMsg(self.lineno, msg=_("Options --nontp and --ntpservers are mutually exclusive"))
            raise KickstartParseError(msg)

        return self

class F25_Timezone(F18_Timezone):
    def __init__(self, writePriority=0, *args, **kwargs):
        F18_Timezone.__init__(self, writePriority, *args, **kwargs)

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        # just "timezone" without any arguments and timezone specification doesn't really make sense,
        # so throw an error when we see it (it might even be an indication of an incorrect machine generated kickstart)
        if not args:
            error_message = _("At least one option and/or an argument are expected for the  %s command") % "timezone"
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=error_message))

        # To be able to support the timezone command being used without
        # a timezone specification:
        # - we don't call the parse() method of the ancestors
        # -> due to the FC3 parse() method that would be eventually called,
        #    which throws an exception if no timezone specification is provided
        # - we implement the relevant functionality of the ancestor methods here

        if len(extra) > 1:
            error_message = _("One or zero arguments are expected for the %s command") % "timezone"
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=error_message))

        if len(extra) > 0:
            self.timezone = extra[0]

        if self.ntpservers and self.nontp:
            msg = formatErrorMsg(self.lineno, msg=_("Options --nontp and --ntpservers are mutually exclusive"))
            raise KickstartParseError(msg)

        return self
