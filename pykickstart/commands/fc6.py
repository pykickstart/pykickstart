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


###
### DISPATCHER
###
class FC6Handler(FC5Handler):
    def __init__(self):
        FC5Handler.__init__(self)

        self.registerHandler(CommandDmRaid(), ["dmraid"])
        self.registerHandler(CommandIscsi(), ["iscsi"])
        self.registerHandler(CommandIscsiName(), ["iscsiname"])
        self.registerHandler(CommandKey(), ["key"])
        self.registerHandler(CommandLogging(), ["logging"])
        self.registerHandler(CommandMultiPath(), ["multipath"])
        self.registerHandler(CommandRepo(), ["repo"])
        self.registerHandler(CommandServices(), ["services"])
        self.registerHandler(CommandUser(), ["user"])


###
### DATA CLASSES
###

class KickstartDmRaidData(BaseData):
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

class KickstartIscsiData(BaseData):
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

class KickstartMpPathData(BaseData):
    def __init__(self, mpdev="", device="", rule=""):
        BaseData.__init__(self)
        self.mpdev = mpdev
        self.device = device
        self.rule = rule

    def __str__(self):
        return " --device=%s --rule=\"%s\"" % (self.device, self.rule)

class KickstartMultiPathData(BaseData):
    def __init__(self, name="", paths=[]):
        BaseData.__init__(self)
        self.name = name
        self.paths = paths

    def __str__(self):
        retval = ""

        for path in self.paths:
            retval += "multipath --mpdev=%s %s\n" % (self.name, path.__str__())

        return retval

class KickstartRepoData(BaseData):
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

class KickstartUserData(BaseData):
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

class CommandDmRaid(KickstartCommand):
    def __init__(self, dmraids=[]):
        KickstartCommand.__init__(self)
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

        dm = KickstartDmRaidData()
        (opts, extra) = op.parse_args(args=args)
        dm.name = dm.name.split('/')[-1]
        self._setToObj(op, opts, dm)
        self.add(dm)

    def add(self, newObj):
        self.dmraids.append(newObj)

class CommandIscsi(KickstartCommand):
    def __init__(self, iscsi=[]):
        KickstartCommand.__init__(self)
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

        dd = KickstartIscsiData()
        self._setToObj(op, opts, dd)
        self.add(dd)

    def add(self, newObj):
        self.iscsi.append(newObj)

class CommandIscsiName(KickstartCommand):
    def __init__(self, iscsiname=""):
        KickstartCommand.__init__(self)
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

class CommandKey(KickstartCommand):
    def __init__(self, key=""):
        KickstartCommand.__init__(self)
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

class CommandLogging(KickstartCommand):
    def __init__(self, host="", level="info", port=""):
        KickstartCommand.__init__(self)
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

class CommandMultiPath(KickstartCommand):
    def __init__(self, mpaths=[]):
        KickstartCommand.__init__(self)
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
        dd = KickstartMpPathData()
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
            mpath = KickstartMultiPathData()
            self.add(mpath)
        else:
            mpath = self.mpaths[x]

        mpath.paths.append(dd)

    def add(self, newObj):
        self.mpaths.append(newObj)

class CommandRepo(KickstartCommand):
    def __init__(self, repoList=[]):
        KickstartCommand.__init__(self)
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

        rd = KickstartRepoData()
        self._setToObj(op, opts, rd)
        self.add(rd)

    def add(self, newObj):
        self.repoList.append(newObj)

class CommandServices(KickstartCommand):
    def __init__(self, disabled=[], enabled=[]):
        KickstartCommand.__init__(self)
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

class CommandUser(KickstartCommand):
    def __init__(self, userList=[]):
        KickstartCommand.__init__(self)
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

        ud = KickstartUserData()
        (opts, extra) = op.parse_args(args=args)
        self._setToObj(op, opts, ud)
        self.add(ud)

    def add(self, newObj):
        self.userList.append(newObj)
