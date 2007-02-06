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
from base import *

class FC3Handler(BaseHandler):
    ##
    ## DATA CLASSES
    ##
    class LogVolData(BaseData):
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

    class NetworkData(BaseData):
        def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                     essid="", ethtool="", gateway="", hostname="", ip="",
                     mtu="", nameserver="", netmask="", nodns=False,
                     onboot=True, wepkey=""):
            BaseData.__init__(self)
            self.bootProto = bootProto
            self.dhcpclass = dhcpclass
            self.device = device
            self.essid = essid
            self.ethtool = ethtool
            self.gateway = gateway
            self.hostname = hostname
            self.ip = ip
            self.mtu = mtu
            self.nameserver = nameserver
            self.netmask = netmask
            self.nodns = nodns
            self.onboot = onboot
            self.wepkey = wepkey

        def __str__(self):
            retval = "network"

            if self.bootProto != "":
                retval += " --bootproto=%s" % self.bootProto
            if self.dhcpclass != "":
                retval += " --dhcpclass=%s" % self.dhcpclass
            if self.device != "":
                retval += " --device=%s" % self.device
            if self.essid != "":
                retval += " --essid=\"%s\"" % self.essid
            if self.ethtool != "":
                retval += " --ethtool=\"%s\"" % self.ethtool
            if self.gateway != "":
                retval += " --gateway=%s" % self.gateway
            if self.hostname != "":
                retval += " --hostname=%s" % self.hostname
            if self.ip != "":
                retval += " --ip=%s" % self.ip
            if self.mtu != "":
                retval += " --mtu=%s" % self.mtu
            if self.nameserver != "":
                retval += " --nameserver=%s" % self.nameserver
            if self.netmask != "":
                retval += " --netmask=%s" % self.netmask
            if self.nodns:
                retval += " --nodns"
            if self.onboot:
                retval += " --onboot=on"
            if self.wepkey != "":
                retval += " --wepkey=%s" % self.wepkey

            return retval + "\n"

    class PartData(BaseData):
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

    class RaidData(BaseData):
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

        def __str__(self):
            retval = "raid %s" % self.mountpoint

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

            return retval + " %s\n" % string.join(self.members)

    class VolGroupData(BaseData):
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

    class ZFCPData(BaseData):
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


    ###
    ### COMMAND CLASSES
    ###
    class Authconfig(KickstartCommand):
        def __init__(self, writePriority=0, authconfig=""):
            KickstartCommand.__init__(self, writePriority)
            self.authconfig = authconfig

        def __str__(self):
            if self.authconfig:
                return "# System authorization information\nauth %s\n" % self.authconfig
            else:
                return ""

        def parse(self, args):
            self.authconfig = string.join(args)

    class AutoPart(KickstartCommand):
        def __init__(self, writePriority=100, autopart=False):
            KickstartCommand.__init__(self, writePriority)
            self.autopart = autopart

        def __str__(self):
            if self.autopart:
                return "autopart\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "autopart")

            self.autopart = True

    class AutoStep(KickstartCommand):
        def __init__(self, writePriority=0, autoscreenshot=False):
            KickstartCommand.__init__(self, writePriority)
            self.autoscreenshot = autoscreenshot

        def __str__(self):
            if self.autoscreenshot:
                return "autostep --autoscreenshot\n"
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--autoscreenshot", dest="autoscreenshot",
                          action="store_true", default=False)

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class Bootloader(KickstartCommand):
        def __init__(self, writePriority=0, appendLine="", driveorder=None,
                     forceLBA=False, linear=True, location="mbr", md5pass="",
                     password="", upgrade=False, useLilo=False):
            KickstartCommand.__init__(self, writePriority)
            self.appendLine = appendLine

            if driveorder == None:
                driveorder = []

            self.driveorder = driveorder

            self.forceLBA = forceLBA
            self.linear = linear
            self.location = location
            self.md5pass = md5pass
            self.password = password
            self.upgrade = upgrade
            self.useLilo = useLilo

        def __str__(self):
            retval = "# System bootloader configuration\nbootloader"

            if self.appendLine != "":
                retval += " --append=\"%s\"" % self.appendLine
            if self.linear:
                retval += " --linear"
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
            if self.useLilo:
                retval += " --useLilo"
            if len(self.driveorder) > 0:
                retval += " --driveorder=%s" % string.join(self.driveorder, ",")

            return retval + "\n"

        def parse(self, args):
            def driveorder_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)
                
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--append", dest="appendLine")
            op.add_option("--linear", dest="linear", action="store_true",
                          default=True)
            op.add_option("--nolinear", dest="linear", action="store_false")
            op.add_option("--location", dest="location", type="choice",
                          default="mbr",
                          choices=["mbr", "partition", "none", "boot"])
            op.add_option("--lba32", dest="forceLBA", action="store_true",
                          default=False)
            op.add_option("--password", dest="password", default="")
            op.add_option("--md5pass", dest="md5pass", default="")
            op.add_option("--upgrade", dest="upgrade", action="store_true",
                          default=False)
            op.add_option("--useLilo", dest="useLilo", action="store_true",
                          default=False)
            op.add_option("--driveorder", dest="driveorder", action="callback",
                          callback=driveorder_cb, nargs=1, type="string")

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

            if self.currentCmd == "lilo":
                self.useLilo = True

    class ClearPart(KickstartCommand):
        def __init__(self, writePriority=120, drives=None, initAll=False,
                     type=CLEARPART_TYPE_NONE):
            KickstartCommand.__init__(self, writePriority)

            if drives == None:
                drives = []

            self.drives = drives
            self.initAll = initAll
            self.type = type

        def __str__(self):
            if self.type == CLEARPART_TYPE_NONE:
                clearstr = "--none"
            elif self.type == CLEARPART_TYPE_LINUX:
                clearstr = "--linux"
            elif self.type == CLEARPART_TYPE_ALL:
                clearstr = "--all"
            else:
                clearstr = ""

            if self.initAll:
                initstr = "--initlabel"
            else:
                initstr = ""

            if len(self.drives) > 0:
                drivestr = "--drives=" + string.join (self.drives, ",")
            else:
                drivestr = ""

            return "# Partition clearing information\nclearpart %s %s %s\n" % (clearstr, initstr, drivestr)

        def parse(self, args):
            def drive_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)
                
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--all", dest="type", action="store_const",
                          const=CLEARPART_TYPE_ALL)
            op.add_option("--drives", dest="drives", action="callback",
                          callback=drive_cb, nargs=1, type="string")
            op.add_option("--initlabel", dest="initAll", action="store_true",
                          default=False)
            op.add_option("--linux", dest="type", action="store_const",
                          const=CLEARPART_TYPE_LINUX)
            op.add_option("--none", dest="type", action="store_const",
                          const=CLEARPART_TYPE_NONE)

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class Device(KickstartCommand):
        def __init__(self, writePriority=0, device=""):
            KickstartCommand.__init__(self, writePriority)
            self.device = device

        def __str__(self):
            if self.device != "":
                return "device %s\n" % self.device
            else:
                return ""

        def parse(self, args):
            self.device = string.join(args)

    class DeviceProbe(KickstartCommand):
        def __init__(self, writePriority=0, deviceprobe=""):
            KickstartCommand.__init__(self, writePriority)
            self.deviceprobe = deviceprobe

        def __str__(self):
            if self.deviceprobe != "":
                return "deviceprobe %s\n" % self.deviceprobe
            else:
                return ""

        def parse(self, args):
            self.deviceprove = string.join(args)

    class DisplayMode(KickstartCommand):
        def __init__(self, writePriority=0, displayMode=DISPLAY_MODE_GRAPHICAL):
            KickstartCommand.__init__(self, writePriority)
            self.displayMode = displayMode

        def __str__(self):
            if self.displayMode == DISPLAY_MODE_CMDLINE:
                return "cmdline\n"
            elif self.displayMode == DISPLAY_MODE_GRAPHICAL:
                return "# Use graphical install\ngraphical\n"
            elif self.displayMode == DISPLAY_MODE_TEXT:
                return "# Use text mode install\ntext\n"

        def parse(self, args):
            if self.currentCmd == "cmdline":
                self.displayMode = DISPLAY_MODE_CMDLINE
            elif self.currentCmd == "graphical":
                self.displayMode = DISPLAY_MODE_GRAPHICAL
            elif self.currentCmd == "text":
                self.displayMode = DISPLAY_MODE_TEXT

    class DriverDisk(KickstartCommand):
        def __init__(self, writePriority=0, driverdisk=""):
            KickstartCommand.__init__(self, writePriority)
            self.driverdisk = driverdisk

        def __str__(self):
            if self.driverdisk != "":
                return "driverdisk %s\n" % self.driverdisk
            else:
                return ""

        def parse(self, args):
            self.driverdisk = string.join(args)

    class Firewall(KickstartCommand):
        def __init__(self, writePriority=0, enabled=True, ports=None, trusts=None):
            KickstartCommand.__init__(self, writePriority)
            self.enabled = enabled

            if ports == None:
                ports = []

            self.ports = ports

            if trusts == None:
                trusts = []

            self.trusts = trusts

        def __str__(self):
            extra = []
            filteredPorts = []

            if self.enabled:
                # It's possible we have words in the ports list instead of
                # port:proto (s-c-kickstart may do this).  So, filter those
                # out into their own list leaving what we expect.
                for port in self.ports:
                    if port == "ssh":
                        extra.append("--ssh")
                    elif port == "telnet":
                        extra.append("--telnet")
                    elif port == "smtp":
                        extra.append("--smtp")
                    elif port == "http":
                        extra.append("--http")
                    elif port == "ftp":
                        extra.append("--ftp")
                    else:
                        filteredPorts.append(port)

                # All the port:proto strings go into a comma-separated list.
                portstr = string.join (filteredPorts, ",")
                if len(portstr) > 0:
                    portstr = "--port=" + portstr
                else:
                    portstr = ""

                extrastr = string.join (extra, " ")

                truststr = string.join (self.trusts, ",")
                if len(truststr) > 0:
                    truststr = "--trust=" + truststr

                # The output port list consists only of port:proto for
                # everything that we don't recognize, and special options for
                # those that we do.
                return "# Firewall configuration\nfirewall --enabled %s %s %s\n" % (extrastr, portstr, truststr)
            else:
                return "# Firewall configuration\nfirewall --disabled\n"

        def parse(self, args):
            def firewall_port_cb (option, opt_str, value, parser):
                for p in value.split(","):
                    p = p.strip()
                    if p.find(":") == -1:
                        p = "%s:tcp" % p
                    parser.values.ensure_value(option.dest, []).append(p)

            op = KSOptionParser(map={"ssh":["22:tcp"], "telnet":["23:tcp"],
                                 "smtp":["25:tcp"], "http":["80:tcp", "443:tcp"],
                                 "ftp":["21:tcp"]}, lineno=self.lineno)

            op.add_option("--disable", "--disabled", dest="enabled",
                          action="store_false")
            op.add_option("--enable", "--enabled", dest="enabled",
                          action="store_true", default=True)
            op.add_option("--ftp", "--http", "--smtp", "--ssh", "--telnet",
                          dest="ports", action="map_extend")
            op.add_option("--high", deprecated=1)
            op.add_option("--medium", deprecated=1)
            op.add_option("--port", dest="ports", action="callback",
                          callback=firewall_port_cb, nargs=1, type="string")
            op.add_option("--trust", dest="trusts", action="append")

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class Firstboot(KickstartCommand):
        def __init__(self, writePriority=0, firstboot=FIRSTBOOT_SKIP):
            KickstartCommand.__init__(self, writePriority)
            self.firstboot = firstboot

        def __str__(self):
            if self.firstboot == FIRSTBOOT_SKIP:
                return "firstboot --disable\n"
            elif self.firstboot == FIRSTBOOT_DEFAULT:
                return "# Run the Setup Agent on first boot\nfirstboot --enable\n"
            elif self.firstboot == FIRSTBOOT_RECONFIG:
                return "# Run the Setup Agent on first boot\nfirstboot --reconfig\n"

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--disable", "--disabled", dest="firstboot",
                          action="store_const", const=FIRSTBOOT_SKIP)
            op.add_option("--enable", "--enabled", dest="firstboot",
                          action="store_const", const=FIRSTBOOT_DEFAULT)
            op.add_option("--reconfig", dest="firstboot", action="store_const",
                          const=FIRSTBOOT_RECONFIG)

            (opts, extra) = op.parse_args(args=args)
            self.firstboot = opts.firstboot

    class IgnoreDisk(KickstartCommand):
        def __init__(self, writePriority=0, ignoredisk=None):
            KickstartCommand.__init__(self, writePriority)

            if ignoredisk == None:
                ignoredisk = []

            self.ignoredisk = ignoredisk

        def __str__(self):
            if len(self.ignoredisk) > 0:
                return "ignoredisk --drives=%s\n" % string.join(self.ignoredisk, ",")
            else:
                return ""

        def parse(self, args):
            def drive_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)
                
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--drives", dest="drives", action="callback",
                          callback=drive_cb, nargs=1, type="string")

            (opts, extra) = op.parse_args(args=args)
            self.ignoredisk = opts.drives

    class Interactive(KickstartCommand):
        def __init__(self, writePriority=0, interactive=False):
            KickstartCommand.__init__(self, writePriority)
            self.interactive = interactive

        def __str__(self):
            if self.interactive:
                return "# Use interactive kickstart installation method\ninteractive\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "interactive")

            self.interactive = True

    class Keyboard(KickstartCommand):
        def __init__(self, writePriority=0, keyboard=""):
            KickstartCommand.__init__(self, writePriority)
            self.keyboard = keyboard

        def __str__(self):
            if self.keyboard != "":
                return "# System keyboard\nkeyboard %s\n" % self.keyboard
            else:
                return ""

        def parse(self, args):
            if len(args) > 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s only takes one argument") % "keyboard")

            self.keyboard = args[0]

    class Lang(KickstartCommand):
        def __init__(self, writePriority=0, lang=""):
            KickstartCommand.__init__(self, writePriority)
            self.lang = lang

        def __str__(self):
            if self.lang != "":
                return "# System language\nlang %s\n" % self.lang
            else:
                return ""

        def parse(self, args):
            if len(args) > 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s only takes one argument") % "lang")

            self.lang = args[0]

    class LangSupport(KickstartCommand):
        def __init__(self, writePriority=0, deflang="en_US.UTF-8", supported=None):
            KickstartCommand.__init__(self, writePriority)
            self.deflang = deflang

            if supported == None:
                supported = []

            self.supported = supported

        def __str__(self):
            retval = "langsupport --default=%s" % self.deflang

            if self.supported:
                retval += " %s" % " ".join(self.supported)

            return retval

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--default", dest="deflang", default="en_US.UTF-8")

            (opts, extra) = op.parse_args(args=args)
            self.deflang = opts.deflang
            self.supported = extra

    class LiloCheck(KickstartCommand):
        def __init__(self, writePriority=0, check=False):
            KickstartCommand.__init__(self, writePriority)
            self.check = check

        def __str__(self):
            if self.check:
                return "lilocheck\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "lilocheck")

            self.check = True

    class LogVol(KickstartCommand):
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

            lvd = self.handler.LogVolData()
            self._setToObj(op, opts, lvd)
            lvd.mountpoint=extra[0]
            self.add(lvd)

        def add(self, newObj):
            self.lvList.append(newObj)

    class Method(KickstartCommand):
        def __init__(self, writePriority=0, method=""):
            KickstartCommand.__init__(self, writePriority)
            self.method = method

        def __str__(self):
            if self.method == "cdrom":
                return "# Use CDROM installation media\ncdrom\n"
            elif self.method == "harddrive":
                msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

                if hasattr(self, "biospart"):
                    return msg + " --biospart=%s\n" % getattr(self, "biospart")
                else:
                    return msg + " --partition=%s\n" % getattr(self, "partition")
            elif self.method == "nfs":
                return "# Use NFS installation media\nnfs --server=%s --dir=%s\n" % (self.server, self.dir)
            elif self.method == "url":
                return "# Use network installation\nurl --url=%s\n" % self.url
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)

            self.method = self.currentCmd

            if self.currentCmd == "cdrom":
                return
            elif self.currentCmd == "harddrive":
                op.add_option("--biospart", dest="biospart")
                op.add_option("--partition", dest="partition")
                op.add_option("--dir", dest="dir", required=1)
            elif self.currentCmd == "nfs":
                op.add_option("--server", dest="server", required=1)
                op.add_option("--dir", dest="dir", required=1)
            elif self.currentCmd == "url":
                op.add_option("--url", dest="url", required=1)

            (opts, extra) = op.parse_args(args=args)

            if self.currentCmd == "harddrive":
                if (getattr(opts, "biospart") == None and getattr(opts, "partition") == None) or \
                   (getattr(opts, "biospart") != None and getattr(opts, "partition") != None):

                    raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

            self._setToSelf(op, opts)

    class Monitor(KickstartCommand):
        def __init__(self, writePriority=0, hsync="", monitor="", vsync=""):
            KickstartCommand.__init__(self, writePriority)
            self.hsync = hsync
            self.monitor = monitor
            self.vsync = vsync

        def __str__(self):
            retval = "monitor"

            if self.hsync != "":
                retval += " --hsync=%s" % self.hsync
            if self.monitor != "":
                retval += " --monitor=\"%s\"" % self.monitor
            if self.vsync != "":
                retval += " --vsync=%s" % self.vsync

            if retval != "monitor":
                return retval + "\n"
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--hsync")
            op.add_option("--monitor")
            op.add_option("--vsync")

            (opts, extra) = op.parse_args(args=args)

            if extra:
                mapping = {"cmd": "monitor", "options": extra}
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(cmd)s command: %(options)s") % mapping)

            self._setToSelf(op, opts)

    class Mouse(DeprecatedCommand):
        def __init__(self):
            DeprecatedCommand.__init__(self)

    class Network(KickstartCommand):
        def __init__(self, writePriority=0, network=None):
            KickstartCommand.__init__(self, writePriority)

            if network == None:
                network = []

            self.network = network

        def __str__(self):
            retval = ""

            for nic in self.network:
                retval += nic.__str__()

            if retval != "":
                return "# Network information\n" + retval
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--bootproto", dest="bootProto",
                          default=BOOTPROTO_DHCP,
                          choices=[BOOTPROTO_DHCP, BOOTPROTO_BOOTP,
                                   BOOTPROTO_STATIC])
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
            op.add_option("--onboot", dest="onboot", action="store",
                          type="ksboolean")
            op.add_option("--wepkey", dest="wepkey")

            (opts, extra) = op.parse_args(args=args)
            nd = self.handler.NetworkData()
            self._setToObj(op, opts, nd)
            self.add(nd)

        def add(self, newObj):
            self.network.append(newObj)

    class Partition(KickstartCommand):
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

            pd = self.handler.PartData()
            self._setToObj(op, opts, pd)
            pd.mountpoint=extra[0]
            self.add(pd)

        def add(self, newObj):
            self.partitions.append(newObj)

    class Raid(KickstartCommand):
        def __init__(self, writePriority=140, raidList=None):
            KickstartCommand.__init__(self, writePriority)

            if raidList == None:
                raidList = []

            self.raidList = raidList

        def __str__(self):
            retval = ""

            for raid in self.raidList:
                retval += raid.__str__()

            return retval

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

        def add(self, newObj):
            self.raidList.append(newObj)

    class Reboot(KickstartCommand):
        def __init__(self, writePriority=0, action=KS_WAIT):
            KickstartCommand.__init__(self, writePriority)
            self.action = action

        def __str__(self):
            if self.action == KS_REBOOT:
                return "# Reboot after installation\nreboot\n"
            elif self.action == KS_SHUTDOWN:
                return "# Shutdown after installation\nshutdown\n"

        def parse(self, args):
            if self.currentCmd == "reboot":
                self.action = KS_REBOOT
            else:
                self.action = KS_SHUTDOWN

    class RootPw(KickstartCommand):
        def __init__(self, writePriority=0, isCrypted=False, password=""):
            KickstartCommand.__init__(self, writePriority)
            self.isCrypted = isCrypted
            self.password = password

        def __str__(self):
            if self.password != "":
                if self.isCrypted:
                    crypted = "--iscrypted"
                else:
                    crypted = ""

                return "# Root password\nrootpw %s %s\n" % (crypted, self.password)
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                          default=False)

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

            if len(extra) != 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw")

            self.password = extra[0]

    class SELinux(KickstartCommand):
        def __init__(self, writePriority=0, selinux=SELINUX_ENFORCING):
            KickstartCommand.__init__(self, writePriority)
            self.selinux = selinux

        def __str__(self):
            retval = "# SELinux configuration\n"

            if self.selinux == SELINUX_DISABLED:
                return retval + "selinux --disabled\n"
            elif self.selinux == SELINUX_ENFORCING:
                return retval + "selinux --enforcing\n"
            elif self.selinux == SELINUX_PERMISSIVE:
                return retval + "selinux --permissive\n"

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--disabled", dest="sel", action="store_const",
                          const=SELINUX_DISABLED)
            op.add_option("--enforcing", dest="sel", action="store_const",
                          const=SELINUX_ENFORCING)
            op.add_option("--permissive", dest="sel", action="store_const",
                          const=SELINUX_PERMISSIVE)

            (opts, extra) = op.parse_args(args=args)
            self.selinux = opts.sel

    class SkipX(KickstartCommand):
        def __init__(self, writePriority=0, skipx=False):
            KickstartCommand.__init__(self, writePriority)
            self.skipx = skipx

        def __str__(self):
            if self.skipx:
                return "# Do not configure the X Window System\nskipx\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "skipx")

            self.skipx = True

    class Timezone(KickstartCommand):
        def __init__(self, writePriority=0, isUtc=False, timezone=""):
            KickstartCommand.__init__(self, writePriority)
            self.isUtc = isUtc
            self.timezone = timezone

        def __str__(self):
            if self.timezone != "":
                if self.isUtc:
                    utc = "--isUtc"
                else:
                    utc = ""

                return "# System timezone\ntimezone %s %s\n" %(utc, self.timezone)
            else:
                return ""

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--utc", "--isUtc", dest="isUtc", action="store_true", default=False)

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

            if len(extra) != 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone")

            self.timezone = extra[0]

    class Upgrade(KickstartCommand):
        def __init__(self, writePriority=0, upgrade=False):
            KickstartCommand.__init__(self, writePriority)
            self.upgrade = upgrade

        def __str__(self):
            if self.upgrade:
                return "# Upgrade existing installation\nupgrade\n"
            else:
                return "# Install OS instead of upgrade\ninstall\n"

        def parse(self, args):
            if len(args) > 0:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "upgrade")

            if self.currentCmd == "upgrade":
               self.upgrade = True
            else:
               self.upgrade = False

    class Vnc(KickstartCommand):
        def __init__(self, writePriority=0, enabled=False, password="", connect=""):
            KickstartCommand.__init__(self, writePriority)
            self.enabled = enabled
            self.password = password
            self.connect = connect

        def __str__(self):
            if not self.enabled:
                return ""

            retval = "vnc --enabled"

            if self.connect != "":
                retval += " --connect=%s" % self.connect
            if self.password != "":
                retval += " --password=%s" % self.password

            return retval + "\n"

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--connect")
            op.add_option("--password", dest="password")

            self.enabled = True

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class VolGroup(KickstartCommand):
        def __init__(self, writePriority=131, vgList=None):
            KickstartCommand.__init__(self, writePriority)

            if vgList == None:
                vgList = []

            self.vgList = vgList

        def __str__(self):
            retval = ""
            for vg in self.vgList:
                retval += vg.__str__()

            return retval

        def parse(self, args):
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

            (opts, extra) = op.parse_args(args=args)
            vg = self.handler.VolGroupData()
            self._setToObj(op, opts, vg)
            vg.vgname = extra[0]
            vg.physvols = extra[1:]
            self.add(vg)

        def add(self, newObj):
            self.vgList.append(newObj)

    class XConfig(KickstartCommand):
        def __init__(self, writePriority=0, card="", defaultdesktop="", depth=0,
                     hsync="", monitor="", noProbe=False, resolution="", server="",
                     startX=False, videoRam="", vsync=""):
            KickstartCommand.__init__(self, writePriority)
            self.card = card
            self.defaultdesktop = defaultdesktop
            self.depth = depth
            self.hsync = hsync
            self.monitor = monitor
            self.noProbe = noProbe
            self.resolution = resolution
            self.server = server
            self.startX = startX
            self.videoRam = videoRam
            self.vsync = vsync

        def __str__(self):
            retval = ""

            if self.card != "":
                retval += " --card=%s" % self.card
            if self.defaultdesktop != "":
                retval += " --defaultdesktop=%s" % self.defaultdesktop
            if self.depth != 0:
                retval += " --depth=%d" % self.depth
            if self.hsync != "":
                retval += " --hsync=%s" % self.hsync
            if self.monitor != "":
                retval += " --monitor=%s" % self.monitor
            if self.noProbe:
                retval += " --noprobe"
            if self.resolution != "":
                retval += " --resolution=%s" % self.resolution
            if self.server != "":
                retval += " --server=%s" % self.server
            if self.startX:
                retval += " --startxonboot"
            if self.videoRam != "":
                retval += " --videoram=%s" % self.videoRam
            if self.vsync != "":
                retval += " --vsync=%s" % self.vsync

            if retval != "":
                retval = "# X Window System configuration information\nxconfig %s\n" % retval

            return retval

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--card")
            op.add_option("--defaultdesktop")
            op.add_option("--depth", action="store", type="int", nargs=1)
            op.add_option("--hsync")
            op.add_option("--monitor")
            op.add_option("--noprobe", dest="noProbe", action="store_true",
                          default=False)
            op.add_option("--resolution")
            op.add_option("--server")
            op.add_option("--startxonboot", dest="startX", action="store_true",
                          default=False)
            op.add_option("--videoram", dest="videoRam")
            op.add_option("--vsync")

            (opts, extra) = op.parse_args(args=args)
            if extra:
                mapping = {"command": "xconfig", "options": extra}
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

            self._setToSelf(op, opts)

    class ZeroMbr(KickstartCommand):
        def __init__(self, writePriority=110, zerombr=False):
            KickstartCommand.__init__(self, writePriority)
            self.zerombr = zerombr

        def __str__(self):
            if self.zerombr:
                return "# Clear the Master Boot Record\nzerombr\n"
            else:
                return ""

        def parse(self, args):
            if len(args) > 0:
                warnings.warn(_("Ignoring deprecated option on line %s:  The zerombr command no longer takes any options.  In future releases, this will result in a fatal error from kickstart.  Please modify your kickstart file to remove any options.") % self.lineno, DeprecationWarning)

            self.zerombr = True

    class ZFCP(KickstartCommand):
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

            zd = self.handler.ZFCPData()
            (opts, extra) = op.parse_args(args)
            self._setToObj(op, opts, zd)
            self.add(zd)

        def add(self, newObj):
            self.zfcp.append(newObj)


    ##
    ## MAIN
    ##
    def __init__(self):
        BaseHandler.__init__(self)
        self.version = FC3

        self.registerCommand(self.Authconfig(), ["auth", "authconfig"])
        self.registerCommand(self.AutoPart(), ["autopart"])
        self.registerCommand(self.AutoStep(), ["autostep"])
        self.registerCommand(self.Bootloader(), ["bootloader", "lilo"])
        self.registerCommand(self.Method(), ["cdrom", "harddrive", "nfs", "url"])
        self.registerCommand(self.ClearPart(), ["clearpart"])
        self.registerCommand(self.DisplayMode(), ["cmdline", "graphical", "text"])
        self.registerCommand(self.Device(), ["device"])
        self.registerCommand(self.DeviceProbe(), ["deviceprobe"])
        self.registerCommand(self.DriverDisk(), ["driverdisk"])
        self.registerCommand(self.Firewall(), ["firewall"])
        self.registerCommand(self.Firstboot(), ["firstboot"])
        self.registerCommand(self.Reboot(), ["halt", "poweroff", "reboot", "shutdown"])
        self.registerCommand(self.IgnoreDisk(), ["ignoredisk"])
        self.registerCommand(self.Interactive(), ["interactive"])
        self.registerCommand(self.Keyboard(), ["keyboard"])
        self.registerCommand(self.Lang(), ["lang"])
        self.registerCommand(self.LangSupport(), ["langsupport"])
        self.registerCommand(self.LiloCheck(), ["lilocheck"])
        self.registerCommand(self.LogVol(), ["logvol"])
        self.registerCommand(self.Monitor(), ["monitor"])
        self.registerCommand(self.Mouse(), ["mouse"])
        self.registerCommand(self.Network(), ["network"])
        self.registerCommand(self.Partition(), ["part", "partition"])
        self.registerCommand(self.Raid(), ["raid"])
        self.registerCommand(self.RootPw(), ["rootpw"])
        self.registerCommand(self.SELinux(), ["selinux"])
        self.registerCommand(self.SkipX(), ["skipx"])
        self.registerCommand(self.Timezone(), ["timezone"])
        self.registerCommand(self.Upgrade(), ["upgrade", "install"])
        self.registerCommand(self.Vnc(), ["vnc"])
        self.registerCommand(self.VolGroup(), ["volgroup"])
        self.registerCommand(self.XConfig(), ["xconfig"])
        self.registerCommand(self.ZeroMbr(), ["zerombr"])
        self.registerCommand(self.ZFCP(), ["zfcp"])
