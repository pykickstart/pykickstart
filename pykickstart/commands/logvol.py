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
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3LogVolData(BaseData):
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

    def __str__(self):
        retval = "logvol %s" % self.mountpoint

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

        return retval + " --name=%s --vgname=%s\n" % (self.name, self.vgname)

class FC4LogVolData(FC3LogVolData):
    def __init__(self, bytesPerInode=4096, fsopts="", fstype="", grow=False,
                 maxSizeMB=0, name="", format=True, percent=0,
                 recommended=False, size=None, preexist=False, vgname="",
                 mountpoint=""):
        FC3LogVolData.__init__(self, fstype=fstype, grow=grow,
                               maxSizeMB=maxSizeMB, name=name,
                               format=format, percent=percent,
                               recommended=recommended, size=size,
                               preexist=preexist, vgname=vgname,
                               mountpoint=mountpoint)
        self.bytesPerInode = bytesPerInode
        self.fsopts = fsopts

    def __str__(self):
        retval = FC3LogVolData.__str__(self).strip()

        if self.bytesPerInode > 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts

        return retval + "\n"

class FC3LogVol(KickstartCommand):
    def __init__(self, writePriority=132, lvList=None):
        KickstartCommand.__init__(self, writePriority)

        if lvList == None:
            lvList = []

        self.lvList = lvList

    def __str__(self):
        retval = ""

        for part in self.lvList:
            retval += part.__str__()

        return retval

    def parse(self, args):
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

        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "logvol")

        lvd = FC3LogVolData()
        self._setToObj(op, opts, lvd)
        lvd.mountpoint=extra[0]
        self.add(lvd)

    def add(self, newObj):
        self.lvList.append(newObj)

class FC4LogVol(FC3LogVol):
    def __init__(self, writePriority=132, lvList=None):
        FC3LogVol.__init__(self, writePriority, lvList)

    def parse(self, args):
        def lv_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
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

        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "logvol")

        lvd = FC4LogVolData()
        self._setToObj(op, opts, lvd)
        lvd.mountpoint=extra[0]
        self.add(lvd)
