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
from pykickstart.constants import *
from pykickstart.options import *

class FC3_SELinux(KickstartCommand):
    def __init__(self, writePriority=0, selinux=None):
        KickstartCommand.__init__(self, writePriority)
        self.selinux = selinux

    def __str__(self):
        retval = "# SELinux configuration\n"

        if self.selinux == SELINUX_DISABLED:
            return retval + "selinux --disabled\n"
        elif self.selinux == SELINUX_ENFORCING:
            return retval + "selinux --enforcing\n"
        elif self.selinux == SELINUX_PERMISSIVE:
            return retval + "selinux --permissive\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disabled", dest="sel", action="store_const",
                      const=SELINUX_DISABLED)
        op.add_option("--enforcing", dest="sel", action="store_const",
                      const=SELINUX_ENFORCING)
        op.add_option("--permissive", dest="sel", action="store_const",
                      const=SELINUX_PERMISSIVE)

        (opts, extra) = op.parse_args(args=args)
        self.selinux = opts.sel
