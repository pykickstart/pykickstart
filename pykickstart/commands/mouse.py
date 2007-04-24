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

class RHEL3_Mouse(KickstartCommand):
    def __init__(self, writePriority=0, device="", emulthree=False, mouse=""):
        KickstartCommand.__init__(self, writePriority)
        self.device = device
        self.emulthree = emulthree
        self.mouse = mouse

    def __str__(self):
        opts = ""
        if self.device:
            opts += "--device=%s " % self.device
        if self.emulthree:
            opts += "--emulthree " 

        retval = ""
        if self.mouse:
            retval = "# System mouse\nmouse %s%s\n" % (opts, self.mouse)
        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--device", dest="device", default="")
        op.add_option("--emulthree", dest="emulthree", default=False, action="store_true")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
        self.mouse = extra

class FC3_Mouse(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)
