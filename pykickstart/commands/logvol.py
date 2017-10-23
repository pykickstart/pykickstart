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

class FC3_LogVolData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.fstype = kwargs.get("fstype", "")
        self.grow = kwargs.get("grow", False)
        self.maxSizeMB = kwargs.get("maxSizeMB", 0)
        self.name = kwargs.get("name", "")
        self.format = kwargs.get("format", True)
        self.percent = kwargs.get("percent", 0)
        self.recommended = kwargs.get("recommended", False)
        self.size = kwargs.get("size", None)
        self.preexist = kwargs.get("preexist", False)
        self.vgname = kwargs.get("vgname", "")
        self.mountpoint = kwargs.get("mountpoint", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.vgname == y.vgname and self.name == y.name

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

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

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "logvol %s %s --name=%s --vgname=%s\n" % (self.mountpoint, self._getArgsAsStr(), self.name, self.vgname)
        return retval

class FC4_LogVolData(FC3_LogVolData):
    removedKeywords = FC3_LogVolData.removedKeywords
    removedAttrs = FC3_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_LogVolData.__init__(self, *args, **kwargs)
        self.bytesPerInode = kwargs.get("bytesPerInode", 4096)
        self.fsopts = kwargs.get("fsopts", "")

    def _getArgsAsStr(self):
        retval = FC3_LogVolData._getArgsAsStr(self)

        if hasattr(self, "bytesPerInode") and self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode
        if self.fsopts != "":
            retval += " --fsoptions=\"%s\"" % self.fsopts

        return retval

class RHEL5_LogVolData(FC4_LogVolData):
    removedKeywords = FC4_LogVolData.removedKeywords
    removedAttrs = FC4_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC4_LogVolData.__init__(self, *args, **kwargs)
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = FC4_LogVolData._getArgsAsStr(self)

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F9_LogVolData(FC4_LogVolData):
    removedKeywords = FC4_LogVolData.removedKeywords + ["bytesPerInode"]
    removedAttrs = FC4_LogVolData.removedAttrs + ["bytesPerInode"]

    def __init__(self, *args, **kwargs):
        FC4_LogVolData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.fsopts = kwargs.get("fsopts", "")
        self.fsprofile = kwargs.get("fsprofile", "")
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = FC4_LogVolData._getArgsAsStr(self)

        if self.fsprofile != "":
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F12_LogVolData(F9_LogVolData):
    removedKeywords = F9_LogVolData.removedKeywords
    removedAttrs = F9_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F9_LogVolData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.escrowcert = kwargs.get("escrowcert", "")
        self.backuppassphrase = kwargs.get("backuppassphrase", False)

    def _getArgsAsStr(self):
        retval = F9_LogVolData._getArgsAsStr(self)

        if self.encrypted and self.escrowcert != "":
            retval += " --escrowcert=\"%s\"" % self.escrowcert

            if self.backuppassphrase:
                retval += " --backuppassphrase"

        return retval

class RHEL6_LogVolData(F12_LogVolData):
    removedKeywords = F12_LogVolData.removedKeywords
    removedAttrs = F12_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F12_LogVolData.__init__(self, *args, **kwargs)

        self.cipher = kwargs.get("cipher", "")
        self.hibernation = kwargs.get("hibernation", False)

    def _getArgsAsStr(self):
        retval = F12_LogVolData._getArgsAsStr(self)

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher
        if self.hibernation:
            retval += " --hibernation"

        return retval

F14_LogVolData = F12_LogVolData

class F15_LogVolData(F14_LogVolData):
    removedKeywords = F14_LogVolData.removedKeywords
    removedAttrs = F14_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_LogVolData.__init__(self, *args, **kwargs)
        self.label = kwargs.get("label", "")

    def _getArgsAsStr(self):
        retval = F14_LogVolData._getArgsAsStr(self)

        if self.label != "":
            retval += " --label=\"%s\"" % self.label

        return retval

class F17_LogVolData(F15_LogVolData):
    def __init__(self, *args, **kwargs):
        F15_LogVolData.__init__(self, *args, **kwargs)
        self.resize = kwargs.get("resize", False)

    def _getArgsAsStr(self):
        retval = F15_LogVolData._getArgsAsStr(self)
        if self.resize:
            retval += " --resize"

        return retval

class F18_LogVolData(F17_LogVolData):
    def __init__(self, *args, **kwargs):
        F17_LogVolData.__init__(self, *args, **kwargs)
        self.hibernation = kwargs.get("hibernation", False)
        self.cipher = kwargs.get("cipher", "")

    def _getArgsAsStr(self):
        retval = F17_LogVolData._getArgsAsStr(self)

        if self.hibernation:
            retval += " --hibernation"

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher

        return retval

class F20_LogVolData(F18_LogVolData):
    def __init__(self, *args, **kwargs):
        F18_LogVolData.__init__(self, *args, **kwargs)
        self.thin_pool = kwargs.get("thin_pool", False)
        self.thin_volume = kwargs.get("thin_volume", False)
        self.pool_name = kwargs.get("pool_name", "")

        # these are only for thin pools
        self.chunk_size = kwargs.get("chunk_size", None)        # kilobytes
        self.metadata_size = kwargs.get("metadata_size", None)  # megabytes

    def _getArgsAsStr(self):
        retval = F18_LogVolData._getArgsAsStr(self)

        if self.thin_pool:
            retval += " --thinpool"

            if self.metadata_size:
                retval += " --metadatasize=%d" % self.metadata_size

            if self.chunk_size:
                retval += " --chunksize=%d" % self.chunk_size

        if self.thin_volume:
            retval += " --thin --poolname=%s" % self.pool_name

        return retval

class F21_LogVolData(F20_LogVolData):
    def __init__(self, *args, **kwargs):
        F20_LogVolData.__init__(self, *args, **kwargs)
        self.profile = kwargs.get("profile", "")

    def _getArgsAsStr(self):
        retval = F20_LogVolData._getArgsAsStr(self)

        if self.profile:
            retval += "--profile=%s" % self.profile

        return retval

class RHEL7_LogVolData(F21_LogVolData):
    removedKeywords = F21_LogVolData.removedKeywords
    removedAttrs = F21_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_LogVolData.__init__(self, *args, **kwargs)
        self.mkfsopts = kwargs.get("mkfsoptions", "")
        self.cache_size = kwargs.get("cache_size", 0)
        self.cache_mode = kwargs.get("cache_mode", "")
        self.cache_pvs = kwargs.get("cache_pvs", [])

    def _getArgsAsStr(self):
        retval = F21_LogVolData._getArgsAsStr(self)

        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        if self.cache_size:
            retval += " --cachesize=%d" % self.cache_size
        if self.cache_pvs:
            retval += " --cachepvs=%s" % ",".join(self.cache_pvs)
        if self.cache_mode:
            retval += " --cachemode=%s" % self.cache_mode

        return retval

class FC3_LogVol(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=133, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.lvList = kwargs.get("lvList", [])

    def __str__(self):
        retval = ""

        for part in self.lvList:
            retval += part.__str__()

        return retval

    def _getParser(self):
        def lv_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        op = KSOptionParser()
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
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) == 0:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "logvol"))

        lvd = self.handler.LogVolData()
        self._setToObj(self.op, opts, lvd)
        lvd.lineno = self.lineno
        lvd.mountpoint=extra[0]

        # Check for duplicates in the data list.
        if lvd in self.dataList():
            warnings.warn(_("A logical volume with the name %s has already been defined in volume group %s.") % (lvd.name, lvd.vgname))

        return lvd

    def dataList(self):
        return self.lvList

