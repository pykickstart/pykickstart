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

class FC3_Lang(KickstartCommand):
    def __init__(self, writePriority=0, lang=""):
        KickstartCommand.__init__(self, writePriority)
        self.lang = lang

    def __str__(self):
        if self.lang != "":
            return "# System language\nlang %s\n" % self.lang
        else:
            return ""

    def parse(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s only takes one argument") % "lang")

        self.lang = args[0]
