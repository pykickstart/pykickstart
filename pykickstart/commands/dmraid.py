#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006, 2007 Red Hat, Inc.
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
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6DmRaidData(BaseData):
    def __init__(self, name="", devices=None, dmset=None):
        BaseData.__init__(self)
        self.name = name

        if devices == None:
            devices = []

        self.devices = devices
        self.dmset = dmset

    def __str__(self):
        retval = "dmraid --name=%s" % self.name

        for dev in self.devices:
            retval += " --dev=\"%s\"" % dev

        return retval + "\n"

class FC6DmRaid(KickstartCommand):
    def __init__(self, writePriority=60, dmraids=None):
        KickstartCommand.__init__(self, writePriority)

        if dmraids == None:
            dmraids = []

        self.dmraids = dmraids

    def __str__(self):
        retval = ""
        for dm in self.dmraids:
            retval += dm.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--dev", dest="devices", action="append", type="string",
                      required=1)

        dm = FC6DmRaidData()
        (opts, extra) = op.parse_args(args=args)
        dm.name = dm.name.split('/')[-1]
        self._setToObj(op, opts, dm)
        self.add(dm)

    def add(self, newObj):
        self.dmraids.append(newObj)
