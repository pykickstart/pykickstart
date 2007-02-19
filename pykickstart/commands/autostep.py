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
from pykickstart.options import *

class FC3_AutoStep(KickstartCommand):
    def __init__(self, writePriority=0, autoscreenshot=False):
        KickstartCommand.__init__(self, writePriority)
        self.autoscreenshot = autoscreenshot

    def __str__(self):
        if self.autoscreenshot:
            return "autostep --autoscreenshot\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--autoscreenshot", dest="autoscreenshot",
                      action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
