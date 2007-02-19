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

class FC3_RootPw(KickstartCommand):
    def __init__(self, writePriority=0, isCrypted=False, password=""):
        KickstartCommand.__init__(self, writePriority)
        self.isCrypted = isCrypted
        self.password = password

    def __str__(self):
        if self.password != "":
            if self.isCrypted:
                crypted = "--iscrypted"
            else:
                crypted = ""

            return "# Root password\nrootpw %s %s\n" % (crypted, self.password)
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw")

        self.password = extra[0]
