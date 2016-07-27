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
from pykickstart.version import FC3, FC4, F9, F12, F14, F15, F17, F18, F20, F21
from pykickstart.version import F23, RHEL5, RHEL6, RHEL7
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser, commaSplit

import warnings
from pykickstart.i18n import _

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

        if self.fstype:
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
        if self.size is not None and self.size > 0:
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
        if self.fsopts:
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

            if self.passphrase:
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

        if self.fsprofile:
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase:
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

        if self.encrypted and self.escrowcert:
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

        self.thin_pool = kwargs.get("thin_pool", False)
        self.thin_volume = kwargs.get("thin_volume", False)
        self.pool_name = kwargs.get("pool_name", "")
        self.chunk_size = kwargs.get("chunk_size", None)        # kilobytes
        self.metadata_size = kwargs.get("metadata_size", None)  # megabytes
        self.profile = kwargs.get("profile", "")

    def _getArgsAsStr(self):
        retval = F12_LogVolData._getArgsAsStr(self)

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher
        if self.hibernation:
            retval += " --hibernation"

        # these are only for thin pools
        if self.thin_pool:
            retval += " --thinpool"

            if self.metadata_size:
                retval += " --metadatasize=%d" % self.metadata_size

            if self.chunk_size:
                retval += " --chunksize=%d" % self.chunk_size

        if self.thin_volume:
            retval += " --thin --poolname=%s" % self.pool_name

        if self.profile:
            retval += " --profile=%s" % self.profile

        return retval

class F14_LogVolData(F12_LogVolData):
    pass

class F15_LogVolData(F14_LogVolData):
    removedKeywords = F14_LogVolData.removedKeywords
    removedAttrs = F14_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_LogVolData.__init__(self, *args, **kwargs)
        self.label = kwargs.get("label", "")

    def _getArgsAsStr(self):
        retval = F14_LogVolData._getArgsAsStr(self)

        if self.label:
            retval += " --label=\"%s\"" % self.label

        return retval

class F17_LogVolData(F15_LogVolData):
    removedKeywords = F15_LogVolData.removedKeywords
    removedAttrs = F15_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F15_LogVolData.__init__(self, *args, **kwargs)
        self.resize = kwargs.get("resize", False)

    def _getArgsAsStr(self):
        retval = F15_LogVolData._getArgsAsStr(self)
        if self.resize:
            retval += " --resize"

        return retval

class F18_LogVolData(F17_LogVolData):
    removedKeywords = F17_LogVolData.removedKeywords
    removedAttrs = F17_LogVolData.removedAttrs

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
    removedKeywords = F18_LogVolData.removedKeywords
    removedAttrs = F18_LogVolData.removedAttrs

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
    removedKeywords = F20_LogVolData.removedKeywords
    removedAttrs = F20_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F20_LogVolData.__init__(self, *args, **kwargs)
        self.profile = kwargs.get("profile", "")

    def _getArgsAsStr(self):
        retval = F20_LogVolData._getArgsAsStr(self)

        if self.profile:
            retval += " --profile=%s" % self.profile

        return retval

class RHEL7_LogVolData(F21_LogVolData):
    removedKeywords = F21_LogVolData.removedKeywords
    removedAttrs = F21_LogVolData.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_LogVolData.__init__(self, *args, **kwargs)
        self.mkfsopts = kwargs.get("mkfsoptions", "") or kwargs.get("mkfsopts", "")

    def _getArgsAsStr(self):
        retval = F21_LogVolData._getArgsAsStr(self)

        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