class FC4_LogVol(FC3_LogVol):
    removedKeywords = FC3_LogVol.removedKeywords
    removedAttrs = FC3_LogVol.removedAttrs

    def _getParser(self):
        op = FC3_LogVol._getParser(self)
        op.add_option("--bytes-per-inode", dest="bytesPerInode", action="store",
                      type="int", nargs=1)
        op.add_option("--fsoptions", dest="fsopts")
        return op

class RHEL5_LogVol(FC4_LogVol):
    removedKeywords = FC4_LogVol.removedKeywords
    removedAttrs = FC4_LogVol.removedAttrs

    def _getParser(self):
        op = FC4_LogVol._getParser(self)
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

class F9_LogVol(FC4_LogVol):
    removedKeywords = FC4_LogVol.removedKeywords
    removedAttrs = FC4_LogVol.removedAttrs

    def _getParser(self):
        op = FC4_LogVol._getParser(self)
        op.add_option("--bytes-per-inode", deprecated=1)
        op.add_option("--fsprofile", dest="fsprofile", action="store",
                      type="string", nargs=1)
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

class F12_LogVol(F9_LogVol):
    removedKeywords = F9_LogVol.removedKeywords
    removedAttrs = F9_LogVol.removedAttrs

    def _getParser(self):
        op = F9_LogVol._getParser(self)
        op.add_option("--escrowcert")
        op.add_option("--backuppassphrase", action="store_true", default=False)
        return op

class RHEL6_LogVol(F12_LogVol):
    removedKeywords = F12_LogVol.removedKeywords
    removedAttrs = F12_LogVol.removedAttrs

    def _getParser(self):
        op = F12_LogVol._getParser(self)
        op.add_option("--cipher")
        op.add_option("--hibernation", dest="hibernation", action="store_true",
                        default=False)

        return op

    def parse(self, args):
        # call the overriden method
        retval = F12_LogVol.parse(self, args)
        # the logvol command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The logvol and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        return retval

class F14_LogVol(F12_LogVol):
    removedKeywords = F12_LogVol.removedKeywords
    removedAttrs = F12_LogVol.removedAttrs

    def _getParser(self):
        op = F12_LogVol._getParser(self)
        op.remove_option("--bytes-per-inode")
        return op

