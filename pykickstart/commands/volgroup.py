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
        self.op = self._getParser()

        self._setDataClass()

        if vgList == None:
            vgList = []

        self.vgList = vgList

    def __str__(self):
        retval = ""
        for vg in self.vgList:
            retval += vg.__str__()

        return retval

    def _setDataClass(self):
        self.dataType = FC3_VolGroupData

    def _getParser(self):
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
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)
        vg = self.dataType()
        self._setToObj(self.op, opts, vg)
        vg.vgname = extra[0]
        vg.physvols = extra[1:]
        self.add(vg)

    def add(self, newObj):
        self.vgList.append(newObj)
