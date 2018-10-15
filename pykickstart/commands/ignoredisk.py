#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2009 Red Hat, Inc.
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

from pykickstart.version import FC3, F8, RHEL6, F29
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning
from pykickstart.i18n import _
from pykickstart.options import KSOptionParser, commaSplit

class FC3_IgnoreDisk(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.ignoredisk = kwargs.get("ignoredisk", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.ignoredisk:
            retval += "ignoredisk --drives=%s\n" % ",".join(self.ignoredisk)

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="ignoredisk", description="""
            Controls anaconda's access to disks attached to the system. By
            default, all disks will be available for partitioning. Only one of
            the following three options may be used.""", version=FC3)
        op.add_argument("--drives", dest="ignoredisk", type=commaSplit,
                        required=True, version=FC3, help="""
                        Specifies those disks that anaconda should not touch
                        when partitioning, formatting, and clearing.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class F8_IgnoreDisk(FC3_IgnoreDisk):
    removedKeywords = FC3_IgnoreDisk.removedKeywords
    removedAttrs = FC3_IgnoreDisk.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_IgnoreDisk.__init__(self, writePriority, *args, **kwargs)

        self.onlyuse = kwargs.get("onlyuse", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.ignoredisk:
            retval += "ignoredisk --drives=%s\n" % ",".join(self.ignoredisk)
        elif self.onlyuse:
            retval += "ignoredisk --only-use=%s\n" % ",".join(self.onlyuse)

        return retval

    def parse(self, args):
        retval = FC3_IgnoreDisk.parse(self, args)

        howmany = 0
        if self.ignoredisk:
            howmany += 1
        if self.onlyuse:
            howmany += 1
        if howmany != 1:
            raise KickstartParseError(_("One of --drives or --only-use must be specified "
                                        "for ignoredisk command."), lineno=self.lineno)

        return retval

    def _getParser(self):
        op = FC3_IgnoreDisk._getParser(self)
        op.add_argument("--drives", dest="ignoredisk", version=F8,
                        type=commaSplit, help="""
                        This argument is no longer required!""")
        op.add_argument("--only-use", dest="onlyuse",
                        type=commaSplit, version=F8, help="""
                        Specifies the opposite - only disks listed here will be
                        used during installation.""")
        return op

class RHEL6_IgnoreDisk(F8_IgnoreDisk):
    removedKeywords = F8_IgnoreDisk.removedKeywords
    removedAttrs = F8_IgnoreDisk.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F8_IgnoreDisk.__init__(self, writePriority, *args, **kwargs)
        self.interactive = kwargs.get("interactive", False)

    def __str__(self):
        retval = F8_IgnoreDisk.__str__(self)

        if self.interactive:
            retval = "ignoredisk --interactive\n"

        return retval

    def parse(self, args):
        retval = FC3_IgnoreDisk.parse(self, args)

        howmany = 0
        if self.ignoredisk:
            howmany += 1
        if self.onlyuse:
            howmany += 1
        if self.interactive:
            howmany += 1
        if howmany != 1:
            raise KickstartParseError(_("One of --drives , --only-use , or --interactive must be specified for ignoredisk command."), lineno=self.lineno)

        if self.interactive:
            self.ignoredisk = []

        return retval

    def _getParser(self):
        op = F8_IgnoreDisk._getParser(self)
        op.add_argument("--interactive", action="store_true",
                        default=False, version=RHEL6, help="""
                        Allow the user manually navigate the advanced storage
                        screen.""")
        return op

class F14_IgnoreDisk(RHEL6_IgnoreDisk):
    pass

class F29_IgnoreDisk(F14_IgnoreDisk):
    removedKeywords = F14_IgnoreDisk.removedKeywords
    removedAttrs = F14_IgnoreDisk.removedAttrs

    def parse(self, args):
        retval = FC3_IgnoreDisk.parse(self, args)

        howmany = 0
        if self.ignoredisk:
            howmany += 1
        if self.onlyuse:
            howmany += 1
        if self.interactive:
            howmany += 1
            warnings.warn(_("Ignoring deprecated option on line %s:  The ignoredisk command "
                            "no longer supports --interactive option.  In future releases, "
                            "this will result in a fatal error from kickstart. "
                            "Please modify your kickstart file to remove the option.")
                          % self.lineno, KickstartDeprecationWarning)
        if howmany != 1:
            if self.interactive:
                raise KickstartParseError(_("--interactive option of ignoredisk command "
                                            "is no longer supported."), lineno=self.lineno)
            else:
                raise KickstartParseError(_("One of --drives or --only-use must be specified "
                                            "for ignoredisk command."), lineno=self.lineno)

        return retval

    def _getParser(self):
        op = F14_IgnoreDisk._getParser(self)
        op.add_argument("--interactive", action="store_true",
                        default=False, deprecated=F29, help="""
                        Allow the user manually navigate the advanced storage
                        screen.""")
        return op
