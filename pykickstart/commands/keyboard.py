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

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Keyboard(KickstartCommand):
    def __init__(self, writePriority=0, keyboard=""):
        KickstartCommand.__init__(self, writePriority)
        self.keyboard = keyboard

    def __str__(self):
        if self.keyboard != "":
            return "# System keyboard\nkeyboard %s\n" % self.keyboard
        else:
            return ""

    def parse(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s only takes one argument") % "keyboard")

        self.keyboard = args[0]
