#
# parser.py:  Kickstart file parser.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import shlex
import sys
import string
import warnings
from copy import copy
from optparse import OptionParser, Option

from constants import *
from data import *

STATE_END = 0
STATE_COMMANDS = 1
STATE_PACKAGES = 2
STATE_SCRIPT_HDR = 3
STATE_PRE = 4
STATE_POST = 5
STATE_TRACEBACK = 6

###
### ERROR HANDLING
###

def formatErrorMsg(lineno, msg=""):
    if msg != "":
        return "The following problem occurred on line %s of the kickstart file:\n\n%s\n" % (lineno, msg)
    else:
        return "There was a problem reading from line %s of the kickstart file" % lineno

class KickstartError(Exception):
    def __init__(self, val = ""):
        self.value = val

    def __str__ (self):
        return self.value

class KickstartParseError(KickstartError):
    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return self.value

class KickstartValueError(KickstartError):
    def __init__(self, msg):
        self.value = msg

    def __str__ (self):
        return self.value

###
### OPTION HANDLING
###

# Specialized OptionParser, mainly to handle the MappableOption and to turn
# off help.
class KSOptionParser(OptionParser):
    def exit(self, status=0, msg=None):
        pass

    def error(self, msg):
        if self.lineno != None:
            raise KickstartParseError, formatErrorMsg(self.lineno, msg=msg)
        else:
            raise KickstartParseError, msg

    def keys(self):
        retval = []

        for opt in self.option_list:
            if opt not in retval:
                retval.append(opt.dest)

        return retval

    def _init_parsing_state (self):
        OptionParser._init_parsing_state(self)
        self.option_seen = {}

    def check_values (self, values, args):
        for option in self.option_list:
            if (isinstance(option, Option) and option.required and \
               not self.option_seen.has_key(option)):
                raise KickstartValueError, formatErrorMsg(self.lineno, "Option %s is required" % option)
            elif isinstance(option, Option) and option.deprecated and \
                 self.option_seen.has_key(option):
                warnings.warn("Ignoring deprecated option on line %s: %s" % (self.lineno, option), DeprecationWarning)

        return (values, args)

    def __init__(self, map={}, lineno=None):
        self.map = map
        self.lineno = lineno
        OptionParser.__init__(self, option_class=KSBooleanOption,
                              add_help_option=False)

# Creates a new Option type that supports a "required" option attribute.  Any
# option with this attribute must be supplied or an exception is thrown.
class RequiredOption (Option):
    ATTRS = Option.ATTRS + ['required']

    def _check_required (self):
        if self.required and not self.takes_value():
            raise OptionError("Required flag set for option that doesn't take a value", self)

    # Make sure _check_required() is called from the constructor!
    CHECK_METHODS = Option.CHECK_METHODS + [_check_required]

    def process (self, opt, value, values, parser):
        Option.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1

