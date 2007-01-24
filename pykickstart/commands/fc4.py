#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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
from pykickstart.version import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

### INHERIT FROM A PREVIOUS RELEASE
from fc3 import *

class FC4Handler(FC3Handler):
    ##
    ## DATA CLASSES
    ##
    class LogVolData(FC3Handler.LogVolData):
        def __init__(self, bytesPerInode=4096, fsopts="", fstype="", grow=False,
                     maxSizeMB=0, name="", format=True, percent=0,
                     recommended=False, size=None, preexist=False, vgname="",
                     mountpoint=""):
            FC3Handler.LogVolData.__init__(self, fstype=fstype, grow=grow,
                                           maxSizeMB=maxSizeMB, name=name,
                                           format=format, percent=percent,
                                           recommended=recommended, size=size,
                                           preexist=preexist, vgname=vgname,
                                           mountpoint=mountpoint)
            self.bytesPerInode = bytesPerInode
            self.fsopts = fsopts

        def __str__(self):
            retval = FC3Handler.LogVolData.__str__().strip()

            if self.bytesPerInode > 0:
                retval += " --bytes-per-inode=%d" % self.bytesPerInode
            if self.fsopts != "":
                retval += " --fsoptions=\"%s\"" % self.fsopts

            return retval + "\n"

    class NetworkData(FC3Handler.NetworkData):
        def __init__(self, bootProto="dhcp", dhcpclass="", device="", essid="",
                     ethtool="", gateway="", hostname="", ip="", mtu="",
                     nameserver="", netmask="", nodns=False, notksdevice=False,
                     onboot=True, wepkey=""):
            FC3Handler.NetworkData.__init__(self, bootProto=bootProto,
                                            dhcpclass=dhcpclass, device=device,
                                            essid=essid, ethtool=ethtool,
                                            gateway=gateway, hostname=hostname,
                                            ip=ip, mtu=mtu, netmask=netmask,
                                            nameserver=nameserver, nodns=nodns,
                                            onboot=onboot, wepkey=wepkey)
            self.notksdevice = notksdevice

        def __str__(self):
            retval = FC3Handler.NetworkData.__str__().strip()

            if self.notksdevice:
                retval += " --notksdevice"

            return retval + "\n"

    class PartData(FC3Handler.PartData):
        def __init__(self, active=False, primOnly=False, bytesPerInode=4096,
                     end=0, fsopts="", fstype="", grow=False, label="",
                     maxSizeMB=0, format=True, onbiosdisk="", disk="",
                     onPart="", recommended=False, size=None, start=0,
                     mountpoint=""):
            FC3Handler.PartData.__init__(self, active=active, primOnly=primOnly,
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
            retval = FC3Handler.PartData.__str__().strip()

            if self.bytesPerInode != 0:
                retval += " --bytes-per-inode=%d" % self.bytesPerInode
            if self.fsopts != "":
                retval += " --fsoptions=\"%s\"" % self.fsopts
            if self.label != "":
                retval += " --label=%s" % self.label

            return retval + "\n"

    class RaidData(FC3Handler.RaidData):
        def __init__(self, device=None, fsopts="", fstype="", level="",
                     format=True, spares=0, preexist=False, mountpoint="",
                     members=None):
            FC3Handler.RaidData.__init__(self, device=device, fstype=fstype,
                                         level=level, format=format,
                                         spares=spares, preexist=preexist,
                                         mountpoint=mountpoint,
                                         members=members)
            self.fsopts = fsopts

        def __str__(self):
            retval = FC3Handler.RaidData.__str__().strip()

            if self.fsopts != "":
                retval += " --fsoptions=\"%s\"" % self.fsopts

            return retval

    ###
    ### COMMAND CLASSES
    ###
    class Bootloader(KickstartCommand):
        def __init__(self, writePriority=0, appendLine="", driveorder=None,
                     forceLBA=False, location="mbr", md5pass="", password="",
                     upgrade=False):
            KickstartCommand.__init__(self, writePriority)
            self.appendLine = appendLine

            if driveorder == None:
                driveorder = []

            self.driveorder = driveorder

            self.forceLBA = forceLBA
            self.location = location
            self.md5pass = md5pass
            self.password = password
            self.upgrade = upgrade

        def __str__(self):
            retval = "# System bootloader configuration\nbootloader"

            if self.appendLine != "":
                retval += " --append=\"%s\"" % self.appendLine
            if self.location:
                retval += " --location=%s" % self.location
            if self.forceLBA:
                retval += " --lba32"
            if self.password != "":
                retval += " --password=%s" % self.password
            if self.md5pass != "":
                retval += " --md5pass=%s" % self.md5pass
            if self.upgrade:
                retval += " --upgrade"
            if len(self.driveorder) > 0:
                retval += " --driveorder=%s" % string.join(self.driveorder, ",")

            return retval + "\n"

        def parse(self, args):
            def driveorder_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)
                
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--append", dest="appendLine")
            op.add_option("--location", dest="location", type="choice",
                          default="mbr",
                          choices=["mbr", "partition", "none", "boot"])
            op.add_option("--lba32", dest="forceLBA", action="store_true",
                          default=False)
            op.add_option("--password", dest="password", default="")
            op.add_option("--md5pass", dest="md5pass", default="")
            op.add_option("--upgrade", dest="upgrade", action="store_true",
                          default=False)
            op.add_option("--driveorder", dest="driveorder", action="callback",
                          callback=driveorder_cb, nargs=1, type="string")

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class LogVol(FC3Handler.LogVol):
        def __init__(self, writePriority=132, lvList=None):
            FC3Handler.LogVol.__init__(self, writePriority, lvList)

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

            lvd = self.handler.LogVolData()
            self._setToObj(op, opts, lvd)
            lvd.mountpoint=extra[0]
            self.add(lvd)

    class MediaCheck(KickstartCommand):
        def __init__(self, writePriority=0, mediacheck=False):
            KickstartCommand.__init__(self, writePriority)
            self.mediacheck = mediacheck

        def __str__(self):
            if self.mediacheck:
                return "mediacheck\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "mediacheck")

            self.mediacheck = True

    class Network(FC3Handler.Network):
        def __init__(self, writePriority=0, network=None):
            FC3Handler.Network.__init__(self, writePriority, network)

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--bootproto", dest="bootProto", default="dhcp",
                          choices=["dhcp", "bootp", "static"])
            op.add_option("--class", dest="dhcpclass")
            op.add_option("--device", dest="device")
            op.add_option("--essid", dest="essid")
            op.add_option("--ethtool", dest="ethtool")
            op.add_option("--gateway", dest="gateway")
            op.add_option("--hostname", dest="hostname")
            op.add_option("--ip", dest="ip")
            op.add_option("--mtu", dest="mtu")
            op.add_option("--nameserver", dest="nameserver")
            op.add_option("--netmask", dest="netmask")
            op.add_option("--nodns", dest="nodns", action="store_true",
                          default=False)
            op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                          default=False)
            op.add_option("--onboot", dest="onboot", action="store",
                          type="ksboolean")
            op.add_option("--wepkey", dest="wepkey")

            (opts, extra) = op.parse_args(args=args)
            nd = self.handler.NetworkData()
            self._setToObj(op, opts, nd)
            self.add(nd)

    class Partition(FC3Handler.Partition):
        def __init__(self, writePriority=130, partitions=None):
            FC3Handler.Partition.__init__(self, writePriority, partitions)

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

            pd = self.handler.PartData()
            self._setToObj(op, opts, pd)
            pd.mountpoint=extra[0]
            self.add(pd)

    class Raid(FC3Handler.Raid):
        def __init__(self, writePriority=140, raidList=None):
            FC3Handler.Raid.__init__(self, writePriority, raidList)

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

            op = KSOptionParser(lineno=self.lineno)
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

            rd = self.handler.RaidData()
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
        FC3Handler.__init__(self)
        self.version = FC4

        self.unregisterCommand(self.Bootloader)
        self.unregisterCommand(self.LiloCheck)

        self.registerCommand(self.Bootloader(), ["bootloader"])
        self.registerCommand(self.LogVol(), ["logvol"])
        self.registerCommand(self.MediaCheck(), ["mediacheck"])
        self.registerCommand(self.Network(), ["network"])
        self.registerCommand(self.Partition(), ["part", "partition"])
        self.registerCommand(self.Raid(), ["raid"])
