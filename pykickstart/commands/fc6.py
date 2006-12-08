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

        self._registerHandler(CommandDmRaid(), ["dmraid"])
        self._registerHandler(CommandIscsi(), ["iscsi"])
        self._registerHandler(CommandIscsiName(), ["iscsiname"])
        self._registerHandler(CommandKey(), ["key"])
        self._registerHandler(CommandLogging(), ["logging"])
        self._registerHandler(CommandMultiPath(), ["multipath"])
        self._registerHandler(CommandRepo(), ["repo"])
        self._registerHandler(CommandServices(), ["services"])
        self._registerHandler(CommandUser(), ["user"])


###
### DATA CLASSES
###

class KickstartDmRaidData:
    def __init__(self):
        self.name = ""
        self.devices = []
        self.dmset = None

    def __str__(self):
        retval = "dmraid --name=%s" % self.name

        for dev in self.devices:
            retval += " --dev=\"%s\"" % dev

        return retval + "\n"

class KickstartIscsiData:
    def __init__(self):
        self.ipaddr = ""
        self.port = ""
        self.target = ""
        self.user = None
        self.password = None

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

class KickstartRepoData:
    def __init__(self):
        self.baseurl = ""
        self.mirrorlist = ""
        self.name = ""

    def __str__(self):
        if self.baseurl:
            urlopt = "--baseurl=%s" % self.baseurl
        elif self.mirrorlist:
            urlopt = "--mirrorlist=%s" % self.mirrorlist

        return "repo --name=%s %s\n" % (self.name, urlopt)

class KickstartUserData:
    def __init__(self):
        self.groups = []
        self.homedir = ""
        self.isCrypted = False
        self.name = ""
        self.password = ""
        self.shell = ""
        self.uid = None

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
    def __init__(self):
        KickstartCommand.__init__(self)
        self.dmraids = []

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

class CommandIscsi(KickstartCommand):
    def __init__(self):
        KickstartCommand.__init__(self)
        self.iscsi = []

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

        self._setToSelf(op, opts)

class CommandIscsiName(KickstartCommand):
    def __init__(self):
        KickstartCommand.__init__(self)
        self.iscsiname = ""

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
    def __init__(self):
        KickstartCommand.__init__(self)
        self.key = ""

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
    def __init__(self):
        KickstartCommand.__init__(self)
        self.host = ""
        self.level = "info"
        self.port = ""

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
    def __init__(self):
        KickstartCommand.__init__(self)
        self.mpdev = ""
        self.device = ""
        self.rule = ""

    def __str__(self):
        return ""

    def parse(self, args):
        op = KSOptionParser(self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--device", dest="device", action="store", type="string",
                      required=1)
        op.add_option("--rule", dest="rule", action="store", type="string",
                      required=1)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
        self.mpdev = self.mpdev.split('/')[-1]

#        ### XXX FIX ALL THIS
#        parent = None
#        for x in range(0, len(self.ksdata.mpaths)):
#            mpath = self.ksdata.mpaths[x]
#            for path in mpath.paths:
#                if path.device == dd.device:
#                    mapping = {"device": path.device, "multipathdev": path.mpdev}
#                    raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Device '%(device)s' is already used in multipath '%(multipathdev)s'") % mapping)
#            if mpath.name == dd.mpdev:
#                parent = x
#
#        if parent is None:
#            mpath = KickstartMultiPathData()
#            self.ksdata.mpaths.append(mpath)
#        else:
#            mpath = self.ksdata.mpaths[x]
#
#        mpath.paths.append(dd)

class CommandRepo(KickstartCommand):
    def __init__(self):
        KickstartCommand.__init__(self)
        self.repoList = []

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

class CommandServices(KickstartCommand):
    def __init__(self):
        KickstartCommand.__init__(self)
        self.disabled = []
        self.enabled = []

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
    def __init__(self):
        KickstartCommand.__init__(self)
        self.userList = []

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
