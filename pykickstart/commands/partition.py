#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008, 2012 Red Hat, Inc.
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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

import gettext
import warnings
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC3_PartData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.active = kwargs.get("active", False)
        self.primOnly = kwargs.get("primOnly", False)
        self.end = kwargs.get("end", 0)
        self.fstype = kwargs.get("fstype", "")
        self.grow = kwargs.get("grow", False)
        self.maxSizeMB = kwargs.get("maxSizeMB", 0)
        self.format = kwargs.get("format", True)
        self.onbiosdisk = kwargs.get("onbiosdisk", "")
        self.disk = kwargs.get("disk", "")
        self.onPart = kwargs.get("onPart", "")
        self.recommended = kwargs.get("recommended", False)
        self.size = kwargs.get("size", None)
        self.start = kwargs.get("start", 0)
        self.mountpoint = kwargs.get("mountpoint", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.mountpoint == y.mountpoint

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.active:
            retval += " --active"
        if self.primOnly:
            retval += " --asprimary"
        if hasattr(self, "end") and self.end != 0:
            retval += " --end=%s" % self.end
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
            retval += " --size=%s" % self.size
        if hasattr(self, "start") and self.start != 0:
            retval += " --start=%s" % self.start

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "part %s%s\n" % (self.mountpoint, self._getArgsAsStr())
        return retval

class FC4_PartData(FC3_PartData):
    removedKeywords = FC3_PartData.removedKeywords
    removedAttrs = FC3_PartData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_PartData.__init__(self, *args, **kwargs)
        self.bytesPerInode = kwargs.get("bytesPerInode", 4096)
        self.fsopts = kwargs.get("fsopts", "")
        self.label = kwargs.get("label", "")

    def _getArgsAsStr(self):
        retval = FC3_PartData._getArgsAsStr(self)

        if hasattr(self, "bytesPerInode") and self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.label != "":
            retval += " --label=%s" % self.label

        return retval

class RHEL5_PartData(FC4_PartData):
    removedKeywords = FC4_PartData.removedKeywords
    removedAttrs = FC4_PartData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC4_PartData.__init__(self, *args, **kwargs)
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = FC4_PartData._getArgsAsStr(self)

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F9_PartData(FC4_PartData):
    removedKeywords = FC4_PartData.removedKeywords + ["bytesPerInode"]
    removedAttrs = FC4_PartData.removedAttrs + ["bytesPerInode"]

    def __init__(self, *args, **kwargs):
        FC4_PartData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.fsopts = kwargs.get("fsopts", "")
        self.label = kwargs.get("label", "")
        self.fsprofile = kwargs.get("fsprofile", "")
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = FC4_PartData._getArgsAsStr(self)

        if self.fsprofile != "":
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F11_PartData(F9_PartData):
    removedKeywords = F9_PartData.removedKeywords + ["start", "end"]
    removedAttrs = F9_PartData.removedAttrs + ["start", "end"]

class F12_PartData(F11_PartData):
    removedKeywords = F11_PartData.removedKeywords
    removedAttrs = F11_PartData.removedAttrs

    def __init__(self, *args, **kwargs):
        F11_PartData.__init__(self, *args, **kwargs)

        self.escrowcert = kwargs.get("escrowcert", "")
        self.backuppassphrase = kwargs.get("backuppassphrase", False)

    def _getArgsAsStr(self):
        retval = F11_PartData._getArgsAsStr(self)

        if self.encrypted and self.escrowcert != "":
            retval += " --escrowcert=\"%s\"" % self.escrowcert

            if self.backuppassphrase:
                retval += " --backuppassphrase"

        return retval

class RHEL6_PartData(F12_PartData):
    removedKeywords = F12_PartData.removedKeywords
    removedAttrs = F12_PartData.removedAttrs

    def __init__(self, *args, **kwargs):
        F12_PartData.__init__(self, *args, **kwargs)

        self.cipher = kwargs.get("cipher", "")
        self.hibernation = kwargs.get("hibernation", False)

    def _getArgsAsStr(self):
        retval = F12_PartData._getArgsAsStr(self)

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher
        if self.hibernation:
            retval += " --hibernation"

        return retval

F14_PartData = F12_PartData

class F17_PartData(F14_PartData):
    def __init__(self, *args, **kwargs):
        F14_PartData.__init__(self, *args, **kwargs)

        self.resize = kwargs.get("resize", False)

    def _getArgsAsStr(self):
        retval = F14_PartData._getArgsAsStr(self)

        if self.resize:
            retval += " --resize"

        return retval

class F18_PartData(F17_PartData):
    def __init__(self, *args, **kwargs):
        F17_PartData.__init__(self, *args, **kwargs)

        self.hibernation = kwargs.get("hibernation", False)
        self.cipher = kwargs.get("cipher", "")

    def _getArgsAsStr(self):
        retval = F17_PartData._getArgsAsStr(self)

        if self.hibernation:
            retval += " --hibernation"

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher

        return retval

class RHEL7_PartData(F18_PartData):
    def __init__(self, *args, **kwargs):
        F18_PartData.__init__(self, *args, **kwargs)

        self.mkfsopts = kwargs.get("mkfsoptions", "")

    def _getArgsAsStr(self):
        retval = F18_PartData._getArgsAsStr(self)

        if self.mkfsopts != "":
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

class FC3_Partition(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=130, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.partitions = kwargs.get("partitions", [])

    def __str__(self):
        retval = ""

        for part in self.partitions:
            retval += part.__str__()

        if retval != "":
            return "# Disk partitioning information\n" + retval
        else:
            return ""

    def _getParser(self):
        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

        op = KSOptionParser()
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
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "partition"))

        pd = self.handler.PartData()
        self._setToObj(self.op, opts, pd)
        pd.lineno = self.lineno
        pd.mountpoint=extra[0]

        # Check for duplicates in the data list.
        if pd in self.dataList():
            warnings.warn(_("A partition with the mountpoint %s has already been defined.") % pd.mountpoint)

        return pd

    def dataList(self):
        return self.partitions

