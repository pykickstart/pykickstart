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

from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

### INHERIT FROM A PREVIOUS RELEASE
from fc5 import *

class FC6Version(FC5Version):
    ###
    ### DATA CLASSES
    ###
    class DmRaidData(BaseData):
        def __init__(self, name="", devices=[], dmset=None):
            BaseData.__init__(self)
            self.name = name
            self.devices = devices
            self.dmset = dmset

        def __str__(self):
            retval = "dmraid --name=%s" % self.name

            for dev in self.devices:
                retval += " --dev=\"%s\"" % dev

            return retval + "\n"

    class IscsiData(BaseData):
        def __init__(self, ipaddr="", port="", target="", user=None, password=None):
            BaseData.__init__(self)
            self.ipaddr = ipaddr
            self.port = port
            self.target = target
            self.user = user
            self.password = password

        def __str__(self):
            retval = "iscsi"

            if self.target != "":
                retval += " --target=%s" % self.target
            if self.ipaddr != "":
                retval += " --ipaddr=%s" % self.ipaddr
            if self.port != "":
                retval += " --port=%s" % self.port
            if self.user is not None:
                retval += " --user=%s" % self.user
            if self.password is not None:
                retval += " --password=%s" % self.password

            return retval + "\n"

    class MpPathData(BaseData):
        def __init__(self, mpdev="", device="", rule=""):
            BaseData.__init__(self)
            self.mpdev = mpdev
            self.device = device
            self.rule = rule

        def __str__(self):
            return " --device=%s --rule=\"%s\"" % (self.device, self.rule)

    class MultiPathData(BaseData):
        def __init__(self, name="", paths=[]):
            BaseData.__init__(self)
            self.name = name
            self.paths = paths

        def __str__(self):
            retval = ""

            for path in self.paths:
                retval += "multipath --mpdev=%s %s\n" % (self.name, path.__str__())

            return retval

    class NetworkData(BaseData):
        def __init__(self, bootProto="dhcp", dhcpclass="", device="", essid="",
                     ethtool="", gateway="", hostname="", ip="", ipv4=True,
                     ipv6=True, mtu="", nameserver="", netmask="", nodns=False,
                     notksdevice=False, onboot=True, wepkey=""):
            BaseData.__init__(self)
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

    class RepoData(BaseData):
        def __init__(self, baseurl="", mirrorlist="", name=""):
            BaseData.__init__(self)
            self.baseurl = baseurl
            self.mirrorlist = mirrorlist
            self.name = name

        def __str__(self):
            if self.baseurl:
                urlopt = "--baseurl=%s" % self.baseurl
            elif self.mirrorlist:
                urlopt = "--mirrorlist=%s" % self.mirrorlist

            return "repo --name=%s %s\n" % (self.name, urlopt)

    class UserData(BaseData):
        def __init__(self, groups=[], homedir="", isCrypted=False, name="",
                     password="", shell="", uid=None):
            BaseData.__init__(self)
            self.groups = groups
            self.homedir = homedir
            self.isCrypted = isCrypted
            self.name = name
            self.password = password
            self.shell = shell
            self.uid = uid

        def __str__(self):
            retval = "user"

            if len(self.groups) > 0:
                retval += " --groups=%s" % string.join(self.groups, ",")
            if self.homedir:
                retval += " --homedir=%s" % self.homedir
            if self.name:
                retval += " --name=%s" % self.name
            if self.password:
                retval += " --password=%s" % self.password
            if self.isCrypted:
                retval += " --isCrypted"
            if self.shell:
                retval += " --shell=%s" % self.shell
            if self.uid:
                retval += " --uid=%s" % self.uid

            return retval + "\n"


    ###
    ### COMMAND CLASSES
    ###
    class DmRaid(KickstartCommand):
        def __init__(self, writePriority=0, dmraids=[]):
            KickstartCommand.__init__(self, writePriority)
            self.dmraids = dmraids

        def __str__(self):
            retval = ""
            for dm in self.dmraids:
                retval += dm.__str__()

            return retval

        def parse(self, args):
            op = KSOptionParser(self.lineno)
            op.add_option("--name", dest="name", action="store", type="string",
                          required=1)
            op.add_option("--dev", dest="devices", action="append", type="string",
                          required=1)

            dm = self.dispatcher.DmRaidData()
            (opts, extra) = op.parse_args(args=args)
            dm.name = dm.name.split('/')[-1]
            self._setToObj(op, opts, dm)
            self.add(dm)

        def add(self, newObj):
            self.dmraids.append(newObj)

    class Iscsi(KickstartCommand):
        def __init__(self, writePriority=0, iscsi=[]):
            KickstartCommand.__init__(self, writePriority)
            self.iscsi = iscsi

        def __str__(self):
            retval = ""
            for iscsi in self.iscsi:
                retval += iscsi.__str__()

            return retval

        def parse(self, args):
            op = KSOptionParser(self.lineno)
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

            dd = self.dispatcher.IscsiData()
            self._setToObj(op, opts, dd)
            self.add(dd)

        def add(self, newObj):
            self.iscsi.append(newObj)

    class IscsiName(KickstartCommand):
        def __init__(self, writePriority=0, iscsiname=""):
            KickstartCommand.__init__(self, writePriority)
            self.iscsiname = iscsiname

        def __str__(self):
            if self.iscsiname != "":
                return "iscsiname %s" % self.iscsiname
            else:
                return ""

        def parse(self, args):
            if len(args) > 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "iscsiname")
            self.iscsiname = args[0]

    class Key(KickstartCommand):
        def __init__(self, writePriority=0, key=""):
            KickstartCommand.__init__(self, writePriority)
            self.key = key

        def __str__(self):
            if self.key == KS_INSTKEY_SKIP:
                return "key --skip"
            elif self.key != "":
                return "key %s" % self.key
            else:
                return ""

        def parse(self, args):
            if len(args) > 1:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Command %s only takes one argument") % "key")

            if args[0] == "--skip":
                self.key = KS_INSTKEY_SKIP
            else:
                self.key = args[0]

    class Logging(KickstartCommand):
        def __init__(self, writePriority=0, host="", level="info", port=""):
            KickstartCommand.__init__(self, writePriority)
            self.host = host
            self.level = level
            self.port = port

        def __str__(self):
            retval = "# Installation logging level\nlogging --level=%s" % self.level

            if self.host != "":
                retval += " --host=%s" % self.host

                if self.port != "":
                    retval += " --port=%s" % self.port

            return retval + "\n"

        def parse(self, args):
            op = KSOptionParser(self.lineno)
            op.add_option("--host")
            op.add_option("--level", type="choice",
                          choices=["debug", "info", "warning", "error", "critical"])
            op.add_option("--port")

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

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
                retval = "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.server, self.dir)
                if self.otps:
                    retval += " --opts=\"%s\"" % self.opts

                return retval + "\n"
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

    class Monitor(KickstartCommand):
        def __init__(self, writePriority=0, hsync="", monitor="", probe=True,
                     vsync=""):
            KickstartCommand.__init__(self, writePriority)
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

    class MultiPath(KickstartCommand):
        def __init__(self, writePriority=0, mpaths=[]):
            KickstartCommand.__init__(self, writePriority)
            self.mpaths = mpaths

        def __str__(self):
            retval = ""
            for mpath in self.mpaths:
                retval += mpath.__str__()

            return retval

        def parse(self, args):
            op = KSOptionParser(self.lineno)
            op.add_option("--name", dest="name", action="store", type="string",
                          required=1)
            op.add_option("--device", dest="device", action="store", type="string",
                          required=1)
            op.add_option("--rule", dest="rule", action="store", type="string",
                          required=1)

            (opts, extra) = op.parse_args(args=args)
            dd = self.dispatcher.MpPathData()
            self._setToObj(op, opts, dd)
            dd.mpdev = dd.mpdev.split('/')[-1]

            parent = None
            for x in range(0, len(self.mpaths)):
                mpath = self.mpaths[x]
                for path in mpath.paths:
                    if path.device == dd.device:
                        mapping = {"device": path.device, "multipathdev": path.mpdev}
                        raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Device '%(device)s' is already used in multipath '%(multipathdev)s'") % mapping)
                if mpath.name == dd.mpdev:
                    parent = x

            if parent is None:
                mpath = self.dispatcher.MultiPathData()
                self.add(mpath)
            else:
                mpath = self.mpaths[x]

            mpath.paths.append(dd)

        def add(self, newObj):
            self.mpaths.append(newObj)

    class Network(KickstartCommand):
        def __init__(self, writePriority=0, network=[]):
            KickstartCommand.__init__(self, writePriority)
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
            op.add_option("--noipv4", dest="ipv4", action="store_false",
                          default=True)
            op.add_option("--noipv6", dest="ipv6", action="store_false",
                          default=True)
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
            nd = self.dispatcher.NetworkData()
            self._setToObj(op, opts, nd)
            self.add(nd)

        def add(self, newObj):
            self.network.append(newObj)

    class Reboot(KickstartCommand):
        def __init__(self, writePriority=0, action=KS_WAIT, eject=False):
            KickstartCommand.__init__(self, writePriority)
            self.action = action
            self.eject = eject

        def __str__(self):
            retval = ""

            if self.action == KS_REBOOT:
                retval = "# Reboot after installation\nreboot\n"
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

    class Repo(KickstartCommand):
        def __init__(self, writePriority=0, repoList=[]):
            KickstartCommand.__init__(self, writePriority)
            self.repoList = repoList

        def __str__(self):
            retval = ""
            for repo in self.repoList:
                retval += repo.__str__()

            return retval

        def parse(self, args):
            op = KSOptionParser(self.lineno)
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

            rd = self.dispatcher.RepoData()
            self._setToObj(op, opts, rd)
            self.add(rd)

        def add(self, newObj):
            self.repoList.append(newObj)

    class Services(KickstartCommand):
        def __init__(self, writePriority=0, disabled=[], enabled=[]):
            KickstartCommand.__init__(self, writePriority)
            self.disabled = disabled
            self.enabled = enabled

        def __str__(self):
            retval = ""

            if len(self.disabled) > 0:
                retval += " --disabled=%s" % string.join(self.disabled, ",")
            if len(self.enabled) > 0:
                retval += " --enabled=%s" % string.join(self.enabled, ",")

            if retval != "":
                return "# System services\nservices %s\n" % retval
            else:
                return ""

        def parse(self, args):
            def services_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)

            op = KSOptionParser(self.lineno)
            op.add_option("--disabled", dest="disabled", action="callback",
                          callback=services_cb, nargs=1, type="string")
            op.add_option("--enabled", dest="enabled", action="callback",
                          callback=services_cb, nargs=1, type="string")

            (opts, extra) = op.parse_args(args=args)
            self._setToSelf(op, opts)

    class User(KickstartCommand):
        def __init__(self, writePriority=0, userList=[]):
            KickstartCommand.__init__(self, writePriority)
            self.userList = userList

        def __str__(self):
            retval = ""
            for user in self.userList:
                retval += user.__str__()

            return retval

        def parse(self, args):
            def groups_cb (option, opt_str, value, parser):
                for d in value.split(','):
                    parser.values.ensure_value(option.dest, []).append(d)
                
            op = KSOptionParser(self.lineno)
            op.add_option("--groups", dest="groups", action="callback",
                          callback=groups_cb, nargs=1, type="string")
            op.add_option("--homedir")
            op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                          default=False)
            op.add_option("--name", required=1)
            op.add_option("--password")
            op.add_option("--shell")
            op.add_option("--uid", type="int")

            ud = self.dispatcher.UserData()
            (opts, extra) = op.parse_args(args=args)
            self._setToObj(op, opts, ud)
            self.add(ud)

        def add(self, newObj):
            self.userList.append(newObj)

    class Vnc(KickstartCommand):
        def __init__(self, writePriority=0, enabled=False, password="", host="",
                     port=""):
            KickstartCommand.__init__(self, writePriority)
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

    class XConfig(KickstartCommand):
        def __init__(self, writePriority=0, driver="", defaultdesktop="", depth=0,
                     resolution="", startX=False, videoRam=""):
            KickstartCommand.__init__(self, writePriority)
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
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

            self._setToSelf(op, opts)

    def __init__(self):
        FC5Version.__init__(self)

        self.registerHandler(self.DmRaid(writePriority=60), ["dmraid"])
        self.registerHandler(self.Iscsi(writePriority=70), ["iscsi"])
        self.registerHandler(self.IscsiName(writePriority=71), ["iscsiname"])
        self.registerHandler(self.Key(), ["key"])
        self.registerHandler(self.Logging(), ["logging"])
        self.registerHandler(self.Method(), ["cdrom", "harddrive", "nfs", "url"])
        self.registerHandler(self.Monitor(), ["monitor"])
        self.registerHandler(self.MultiPath(writePriority=50), ["multipath"])
        self.registerHandler(self.Network(), ["network"])
        self.registerHandler(self.Reboot(), ["halt", "poweroff", "reboot", "shutdown"])
        self.registerHandler(self.Repo(), ["repo"])
        self.registerHandler(self.Services(), ["services"])
        self.registerHandler(self.User(), ["user"])
        self.registerHandler(self.Vnc(), ["vnc"])
        self.registerHandler(self.XConfig(), ["xconfig"])
