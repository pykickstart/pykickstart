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
from pykickstart.version import RHEL5, RHEL6, RHEL8, versionToLongString
from pykickstart.version import FC3, FC4, F9, F11, F12, F14, F17, F18, F23, F29
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser, mountpoint

import warnings
from pykickstart.i18n import _

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
        if self.fstype:
            retval += " --fstype=\"%s\"" % self.fstype
        if self.grow:
            retval += " --grow"
        if self.maxSizeMB > 0:
            retval += " --maxsize=%d" % self.maxSizeMB
        if not self.format:
            retval += " --noformat"
        if self.onbiosdisk:
            retval += " --onbiosdisk=%s" % self.onbiosdisk
        if self.disk:
            retval += " --ondisk=%s" % self.disk
        if self.onPart:
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
        if self.fsopts:
            retval += " --fsoptions=\"%s\"" % self.fsopts
        if self.label:
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

            if self.passphrase:
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

        if self.fsprofile:
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase:
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

        if self.encrypted and self.escrowcert:
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

class F14_PartData(F12_PartData):
    pass

class F17_PartData(F14_PartData):
    removedKeywords = F14_PartData.removedKeywords
    removedAttrs = F14_PartData.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_PartData.__init__(self, *args, **kwargs)

        self.resize = kwargs.get("resize", False)

    def _getArgsAsStr(self):
        retval = F14_PartData._getArgsAsStr(self)

        if self.resize:
            retval += " --resize"

        return retval

class F18_PartData(F17_PartData):
    removedKeywords = F17_PartData.removedKeywords
    removedAttrs = F17_PartData.removedAttrs

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

class F23_PartData(F18_PartData):
    def __init__(self, *args, **kwargs):
        F18_PartData.__init__(self, *args, **kwargs)

        self.mkfsopts = kwargs.get("mkfsoptions", "") or kwargs.get("mkfsopts", "")

    def _getArgsAsStr(self):
        retval = F18_PartData._getArgsAsStr(self)

        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

class RHEL7_PartData(F23_PartData):
    pass

class F29_PartData(F23_PartData):
    def __init__(self, *args, **kwargs):
        F23_PartData.__init__(self, *args, **kwargs)
        self.luks_version = kwargs.get("luks_version", "")
        self.pbkdf = kwargs.get("pbkdf", "")
        self.pbkdf_memory = kwargs.get("pbkdf_memory", 0)
        self.pbkdf_time = kwargs.get("pbkdf_time", 0)
        self.pbkdf_iterations = kwargs.get("pbkdf_iterations", 0)

    def _getArgsAsStr(self):
        retval = F23_PartData._getArgsAsStr(self)

        if self.encrypted and self.luks_version:
            retval += " --luks-version=%s" % self.luks_version

        if self.encrypted and self.pbkdf:
            retval += " --pbkdf=%s" % self.pbkdf

        if self.encrypted and self.pbkdf_memory:
            retval += " --pbkdf-memory=%s" % self.pbkdf_memory

        if self.encrypted and self.pbkdf_time:
            retval += " --pbkdf-time=%s" % self.pbkdf_time

        if self.encrypted and self.pbkdf_iterations:
            retval += " --pbkdf-iterations=%s" % self.pbkdf_iterations

        return retval