# Additional OptionParser actions.  "map" allows you to define a opt -> val
# mapping such that dest gets val when opt is seen.  "map_extend" allows you
# to define an opt -> [val1, ... valn] mapping such that dest gets a list of
# vals build up when opt is seen.
class MappableOption(RequiredOption):
    ACTIONS = RequiredOption.ACTIONS + ("map", "map_extend",)
    STORE_ACTIONS = RequiredOption.STORE_ACTIONS + ("map", "map_extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "map":
            values.ensure_value(dest, parser.map[opt.lstrip('-')])
        elif action == "map_extend":
            values.ensure_value(dest, []).extend(parser.map[opt.lstrip('-')])
        else:
            RequiredOption.take_action(self, action, dest, opt, value, values, parser)

# Creates a new Option type that supports a "deprecated" option attribute.
# Any option with this attribute will cause a DeprecationWarning to be
# thrown if the option is used.
class DeprecatedOption(MappableOption):
    ATTRS = MappableOption.ATTRS + ['deprecated']

    def process (self, opt, value, values, parser):
        MappableOption.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1

# Creates a new Option type that supports various booleans for values
class KSBooleanOption(DeprecatedOption):
    def _check_ksboolean(option, opt, value):
        if value in ("on", "yes", "1"):
            return True
        elif value in ("off", "no", "0"):
            return False
        else:
            raise OptionValueError("option %s: invalid boolean "
                                   "value: %r" % (opt, value))
    
    TYPES = Option.TYPES + ("ksboolean",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["ksboolean"] = _check_ksboolean

###
### SCRIPT HANDLING
###

# You may make a subclass of Script if you need additional script handling
# besides just a data representation.  For instance, anaconda may subclass
# this to add a run method.
class Script:
    def __repr__(self):
        str = ("(s: '%s' i: %s c: %d)") %  \
              (self.script, self.interp, self.inChroot)
        return string.replace(str, "\n", "|")

    def __init__(self, script, interp = "/bin/sh", inChroot = False,
                 logfile = None, errorOnFail = False, type = KS_SCRIPT_PRE):
        self.script = string.join(script, "")
        self.interp = interp
        self.inChroot = inChroot
        self.logfile = logfile
        self.errorOnFail = errorOnFail
        self.type = type

    # Produce a string representation of the script suitable for writing
    # to a kickstart file.  Add this to the end of the %whatever header.
    def write(self):
        str = ""
        if self.interp != "/bin/sh" and self.interp != "":
            str = str + " --interp %s" % self.interp
        if self.type == KS_SCRIPT_POST and not self.inChroot:
            str = str + " --nochroot"
        if self.logfile != None:
            str = str + " --logfile %s" % self.logfile
        if self.errorOnFail:
            str = str + " --erroronfail"
        
        str = str + "\n%s\n" % self.script
        return str

###
### COMMAND HANDLERS
###

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
                     "keyboard"     : self.doKeyboard,
                     "lang"         : self.doLang,
                     "langsupport"  : self.doLangSupport,
                     "logvol"       : self.doLogicalVolume,
                     "mediacheck"   : self.doMediaCheck,
                     "monitor"      : self.doMonitor,
                     "mouse"        : self.doMouse,
                     "network"      : self.doNetwork,
                     "nfs"          : self.doMethod,
                     "dmraid"       : self.doDmRaid,
                     "part"         : self.doPartition,
                     "partition"    : self.doPartition,
                     "poweroff"     : self.doReboot,
                     "raid"         : self.doRaid,
                     "reboot"       : self.doReboot,
                     "rootpw"       : self.doRootPw,
                     "selinux"      : self.doSELinux,
                     "shutdown"     : self.doReboot,
                     "skipx"        : self.doSkipX,
                     "text"         : self.doDisplayMode,
                     "timezone"     : self.doTimezone,
                     "url"          : self.doMethod,
                     "upgrade"      : self.doUpgrade,
                     "vnc"          : self.doVnc,
                     "volgroup"     : self.doVolumeGroup,
                     "xconfig"      : self.doXConfig,
                     "zerombr"      : self.doZeroMbr,
                     "zfcp"         : self.doZFCP,
                   }

    def resetHandlers (self):
        for key in self.handlers.keys():
            self.handlers[key] = None

    def deprecatedCommand(self, cmd):
        warnings.warn("The %s command has been deprecated and no longer has any effect.  It may be removed from future releases, which will result in a fatal error from kickstart.  Please modify your kickstart file to remove this command." % cmd, DeprecationWarning)

    def doAuthconfig(self, args):
        self.ksdata.authconfig = string.join(args)

    def doAutoPart(self, args):
        self.ksdata.autopart = True

    def doAutoStep(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--autoscreenshot", dest="autoscreenshot",
                      action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self.ksdata.autostep["autoscreenshot"] = opts.autoscreenshot

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

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.bootloader[key] = getattr(opts, key)

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

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.clearpart[key] = getattr(opts, key)

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

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.firewall[key] = getattr(opts, key)

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
        op.add_option("--drives", dest="drives", action=callback,
                      callback=drive_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)

        self.ksdata.ignoredisk = opt.ignoredisk

    def doInteractive(self, args):
        self.ksdata.interactive = True

    def doKeyboard(self, args):
        self.ksdata.keyboard = args[0]

    def doLang(self, args):
        self.ksdata.lang = args[0]

    def doLangSupport(self, args):
        self.deprecatedCommand("langsupport")

    def doLogicalVolume(self, args):
        def lv_cb (option, opt_str, value, parser):
            parser.values.ensure_value(option.dest, False)
            parser.values.ensure_value("preexist", True)

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
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="Mount point required for logvol")

        lvd = KickstartLogVolData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(lvd, key, getattr(opts, key))

        lvd.mountpoint = extra[0]
        self.ksdata.lvList.append(lvd)

    def doMediaCheck(self, args):
        self.ksdata.mediacheck = True

    def doMethod(self, args):
        op = KSOptionParser(lineno=self.lineno)

        self.ksdata.method["method"] = self.currentCmd

        if self.currentCmd == "cdrom":
            pass
        elif self.currentCmd == "harddrive":
            op.add_option("--partition", dest="partition", required=1)
            op.add_option("--dir", dest="dir", required=1)

            (opts, extra) = op.parse_args(args=args)
            self.ksdata.method["partition"] = opts.partition
            self.ksdata.method["dir"] = opts.dir
        elif self.currentCmd == "nfs":
            op.add_option("--server", dest="server", required=1)
            op.add_option("--dir", dest="dir", required=1)

            (opts, extra) = op.parse_args(args=args)
            self.ksdata.method["server"] = opts.server
            self.ksdata.method["dir"] = opts.dir
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

            (opts, extra) = op.parse_args(args=args)
            self.ksdata.method["url"] = opts.url

    def doMonitor(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--hsync", dest="hsync")
        op.add_option("--monitor", dest="monitor")
        op.add_option("--noprobe", dest="probe", action="store_false",
                      default=True)
        op.add_option("--vsync", dest="vsync")

        (opts, extra) = op.parse_args(args=args)

        if extra:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="Unexpected arguments to monitor command: %s" % extra)

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.monitor[key] = getattr(opts, key)

    def doMouse(self, args):
        self.deprecatedCommand("mouse")

    def doNetwork(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--bootproto", dest="bootProto", default="dhcp")
        op.add_option("--class", dest="dhcpclass")
        op.add_option("--device", dest="device")
        op.add_option("--essid", dest="essid")
        op.add_option("--ethtool", dest="ethtool")
        op.add_option("--gateway", dest="gateway")
        op.add_option("--hostname", dest="hostname")
        op.add_option("--ip", dest="ip")
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

        nd = KickstartNetworkData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(nd, key, getattr(opts, key))

        self.ksdata.network.append(nd)

    def doDmRaid(self, args):
        def name_cb(option, opt_str, value, parser):
            pass
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      nargs=1, required=1)
        op.add_option("--dev", dest="devices", action="append", type="string",
                      required=1)

        (opts, extra) = op.parse_args(args=args)

        dd = KickstartDmRaidData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(dd, key, getattr(opts, key))
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
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="Mount point required for partition")

        pd = KickstartPartData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(pd, key, getattr(opts, key))

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
        self.ksdata.reboot["eject"] = opts.eject

    def doRaid(self, args):
        def raid_cb (option, opt_str, value, parser):
            parser.values.ensure_value(option.dest, False)
            parser.values.ensure_value("preexist", True)

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
                      callback=level_cb, type="string", nargs=1, required=1)
        op.add_option("--noformat", action="callback", callback=raid_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--spares", dest="spares", action="store", type="int",
                      nargs=1, default=0)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)

        if len(extra) == 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="Mount point required for raid")

        rd = KickstartRaidData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(rd, key, getattr(opts, key))

        rd.mountpoint = extra[0]
        rd.members = extra[1:]
        self.ksdata.raidList.append(rd)

    def doRootPw(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self.ksdata.rootpw["isCrypted"] = opts.isCrypted

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="A single argument is expected for rootpw")

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

    def doSkipX(self, args):
        self.ksdata.skipx = True

    def doTimezone(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--utc", dest="isUtc", action="store_true", default=False)

        (opts, extra) = op.parse_args(args=args)
        self.ksdata.timezone["isUtc"] = opts.isUtc

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="A single argument is expected for timezone")

        self.ksdata.timezone["timezone"] = extra[0]

    def doUpgrade(self, args):
        self.ksdata.upgrade = True

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
        op.add_option("--port", dest="port", default="5500")

        (opts, extra) = op.parse_args(args=args)

        self.ksdata.vnc["enabled"] = True

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.vnc[key] = getattr(opts, key)

    def doVolumeGroup(self, args):
        # Have to be a little more complicated to set two values.
        def vg_cb (option, opt_str, value, parser):
            parser.values.ensure_value(option.dest, False)
            parser.values.ensure_value("preexist", True)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--noformat", action="callback", callback=vg_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--pesize", dest="pesize", type="int", nargs=1,
                      default=32768)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)

        vgd = KickstartVolGroupData()
        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            setattr(vgd, key, getattr(opts, key))

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
            raise KickstartValueError, formatErrorMsg(self.lineno, msg="Unexpected arguments to xconfig command: %s" % extra)

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.xconfig[key] = getattr(opts, key)

    def doZeroMbr(self, args):
        self.ksdata.zerombr = True

    def doZFCP(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--devnum", dest="devnum", required=1)
        op.add_option("--fcplun", dest="fcplun", required=1)
        op.add_option("--scsiid", dest="scsiid", required=1)
        op.add_option("--scsilun", dest="scsilun", required=1)
        op.add_option("--wwpn", dest="wwpn", required=1)

        (opts, extra) = op.parse_args(args=args)

        for key in filter (lambda k: getattr(opts, k) != None, op.keys()):
            self.ksdata.zfcp[key] = getattr(opts, key)

###
### PARSER
###

# The kickstart file parser.  This only transitions between states and calls
# handlers at certain points.  To create a specialized parser, make a subclass
# of this and override the methods you care about.  Methods that don't need to
# do anything may just pass.
#
# Passing None for kshandlers is valid just in case you don't care about
# handling any commands.
class KickstartParser:
    def __init__ (self, ksdata, kshandlers):
        self.handler = kshandlers
        self.ksdata = ksdata
        self.followIncludes = True
        self.state = STATE_COMMANDS
        self.script = None
        self.includeDepth = 0

    # Functions to be called when we are at certain points in the
    # kickstart file parsing.  Override these if you need special
    # behavior.
    def addScript (self):
        if string.join(self.script["body"]).strip() == "":
            return

        s = Script (self.script["body"], self.script["interp"],
                    self.script["chroot"], self.script["log"],
                    self.script["errorOnFail"], self.script["type"])

        self.ksdata.scripts.append(s)

    def addPackages (self, line):
        if line[0] == '@':
            line = line[1:]
            self.ksdata.groupList.append(line.lstrip())
        elif line[0] == '-':
            line = line[1:]
            self.ksdata.excludedList.append(line.lstrip())
        else:
            self.ksdata.packageList.append(line.lstrip())

    def handleCommand (self, lineno, args):
        if not self.handler:
            return

        cmd = args[0]
        cmdArgs = args[1:]

        if not self.handler.handlers.has_key(cmd):
            raise KickstartParseError, formatErrorMsg(lineno)
        else:
            if self.handler.handlers[cmd] != None:
                setattr(self.handler, "currentCmd", cmd)
                setattr(self.handler, "lineno", lineno)
                self.handler.handlers[cmd](cmdArgs)

    def handlePackageHdr (self, lineno, args):
        op = KSOptionParser(lineno=lineno)
        op.add_option("--excludedocs", dest="excludedocs", action="store_true",
                      default=False)
        op.add_option("--ignoremissing", dest="ignoremissing",
                      action="store_true", default=False)
        op.add_option("--nobase", dest="nobase", action="store_true",
                      default=False)
        op.add_option("--ignoredeps", dest="resolveDeps", action="store_false",
                      deprecated=1)
        op.add_option("--resolvedeps", dest="resolveDeps", action="store_true",
                      deprecated=1)

        (opts, extra) = op.parse_args(args=args[1:])

        self.ksdata.excludeDocs = opts.excludedocs
        self.ksdata.addBase = not opts.nobase
        if opts.ignoremissing:
            self.ksdata.handleMissing = KS_MISSING_IGNORE
        else:
            self.ksdata.handleMissing = KS_MISSING_PROMPT

    def handleScriptHdr (self, lineno, args):
        op = KSOptionParser(lineno=lineno)
        op.add_option("--erroronfail", dest="errorOnFail", action="store_true",
                      default=False)
        op.add_option("--interpreter", dest="interpreter", default="/bin/sh")
        op.add_option("--log", "--logfile", dest="log")

        if args[0] == "%pre" or args[0] == "%traceback":
            self.script["chroot"] = False
        elif args[0] == "%post":
            self.script["chroot"] = True
            op.add_option("--nochroot", dest="nochroot", action="store_true",
                          default=False)

        (opts, extra) = op.parse_args(args=args[1:])

        self.script["interp"] = opts.interpreter
        self.script["log"] = opts.log
        self.script["errorOnFail"] = opts.errorOnFail
        if hasattr(opts, "nochroot"):
            self.script["chroot"] = not opts.nochroot

    def readKickstart (self, file):
        # For error reporting.
        lineno = 0

        fh = open(file)
        needLine = True

        while True:
            if needLine:
                line = fh.readline()
                lineno += 1
                needLine = False

            # At the end of an included file
            if line == "" and self.includeDepth > 0:
                fh.close()
                break

            # Don't eliminate whitespace or comments from scripts.
            if line.isspace() or (line != "" and line.lstrip()[0] == '#'):
                # Save the platform for s-c-kickstart, though.
                if line[:10] == "#platform=" and self.state == STATE_COMMANDS:
                    self.ksdata.platform = line[11:]

                if self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                    self.script["body"].append(line)

                needLine = True
                continue

            # We only want to split the line if we're outside of a script,
            # as inside the script might involve some pretty weird quoting
            # that shlex doesn't understand.
            if self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                # Have we found a state transition?  If so, we still want
                # to split.  Otherwise, args won't be set but we'll fall through
                # all the way to the last case.
                if line != "" and string.split(line.lstrip())[0] in \
                   ["%post", "%pre", "%traceback", "%include", "%packages"]:
                    args = shlex.split(line)
                else:
                    args = None
            else:
                args = shlex.split(line)

            if args and args[0] == "%include" and self.followIncludes:
                if not args[1]:
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    self.includeDepth += 1
                    self.readKickstart (args[1])
                    self.includeDepth -= 1
                    needLine = True
                    continue

            if self.state == STATE_COMMANDS:
                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self.state = STATE_SCRIPT_HDR
                elif args[0] == "%packages":
                    self.state = STATE_PACKAGES
                elif args[0][0] == '%':
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    needLine = True
                    self.handleCommand(lineno, args)

            elif self.state == STATE_PACKAGES:
                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] in ["%pre", "%post", "%traceback"]:
                    self.state = STATE_SCRIPT_HDR
                elif args[0] == "%packages":
                    needLine = True
                    self.handlePackageHdr (lineno, args)
                elif args[0][0] == '%':
                    raise KickstartParseError, formatErrorMsg(lineno)
                else:
                    needLine = True
                    self.addPackages (string.rstrip(line))

            elif self.state == STATE_SCRIPT_HDR:
                needLine = True
                self.script = {"body": [], "interp": "/bin/sh", "log": None,
                               "errorOnFail": False}

                if not args and self.includeDepth == 0:
                    self.state = STATE_END
                elif args[0] == "%pre":
                    self.state = STATE_PRE
                    self.script["type"] = KS_SCRIPT_PRE
                elif args[0] == "%post":
                    self.state = STATE_POST
                    self.script["type"] = KS_SCRIPT_POST
                elif args[0] == "%traceback":
                    self.state = STATE_TRACEBACK
                    self.script["type"] = KS_SCRIPT_TRACEBACK
                elif args[0][0] == '%':
                    raise KickstartParseError, formatErrorMsg(lineno)

                self.handleScriptHdr (lineno, args)

            elif self.state in [STATE_PRE, STATE_POST, STATE_TRACEBACK]:
                if line == "" and self.includeDepth == 0:
                    # If we're at the end of the kickstart file, add the script.
                    self.addScript()
                    self.state = STATE_END
                elif args and args[0] in ["%pre", "%post", "%traceback", "%packages"]:
                    # Otherwise we're now at the start of the next section.
                    # Figure out what kind of a script we just finished
                    # reading, add it to the list, and switch to the initial
                    # state.
                    self.addScript()
                    self.state = STATE_COMMANDS
                else:
                    # Otherwise just add to the current script body.
                    self.script["body"].append(line)
                    needLine = True

            elif self.state == STATE_END:
                break
