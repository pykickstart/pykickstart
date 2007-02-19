#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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

class FC6Logging(KickstartCommand):
    def __init__(self, writePriority=0, host="", level="info", port=""):
        KickstartCommand.__init__(self, writePriority)
        self.host = host
        self.level = level
        self.port = port

    def __str__(self):
        retval = "# Installation logging level\nlogging --level=%s" % self.level

        if self.host != "":
            retval += " --host=%s" % self.host

            if self.port != "":
                retval += " --port=%s" % self.port

        return retval + "\n"

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--host")
        op.add_option("--level", type="choice",
                      choices=["debug", "info", "warning", "error", "critical"])
        op.add_option("--port")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
