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
import string

from pykickstart.base import *

class FC3_Device(KickstartCommand):
    def __init__(self, writePriority=0, device=""):
        KickstartCommand.__init__(self, writePriority)
        self.device = device

    def __str__(self):
        if self.device != "":
            return "device %s\n" % self.device
        else:
            return ""

    def parse(self, args):
        self.device = string.join(args)
