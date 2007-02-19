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

class FC3_DisplayMode(KickstartCommand):
    def __init__(self, writePriority=0, displayMode=DISPLAY_MODE_GRAPHICAL):
        KickstartCommand.__init__(self, writePriority)
        self.displayMode = displayMode

    def __str__(self):
        if self.displayMode == DISPLAY_MODE_CMDLINE:
            return "cmdline\n"
        elif self.displayMode == DISPLAY_MODE_GRAPHICAL:
            return "# Use graphical install\ngraphical\n"
        elif self.displayMode == DISPLAY_MODE_TEXT:
            return "# Use text mode install\ntext\n"

    def parse(self, args):
        if self.currentCmd == "cmdline":
            self.displayMode = DISPLAY_MODE_CMDLINE
        elif self.currentCmd == "graphical":
            self.displayMode = DISPLAY_MODE_GRAPHICAL
        elif self.currentCmd == "text":
            self.displayMode = DISPLAY_MODE_TEXT
