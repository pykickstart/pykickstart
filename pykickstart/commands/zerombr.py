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
import warnings

from pykickstart.base import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_ZeroMbr(KickstartCommand):
    def __init__(self, writePriority=110, zerombr=False):
        KickstartCommand.__init__(self, writePriority)
        self.zerombr = zerombr

    def __str__(self):
        if self.zerombr:
            return "# Clear the Master Boot Record\nzerombr\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            warnings.warn(_("Ignoring deprecated option on line %s:  The zerombr command no longer takes any options.  In future releases, this will result in a fatal error from kickstart.  Please modify your kickstart file to remove any options.") % self.lineno, DeprecationWarning)

        self.zerombr = True
