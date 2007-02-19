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

class FC3PartData(BaseData):
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

    def __str__(self):
        retval = "part %s" % self.mountpoint

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

        return retval + "\n"

class FC4PartData(FC3PartData):
    def __init__(self, active=False, primOnly=False, bytesPerInode=4096,
                 end=0, fsopts="", fstype="", grow=False, label="",
                 maxSizeMB=0, format=True, onbiosdisk="", disk="",
                 onPart="", recommended=False, size=None, start=0,
                 mountpoint=""):
        FC3PartData.__init__(self, active=active, primOnly=primOnly,
                             end=end, fstype=fstype, grow=grow,
                             maxSizeMB=maxSizeMB, format=format,
                             onbiosdisk=onbiosdisk, disk=disk,
                             onPart=onPart, size=size, start=start,
                             recommended=recommended,
                             mountpoint=mountpoint)
        self.bytesPerInode = bytesPerInode
        self.fsopts = fsopts
        self.label = label

    def __str__(self):
        retval = FC3PartData.__str__(self).strip()

        if self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.label != "":
            retval += " --label=%s" % self.label

        return retval + "\n"

class FC3Partition(KickstartCommand):
    def __init__(self, writePriority=130, partitions=None):
        KickstartCommand.__init__(self, writePriority)

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

    def parse(self, args):
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

        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "partition")

        pd = FC3PartData()
        self._setToObj(op, opts, pd)
        pd.mountpoint=extra[0]
        self.add(pd)

    def add(self, newObj):
        self.partitions.append(newObj)

class FC4Partition(FC3Partition):
    def __init__(self, writePriority=130, partitions=None):
        FC3Partition.__init__(self, writePriority, partitions)

    def parse(self, args):
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
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--end", dest="end", action="store", type="int",
                      nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        op.add_option("--fstype", "--type", dest="fstype")
        op.add_option("--grow", dest="grow", action="store_true", default=False)
        op.add_option("--label", dest="label")
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

        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "partition")

        pd = FC4PartData()
        self._setToObj(op, opts, pd)
        pd.mountpoint=extra[0]
        self.add(pd)
