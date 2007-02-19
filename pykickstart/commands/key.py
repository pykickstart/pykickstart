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
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class F7_Key(KickstartCommand):
    def __init__(self, writePriority=0, key=""):
        KickstartCommand.__init__(self, writePriority)
        self.key = key

    def __str__(self):
        if self.key == KS_INSTKEY_SKIP:
            return "key --skip\n"
        elif self.key != "":
            return "key %s\n" % self.key
        else:
            return ""

    def parse(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "key")

        if args[0] == "--skip":
            self.key = KS_INSTKEY_SKIP
        else:
            self.key = args[0]

RHEL5_Key = F7_Key
