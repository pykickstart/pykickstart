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
from pykickstart.options import *

class FC3_VolGroupData(BaseData):
    def __init__(self, format=True, pesize=32768, preexist=False, vgname="",
                 physvols=None):
        BaseData.__init__(self)
        self.format = format
        self.pesize = pesize
        self.preexist = preexist
        self.vgname = vgname

        if physvols == None:
            physvols = []

        self.physvols = physvols

    def __str__(self):
        retval = "volgroup %s" % self.vgname

        if not self.format:
            retval += " --noformat"
        if self.pesize != 0:
            retval += " --pesize=%d" % self.pesize
        if self.preexist:
            retval += " --useexisting"

        return retval + " " + string.join(self.physvols, ",") + "\n"

class FC3_VolGroup(KickstartCommand):
    def __init__(self, writePriority=131, vgList=None):
        KickstartCommand.__init__(self, writePriority)

        if vgList == None:
            vgList = []

        self.vgList = vgList

    def __str__(self):
        retval = ""
        for vg in self.vgList:
            retval += vg.__str__()

        return retval

    def parse(self, args):
        # Have to be a little more complicated to set two values.
        def vg_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--noformat", action="callback", callback=vg_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--pesize", dest="pesize", type="int", nargs=1,
                      default=32768)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        vg = FC3_VolGroupData()
        self._setToObj(op, opts, vg)
        vg.vgname = extra[0]
        vg.physvols = extra[1:]
        self.add(vg)

    def add(self, newObj):
        self.vgList.append(newObj)
