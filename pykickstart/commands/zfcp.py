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
from pykickstart.options import *

class FC3_ZFCPData(BaseData):
    def __init__(self, devnum="", wwpn="", fcplun="", scsiid="", scsilun=""):
        BaseData.__init__(self)
        self.devnum = devnum
        self.wwpn = wwpn
        self.fcplun = fcplun
        self.scsiid = scsiid
        self.scsilun = scsilun

    def __str__(self):
        retval = "zfcp"

        if self.devnum != "":
            retval += " --devnum=%s" % self.devnum
        if self.wwpn != "":
            retval += " --wwpn=%s" % self.wwpn
        if self.fcplun != "":
            retval += " --fcplun=%s" % self.fcplun
        if self.scsiid != "":
            retval += " --scsiid=%s" % self.scsiid
        if self.scsilun != "":
            retval += " --scsilun=%s" % self.scsilun

        return retval + "\n"

class FC3_ZFCP(KickstartCommand):
    def __init__(self, writePriority=0, zfcp=None):
        KickstartCommand.__init__(self, writePriority)

        if zfcp == None:
            zfcp = []

        self.zfcp = zfcp

    def __str__(self):
        retval = ""
        for zfcp in self.zfcp:
            retval += zfcp.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--devnum", dest="devnum", required=1)
        op.add_option("--fcplun", dest="fcplun", required=1)
        op.add_option("--scsiid", dest="scsiid", required=1)
        op.add_option("--scsilun", dest="scsilun", required=1)
        op.add_option("--wwpn", dest="wwpn", required=1)

        zd = FC3_ZFCPData()
        (opts, extra) = op.parse_args(args)
        self._setToObj(op, opts, zd)
        self.add(zd)

    def add(self, newObj):
        self.zfcp.append(newObj)
