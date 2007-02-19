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
