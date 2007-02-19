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

class FC3Firstboot(KickstartCommand):
    def __init__(self, writePriority=0, firstboot=FIRSTBOOT_SKIP):
        KickstartCommand.__init__(self, writePriority)
        self.firstboot = firstboot

    def __str__(self):
        if self.firstboot == FIRSTBOOT_SKIP:
            return "firstboot --disable\n"
        elif self.firstboot == FIRSTBOOT_DEFAULT:
            return "# Run the Setup Agent on first boot\nfirstboot --enable\n"
        elif self.firstboot == FIRSTBOOT_RECONFIG:
            return "# Run the Setup Agent on first boot\nfirstboot --reconfig\n"

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disable", "--disabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_SKIP)
        op.add_option("--enable", "--enabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_DEFAULT)
        op.add_option("--reconfig", dest="firstboot", action="store_const",
                      const=FIRSTBOOT_RECONFIG)

        (opts, extra) = op.parse_args(args=args)
        self.firstboot = opts.firstboot
