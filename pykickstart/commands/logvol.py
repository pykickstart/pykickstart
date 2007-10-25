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
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_LogVolData(BaseData):
    def __init__(self, fstype="", grow=False, maxSizeMB=0, name="",
                 format=True, percent=0, recommended=False, size=None,
                 preexist=False, vgname="", mountpoint=""):
        BaseData.__init__(self)
        self.fstype = fstype
        self.grow = grow
        self.maxSizeMB = maxSizeMB
        self.name = name
        self.format = format
        self.percent = percent
        self.recommended = recommended
        self.size = size
        self.preexist = preexist
        self.vgname = vgname
        self.mountpoint = mountpoint

    def _getArgsAsStr(self):
        retval = ""

        if self.fstype != "":
            retval += " --fstype=\"%s\"" % self.fstype
        if self.grow:
            retval += " --grow"
        if self.maxSizeMB > 0:
            retval += " --maxsize=%d" % self.maxSizeMB
        if not self.format:
            retval += " --noformat"
        if self.percent > 0:
            retval += " --percent=%d" % self.percent
        if self.recommended:
            retval += " --recommended"
        if self.size > 0:
            retval += " --size=%d" % self.size
        if self.preexist:
            retval += " --useexisting"

        return retval

    def __str__(self):
        return "logvol %s %s --name=%s --vgname=%s\n" % (self.mountpoint, self._getArgsAsStr(), self.name, self.vgname)

class FC4_LogVolData(FC3_LogVolData):
    def __init__(self, bytesPerInode=4096, fsopts="", fstype="", grow=False,
                 maxSizeMB=0, name="", format=True, percent=0,
                 recommended=False, size=None, preexist=False, vgname="",
                 mountpoint=""):
        FC3_LogVolData.__init__(self, fstype=fstype, grow=grow,
                               maxSizeMB=maxSizeMB, name=name,
                               format=format, percent=percent,
                               recommended=recommended, size=size,
                               preexist=preexist, vgname=vgname,
                               mountpoint=mountpoint)
        self.bytesPerInode = bytesPerInode
        self.fsopts = fsopts

    def _getArgsAsStr(self):
        retval = FC3_LogVolData._getArgsAsStr(self)

        if self.bytesPerInode > 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts

        return retval

class FC3_LogVol(KickstartCommand):
    def __init__(self, writePriority=132, lvList=None):
        KickstartCommand.__init__(self, writePriority)
        self._setClassData()

        if lvList == None:
            lvList = []

        self.lvList = lvList

    def __str__(self):
        retval = ""

        for part in self.lvList:
            retval += part.__str__()

        return retval

    def _setClassData(self):
        self.dataType = FC3_LogVolData

    def _getParser(self):
        def lv_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--fstype", dest="fstype")
        op.add_option("--grow", dest="grow", action="store_true",
                      default=False)
        op.add_option("--maxsize", dest="maxSizeMB", action="store", type="int",
                      nargs=1)
        op.add_option("--name", dest="name", required=1)
        op.add_option("--noformat", action="callback", callback=lv_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--percent", dest="percent", action="store", type="int",
                      nargs=1)
        op.add_option("--recommended", dest="recommended", action="store_true",
                      default=False)
        op.add_option("--size", dest="size", action="store", type="int",
                      nargs=1)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)
        op.add_option("--vgname", dest="vgname", required=1)
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "logvol")

        lvd = self.dataType()
        self._setToObj(op, opts, lvd)
        lvd.mountpoint=extra[0]
        self.add(lvd)

    def add(self, newObj):
        self.lvList.append(newObj)

class FC4_LogVol(FC3_LogVol):
    def __init__(self, writePriority=132, lvList=None):
        FC3_LogVol.__init__(self, writePriority, lvList)

    def _getParser(self):
        op = FC3_LogVol._getParser(self)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        return op

    def _setClassData(self):
        self.dataType = FC4_LogVolData
