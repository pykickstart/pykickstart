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

class FC3DriverDisk(KickstartCommand):
    def __init__(self, writePriority=0, driverdisk=""):
        KickstartCommand.__init__(self, writePriority)
        self.driverdisk = driverdisk

    def __str__(self):
        if self.driverdisk != "":
            return "driverdisk %s\n" % self.driverdisk
        else:
            return ""

    def parse(self, args):
        self.driverdisk = string.join(args)