class F23_LogVolData(F21_LogVolData):
    def __init__(self, *args, **kwargs):
        F21_LogVolData.__init__(self, *args, **kwargs)
        self.cache_size = kwargs.get("cache_size", 0)
        self.cache_mode = kwargs.get("cache_mode", "")
        self.cache_pvs = kwargs.get("cache_pvs", [])
        self.mkfsopts = kwargs.get("mkfsoptions", "") or kwargs.get("mkfsopts", "")

    def _getArgsAsStr(self):
        retval = F21_LogVolData._getArgsAsStr(self)

        if self.cache_size:
            retval += " --cachesize=%d" % self.cache_size
        if self.cache_pvs:
            retval += " --cachepvs=%s" % ",".join(self.cache_pvs)
        if self.cache_mode:
            retval += " --cachemode=%s" % self.cache_mode
        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

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
        op = KSOptionParser(prog="logvol", description="""
                            Create a logical volume for Logical Volume Management
                            (LVM).""", version=FC3, epilog="""
                            Create the partition first, create the logical volume
                            group, and then create the logical volume. For example::

                                part pv.01 --size 3000
                                volgroup myvg pv.01
                                logvol / --vgname=myvg --size=2000 --name=rootvol
                            """)
        op.add_argument("mntpoint", metavar="<mntpoint>", nargs=1, version=FC3,
                        help="Mountpoint for this logical volume or 'none'.")
        op.add_argument("--fstype", version=FC3, help="""
                        Sets the file system type for the logical volume. Valid
                        values include ext4, ext3, ext2, btrfs, swap, and vfat.
                        Other filesystems may be valid depending on command line
                        arguments passed to Anaconda to enable other filesystems.
                        """)
        op.add_argument("--grow", action="store_true", default=False,
                        version=FC3, help="""
                        Tells the logical volume to grow to fill available space
                        (if any), or up to the maximum size setting. Note that
                        --grow is not supported for logical volumes containing
                        a RAID volume on top of them.""")
        op.add_argument("--maxsize", dest="maxSizeMB", type=int,
                        version=FC3, help="""
                        The maximum size in MiB the logical volume may grow to.
                        Specify an integer value here, and do not append any
                        units.  This option is only relevant if ``--grow`` is
                        specified as well.""")
        op.add_argument("--name", required=True, version=FC3, help="""
                        The name of this logical volume.""")
        op.add_argument("--noformat", action="store_false", version=FC3,
                        dest="format", default=True, help="""
                        Use an existing logical volume and do not format it.
                        """)
        op.add_argument("--percent", dest="percent", type=int,
                        version=FC3, help="""
                        Specify the size of the logical volume as a percentage
                        of available space in the volume group. Without the above
                        --grow option, this may not work.""")
        op.add_argument("--recommended", action="store_true", default=False,
                        version=FC3, help="""
                        Determine the size of the logical volume automatically.
                        """)
        op.add_argument("--size", type=int, version=FC3, help="""
                        Size of this logical volume.""")
        op.add_argument("--useexisting", dest="preexist", version=FC3,
                        action="store_true", default=False,
                        help="Use an existing logical volume and reformat it.")
        op.add_argument("--vgname", required=True, version=FC3, help="""
                        Name of the Volume Group this logical volume belongs to.
                        """)
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(ns.mntpoint) != 1:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Mount point required for %s") % "logvol"))
        elif len(extra) > 0:
            mapping = {"command": "logvol", "options": extra}
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

        lvd = self.dataClass()  # pylint: disable=not-callable
        self.set_to_obj(ns, lvd)
        lvd.lineno = self.lineno
        lvd.mountpoint = ns.mntpoint[0]

        if not lvd.format:
            lvd.preexist = True

        # Check for duplicates in the data list.
        if lvd in self.dataList():
            warnings.warn(_("A logical volume with the name %(logical_volume_name)s has already been defined in volume group %(volume_group)s.") % {"logical_volume_name": lvd.name, "volume_group": lvd.vgname})

        return lvd

    def dataList(self):
        return self.lvList

    @property
    def dataClass(self):
        return self.handler.LogVolData

