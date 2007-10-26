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

class FC3_PartData(BaseData):
    def __init__(self, active=False, primOnly=False, end=0, fstype="",
                 grow=False, maxSizeMB=0, format=True, onbiosdisk="",
                 disk="", onPart="", recommended=False, size=None,
                 start=0, mountpoint=""):
        BaseData.__init__(self)
        self.active = active
        self.primOnly = primOnly
        self.end = end
        self.fstype = fstype
        self.grow = grow
        self.maxSizeMB = maxSizeMB
        self.format = format
        self.onbiosdisk = onbiosdisk
        self.disk = disk
        self.onPart = onPart
        self.recommended = recommended
        self.size = size
        self.start = start
        self.mountpoint = mountpoint

    def _getArgsAsStr(self):
        retval = ""

        if self.active:
            retval += " --active"
        if self.primOnly:
            retval += " --asprimary"
        if self.end != 0:
            retval += " --end=%d" % self.end
        if self.fstype != "":
            retval += " --fstype=\"%s\"" % self.fstype
        if self.grow:
            retval += " --grow"
        if self.maxSizeMB > 0:
            retval += " --maxsize=%d" % self.maxSizeMB
        if not self.format:
            retval += " --noformat"
        if self.onbiosdisk != "":
            retval += " --onbiosdisk=%s" % self.onbiosdisk
        if self.disk != "":
            retval += " --ondisk=%s" % self.disk
        if self.onPart != "":
            retval += " --onpart=%s" % self.onPart
        if self.recommended:
            retval += " --recommended"
        if self.size and self.size != 0:
            retval += " --size=%d" % int(self.size)
        if self.start != 0:
            retval += " --start=%d" % self.start

        return retval

    def __str__(self):
        return "part %s %s\n" % (self.mountpoint, self._getArgsAsStr())

class FC4_PartData(FC3_PartData):
    def __init__(self, active=False, primOnly=False, bytesPerInode=4096,
                 end=0, fsopts="", fstype="", grow=False, label="",
                 maxSizeMB=0, format=True, onbiosdisk="", disk="",
                 onPart="", recommended=False, size=None, start=0,
                 mountpoint=""):
        FC3_PartData.__init__(self, active=active, primOnly=primOnly,
                             end=end, fstype=fstype, grow=grow,
                             maxSizeMB=maxSizeMB, format=format,
                             onbiosdisk=onbiosdisk, disk=disk,
                             onPart=onPart, size=size, start=start,
                             recommended=recommended,
                             mountpoint=mountpoint)
        self.bytesPerInode = bytesPerInode
        self.fsopts = fsopts
        self.label = label

    def _getArgsAsStr(self):
        retval = FC3_PartData._getArgsAsStr(self)

        if self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.label != "":
            retval += " --label=%s" % self.label

        return retval

class F9_PartData(FC3_PartData):
    def __init__(self, active=False, primOnly=False, fsprofile="",
                 end=0, fsopts="", fstype="", grow=False, label="",
                 maxSizeMB=0, format=True, onbiosdisk="", disk="",
                 onPart="", recommended=False, size=None, start=0,
                 mountpoint=""):
        FC3_PartData.__init__(self, active=active, primOnly=primOnly,
                             end=end, fstype=fstype, grow=grow,
                             maxSizeMB=maxSizeMB, format=format,
                             onbiosdisk=onbiosdisk, disk=disk,
                             onPart=onPart, size=size, start=start,
                             recommended=recommended,
                             mountpoint=mountpoint)
        self.fsopts = fsopts
        self.label = label
        self.fsprofile = fsprofile

    def _getArgsAsStr(self):
        retval = FC3_PartData._getArgsAsStr(self)

        if self.fsprofile != "":
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.label != "":
            retval += " --label=%s" % self.label

        return retval


class FC3_Partition(KickstartCommand):
    def __init__(self, writePriority=130, partitions=None):
        KickstartCommand.__init__(self, writePriority)
        self._setClassData()

        if partitions == None:
            partitions = []

        self.partitions = partitions

    def __str__(self):
        retval = ""

        for part in self.partitions:
            retval += part.__str__()

        if retval != "":
            return "# Disk partitioning information\n" + retval
        else:
            return ""

    def _setClassData(self):
        self.dataType = FC3_PartData

    def _getParser(self):
        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--active", dest="active", action="store_true",
                      default=False)
        op.add_option("--asprimary", dest="primOnly", action="store_true",
                      default=False)
        op.add_option("--end", dest="end", action="store", type="int",
                      nargs=1)
        op.add_option("--fstype", "--type", dest="fstype")
        op.add_option("--grow", dest="grow", action="store_true", default=False)
        op.add_option("--maxsize", dest="maxSizeMB", action="store", type="int",
                      nargs=1)
        op.add_option("--noformat", dest="format", action="store_false",
                      default=True)
        op.add_option("--onbiosdisk", dest="onbiosdisk")
        op.add_option("--ondisk", "--ondrive", dest="disk")
        op.add_option("--onpart", "--usepart", dest="onPart", action="callback",
                      callback=part_cb, nargs=1, type="string")
        op.add_option("--recommended", dest="recommended", action="store_true",
                      default=False)
        op.add_option("--size", dest="size", action="store", type="int",
                      nargs=1)
        op.add_option("--start", dest="start", action="store", type="int",
                      nargs=1)
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "partition")

        pd = self.dataType()
        self._setToObj(op, opts, pd)
        pd.mountpoint=extra[0]
        self.add(pd)

    def add(self, newObj):
        self.partitions.append(newObj)

class FC4_Partition(FC3_Partition):
    def __init__(self, writePriority=130, partitions=None):
        FC3_Partition.__init__(self, writePriority, partitions)

        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

    def _setClassData(self):
        self.dataType = FC4_PartData

    def _getParser(self):
        op = FC3_Partition._getParser(self)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        op.add_option("--label", dest="label")
        return op

class F9_Partition(FC3_Partition):
    def __init__(self, writePriority=130, partitions=None):
        FC3_Partition.__init__(self, writePriority, partitions)

        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

    def _setClassData(self):
        self.dataType = F9_PartData

    def _getParser(self):
        op = FC3_Partition._getParser(self)
        op.add_option("--fsprofile", dest="fsprofile", action="store",
                      type="string", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        op.add_option("--label", dest="label")
        return op



