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
from base import *


###
### HANDLER/DISPATCHER
###
class FC4Handler(BaseHandler):
    def __init__(self):
        BaseHandler.__init__(self)

        self.registerHandler(CommandAuthconfig(), ["auth", "authconfig"])
        self.registerHandler(CommandAutoPart(), ["autopart"])
        self.registerHandler(CommandAutoStep(), ["autostep"])
        self.registerHandler(CommandBootloader(), ["bootloader"])
        self.registerHandler(CommandMethod(), ["cdrom", "harddrive", "nfs", "url"])
        self.registerHandler(CommandClearPart(), ["clearpart"])
        self.registerHandler(CommandDisplayMode(), ["cmdline", "graphical", "text"])
        self.registerHandler(CommandDevice(), ["device"])
        self.registerHandler(CommandDeviceProbe(), ["deviceprobe"])
        self.registerHandler(CommandDriverDisk(), ["driverdisk"])
        self.registerHandler(CommandFirewall(), ["firewall"])
        self.registerHandler(CommandFirstboot(), ["firstboot"])
        self.registerHandler(CommandReboot(), ["halt", "poweroff", "reboot", "shutdown"])
        self.registerHandler(CommandIgnoreDisk(), ["ignoredisk"])
        self.registerHandler(CommandInteractive(), ["interactive"])
        self.registerHandler(CommandKeyboard(), ["keyboard"])
        self.registerHandler(CommandLang(), ["lang"])
        self.registerHandler(CommandLangSupport(), ["langsupport"])
        self.registerHandler(CommandLogVol(), ["logvol"])
        self.registerHandler(CommandMediaCheck(), ["mediacheck"])
        self.registerHandler(CommandMonitor(), ["monitor"])
        self.registerHandler(CommandMouse(), ["mouse"])
        self.registerHandler(CommandNetwork(), ["network"])
        self.registerHandler(CommandPartition(), ["part", "partition"])
        self.registerHandler(CommandRaid(), ["raid"])
        self.registerHandler(CommandRootPw(), ["rootpw"])
        self.registerHandler(CommandSELinux(), ["selinux"])
        self.registerHandler(CommandSkipX(), ["skipx"])
        self.registerHandler(CommandTimezone(), ["timezone"])
        self.registerHandler(CommandUpgrade(), ["upgrade", "install"])
        self.registerHandler(CommandVnc(), ["vnc"])
        self.registerHandler(CommandVolGroup(), ["volgroup"])
        self.registerHandler(CommandXConfig(), ["xconfig"])
        self.registerHandler(CommandZeroMbr(), ["zerombr"])
        self.registerHandler(CommandZFCP(), ["zfcp"])


###
### DATA CLASSES
###
class KickstartLogVolData:
    def __init__(self, bytesPerInode=4096, fsopts="", fstype="", grow=False,
                 maxSizeMB=0, name="", format=True, percent=0,
                 recommended=False, size=None, preexist=False, vgname="",
                 mountpoint=""):
        self.bytesPerInode = bytesPerInode
        self.fsopts = fsopts
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

        if self.bytesPerInode > 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
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

class KickstartNetworkData:
    def __init__(self, bootProto="dhcp", dhcpclass="", device="", essid="",
                 ethtool="", gateway="", hostname="", ip="", ipv4=True,
                 ipv6=True, mtu="", nameserver="", netmask="", nodns=False,
                 notksdevice=False, onboot=True, wepkey=""):
        self.bootProto = bootProto
        self.dhcpclass = dhcpclass
        self.device = device
        self.essid = essid
        self.ethtool = ethtool
        self.gateway = gateway
        self.hostname = hostname
        self.ip = ip
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.mtu = mtu
        self.nameserver = nameserver
        self.netmask = netmask
        self.nodns = nodns
        self.notksdevice = notksdevice
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
        if not self.ipv4:
            retval += " --noipv4"
        if not self.ipv6:
            retval += " --noipv6"
        if self.mtu != "":
            retval += " --mtu=%s" % self.mtu
        if self.nameserver != "":
            retval += " --nameserver=%s" % self.nameserver
        if self.netmask != "":
            retval += " --netmask=%s" % self.netmask
        if self.nodns:
            retval += " --nodns"
        if self.notksdevice:
            retval += " --notksdevice"
        if self.onboot:
            retval += " --onboot=on"
        if self.wepkey != "":
            retval += " --wepkey=%s" % self.wepkey

        return retval + "\n"