class FC4_LogVol(FC3_LogVol):
    removedKeywords = FC3_LogVol.removedKeywords
    removedAttrs = FC3_LogVol.removedAttrs

    def _getParser(self):
        op = FC3_LogVol._getParser(self)
        op.add_argument("--bytes-per-inode", dest="bytesPerInode", type=int,
                        version=FC4, help="Specify the bytes/inode ratio.")
        op.add_argument("--fsoptions", dest="fsopts", version=FC4, help="""
                        Specifies a free form string of options to be used when
                        mounting the filesystem. This string will be copied into
                        the /etc/fstab file of the installed system and should
                        be enclosed in quotes.""")
        return op

class RHEL5_LogVol(FC4_LogVol):
    removedKeywords = FC4_LogVol.removedKeywords
    removedAttrs = FC4_LogVol.removedAttrs

    def _getParser(self):
        op = FC4_LogVol._getParser(self)
        op.add_argument("--encrypted", action="store_true", version=RHEL5,
                        default=False, help="""
                        Specify that this logical volume should be encrypted.
                        """)
        op.add_argument("--passphrase", version=RHEL5, help="""
                        Specify the passphrase to use when encrypting this
                        logical volume. Without the above ``--encrypted``
                        option, this option does nothing. If no passphrase is
                        specified, the default system-wide one is used, or the
                        installer will stop and prompt if there is no default.
                        """)
        return op

class F9_LogVol(FC4_LogVol):
    removedKeywords = FC4_LogVol.removedKeywords
    removedAttrs = FC4_LogVol.removedAttrs

    def _getParser(self):
        op = FC4_LogVol._getParser(self)
        op.add_argument("--bytes-per-inode", deprecated=F9)
        op.add_argument("--fsprofile", version=F9, help="""
                        Specifies a usage type to be passed to the program that
                        makes a filesystem on this partition. A usage type
                        defines a variety of tuning parameters to be used when
                        making a filesystem. For this option to work, the
                        filesystem must support the concept of usage types and
                        there must be a configuration file that lists valid
                        types. For ext2/3/4, this configuration file is
                        ``/etc/mke2fs.conf``.""")
        op.add_argument("--encrypted", action="store_true", default=False,
                        version=F9, help="""
                        Specify that this logical volume should be encrypted.
                        """)
        op.add_argument("--passphrase", version=F9, help="""
                        Specify the passphrase to use when encrypting this
                        logical volume. Without the above ``--encrypted``
                        option, this option does nothing. If no passphrase is
                        specified, the default system-wide one is used, or the
                        installer will stop and prompt if there is no default.
                        """)
        return op

class F12_LogVol(F9_LogVol):
    removedKeywords = F9_LogVol.removedKeywords
    removedAttrs = F9_LogVol.removedAttrs

    def _getParser(self):
        op = F9_LogVol._getParser(self)
        op.add_argument("--escrowcert", metavar="<url>", version=F12, help="""
                        Load an X.509 certificate from ``<url>``. Store the data
                        encryption key of this logical volume, encrypted using
                        the certificate, as a file in ``/root``. Only relevant
                        if ``--encrypted`` is specified as well.""")
        op.add_argument("--backuppassphrase", action="store_true", version=F12,
                        default=False, help="""
                        Only relevant if ``--escrowcert`` is specified as well.
                        In addition to storing the data encryption key, generate
                        a random passphrase and add it to this logical volume.
                        Then store the passphrase, encrypted using the certificate
                        specified by ``--escrowcert``, as a file in ``/root``. If
                        more than one LUKS volume uses ``--backuppassphrase``,
                        the same passphrase will be used for all such volumes.
                        """)
        return op

