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

from constants import *
from data import *
from errors import *
from options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

# You may make a subclass of KickstartHandlers if you need to do something
# besides just build up the data store.  If you need to do additional processing
# just make a subclass, define handlers for each command in your subclass, and
# make sure to call the same handler in the super class before whatever you
# want to do.  Also if you need to make a new parser that only takes action
# for a subset of commands, make a subclass and define all the handlers to
# None except the ones you care about.
class KickstartHandlers:
    def __init__ (self, ksdata):
        self.ksdata = ksdata

        # These will get set by the handleCommand method in the parser.
        self.lineno = 0
        self.currentCmd = ""

        self.handlers = { "auth"    : self.doAuthconfig,
                     "authconfig"   : self.doAuthconfig,
                     "autopart"     : self.doAutoPart,
                     "autostep"     : self.doAutoStep,
                     "bootloader"   : self.doBootloader,
                     "cdrom"        : self.doMethod,
                     "clearpart"    : self.doClearPart,
                     "cmdline"      : self.doDisplayMode,
                     "device"       : self.doDevice,
                     "deviceprobe"  : self.doDeviceProbe,
                     "driverdisk"   : self.doDriverDisk,
                     "firewall"     : self.doFirewall,
                     "firstboot"    : self.doFirstboot,
                     "graphical"    : self.doDisplayMode,
                     "halt"         : self.doReboot,
                     "harddrive"    : self.doMethod,
                     "ignoredisk"   : self.doIgnoreDisk,
                     # implied by lack of "upgrade" command
                     "install"      : None,
                     "interactive"  : self.doInteractive,
                     "iscsi"        : self.doIscsi,
                     "iscsiname"    : self.doIscsiName,
                     "key"          : self.doKey,
                     "keyboard"     : self.doKeyboard,
                     "lang"         : self.doLang,
                     "langsupport"  : self.doLangSupport,
                     "logvol"       : self.doLogicalVolume,
                     "logging"      : self.doLogging,
                     "mediacheck"   : self.doMediaCheck,
                     "monitor"      : self.doMonitor,
                     "mouse"        : self.doMouse,
                     "network"      : self.doNetwork,
                     "nfs"          : self.doMethod,
                     "multipath"    : self.doMultiPath,
                     "dmraid"       : self.doDmRaid,
                     "part"         : self.doPartition,
                     "partition"    : self.doPartition,
                     "poweroff"     : self.doReboot,
                     "raid"         : self.doRaid,
                     "reboot"       : self.doReboot,
                     "repo"         : self.doRepo,
                     "rootpw"       : self.doRootPw,
                     "selinux"      : self.doSELinux,
                     "services"     : self.doServices,
                     "shutdown"     : self.doReboot,
                     "skipx"        : self.doSkipX,
                     "text"         : self.doDisplayMode,
                     "timezone"     : self.doTimezone,
                     "url"          : self.doMethod,
                     "user"         : self.doUser,
                     "upgrade"      : self.doUpgrade,
                     "vnc"          : self.doVnc,
                     "volgroup"     : self.doVolumeGroup,
                     "xconfig"      : self.doXConfig,
                     "zerombr"      : self.doZeroMbr,
                     "zfcp"         : self.doZFCP,
                   }

    def _setToDict(self, optParser, opts, dict):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            dict[key] = getattr(opts, key)

    def _setToObj(self, optParser, opts, obj):
        for key in filter (lambda k: getattr(opts, k) != None, optParser.keys()):
            setattr(obj, key, getattr(opts, key))

    def resetHandlers (self):
        for key in self.handlers.keys():
            self.handlers[key] = None

    def deprecatedCommand(self, cmd):
        mapping = {"lineno": self.lineno, "cmd": cmd}
        warnings.warn(_("Ignoring deprecated command on line %(lineno)s:  The %(cmd)s command has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this command.") % mapping, DeprecationWarning)

    def doAuthconfig(self, args):
        self.ksdata.authconfig = string.join(args)

    def doAutoPart(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "autopart")

        self.ksdata.autopart = True

    def doAutoStep(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--autoscreenshot", dest="autoscreenshot",
                      action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.autostep)

    def doBootloader(self, args):
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
        self._setToDict(op, opts, self.ksdata.bootloader)

    def doClearPart(self, args):
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
        self._setToDict(op, opts, self.ksdata.clearpart)

    def doDevice(self, args):
        self.ksdata.device = string.join(args)

    def doDeviceProbe(self, args):
        self.ksdata.deviceprobe = string.join(args)

    def doDisplayMode(self, args):
        if self.currentCmd == "cmdline":
            self.ksdata.displayMode = DISPLAY_MODE_CMDLINE
        elif self.currentCmd == "graphical":
            self.ksdata.displayMode = DISPLAY_MODE_GRAPHICAL
        elif self.currentCmd == "text":
            self.ksdata.displayMode = DISPLAY_MODE_TEXT

    def doDriverDisk(self, args):
        self.ksdata.driverdisk = string.join(args)

    def doFirewall(self, args):
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
        self._setToDict(op, opts, self.ksdata.firewall)

    def doFirstboot(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disable", "--disabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_SKIP)
        op.add_option("--enable", "--enabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_DEFAULT)
        op.add_option("--reconfig", dest="firstboot", action="store_const",
                      const=FIRSTBOOT_RECONFIG)

        (opts, extra) = op.parse_args(args=args)
        self.ksdata.firstboot = opts.firstboot

    def doIgnoreDisk(self, args):
        def drive_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--drives", dest="drives", action="callback",
                      callback=drive_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)

        self.ksdata.ignoredisk = opts.drives

    def doInteractive(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "interactive")

        self.ksdata.interactive = True

    def doIscsi(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--target", dest="ipaddr", action="store", type="string")
        op.add_option("--ipaddr", dest="ipaddr", action="store", type="string",
                      required=1)
        op.add_option("--port", dest="port", action="store", type="string")
        op.add_option("--user", dest="user", action="store", type="string")
        op.add_option("--password", dest="password", action="store",
                      type="string")

        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 0:
            mapping = {"command": "scsi", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

        dd = KickstartIscsiData()
        self._setToObj(op, opts, dd)
        self.ksdata.iscsi.append(dd)

    def doIscsiName(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "iscsiname")
        self.ksdata.iscsiname = args[0]

    def doKey(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "key")

        if args[0] == "--skip":
            self.ksdata.key = KS_INSTKEY_SKIP
        else:
            self.ksdata.key = args[0]

    def doKeyboard(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "keyboard")

        self.ksdata.keyboard = args[0]

    def doLang(self, args):
        if len(args) > 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "lang")

        self.ksdata.lang = args[0]

    def doLangSupport(self, args):
        self.deprecatedCommand("langsupport")

    def doLogicalVolume(self, args):
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

        lvd = KickstartLogVolData()
        self._setToObj(op, opts, lvd)
        lvd.mountpoint = extra[0]
        self.ksdata.lvList.append(lvd)

    def doLogging(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--host")
        op.add_option("--level", type="choice",
                      choices=["debug", "info", "warning", "error", "critical"])
        op.add_option("--port")

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.logging)

    def doMediaCheck(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "mediacheck")

        self.ksdata.mediacheck = True

    def doMethod(self, args):
        op = KSOptionParser(lineno=self.lineno)

        self.ksdata.method["method"] = self.currentCmd

        if self.currentCmd == "cdrom":
            return
        elif self.currentCmd == "harddrive":
            op.add_option("--biospart", dest="biospart")
            op.add_option("--partition", dest="partition")
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "nfs":
            op.add_option("--server", dest="server", required=1)
            op.add_option("--dir", dest="dir", required=1)
            op.add_option("--opts", dest="opts", required=0)
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

        (opts, extra) = op.parse_args(args=args)

        if self.currentCmd == "harddrive":
            if (getattr(opts, "biospart") == None and getattr(opts, "partition") == None) or \
               (getattr(opts, "biospart") != None and getattr(opts, "partition") != None):

                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

        self._setToDict(op, opts, self.ksdata.method)

    def doMonitor(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--hsync", dest="hsync")
        op.add_option("--monitor", dest="monitor")
        op.add_option("--noprobe", dest="probe", action="store_false",
                      default=True)
        op.add_option("--vsync", dest="vsync")

        (opts, extra) = op.parse_args(args=args)

        if extra:
            mapping = {"cmd": "monitor", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(cmd)s command: %(options)s") % mapping)

        self._setToDict(op, opts, self.ksdata.monitor)

    def doMouse(self, args):
        self.deprecatedCommand("mouse")

    def doNetwork(self, args):
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
        self.ksdata.network.append(nd)

    def doMultiPath(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--device", dest="device", action="store", type="string",
                      required=1)
        op.add_option("--rule", dest="rule", action="store", type="string",
                      required=1)

        (opts, extra) = op.parse_args(args=args)

        dd = KickstartMpPathData()
        self._setToObj(op, opts, dd)
        dd.mpdev = dd.mpdev.split('/')[-1]

        parent = None
        for x in range(0, len(self.ksdata.mpaths)):
            mpath = self.ksdata.mpaths[x]
            for path in mpath.paths:
                if path.device == dd.device:
                    mapping = {"device": path.device, "multipathdev": path.mpdev}
                    raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Device '%(device)s' is already used in multipath '%(multipathdev)s'") % mapping)
            if mpath.name == dd.mpdev:
                parent = x

        if parent is None:
            mpath = KickstartMultiPathData()
            self.ksdata.mpaths.append(mpath)
        else:
            mpath = self.ksdata.mpaths[x]

        mpath.paths.append(dd)

    def doDmRaid(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--dev", dest="devices", action="append", type="string",
                      required=1)

        (opts, extra) = op.parse_args(args=args)

        dd = KickstartDmRaidData()
        self._setToObj(op, opts, dd)
        dd.name = dd.name.split('/')[-1]
        self.ksdata.dmraids.append(dd)

    def doPartition(self, args):
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

        pd = KickstartPartData()
        self._setToObj(op, opts, pd)
        pd.mountpoint = extra[0]
        self.ksdata.partitions.append(pd)

    def doReboot(self, args):
        if self.currentCmd == "reboot":
            self.ksdata.reboot["action"] = KS_REBOOT
        else:
            self.ksdata.reboot["action"] = KS_SHUTDOWN

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--eject", dest="eject", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.reboot)

    def doRepo(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", required=1)
        op.add_option("--baseurl")
        op.add_option("--mirrorlist")

        (opts, extra) = op.parse_args(args=args)

        # This is lame, but I can't think of a better way to make sure only
        # one of these two is specified.
        if opts.baseurl and opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Only one of --baseurl and --mirrorlist may be specified for repo command."))

        if not opts.baseurl and not opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of --baseurl or --mirrorlist must be specified for repo command."))

        rd = KickstartRepoData()
        self._setToObj(op, opts, rd)
        self.ksdata.repoList.append(rd)

    def doRaid(self, args):
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
        self.ksdata.raidList.append(rd)

    def doRootPw(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.rootpw)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw")

        self.ksdata.rootpw["password"] = extra[0]

    def doSELinux(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disabled", dest="sel", action="store_const",
                      const=SELINUX_DISABLED)
        op.add_option("--enforcing", dest="sel", action="store_const",
                      const=SELINUX_ENFORCING)
        op.add_option("--permissive", dest="sel", action="store_const",
                      const=SELINUX_PERMISSIVE)

        (opts, extra) = op.parse_args(args=args)
        self.ksdata.selinux = opts.sel

    def doServices(self, args):
        def services_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disabled", dest="disabled", action="callback",
                      callback=services_cb, nargs=1, type="string")
        op.add_option("--enabled", dest="enabled", action="callback",
                      callback=services_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.services)

    def doSkipX(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "skipx")

        self.ksdata.skipx = True

    def doTimezone(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--utc", "--isUtc", dest="isUtc", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.timezone)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "timezone")

        self.ksdata.timezone["timezone"] = extra[0]

    def doUpgrade(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s does not take any arguments") % "upgrade")

        self.ksdata.upgrade = True

    def doUser(self, args):
        def groups_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--groups", dest="groups", action="callback",
                      callback=groups_cb, nargs=1, type="string")
        op.add_option("--homedir")
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)
        op.add_option("--name", required=1)
        op.add_option("--password")
        op.add_option("--shell")
        op.add_option("--uid", type="int")

        (opts, extra) = op.parse_args(args=args)

        user = KickstartUserData()
        self._setToObj(op, opts, user)
        self.ksdata.userList.append(user)

    def doVnc(self, args):
        def connect_cb (option, opt_str, value, parser):
            cargs = value.split(":")
            parser.values.ensure_value("host", cargs[0])

            if len(cargs) > 1:
                parser.values.ensure_value("port", cargs[1])

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--connect", action="callback", callback=connect_cb,
                      nargs=1, type="string", deprecated=1)
        op.add_option("--password", dest="password")
        op.add_option("--host", dest="host")
        op.add_option("--port", dest="port")

        self.ksdata.vnc["enabled"] = True

        (opts, extra) = op.parse_args(args=args)
        self._setToDict(op, opts, self.ksdata.vnc)

    def doVolumeGroup(self, args):
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

        vgd = KickstartVolGroupData()
        self._setToObj(op, opts, vgd)
        vgd.vgname = extra[0]
        vgd.physvols = extra[1:]
        self.ksdata.vgList.append(vgd)

    def doXConfig(self, args):
        op = KSOptionParser(lineno=self.lineno)
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

        self._setToDict(op, opts, self.ksdata.xconfig)

    def doZeroMbr(self, args):
        if len(args) > 0:
            warnings.warn(_("Ignoring deprecated option on line %s:  The zerombr command no longer takes any options.  In future releases, this will result in a fatal error from kickstart.  Please modify your kickstart file to remove any options.") % self.lineno, DeprecationWarning)

        self.ksdata.zerombr = True

    def doZFCP(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--devnum", dest="devnum", required=1)
        op.add_option("--fcplun", dest="fcplun", required=1)
        op.add_option("--scsiid", dest="scsiid")
        op.add_option("--scsilun", dest="scsilun")
        op.add_option("--wwpn", dest="wwpn", required=1)

        (opts, extra) = op.parse_args(args=args)

        dd = KickstartZFCPData()
        self._setToObj(op, opts, dd)
        self.ksdata.zfcp.append(dd)