class F15_LogVol(F14_LogVol):
    removedKeywords = F14_LogVol.removedKeywords
    removedAttrs = F14_LogVol.removedAttrs

    def _getParser(self):
        op = F14_LogVol._getParser(self)
        op.add_option("--label")
        return op

class F17_LogVol(F15_LogVol):
    def _getParser(self):
        op = F15_LogVol._getParser(self)
        op.add_option("--resize", action="store_true", default=False)
        return op

    def parse(self, args):
        retval = F15_LogVol.parse(self, args)

        if retval.resize and not retval.preexist:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize can only be used in conjunction with --useexisting")))

        if retval.resize and not retval.size:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize requires --size to indicate new size")))

        return retval

class F18_LogVol(F17_LogVol):
    def _getParser(self):
        op = F17_LogVol._getParser(self)
        op.add_option("--hibernation", action="store_true", default=False)
        op.add_option("--cipher")
        return op

class F20_LogVol(F18_LogVol):
    def _getParser(self):
        op = F18_LogVol._getParser(self)
        op.add_option("--thinpool", action="store_true", dest="thin_pool",
                      default=False)
        op.add_option("--thin", action="store_true", dest="thin_volume",
                      default=False)
        op.add_option("--poolname", dest="pool_name")
        op.add_option("--chunksize", type="int", dest="chunk_size")
        op.add_option("--metadatasize", type="int", dest="metadata_size")
        return op

    def parse(self, args):
        retval = F18_LogVol.parse(self, args)

        if retval.thin_volume and retval.thin_pool:
            err = formatErrorMsg(self.lineno,
                                 msg=_("--thin and --thinpool cannot both be "
                                       "specified for the same logvol"))
            raise KickstartParseError(err)

        if retval.thin_volume and not retval.pool_name:
            err = formatErrorMsg(self.lineno,
                                 msg=_("--thin requires --poolname to specify "
                                       "pool name"))
            raise KickstartParseError(err)

        if (retval.chunk_size or retval.metadata_size) and \
           not retval.thin_pool:
            err = formatErrorMsg(self.lineno,
                                 msg=_("--chunksize and --metadatasize are "
                                       "for thin pools only"))
            raise KickstartParseError(err)

        # the logvol command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The logvol and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The logvol and mount commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if not retval.preexist and not retval.percent and not retval.size and not retval.recommended:
            errorMsg = _("Size required")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if retval.percent is not None and (retval.percent < 0 or retval.percent > 100):
            errorMsg = _("Percentage must be between 0 and 100.")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=errorMsg))

        return retval

class F21_LogVol(F20_LogVol):
    def _getParser(self):
        op = F20_LogVol._getParser(self)
        op.add_option("--profile")

        return op

    def parse(self, args):
        retval = F20_LogVol.parse(self, args)

        if retval.size and retval.percent:
            err = formatErrorMsg(self.lineno,
                                 msg=_("--size and --percent cannot both be "
                                       "specified for the same logvol"))
            raise KickstartParseError(err)

        return retval

class RHEL7_LogVol(F21_LogVol):
    removedKeywords = F21_LogVol.removedKeywords
    removedAttrs = F21_LogVol.removedAttrs

    def _getParser(self):
        def pvs_cb(option, opt_str, value, parser):
            for pv in value.split(","):
                if pv:
                    parser.values.ensure_value(option.dest, list()).append(pv)

        op = F21_LogVol._getParser(self)
        op.add_option("--mkfsoptions", dest="mkfsopts")
        op.add_option("--cachesize", type="int", dest="cache_size")
        op.add_option("--cachemode", type="string", action="store", nargs=1, dest="cache_mode")
        op.add_option("--cachepvs", dest="cache_pvs", action="callback",
                      callback=pvs_cb, nargs=1, type="string")

        return op

    def parse(self, args):
        retval = F21_LogVol.parse(self, args)

        if not retval.format and retval.mkfsopts:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions with --noformat has no effect.")))

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions and --fsprofile cannot be used together.")))

        if retval.cache_size or retval.cache_mode or retval.cache_pvs:
            if retval.preexist:
                err = formatErrorMsg(self.lineno, msg=_("Adding a cache to an existing logical volume is not supported"))
                raise KickstartParseError(err)

            if retval.thin_volume:
                err = formatErrorMsg(self.lineno, msg=_("Thin volumes cannot be cached"))
                raise KickstartParseError(err)

            if not retval.cache_pvs:
                err = formatErrorMsg(self.lineno, msg=_("Cache needs to have a list of (fast) PVs specified"))
                raise KickstartParseError(err)

            if not retval.cache_size:
                err = formatErrorMsg(self.lineno, msg=_("Cache needs to have size specified"))
                raise KickstartParseError(err)

            if retval.cache_mode and retval.cache_mode not in ("writeback", "writethrough"):
                err = formatErrorMsg(self.lineno, msg=_("Invalid cache mode given: %s") % retval.cache_mode)
                raise KickstartParseError(err)

        return retval
