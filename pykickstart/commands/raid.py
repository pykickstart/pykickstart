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
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_RaidData(BaseData):
    def __init__(self, device=None, fstype="", level="", format=True,
                 spares=0, preexist=False, mountpoint="", members=None):
        BaseData.__init__(self)
        self.device = device
        self.fstype = fstype
        self.level = level
        self.format = format
        self.spares = spares
        self.preexist = preexist
        self.mountpoint = mountpoint

        if members == None:
            members = []

        self.members = members

    def _getArgsAsStr(self):
        retval = ""

        if self.device != "":
            retval += " --device=%s" % self.device
        if self.fstype != "":
            retval += " --fstype=\"%s\"" % self.fstype
        if self.level != "":
            retval += " --level=%s" % self.level
        if not self.format:
            retval += " --noformat"
        if self.spares != 0:
            retval += " --spares=%d" % self.spares
        if self.preexist:
            retval += " --useexisting"

        return retval

    def __str__(self):
        return "raid %s %s %s\n" % (self.mountpoint, self._getArgsAsStr(),
                                    string.join(self.members))

class FC4_RaidData(FC3_RaidData):
    def __init__(self, device=None, fsopts="", fstype="", level="",
                 format=True, spares=0, preexist=False, mountpoint="",
                 members=None):
        FC3_RaidData.__init__(self, device=device, fstype=fstype,
                             level=level, format=format,
                             spares=spares, preexist=preexist,
                             mountpoint=mountpoint,
                             members=members)
        self.fsopts = fsopts

    def _getArgsAsStr(self):
        retval = FC3_RaidData._getArgsAsStr(self)

        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts

        return retval

class FC5_RaidData(FC4_RaidData):
    def __init__(self, device=None, fsopts="", fstype="", level="",
                 format=True, spares=0, preexist=False, mountpoint="",
                 members=None, bytesPerInode=4096):
        FC4_RaidData.__init__(self, device=device, fsopts=fsopts,
                             fstype=fstype, level=level,
                             format=format, spares=spares,
                             preexist=preexist,
                             mountpoint=mountpoint, members=members)
        self.bytesPerInode = bytesPerInode

    def _getArgsAsStr(self):
        retval = FC4_RaidData._getArgsAsStr(self)

        if self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode

        return retval

F7_RaidData = FC5_RaidData

class FC3_Raid(KickstartCommand):
    def __init__(self, writePriority=140, raidList=None):
        KickstartCommand.__init__(self, writePriority)

        # A dict of all the RAID levels we support.  This means that if we
        # support more levels in the future, subclasses don't have to
        # duplicate too much.
        self.levelMap = { "RAID0": "RAID0", "0": "RAID0",
                          "RAID1": "RAID1", "1": "RAID1",
                          "RAID5": "RAID5", "5": "RAID5",
                          "RAID6": "RAID6", "6": "RAID6" }

        if raidList == None:
            raidList = []

        self.raidList = raidList

    def __str__(self):
        retval = ""

        for raid in self.raidList:
            retval += raid.__str__()

        return retval

    def _getParser(self):
        def raid_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        def device_cb (option, opt_str, value, parser):
            if value[0:2] == "md":
                parser.values.ensure_value(option.dest, value[2:])
            else:
                parser.values.ensure_value(option.dest, value)

        def level_cb (option, opt_str, value, parser):
            if self.levelMap.has_key(value):
                parser.values.ensure_value(option.dest, self.levelMap[value])

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--device", action="callback", callback=device_cb,
                      dest="device", type="string", nargs=1, required=1)
        op.add_option("--fstype", dest="fstype")
        op.add_option("--level", dest="level", action="callback",
                      callback=level_cb, type="string", nargs=1)
        op.add_option("--noformat", action="callback", callback=raid_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--spares", dest="spares", action="store", type="int",
                      nargs=1, default=0)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "raid")

        rd = FC3_RaidData()
        self._setToObj(op, opts, rd)

        # --device can't just take an int in the callback above, because it
        # could be specificed as "mdX", which causes optparse to error when
        # it runs int().
        rd.device = int(rd.device)
        rd.mountpoint = extra[0]
        rd.members = extra[1:]
        self.add(rd)

    def add(self, newObj):
        self.raidList.append(newObj)

class FC4_Raid(FC3_Raid):
    def __init__(self, writePriority=140, raidList=None):
        FC3_Raid.__init__(self, writePriority, raidList)

    def _getParser(self):
        op = FC3_Raid._getParser(self)
        op.add_option("--fsoptions", dest="fsopts")
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "raid")

        rd = FC4_RaidData()
        self._setToObj(op, opts, rd)

        # --device can't just take an int in the callback above, because it
        # could be specificed as "mdX", which causes optparse to error when
        # it runs int().
        rd.device = int(rd.device)
        rd.mountpoint = extra[0]
        rd.members = extra[1:]
        self.add(rd)

class FC5_Raid(FC4_Raid):
    def __init__(self, writePriority=140, raidList=None):
        FC4_Raid.__init__(self, writePriority, raidList)

    def reset(self):
        self.raidList = []

    def _getParser(self):
        op = FC4_Raid._getParser(self)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "raid")

        rd = FC5_RaidData()
        self._setToObj(op, opts, rd)

        # --device can't just take an int in the callback above, because it
        # could be specificed as "mdX", which causes optparse to error when
        # it runs int().
        rd.device = int(rd.device)
        rd.mountpoint = extra[0]
        rd.members = extra[1:]
        self.add(rd)

class F7_Raid(FC5_Raid):
    def __init__(self, writePriority=140, raidList=None):
        FC5_Raid.__init__(self, writePriority, raidList)

        self.levelMap.update({"RAID10": "RAID10", "10": "RAID10"})