class KickstartPartData:
    def __init__(self, active=False, primOnly=False, bytesPerInode=4096, end=0,
                 fsopts="", fstype="", grow=False, label="", maxSizeMB=0,
                 format=True, onbiosdisk="", disk="", onPart="",
                 recommended=False, size=None, start=0, mountpoint=""):
        self.active = active
        self.primOnly = primOnly
        self.bytesPerInode = bytesPerInode
        self.end = end
        self.fsopts = fsopts
        self.fstype = fstype
        self.grow = grow
        self.label = label
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
        if self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.end != 0:
            retval += " --end=%d" % self.end
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.fstype != "":
            retval += " --fstype=\"%s\"" % self.fstype
        if self.grow:
            retval += " --grow"
        if self.label != "":
            retval += " --label=%s" % self.label
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

class KickstartRaidData:
    def __init__(self, device=None, fsopts="", fstype="", level="", format=True,
                 spares=0, preexist=False, mountpoint="", members=[],
                 bytesPerInode=4096):
        self.device = device
        self.fsopts = fsopts
        self.fstype = fstype
        self.level = level
        self.format = format
        self.spares = spares
        self.preexist = preexist
        self.mountpoint = mountpoint
        self.members = members
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

class KickstartVolGroupData:
    def __init__(self, format=True, pesize=32768, preexist=False, vgname="",
                 physvols=[]):
        self.format = format
        self.pesize = pesize
        self.preexist = preexist
        self.vgname = vgname
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

class KickstartZFCPData:
    def __init__(self, devnum="", wwpn="", fcplun="", scsiid="", scsilun=""):
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

class CommandAuthconfig(KickstartCommand):
    def __init__(self, authconfig=""):
        KickstartCommand.__init__(self)
        self.authconfig = authconfig

    def __str__(self):
        if self.authconfig:
            return "# System authorization information\nauth %s\n" % self.authconfig
        else:
            return ""

    def parse(self, args):
        self.authconfig = string.join(args)

class CommandAutoPart(KickstartCommand):
    def __init__(self, autopart=False):
        KickstartCommand.__init__(self)
        self.autopart = autopart

    def __str__(self):
        if self.autopart:
            return "autopart\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "autopart")

        self.autopart = True

class CommandAutoStep(KickstartCommand):
    def __init__(self, autoscreenshot=False):
        KickstartCommand.__init__(self)
        self.autoscreenshot = False

    def __str__(self):
        if self.autoscreenshot:
            return "autostep --autoscreenshot\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--autoscreenshot", dest="autoscreenshot",
                      action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class CommandBootloader(KickstartCommand):
    def __init__(self, appendLine="", driveorder=[], forceLBA=False,
                 location="mbr", md5pass="", password="", upgrade=""):
        KickstartCommand.__init__(self)
        self.appendLine = appendLine
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
            
        op = KSOptionParser(self.lineno)
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

class CommandClearPart(KickstartCommand):
    def __init__(self, drives=[], initAll=False, type=CLEARPART_TYPE_NONE):
        KickstartCommand.__init__(self)
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
            
        op = KSOptionParser(self.lineno)
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

class CommandDevice(KickstartCommand):
    def __init__(self, device=""):
        KickstartCommand.__init__(self)
        self.device = device

    def __str__(self):
        if self.device != "":
            return "device %s\n" % self.device
        else:
            return ""

    def parse(self, args):
        self.device = string.join(args)

class CommandDeviceProbe(KickstartCommand):
    def __init__(self, deviceprobe=""):
        KickstartCommand.__init__(self)
        self.deviceprobe = deviceprobe

    def __str__(self):
        if self.deviceprobe != "":
            return "deviceprobe %s\n" % self.deviceprobe
        else:
            return ""

    def parse(self, args):
        self.deviceprove = string.join(args)

class CommandDisplayMode(KickstartCommand):
    def __init__(self, displayMode=DISPLAY_MODE_GRAPHICAL):
        KickstartCommand.__init__(self)
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

class CommandDriverDisk(KickstartCommand):
    def __init__(self, driverdisk=""):
        KickstartCommand.__init__(self)
        self.driverdisk = driverdisk

    def __str__(self):
        if self.driverdisk != "":
            return "driverdisk %s\n" % self.driverdisk
        else:
            return ""

    def parse(self, args):
        self.driverdisk = string.join(args)