class RHEL8_PartData(F29_PartData):
    pass

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

        if retval:
            return "# Disk partitioning information\n" + retval
        else:
            return ""

    def _getParser(self):
        def part_cb(value):
            if value.startswith("/dev/"):
                return value[5:]
            else:
                return value

        op = KSOptionParser(prog="part|partition", description="""
                            Creates a partition on the system. This command is
                            required. All partitions created will be formatted
                            as part of the installation process unless
                            ``--noformat`` and ``--onpart`` are used.
                            """, epilog="""
                            If partitioning fails for any reason, diagnostic
                            messages will appear on virtual console 3.""",
                            version=FC3)
        op.add_argument("mntpoint", metavar="<mntpoint>", type=mountpoint, nargs=1,
                        version=FC3, help="""
                        The ``<mntpoint>`` is where the partition will be mounted
                        and must be of one of the following forms:

                        ``/<path>``

                        For example, ``/``, ``/usr``, ``/home``

                        ``swap``

                        The partition will be used as swap space.

                        ``raid.<id>``

                        The partition will be used for software RAID.
                        Refer to the ``raid`` command.

                        ``pv.<id>``

                        The partition will be used for LVM. Refer to the
                        ``logvol`` command.

                        ``btrfs.<id>``

                        The partition will be used for BTRFS volume. Rerefer to
                        the ``btrfs`` command.

                        ``biosboot``

                        The partition will be used for a BIOS Boot Partition. As
                        of Fedora 16 there must be a biosboot partition for the
                        bootloader to be successfully installed onto a disk that
                        contains a GPT/GUID partition table. Rerefer to the
                        ``bootloader`` command.
                        """)
        op.add_argument("--active", action="store_true", default=False,
                        version=FC3, help="Set partition as active")
        op.add_argument("--asprimary", dest="primOnly", action="store_true",
                        default=False, version=FC3, help="""
                        Forces automatic allocation of the partition as a primary
                        partition or the partitioning will fail.

                        **TIP:** The ``--asprimary`` option only makes sense
                        with the MBR partitioning scheme and is ignored when the
                        GPT partitioning scheme is used.""")
        op.add_argument("--start", type=int, version=FC3, help="REMOVED")
        op.add_argument("--end", type=int, version=FC3, help="REMOVED")
        op.add_argument("--fstype", "--type", dest="fstype", version=FC3,
                        help="""
                        Sets the file system type for the partition. Valid
                        values include ext4, ext3, ext2, xfs, btrfs, swap, and
                        vfat. Other filesystems may be valid depending on
                        command line arguments passed to anaconda to enable
                        other filesystems.""")
        op.add_argument("--grow", action="store_true", default=False,
                        version=FC3, help="""
                        Tells the partition to grow to fill available space
                        (if any), or up to the maximum size setting. Note that
                        ``--grow`` is not supported for partitions containing a
                        RAID volume on top of them.""")
        op.add_argument("--maxsize", dest="maxSizeMB", type=int,
                        version=FC3, help="""
                        The maximum size in MiB the partition may grow to.
                        Specify an integer value here, and do not append any
                        units. This option is only relevant if ``--grow`` is
                        specified as well.""")
        op.add_argument("--noformat", dest="format", version=FC3,
                        action="store_false", default=True, help="""
                        Tells the installation program not to format the
                        partition, for use with the ``--onpart`` command.""")
        op.add_argument("--onbiosdisk", version=FC3, help="""
                        Forces the partition to be created on a particular disk
                        as discovered by the BIOS.""")
        op.add_argument("--ondisk", "--ondrive", dest="disk",
                        version=FC3, help="""
                        Forces the partition to be created on a particular disk.
                        """)
        op.add_argument("--onpart", "--usepart", dest="onPart", type=part_cb,
                        version=FC3, help="""
                        Put the partition on an already existing device. Use
                        ``--onpart=LABEL=name`` or ``--onpart=UUID=name`` to specify
                        a partition by label or uuid respectively.

                        Anaconda may create partitions in any particular order,
                        so it is safer to use labels than absolute partition
                        names.""")
        op.add_argument("--recommended", action="store_true", default=False,
                        version=FC3, help="""
                        Determine the size of the partition automatically.
                        """)
        op.add_argument("--size", type=int, version=FC3, help="""
                        The minimum partition size in MiB. Specify an integer
                        value here and do not append any units.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        assert len(ns.mntpoint) == 1

        if extra:
            mapping = {"command": "partition", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        pd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, pd)
        pd.lineno = self.lineno
        pd.mountpoint = ns.mntpoint[0]

        # Check for duplicates in the data list.
        if pd.mountpoint != "swap" and pd in self.dataList():
            warnings.warn(_("A partition with the mountpoint %s has already been defined.") % pd.mountpoint, KickstartParseWarning)

        return pd

    def dataList(self):
        return self.partitions

    @property
    def dataClass(self):
        return self.handler.PartData

class FC4_Partition(FC3_Partition):
    removedKeywords = FC3_Partition.removedKeywords
    removedAttrs = FC3_Partition.removedAttrs

    def _getParser(self):
        op = FC3_Partition._getParser(self)
        op.add_argument("--bytes-per-inode", dest="bytesPerInode", type=int,
                        version=FC4, help="Specify the bytes/inode ratio.")
        op.add_argument("--fsoptions", dest="fsopts", version=FC4, help="""
                        Specifies a free form string of options to be used when
                        mounting the filesystem. This string will be copied into
                        the /etc/fstab file of the installed system and should
                        be enclosed in quotes.""")
        op.add_argument("--label", version=FC4, help="""
                        Specify the label to give to the filesystem to be made
                        on the partition. If the given label is already in use
                        by another filesystem, a new label will be created for
                        this partition.""")
        return op

class RHEL5_Partition(FC4_Partition):
    removedKeywords = FC4_Partition.removedKeywords
    removedAttrs = FC4_Partition.removedAttrs

    def _getParser(self):
        op = FC4_Partition._getParser(self)
        op.add_argument("--encrypted", action="store_true", version=RHEL5,
                        default=False, help="""
                        Specify that this partition should be encrypted.""")
        op.add_argument("--passphrase", version=RHEL5, help="""
                        Specify the passphrase to use when encrypting this
                        partition. Without the above --encrypted option, this
                        option does nothing. If no passphrase is specified, the
                        default system-wide one is used, or the installer will
                        stop and prompt if there is no default.""")
        return op

class F9_Partition(FC4_Partition):
    removedKeywords = FC4_Partition.removedKeywords
    removedAttrs = FC4_Partition.removedAttrs

    def _getParser(self):
        op = FC4_Partition._getParser(self)
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
        op.add_argument("--encrypted", action="store_true", version=F9,
                        default=False, help="""
                        Specify that this partition should be encrypted.""")
        op.add_argument("--passphrase", version=F9, help="""
                        Specify the passphrase to use when encrypting this
                        partition. Without the above --encrypted option, this
                        option does nothing. If no passphrase is specified, the
                        default system-wide one is used, or the installer will
                        stop and prompt if there is no default.""")
        return op

class F11_Partition(F9_Partition):
    removedKeywords = F9_Partition.removedKeywords
    removedAttrs = F9_Partition.removedAttrs

    def _getParser(self):
        op = F9_Partition._getParser(self)
        op.add_argument("--start", deprecated=F11)
        op.add_argument("--end", deprecated=F11)
        return op

class F12_Partition(F11_Partition):
    removedKeywords = F11_Partition.removedKeywords
    removedAttrs = F11_Partition.removedAttrs

    def _getParser(self):
        op = F11_Partition._getParser(self)
        op.add_argument("--escrowcert", metavar="<url>", version=F12, help="""
                        Load an X.509 certificate from ``<url>``. Store the
                        data encryption key of this partition, encrypted using
                        the certificate, as a file in ``/root``. Only relevant
                        if ``--encrypted`` is specified as well.""")
        op.add_argument("--backuppassphrase", action="store_true", version=F12,
                        default=False, help="""
                        Only relevant if ``--escrowcert`` is specified as well.
                        In addition to storing the data encryption key, generate
                        a random passphrase and add it to this partition. Then
                        store the passphrase, encrypted using the certificate
                        specified by ``--escrowcert``, as a file in ``/root``.
                        If more than one LUKS volume uses ``--backuppassphrase``,
                        the same passphrase will be used for all such volumes.
                        """)
        return op

class RHEL6_Partition(F12_Partition):
    removedKeywords = F12_Partition.removedKeywords
    removedAttrs = F12_Partition.removedAttrs

    def _getParser(self):
        op = F12_Partition._getParser(self)
        op.add_argument("--cipher", version=RHEL6, help="""
                        Only relevant if ``--encrypted`` is specified.
                        Specifies which encryption algorithm should be used to
                        encrypt the filesystem.""")
        op.add_argument("--hibernation", action="store_true", default=False,
                        version=RHEL6, help="""
                        This option can be used to automatically determine the
                        size of the swap partition big enough for hibernation.
                        """)
        return op

    def parse(self, args):
        # first call the overriden command
        retval = F12_Partition.parse(self, args)
        # the part command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The part/partition and autopart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval

class F14_Partition(F12_Partition):
    removedKeywords = F12_Partition.removedKeywords
    removedAttrs = F12_Partition.removedAttrs

    def _getParser(self):
        op = F12_Partition._getParser(self)
        op.remove_argument("--bytes-per-inode", version=F14)
        op.remove_argument("--start", version=F14)
        op.remove_argument("--end", version=F14)
        return op

class F17_Partition(F14_Partition):
    removedKeywords = F14_Partition.removedKeywords
    removedAttrs = F14_Partition.removedAttrs

    def _getParser(self):
        op = F14_Partition._getParser(self)
        op.add_argument("--resize", action="store_true", version=F17,
                        default=False, help="""
                        Attempt to resize this partition to the size given by
                        ``--size=``. This option must be used with
                        ``--onpart --size=``, or an error will be raised.""")
        return op

    def parse(self, args):
        retval = F14_Partition.parse(self, args)

        if retval.resize and not retval.onPart:
            raise KickstartParseError(_("--resize can only be used in conjunction with --onpart"), lineno=self.lineno)

        if retval.resize and not retval.size:
            raise KickstartParseError(_("--resize requires --size to specify new size"), lineno=self.lineno)

        return retval

class F18_Partition(F17_Partition):
    removedKeywords = F17_Partition.removedKeywords
    removedAttrs = F17_Partition.removedAttrs

    def _getParser(self):
        op = F17_Partition._getParser(self)
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

class F20_Partition(F18_Partition):
    removedKeywords = F18_Partition.removedKeywords
    removedAttrs = F18_Partition.removedAttrs

    def parse(self, args):
        # first call the overriden command
        retval = F18_Partition.parse(self, args)
        # the part command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The part/partition and autopart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The part/partition and mount commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)

        # when using tmpfs, grow is not suported
        if retval.fstype == "tmpfs":
            if retval.grow or retval.maxSizeMB != 0:
                errorMsg = _("The --fstype=tmpfs option can't be used together with --grow or --maxsize")
                raise KickstartParseError(errorMsg, lineno=self.lineno)

        return retval

class F23_Partition(F20_Partition):
    removedKeywords = F20_Partition.removedKeywords
    removedAttrs = F20_Partition.removedAttrs

    def _getParser(self):
        op = F20_Partition._getParser(self)
        op.add_argument("--mkfsoptions", dest="mkfsopts", version=F23, help="""
                        Specifies additional parameters to be passed to the
                        program that makes a filesystem on this partition. This
                        is similar to ``--fsprofile`` but works for all
                        filesystems, not just the ones that support the profile
                        concept. No processing is done on the list of arguments,
                        so they must be supplied in a format that can be passed
                        directly to the mkfs program. This means multiple
                        options should be comma-separated or surrounded by
                        double quotes, depending on the filesystem.""")
        return op

    def parse(self, args):
        retval = F20_Partition.parse(self, args)

        if not retval.format and retval.mkfsopts:
            raise KickstartParseError(_("--mkfsoptions with --noformat has no effect."), lineno=self.lineno)

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartParseError(_("--mkfsoptions and --fsprofile cannot be used together."), lineno=self.lineno)

        return retval

class RHEL7_Partition(F23_Partition):
    pass

class F29_Partition(F23_Partition):
    removedKeywords = F23_Partition.removedKeywords
    removedAttrs = F23_Partition.removedAttrs

    def _getParser(self):
        op = F23_Partition._getParser(self)
        op.add_argument("--active", action="store_true", default=False,
                        deprecated=F29, help="")
        op.add_argument("--luks-version", dest="luks_version", version=F29, default="",
                        help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which version of LUKS format should be used to encrypt
                        the filesystem.""")
        op.add_argument("--pbkdf", version=F29, default="", help="""
                        Only relevant if ``--encrypted`` is specified. Sets
                        Password-Based Key Derivation Function (PBKDF) algorithm
                        for LUKS keyslot. See ``man cryptsetup``.""")
        op.add_argument("--pbkdf-memory", dest="pbkdf_memory", type=int, default=0,
                        version=F29, help="""
                        Only relevant if ``--encrypted`` is specified. Sets
                        the memory cost for PBKDF. See ``man cryptsetup``.""")
        op.add_argument("--pbkdf-time", dest="pbkdf_time", type=int, default=0,
                        version=F29, help="""
                        Only relevant if ``--encrypted`` is specified. Sets
                        the number of milliseconds to spend with PBKDF passphrase
                        processing. See ``--iter-time`` in ``man cryptsetup``.

                        Only one of ``--pbkdf-time`` and ``--pbkdf-iterations``
                        can be specified.
                        """)
        op.add_argument("--pbkdf-iterations", dest="pbkdf_iterations", type=int, default=0,
                        version=F29, help="""
                        Only relevant if ``--encrypted`` is specified. Sets
                        the number of iterations directly and avoids PBKDF benchmark.
                        See ``--pbkdf-force-iterations`` in ``man cryptsetup``.

                        Only one of ``--pbkdf-time`` and ``--pbkdf-iterations``
                        can be specified.
                        """)
        return op

    def parse(self, args):
        retval = F23_Partition.parse(self, args)

        if retval.pbkdf_time and retval.pbkdf_iterations:
            msg = _("Only one of --pbkdf-time and --pbkdf-iterations can be specified.")
            raise KickstartParseError(msg, lineno=self.lineno)

        return retval

class RHEL8_Partition(F29_Partition):
    removedKeywords = F29_Partition.removedKeywords
    removedAttrs = F29_Partition.removedAttrs

    def parse(self, args):
        retval = F29_Partition.parse(self, args)
        if retval.mountpoint.startswith("btrfs.") or retval.fstype == "btrfs":
            raise KickstartParseError(_("Btrfs file system is not supported"), lineno=self.lineno)
        return retval

    def _getParser(self):
        "Only necessary for the type change documentation"
        op = F29_Partition._getParser(self)
        for action in op._actions:
            if "--fstype" in action.option_strings:
                action.help += """

                    .. versionchanged:: %s

                    Btrfs support was removed.""" % versionToLongString(RHEL8)
        return op
