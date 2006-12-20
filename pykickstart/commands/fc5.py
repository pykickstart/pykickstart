#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import string
import warnings

from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

### INHERIT FROM A PREVIOUS RELEASE
from fc4 import *


###
### HANDLER/DISPATCHER
###
class FC5Handler(FC4Handler):
    def __init__(self):
        FC4Handler.__init__(self)
        self.registerHandler(CommandLangSupport(), ["langsupport"])


###
### COMMAND CLASSES
###

class CommandLangSupport(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)