class CommandFirewall(KickstartCommand):
    def __init__(self, enabled=True, ports=[], trusts=[]):
        KickstartCommand.__init__(self)
        self.enabled = enabled
        self.ports = ports
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
        op.add_option("--port", dest="ports", action="callback",
                      callback=firewall_port_cb, nargs=1, type="string")
        op.add_option("--trust", dest="trusts", action="append")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class CommandFirstboot(KickstartCommand):
    def __init__(self, firstboot=FIRSTBOOT_SKIP):
        KickstartCommand.__init__(self)
        self.firstboot = firstboot

    def __str__(self):
        if self.firstboot == FIRSTBOOT_SKIP:
            return "firstboot --disable\n"
        elif self.firstboot == FIRSTBOOT_DEFAULT:
            return "# Run the Setup Agent on first boot\nfirstboot --enable\n"
        elif self.firstboot == FIRSTBOOT_RECONFIG:
            return "# Run the Setup Agent on first boot\nfirstboot --reconfig\n"

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--disable", "--disabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_SKIP)
        op.add_option("--enable", "--enabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_DEFAULT)
        op.add_option("--reconfig", dest="firstboot", action="store_const",
                      const=FIRSTBOOT_RECONFIG)

        (opts, extra) = op.parse_args(args=args)
        self.firstboot = opts.firstboot

class CommandIgnoreDisk(KickstartCommand):
    def __init__(self, ignoredisk=[]):
        KickstartCommand.__init__(self)
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
            
        op = KSOptionParser(self.lineno)
        op.add_option("--drives", dest="drives", action="callback",
                      callback=drive_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)
        self.ignoredisk = opts.drives

class CommandInteractive(KickstartCommand):
    def __init__(self, interactive=False):
        KickstartCommand.__init__(self)
        self.interactive = interactive

    def __str__(self):
        if self.interactive:
            return "# Use interactive kickstart installation method\ninteractive\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "interactive")

        self.interactive = True

class CommandKeyboard(KickstartCommand):
    def __init__(self, keyboard=""):
        KickstartCommand.__init__(self)
        self.keyboard = keyboard

    def __str__(self):
        if self.keyboard != "":
            return "# System keyboard\nkeyboard %s\n" % self.keyboard
        else:
            return ""

    def parse(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "keyboard")

        self.keyboard = args[0]

class CommandLang(KickstartCommand):
    def __init__(self, lang=""):
        KickstartCommand.__init__(self)
        self.lang = lang

    def __str__(self):
        if self.lang != "":
            return "# System language\nlang %s\n" % self.lang
        else:
            return ""

    def parse(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "lang")

        self.lang = args[0]

class CommandLangSupport(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)

class CommandLogVol(KickstartCommand):
    def __init__(self, lvList=[]):
        KickstartCommand.__init__(self)
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

        op = KSOptionParser(self.lineno)
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

        lvd = KickstartLogVolData()
        self._setToObj(op, opts, lvd)
        lvd.mountpoint=extra[0]
        self.add(lvd)

    def add(self, newObj):
        self.lvList.append(newObj)

class CommandMediaCheck(KickstartCommand):
    def __init__(self, mediacheck=False):
        KickstartCommand.__init__(self)
        self.mediacheck = mediacheck

    def __str__(self):
        if self.mediacheck:
            return "mediacheck\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "mediacheck")

        self.mediacheck = True

class CommandMethod(KickstartCommand):
    def __init__(self, method=""):
        KickstartCommand.__init__(self)
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
        op = KSOptionParser(self.lineno)

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
            op.add_option("--opts", dest="opts")
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

        (opts, extra) = op.parse_args(args=args)

        if self.currentCmd == "harddrive":
            if (getattr(opts, "biospart") == None and getattr(opts, "partition") == None) or \
               (getattr(opts, "biospart") != None and getattr(opts, "partition") != None):

                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

        self._setToSelf(op, opts)

class CommandMonitor(KickstartCommand):
    def __init__(self, hsync="", monitor="", probe=True, vsync=""):
        KickstartCommand.__init__(self)
        self.hsync = hsync
        self.monitor = monitor
        self.probe = probe
        self.vsync = vsync

    def __str__(self):
        retval = "monitor"

        if self.hsync != "":
            retval += " --hsync=%s" % self.hsync
        if self.monitor != "":
            retval += " --monitor=\"%s\"" % self.monitor
        if not self.probe:
            retval += " --noprobe"
        if self.vsync != "":
            retval += " --vsync=%s" % self.vsync

        if retval != "monitor":
            return retval + "\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--hsync", dest="hsync")
        op.add_option("--monitor", dest="monitor")
        op.add_option("--noprobe", dest="probe", action="store_false",
                      default=True)
        op.add_option("--vsync", dest="vsync")

        (opts, extra) = op.parse_args(args=args)

        if extra:
            mapping = {"cmd": "monitor", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(cmd)s command: %(options)s") % mapping)

        self._setToSelf(op, opts)

class CommandMouse(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)

class CommandNetwork(KickstartCommand):
    def __init__(self, network=[]):
        KickstartCommand.__init__(self)
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
        op = KSOptionParser(self.lineno)
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
        op.add_option("--noipv4", dest="ipv4", action="store_false",
                      default=True)
        op.add_option("--noipv6", dest="ipv6", action="store_false",
                      default=True)
        op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                      default=False)
        op.add_option("--onboot", dest="onboot", action="store",
                      type="ksboolean")
        op.add_option("--wepkey", dest="wepkey")

        (opts, extra) = op.parse_args(args=args)
        nd = KickstartNetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)

    def add(self, newObj):
        self.network.append(newObj)

