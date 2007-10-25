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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Timezone(KickstartCommand):
    def __init__(self, writePriority=0, isUtc=False, timezone=""):
        KickstartCommand.__init__(self, writePriority)
        self.isUtc = isUtc
        self.timezone = timezone

    def __str__(self):
        if self.timezone != "":
            if self.isUtc:
                utc = "--utc"
            else:
                utc = ""

            return "# System timezone\ntimezone %s %s\n" %(utc, self.timezone)
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--utc", dest="isUtc", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone")

        self.timezone = extra[0]

class FC6_Timezone(FC3_Timezone):
    def __init__(self, writePriority=0, isUtc=False, timezone=""):
        FC3_Timezone.__init__(self, writePriority, isUtc, timezone)

    def __str__(self):
        if self.timezone != "":
            if self.isUtc:
                utc = "--isUtc"
            else:
                utc = ""

            return "# System timezone\ntimezone %s %s\n" %(utc, self.timezone)
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--utc", "--isUtc", dest="isUtc", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone")

        self.timezone = extra[0]
