#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
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
        self.op = self._getParser()

        self._setDataClass()

        if zfcp == None:
            zfcp = []

        self.zfcp = zfcp

    def __str__(self):
        retval = ""
        for zfcp in self.zfcp:
            retval += zfcp.__str__()

        return retval

    def _setDataClass(self):
        self.dataType = FC3_ZFCPData

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--devnum", dest="devnum", required=1)
        op.add_option("--fcplun", dest="fcplun", required=1)
        op.add_option("--scsiid", dest="scsiid", required=1)
        op.add_option("--scsilun", dest="scsilun", required=1)
        op.add_option("--wwpn", dest="wwpn", required=1)
        return op

    def parse(self, args):
        zd = self._setDataClass()
        (opts, extra) = self.op.parse_args(args)
        self._setToObj(self.op, opts, zd)
        self.add(zd)

    def add(self, newObj):
        self.zfcp.append(newObj)