class CommandPartition(KickstartCommand):
    def __init__(self, partitions=[]):
        KickstartCommand.__init__(self)
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

        op = KSOptionParser(self.lineno)
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

        pd = KickstartPartData()
        self._setToObj(op, opts, pd)
        pd.mountpoint=extra[0]
        self.add(pd)

    def add(self, newObj):
        self.partitions.append(newObj)

class CommandRaid(KickstartCommand):
    def __init__(self, raidList=[]):
        KickstartCommand.__init__(self)
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

        rd = KickstartRaidData()
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

class CommandReboot(KickstartCommand):
    def __init__(self, action=KS_WAIT, eject=False):
        KickstartCommand.__init__(self)
        self.action = action
        self.eject = eject

    def __str__(self):
        retval = ""

        if self.action == KS_REBOOT:
            retval = "# Reboot after installation\nreboot\,"
        elif self.action == KS_SHUTDOWN:
            retval = "# Shutdown after installation\nshutdown\n"

        if self.eject:
            retval += " --eject"

        return retval

    def parse(self, args):
        if self.currentCmd == "reboot":
            self.action = KS_REBOOT
        else:
            self.action = KS_SHUTDOWN

        op = KSOptionParser(self.lineno)
        op.add_option("--eject", dest="eject", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class CommandRootPw(KickstartCommand):
    def __init__(self, isCrypted=False, password=""):
        KickstartCommand.__init__(self)
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
        op = KSOptionParser(self.lineno)
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw")

        self.rootpw = extra[0]

class CommandSELinux(KickstartCommand):
    def __init__(self, selinux=SELINUX_ENFORCING):
        KickstartCommand.__init__(self)
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
        op = KSOptionParser(self.lineno)
        op.add_option("--disabled", dest="sel", action="store_const",
                      const=SELINUX_DISABLED)
        op.add_option("--enforcing", dest="sel", action="store_const",
                      const=SELINUX_ENFORCING)
        op.add_option("--permissive", dest="sel", action="store_const",
                      const=SELINUX_PERMISSIVE)

        (opts, extra) = op.parse_args(args=args)
        self.selinux = opts.sel

class CommandSkipX(KickstartCommand):
    def __init__(self, skipx=False):
        KickstartCommand.__init__(self)
        self.skipx = skipx

    def __str__(self):
        if self.skipx:
            return "# Do not configure the X Window System\nskipx\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "skipx")

        self.skipx = True

class CommandTimezone(KickstartCommand):
    def __init__(self, isUtc=False, timezone=""):
        KickstartCommand.__init__(self)
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
        op = KSOptionParser(self.lineno)
        op.add_option("--utc", "--isUtc", dest="isUtc", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone")

        self.timezone = extra[0]

class CommandUpgrade(KickstartCommand):
    def __init__(self, upgrade=False):
        KickstartCommand.__init__(self)
        self.upgrade = upgrade

    def __str__(self):
        if self.upgrade:
            return "# Upgrade existing installation\nupgrade\n"
        else:
            return "# Install OS instead of upgrade\ninstall\n"

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "upgrade")

        self.upgrade = True

class CommandVnc(KickstartCommand):
    def __init__(self, enabled=False, password="", host="", port=""):
        KickstartCommand.__init__(self)
        self.enabled = enabled
        self.password = password
        self.host = host
        self.port = port

    def __str__(self):
        if not self.enabled:
            return ""

        retval = "vnc --enabled %s" % self.host

        if self.port != "":
            retval += " --port=%s" % self.port
        if self.password != "":
            retval += " --password=%s" % self.password

        return retval + "\n"

    def parse(self, args):
        def connect_cb (option, opt_str, value, parser):
            cargs = value.split(":")
            parser.values.ensure_value("host", cargs[0])

            if len(cargs) > 1:
                parser.values.ensure_value("port", cargs[1])

        op = KSOptionParser(self.lineno)
        op.add_option("--connect", action="callback", callback=connect_cb,
                      nargs=1, type="string", deprecated=1)
        op.add_option("--password", dest="password")
        op.add_option("--host", dest="host")
        op.add_option("--port", dest="port")

        self.enabled = True

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class CommandVolGroup(KickstartCommand):
    def __init__(self, vgList=[]):
        KickstartCommand.__init__(self)
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

        op = KSOptionParser(self.lineno)
        op.add_option("--noformat", action="callback", callback=vg_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--pesize", dest="pesize", type="int", nargs=1,
                      default=32768)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        vg = KickstartVolGroupData()
        self._setToObj(op, opts, vg)
        vg.vgname = extra[0]
        vg.physvols = extra[1:]
        self.add(vg)

    def add(self, newObj):
        self.vgList.append(newObj)

class CommandXConfig(KickstartCommand):
    def __init__(self, driver="", defaultdesktop="", depth=0, resolution="",
                 startX=False, videoRam=""):
        KickstartCommand.__init__(self)
        self.driver = driver
        self.defaultdesktop = defaultdesktop
        self.depth = depth
        self.resolution = resolution
        self.startX = startX
        self.videoRam = videoRam

    def __str__(self):
        retval = ""

        if self.driver != "":
            retval += " --driver=%s" % self.driver
        if self.defaultdesktop != "":
            retval += " --defaultdesktop=%s" % self.defaultdesktop
        if self.depth != 0:
            retval += " --depth=%d" % self.depth
        if self.resolution != "":
            retval += " --resolution=%s" % self.resolution
        if self.startX:
            retval += " --startxonboot"
        if self.videoRam != "":
            retval += " --videoram=%s" % self.videoRam

        if retval != "":
            retval = "# X Window System configuration information\nxconfig %s\n" % retval

        return retval

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--card", deprecated=1)
        op.add_option("--driver", dest="driver")
        op.add_option("--defaultdesktop", dest="defaultdesktop")
        op.add_option("--depth", dest="depth", action="store", type="int",
                      nargs=1)
        op.add_option("--hsync", deprecated=1)
        op.add_option("--monitor", deprecated=1)
        op.add_option("--noprobe", deprecated=1)
        op.add_option("--resolution", dest="resolution")
        op.add_option("--startxonboot", dest="startX", action="store_true",
                      default=False)
        op.add_option("--videoram", dest="videoRam")
        op.add_option("--vsync", deprecated=1)

        (opts, extra) = op.parse_args(args=args)
        if extra:
            mapping = {"command": "xconfig", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s" % mapping))

        self._setToSelf(op, opts)

class CommandZeroMbr(KickstartCommand):
    def __init__(self, zerombr=False):
        KickstartCommand.__init__(self)
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

class CommandZFCP(KickstartCommand):
    def __init__(self, zfcp=[]):
        KickstartCommand.__init__(self)
        self.zfcp = zfcp

    def __str__(self):
        retval = ""
        for zfcp in self.zfcp:
            retval += zfcp.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--devnum", dest="devnum", required=1)
        op.add_option("--fcplun", dest="fcplun", required=1)
        op.add_option("--scsiid", dest="scsiid")
        op.add_option("--scsilun", dest="scsilun")
        op.add_option("--wwpn", dest="wwpn", required=1)

        zd = KickstartZFCPData()
        (opts, extra) = op.parse_args(args)
        self._setToObj(op, opts, zd)
        self.add(zd)

    def add(self, newObj):
        self.zfcp.append(newObj)