class FC4_Partition(FC3_Partition):
    removedKeywords = FC3_Partition.removedKeywords
    removedAttrs = FC3_Partition.removedAttrs

    def __init__(self, writePriority=130, *args, **kwargs):
        FC3_Partition.__init__(self, writePriority, *args, **kwargs)

        # pylint: disable=unused-variable
        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

    def _getParser(self):
        op = FC3_Partition._getParser(self)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        op.add_option("--label", dest="label")
        return op

class RHEL5_Partition(FC4_Partition):
    removedKeywords = FC4_Partition.removedKeywords
    removedAttrs = FC4_Partition.removedAttrs

    def __init__(self, writePriority=130, *args, **kwargs):
        FC4_Partition.__init__(self, writePriority, *args, **kwargs)

        # pylint: disable=unused-variable
        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

    def _getParser(self):
        op = FC4_Partition._getParser(self)
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

class F9_Partition(FC4_Partition):
    removedKeywords = FC4_Partition.removedKeywords
    removedAttrs = FC4_Partition.removedAttrs

    def __init__(self, writePriority=130, *args, **kwargs):
        FC4_Partition.__init__(self, writePriority, *args, **kwargs)

        # pylint: disable=unused-variable
        def part_cb (option, opt_str, value, parser):
            if value.startswith("/dev/"):
                parser.values.ensure_value(option.dest, value[5:])
            else:
                parser.values.ensure_value(option.dest, value)

    def _getParser(self):
        op = FC4_Partition._getParser(self)
        op.add_option("--bytes-per-inode", deprecated=1)
        op.add_option("--fsprofile")
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

class F11_Partition(F9_Partition):
    removedKeywords = F9_Partition.removedKeywords
    removedAttrs = F9_Partition.removedAttrs

    def _getParser(self):
        op = F9_Partition._getParser(self)
        op.add_option("--start", deprecated=1)
        op.add_option("--end", deprecated=1)
        return op

class F12_Partition(F11_Partition):
    removedKeywords = F11_Partition.removedKeywords
    removedAttrs = F11_Partition.removedAttrs

    def _getParser(self):
        op = F11_Partition._getParser(self)
        op.add_option("--escrowcert")
        op.add_option("--backuppassphrase", action="store_true", default=False)
        return op

class RHEL6_Partition(F12_Partition):
    removedKeywords = F12_Partition.removedKeywords
    removedAttrs = F12_Partition.removedAttrs

    def _getParser(self):
        op = F12_Partition._getParser(self)
        op.add_option("--cipher")
        op.add_option("--hibernation", dest="hibernation", action="store_true",
                        default=False)
        return op

    def parse(self, args):
        # first call the overriden command
        retval = F12_Partition.parse(self, args)
        # the part command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The part/partition and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        return retval

class F14_Partition(F12_Partition):
    removedKeywords = F12_Partition.removedKeywords
    removedAttrs = F12_Partition.removedAttrs

    def _getParser(self):
        op = F12_Partition._getParser(self)
        op.remove_option("--bytes-per-inode")
        op.remove_option("--start")
        op.remove_option("--end")
        return op

class F17_Partition(F14_Partition):
    def _getParser(self):
        op = F14_Partition._getParser(self)
        op.add_option("--resize", action="store_true", default=False)
        return op

    def parse(self, args):
        retval = F14_Partition.parse(self, args)

        if retval.resize and not retval.onPart:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize can only be used in conjunction with --onpart")))

        if retval.resize and not retval.size:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize requires --size to specify new size")))

        return retval

class F18_Partition(F17_Partition):
    def _getParser(self):
        op = F17_Partition._getParser(self)
        op.add_option("--hibernation", dest="hibernation", action="store_true", default=False)
        op.add_option("--cipher")

        return op

class F20_Partition(F18_Partition):
    def parse(self, args):
        # first call the overriden command
        retval = F18_Partition.parse(self, args)
        # the part command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The part/partition and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The part/partition and mount commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        # when using tmpfs, grow is not suported
        if retval.fstype == "tmpfs":
            if retval.grow or retval.maxSizeMB != 0:
                errorMsg = _("The --fstype=tmpfs option can't be used together with --grow or --maxsize")
                raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg)) 

        return retval

class RHEL7_Partition(F20_Partition):
    removedKeywords = F20_Partition.removedKeywords
    removedAttrs = F20_Partition.removedAttrs

    def _getParser(self):
        op = F20_Partition._getParser(self)
        op.add_option("--mkfsoptions", dest="mkfsopts")

        return op

    def parse(self, args):
        retval = F20_Partition.parse(self, args)

        if not retval.format and retval.mkfsopts:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions with --noformat has no effect.")))

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions and --fsprofile cannot be used together.")))

        return retval