class RHEL6_LogVol(F12_LogVol):
    removedKeywords = F12_LogVol.removedKeywords
    removedAttrs = F12_LogVol.removedAttrs

    def _getParser(self):
        op = F12_LogVol._getParser(self)
        op.add_argument("--cipher", version=RHEL6, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        op.add_argument("--hibernation", action="store_true", default=False,
                        version=RHEL6, help="""
                        This option can be used to automatically determine the
                        size of the swap partition big enough for hibernation.
                        """)
        op.add_argument("--thinpool", action="store_true", version=RHEL6,
                        dest="thin_pool", default=False, help="""
                        Create a thin pool logical volume. Use a mountpoint of
                        'none'""")
        op.add_argument("--thin", action="store_true", version=RHEL6,
                        dest="thin_volume", default=False, help="""
                        Create a thin logical volume. Requires ``--poolname``.
                        """)
        op.add_argument("--poolname", dest="pool_name", version=RHEL6, help="""
                        Specify the name of the thin pool in which to create a
                        thin logical volume. Requires ``--thin``.""")
        op.add_argument("--chunksize", type=int, dest="chunk_size",
                        version=RHEL6, help="""
                        Specify the chunk size (in KiB) for a new thin pool
                        device.""")
        op.add_argument("--metadatasize", type=int, dest="metadata_size",
                        version=RHEL6, help="""
                        Specify the metadata area size (in MiB) for a new thin
                        pool device.""")
        op.add_argument("--profile", version=RHEL6, help="""
                        Specify an LVM profile for the thin pool (see lvm(8),
                        standard profiles are 'default' and 'thin-performance'
                        defined in the /etc/lvm/profile/ directory).""")
        return op

    def parse(self, args):
        # call the overriden method
        retval = F12_LogVol.parse(self, args)
        # the logvol command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The logvol and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if retval.thin_volume and retval.thin_pool:
            errorMsg = _("--thin and --thinpool cannot both be specified for "
                         "the same logvol")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if retval.thin_volume and not retval.pool_name:
            errorMsg = _("--thin requires --poolname to specify pool name")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if (retval.chunk_size or retval.metadata_size) and \
           not retval.thin_pool:
            errorMsg = _("--chunksize and --metadatasize are for thin pools only")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        return retval

#todo: this also breaks inheritance
class F14_LogVol(F12_LogVol):
    removedKeywords = F12_LogVol.removedKeywords
    removedAttrs = F12_LogVol.removedAttrs

    def _getParser(self):
        op = F12_LogVol._getParser(self)
        op.remove_argument("--bytes-per-inode", version=F14)
        return op

class F15_LogVol(F14_LogVol):
    removedKeywords = F14_LogVol.removedKeywords
    removedAttrs = F14_LogVol.removedAttrs

    def _getParser(self):
        op = F14_LogVol._getParser(self)
        op.add_argument("--label", version=F15, help="""
                        Specify the label to give to the filesystem to be made.
                        If the given label is already in use by another
                        filesystem, a new label will be created.""")
        return op

class F17_LogVol(F15_LogVol):
    removedKeywords = F15_LogVol.removedKeywords
    removedAttrs = F15_LogVol.removedAttrs

    def _getParser(self):
        op = F15_LogVol._getParser(self)
        op.add_argument("--resize", action="store_true", default=False,
                        version=F17, help="""
                        Attempt to resize this logical volume to the size given
                        by ``--size=``. This option must be used with
                        ``--useexisting --size=``, or an error will be raised.
                        """)
        return op

    def parse(self, args):
        retval = F15_LogVol.parse(self, args)

        if retval.resize and not retval.preexist:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize can only be used in conjunction with --useexisting")))

        if retval.resize and not retval.size:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--resize requires --size to indicate new size")))

        return retval

class F18_LogVol(F17_LogVol):
    removedKeywords = F17_LogVol.removedKeywords
    removedAttrs = F17_LogVol.removedAttrs

    def _getParser(self):
        op = F17_LogVol._getParser(self)
        op.add_argument("--hibernation", action="store_true", default=False,
                        version=F18, help="""
                        This option can be used to automatically determine the
                        size of the swap partition big enough for hibernation.
                        """)

        op.add_argument("--cipher", version=F18, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        return op

class F20_LogVol(F18_LogVol):
    removedKeywords = F18_LogVol.removedKeywords
    removedAttrs = F18_LogVol.removedAttrs

    def _getParser(self):
        op = F18_LogVol._getParser(self)
        op.add_argument("--thinpool", action="store_true", version=F20,
                        dest="thin_pool", default=False, help="""
                        Create a thin pool logical volume. Use a mountpoint
                        of 'none'.""")
        op.add_argument("--thin", action="store_true", version=F20,
                        dest="thin_volume", default=False, help="""
                        Create a thin logical volume. Requires ``--poolname``.
                        """)
        op.add_argument("--poolname", dest="pool_name", version=F20, help="""
                        Specify the name of the thin pool in which to create a
                        thin logical volume. Requires ``--thin``.""")
        op.add_argument("--chunksize", type=int, dest="chunk_size",
                        version=F20, help="""
                        Specify the chunk size (in KiB) for a new thin pool
                        device.""")
        op.add_argument("--metadatasize", type=int, dest="metadata_size",
                        version=F20, help="""
                        Specify the metadata area size (in MiB) for a new thin
                        pool device.""")
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

        if not retval.preexist and not retval.percent and not retval.size and not retval.recommended:
            errorMsg = _("No size given for logical volume. Use one of --useexisting, --noformat, --size, or --percent.")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        if retval.percent is not None and (retval.percent < 0 or retval.percent > 100):
            errorMsg = _("Percentage must be between 0 and 100.")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        return retval

class F21_LogVol(F20_LogVol):
    removedKeywords = F20_LogVol.removedKeywords
    removedAttrs = F20_LogVol.removedAttrs

    def _getParser(self):
        op = F20_LogVol._getParser(self)
        op.add_argument("--profile", version=F21, help="""
                        Specify an LVM profile for the thin pool (see lvm(8),
                        standard profiles are 'default' and 'thin-performance'
                        defined in the /etc/lvm/profile/ directory).""")
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
        op = F21_LogVol._getParser(self)
        op.add_argument("--mkfsoptions", dest="mkfsopts", version=RHEL7, help="""
                        Specifies additional parameters to be passed to the
                        program that makes a filesystem on this partition. No
                        processing is done on the list of arguments, so they
                        must be supplied in a format that can be passed directly
                        to the mkfs program.  This means multiple options should
                        be comma-separated or surrounded by double quotes,
                        depending on the filesystem.""")
        return op

    def parse(self, args):
        retval = F21_LogVol.parse(self, args)

        if not retval.format and retval.mkfsopts:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions with --noformat has no effect.")))

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions and --fsprofile cannot be used together.")))

        return retval

# todo: another inheritance problem here
class F23_LogVol(F21_LogVol):
    def _getParser(self):
        op = F21_LogVol._getParser(self)
        op.add_argument("--cachesize", type=int, dest="cache_size",
                        version=F23, help="""
                        Requested size (in MiB) of cache attached to the logical
                        volume. Requires ``--cachepvs``.""")
        op.add_argument("--cachemode", dest="cache_mode", version=F23, help="""
                        Mode that should be used for the cache. Either
                        ``writeback`` or ``writethrough``.""")
        op.add_argument("--cachepvs", dest="cache_pvs", type=commaSplit,
                        version=F23, help="""
                        Comma-separated list of (fast) physical volumes that
                        should be used for the cache.""")
        op.add_argument("--mkfsoptions", dest="mkfsopts", version=F23, help="""
                        Specifies additional parameters to be passed to the
                        program that makes a filesystem on this partition. No
                        processing is done on the list of arguments, so they
                        must be supplied in a format that can be passed directly
                        to the mkfs program.  This means multiple options should
                        be comma-separated or surrounded by double quotes,
                        depending on the filesystem.""")
        return op

    def parse(self, args):
        retval = F21_LogVol.parse(self, args)

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

        if not retval.format and retval.mkfsopts:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions with --noformat has no effect.")))

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions and --fsprofile cannot be used together.")))

        return retval
