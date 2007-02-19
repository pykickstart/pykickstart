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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6MpPathData(BaseData):
    def __init__(self, mpdev="", device="", rule=""):
        BaseData.__init__(self)
        self.mpdev = mpdev
        self.device = device
        self.rule = rule

    def __str__(self):
        return " --device=%s --rule=\"%s\"" % (self.device, self.rule)

class FC6MultiPathData(BaseData):
    def __init__(self, name="", paths=None):
        BaseData.__init__(self)
        self.name = name

        if paths == None:
            paths = []

        self.paths = paths

    def __str__(self):
        retval = ""

        for path in self.paths:
            retval += "multipath --mpdev=%s %s\n" % (self.name, path.__str__())

        return retval

class FC6MultiPath(KickstartCommand):
    def __init__(self, writePriority=50, mpaths=None):
        KickstartCommand.__init__(self, writePriority)

        if mpaths == None:
            mpaths = []

        self.mpaths = mpaths

    def __str__(self):
        retval = ""
        for mpath in self.mpaths:
            retval += mpath.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--device", dest="device", action="store", type="string",
                      required=1)
        op.add_option("--rule", dest="rule", action="store", type="string",
                      required=1)

        (opts, extra) = op.parse_args(args=args)
        dd = FC6MpPathData()
        self._setToObj(op, opts, dd)
        dd.mpdev = dd.mpdev.split('/')[-1]

        parent = None
        for x in range(0, len(self.mpaths)):
            mpath = self.mpaths[x]
            for path in mpath.paths:
                if path.device == dd.device:
                    mapping = {"device": path.device, "multipathdev": path.mpdev}
                    raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Device '%(device)s' is already used in multipath '%(multipathdev)s'") % mapping)
            if mpath.name == dd.mpdev:
                parent = x

        if parent is None:
            mpath = FC6MultiPathData()
            self.add(mpath)
        else:
            mpath = self.mpaths[x]

        mpath.paths.append(dd)

    def add(self, newObj):
        self.mpaths.append(newObj)
