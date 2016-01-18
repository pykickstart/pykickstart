#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007-2014 Red Hat, Inc.
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
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser, commaSplit

from pykickstart.i18n import _

class FC3_Bootloader(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.driveorder = kwargs.get("driveorder", [])
        self.appendLine = kwargs.get("appendLine", "")
        self.forceLBA = kwargs.get("forceLBA", False)
        self.linear = kwargs.get("linear", True)
        self.location = kwargs.get("location", "none")
        self.md5pass = kwargs.get("md5pass", "")
        self.password = kwargs.get("password", "")
        self.upgrade = kwargs.get("upgrade", False)
        self.useLilo = kwargs.get("useLilo", False)

        self.deleteRemovedAttrs()

    def _getArgsAsStr(self):
        retval = ""

        if self.appendLine != "":
            retval += " --append=\"%s\"" % self.appendLine
        if self.linear:
            retval += " --linear"
        if self.location:
            retval += " --location=%s" % self.location
        if hasattr(self, "forceLBA") and self.forceLBA:
            retval += " --lba32"
        if self.password != "":
            retval += " --password=\"%s\"" % self.password
        if self.md5pass != "":
            retval += " --md5pass=\"%s\"" % self.md5pass
        if self.upgrade:
            retval += " --upgrade"
        if self.useLilo:
            retval += " --useLilo"
        if len(self.driveorder) > 0:
            retval += " --driveorder=\"%s\"" % ",".join(self.driveorder)

        return retval

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.location != "":
            retval += "# System bootloader configuration\nbootloader"
            retval += self._getArgsAsStr() + "\n"

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--append", dest="appendLine")
        op.add_argument("--linear", action="store_true", default=True)
        op.add_argument("--nolinear", dest="linear", action="store_false")
        op.add_argument("--location", default="mbr",
                        choices=["mbr", "partition", "none", "boot"])
        op.add_argument("--lba32", dest="forceLBA", action="store_true", default=False)
        op.add_argument("--password", default="")
        op.add_argument("--md5pass", default="")
        op.add_argument("--upgrade", action="store_true", default=False)
        op.add_argument("--useLilo", action="store_true", default=False)
        op.add_argument("--driveorder", type=commaSplit)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(ns)

        if self.currentCmd == "lilo":
            self.useLilo = True

        return self

class FC4_Bootloader(FC3_Bootloader):
    removedKeywords = FC3_Bootloader.removedKeywords + ["linear", "useLilo"]
    removedAttrs = FC3_Bootloader.removedAttrs + ["linear", "useLilo"]

    def __init__(self, writePriority=10, *args, **kwargs):
        FC3_Bootloader.__init__(self, writePriority, *args, **kwargs)

    def _getArgsAsStr(self):
        retval = ""
        if self.appendLine != "":
            retval += " --append=\"%s\"" % self.appendLine
        if self.location:
            retval += " --location=%s" % self.location
        if hasattr(self, "forceLBA") and self.forceLBA:
            retval += " --lba32"
        if self.password != "":
            retval += " --password=\"%s\"" % self.password
        if self.md5pass != "":
            retval += " --md5pass=\"%s\"" % self.md5pass
        if self.upgrade:
            retval += " --upgrade"
        if len(self.driveorder) > 0:
            retval += " --driveorder=\"%s\"" % ",".join(self.driveorder)
        return retval

    def _getParser(self):
        op = FC3_Bootloader._getParser(self)
        op.remove_argument("--linear")
        op.remove_argument("--nolinear")
        op.remove_argument("--useLilo")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(ns)
        return self

class F8_Bootloader(FC4_Bootloader):
    removedKeywords = FC4_Bootloader.removedKeywords
    removedAttrs = FC4_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        FC4_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.timeout = kwargs.get("timeout", None)
        self.default = kwargs.get("default", "")

    def _getArgsAsStr(self):
        ret = FC4_Bootloader._getArgsAsStr(self)

        if self.timeout is not None:
            ret += " --timeout=%d" %(self.timeout,)
        if self.default:
            ret += " --default=%s" %(self.default,)

        return ret

    def _getParser(self):
        op = FC4_Bootloader._getParser(self)
        op.add_argument("--timeout", type=int)
        op.add_argument("--default")
        return op

class F12_Bootloader(F8_Bootloader):
    removedKeywords = F8_Bootloader.removedKeywords
    removedAttrs = F8_Bootloader.removedAttrs

    def _getParser(self):
        op = F8_Bootloader._getParser(self)
        op.add_argument("--lba32", dest="forceLBA", deprecated=1, action="store_true")
        return op

class F14_Bootloader(F12_Bootloader):
    removedKeywords = F12_Bootloader.removedKeywords + ["forceLBA"]
    removedAttrs = F12_Bootloader.removedKeywords + ["forceLBA"]

    def _getParser(self):
        op = F12_Bootloader._getParser(self)
        op.remove_argument("--lba32")
        return op

class F15_Bootloader(F14_Bootloader):
    removedKeywords = F14_Bootloader.removedKeywords
    removedAttrs = F14_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F14_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.isCrypted = kwargs.get("isCrypted", False)

    def _getArgsAsStr(self):
        ret = F14_Bootloader._getArgsAsStr(self)

        if self.isCrypted:
            ret += " --iscrypted"

        return ret

    def _getParser(self):
        op = F14_Bootloader._getParser(self)
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true", default=False)
        op.add_argument("--md5pass", dest="_md5pass")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        # argparse doesn't give us a way to set two things at once, so we need to check if
        # _md5pass was given and if so, set everything now.
        if getattr(ns, "_md5pass", None):
            ns.password = ns._md5pass
            ns.isCrypted = True
            del(ns._md5pass)

        self._setToSelf(ns)
        return self

class F17_Bootloader(F15_Bootloader):
    removedKeywords = F15_Bootloader.removedKeywords
    removedAttrs = F15_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F15_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.bootDrive = kwargs.get("bootDrive", "")

    def _getArgsAsStr(self):
        ret = F15_Bootloader._getArgsAsStr(self)

        if self.bootDrive:
            ret += " --boot-drive=%s" % self.bootDrive

        return ret

    def _getParser(self):
        op = F15_Bootloader._getParser(self)
        op.add_argument("--boot-drive", dest="bootDrive", default="")
        return op

    def parse(self, args):
        retval = F15_Bootloader.parse(self, args)

        if "," in retval.bootDrive:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--boot-drive accepts only one argument")))

        return retval

class F18_Bootloader(F17_Bootloader):
    removedKeywords = F17_Bootloader.removedKeywords
    removedAttrs = F17_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F17_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.leavebootorder = kwargs.get("leavebootorder", False)

    def _getArgsAsStr(self):
        ret = F17_Bootloader._getArgsAsStr(self)

        if self.leavebootorder:
            ret += " --leavebootorder"

        return ret

    def _getParser(self):
        op = F17_Bootloader._getParser(self)
        op.add_argument("--leavebootorder", action="store_true", default=False)
        return op

class RHEL5_Bootloader(FC4_Bootloader):
    removedKeywords = FC4_Bootloader.removedKeywords
    removedAttrs = FC4_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        FC4_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.hvArgs = kwargs.get("hvArgs", "")

    def _getArgsAsStr(self):
        ret = FC4_Bootloader._getArgsAsStr(self)

        if self.hvArgs:
            ret += " --hvargs=\"%s\"" %(self.hvArgs,)

        return ret

    def _getParser(self):
        op = FC4_Bootloader._getParser(self)
        op.add_argument("--hvargs", dest="hvArgs")
        return op

class RHEL6_Bootloader(F12_Bootloader):
    removedKeywords = F12_Bootloader.removedKeywords
    removedAttrs = F12_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F12_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.isCrypted = kwargs.get("isCrypted", False)

    def _getArgsAsStr(self):
        ret = F12_Bootloader._getArgsAsStr(self)

        if self.isCrypted:
            ret += " --iscrypted"

        return ret

    def _getParser(self):
        op = F12_Bootloader._getParser(self)
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true", default=False)
        op.add_argument("--md5pass", dest="_md5pass")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        # argparse doesn't give us a way to set two things at once, so we need to check if
        # _md5pass was given and if so, set everything now.
        if getattr(ns, "_md5pass", None):
            ns.password = ns._md5pass
            ns.isCrypted = True
            del(ns._md5pass)

        self._setToSelf(ns)
        return self

class F19_Bootloader(F18_Bootloader):
    removedKeywords = F18_Bootloader.removedKeywords
    removedAttrs = F18_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F18_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.extlinux = kwargs.get("extlinux", False)

    def _getArgsAsStr(self):
        ret = F18_Bootloader._getArgsAsStr(self)

        if self.extlinux:
            ret += " --extlinux"

        return ret

    def _getParser(self):
        op = F18_Bootloader._getParser(self)
        op.add_argument("--extlinux", action="store_true", default=False)
        return op

class F21_Bootloader(F19_Bootloader):
    removedKeywords = F19_Bootloader.removedKeywords
    removedAttrs = F19_Bootloader.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        F19_Bootloader.__init__(self, writePriority, *args, **kwargs)

        self.disabled = kwargs.get("disabled", False)
        self.nombr = kwargs.get("nombr", False)

    def _getArgsAsStr(self):
        if self.disabled:
            return " --disabled"

        ret = F19_Bootloader._getArgsAsStr(self)
        if self.nombr:
            ret += " --nombr"
        return ret

    def _getParser(self):
        op = F19_Bootloader._getParser(self)
        op.add_argument("--disabled", action="store_true", default=False)
        op.add_argument("--nombr", action="store_true", default=False)
        return op

RHEL7_Bootloader = F21_Bootloader
