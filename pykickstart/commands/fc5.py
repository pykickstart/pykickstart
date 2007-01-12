#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import string
import warnings

from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

### INHERIT FROM A PREVIOUS RELEASE
from fc4 import *

class FC5Version(FC4Version):
    ###
    ### DATA CLASSES
    ###
    class RaidData(FC4Version.RaidData):
        def __init__(self, device=None, fsopts="", fstype="", level="",
                     format=True, spares=0, preexist=False, mountpoint="",
                     members=None, bytesPerInode=4096):
            FC4Version.RaidData.__init__(self, device=device, fsopts=fsopts,
                                         fstype=fstype, level=level,
                                         format=format, spares=spares,
                                         preexist=preexist,
                                         mountpoint=mountpoint, members=members)
            self.bytesPerInode = bytesPerInode

        def __str__(self):
            retval = "raid %s" % self.mountpoint

            if self.bytesPerInode != 0:
                retval += " --bytes-per-inode=%d" % self.bytesPerInode
            if self.device != "":
                retval += " --device=%s" % self.device
            if self.fsopts != "":
                retval += " --fsoptions=\"%s\"" % self.fsopts
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

            return retval + " %s\n" % string.join(self.members)


    ###
    ### COMMAND CLASSES
    ###
    class LangSupport(DeprecatedCommand):
        def __init__(self):
            DeprecatedCommand.__init__(self)

    class Raid(FC4Version.Raid):
        def __init__(self, writePriority=140, raidList=None):
            FC4Version.Raid.__init__(self, writePriority, raidList)

        def reset(self):
            self.raidList = []

        def parse(self, args):
            def raid_cb (option, opt_str, value, parser):
                parser.values.format = False
                parser.values.preexist = True

            def device_cb (option, opt_str, value, parser):
                if value[0:2] == "md":
                    parser.values.ensure_value(option.dest, value[2:])
                else:
                    parser.values.ensure_value(option.dest, value)

            def level_cb (option, opt_str, value, parser):
                if value == "RAID0" or value == "0":
                    parser.values.ensure_value(option.dest, "RAID0")
                elif value == "RAID1" or value == "1":
                    parser.values.ensure_value(option.dest, "RAID1")
                elif value == "RAID5" or value == "5":
                    parser.values.ensure_value(option.dest, "RAID5")
                elif value == "RAID6" or value == "6":
                    parser.values.ensure_value(option.dest, "RAID6")

            op = KSOptionParser(self.lineno)
            op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                          type="int", nargs=1)
            op.add_option("--device", action="callback", callback=device_cb,
                          dest="device", type="string", nargs=1, required=1)
            op.add_option("--fsoptions", dest="fsopts")
            op.add_option("--fstype", dest="fstype")
            op.add_option("--level", dest="level", action="callback",
                          callback=level_cb, type="string", nargs=1)
            op.add_option("--noformat", action="callback", callback=raid_cb,
                          dest="format", default=True, nargs=0)
            op.add_option("--spares", dest="spares", action="store", type="int",
                          nargs=1, default=0)
            op.add_option("--useexisting", dest="preexist", action="store_true",
                          default=False)

            (opts, extra) = op.parse_args(args=args)

            if len(extra) == 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "raid")

            rd = self.dispatcher.RaidData()
            self._setToObj(op, opts, rd)

            # --device can't just take an int in the callback above, because it
            # could be specificed as "mdX", which causes optparse to error when
            # it runs int().
            rd.device = int(rd.device)
            rd.mountpoint = extra[0]
            rd.members = extra[1:]
            self.add(rd)

    ##
    ## MAIN
    ##
    def __init__(self):
        FC4Version.__init__(self)
        self.registerHandler(self.LangSupport(), ["langsupport"])
        self.registerHandler(self.Raid(), ["raid"])
