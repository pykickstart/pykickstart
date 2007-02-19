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

class FC3_Upgrade(KickstartCommand):
    def __init__(self, writePriority=0, upgrade=False):
        KickstartCommand.__init__(self, writePriority)
        self.upgrade = upgrade

    def __str__(self):
        if self.upgrade:
            return "# Upgrade existing installation\nupgrade\n"
        else:
            return "# Install OS instead of upgrade\ninstall\n"

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "upgrade")

        if self.currentCmd == "upgrade":
           self.upgrade = True
        else:
           self.upgrade = False
