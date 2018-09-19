#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008, 2011 Red Hat, Inc.
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
from textwrap import dedent
from pykickstart.version import versionToLongString, RHEL5, RHEL6, FC3, FC4, FC5, F29
from pykickstart.version import F7, F9, F12, F13, F14, F15, F18, F23, F25, RHEL8
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser, mountpoint

import warnings
from pykickstart.i18n import _

class FC3_RaidData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.device = kwargs.get("device", None)
        self.fstype = kwargs.get("fstype", "")
        self.level = kwargs.get("level", "")
        self.format = kwargs.get("format", True)
        self.spares = kwargs.get("spares", 0)
        self.preexist = kwargs.get("preexist", False)
        self.mountpoint = kwargs.get("mountpoint", "")
        self.members = kwargs.get("members", [])

    def __eq__(self, y):
        if not y:
            return False

        return self.device == y.device

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        # NB: using str(device) b/c when device=0 (as int) the condition fails
        # I'm not sure if we want to modify the tests b/c they compare device=md0 to device=0
        # and expect both to be equal
        if str(self.device):
            retval += " --device=%s" % self.device
        if self.fstype:
            retval += " --fstype=\"%s\"" % self.fstype
        if self.level:
            retval += " --level=%s" % self.level.upper()
        if not self.format:
            retval += " --noformat"
        if self.spares != 0:
            retval += " --spares=%d" % self.spares
        if self.preexist:
            retval += " --useexisting"

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "raid %s%s" % (self.mountpoint, self._getArgsAsStr())

        # Do not output the members list if --preexist was passed in.
        # This would be invalid input according to the parse method.
        if not self.preexist:
            retval += " " + " ".join(self.members)

        return retval.strip() + "\n"

class FC4_RaidData(FC3_RaidData):
    removedKeywords = FC3_RaidData.removedKeywords
    removedAttrs = FC3_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_RaidData.__init__(self, *args, **kwargs)
        self.fsopts = kwargs.get("fsopts", "")

    def _getArgsAsStr(self):
        retval = FC3_RaidData._getArgsAsStr(self)

        if self.fsopts:
            retval += " --fsoptions=\"%s\"" % self.fsopts

        return retval

class FC5_RaidData(FC4_RaidData):
    removedKeywords = FC4_RaidData.removedKeywords
    removedAttrs = FC4_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC4_RaidData.__init__(self, *args, **kwargs)
        self.bytesPerInode = kwargs.get("bytesPerInode", 4096)

    def _getArgsAsStr(self):
        retval = FC4_RaidData._getArgsAsStr(self)

        if hasattr(self, "bytesPerInode") and self.bytesPerInode != 0:
            retval += " --bytes-per-inode=%d" % self.bytesPerInode

        return retval

class RHEL5_RaidData(FC5_RaidData):
    removedKeywords = FC5_RaidData.removedKeywords
    removedAttrs = FC5_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC5_RaidData.__init__(self, *args, **kwargs)
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = FC5_RaidData._getArgsAsStr(self)

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase:
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F7_RaidData(FC5_RaidData):
    pass

class F9_RaidData(F7_RaidData):
    removedKeywords = F7_RaidData.removedKeywords + ["bytesPerInode"]
    removedAttrs = F7_RaidData.removedAttrs + ["bytesPerInode"]

    def __init__(self, *args, **kwargs):
        F7_RaidData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.fsprofile = kwargs.get("fsprofile", "")
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

    def _getArgsAsStr(self):
        retval = F7_RaidData._getArgsAsStr(self)

        if self.fsprofile:
            retval += " --fsprofile=\"%s\"" % self.fsprofile
        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase:
                retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

class F12_RaidData(F9_RaidData):
    removedKeywords = F9_RaidData.removedKeywords
    removedAttrs = F9_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F9_RaidData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.escrowcert = kwargs.get("escrowcert", "")
        self.backuppassphrase = kwargs.get("backuppassphrase", False)

    def _getArgsAsStr(self):
        retval = F9_RaidData._getArgsAsStr(self)

        if self.encrypted and self.escrowcert:
            retval += " --escrowcert=\"%s\"" % self.escrowcert

            if self.backuppassphrase:
                retval += " --backuppassphrase"
        return retval

class F13_RaidData(F12_RaidData):
    pass

class RHEL6_RaidData(F13_RaidData):
    removedKeywords = F13_RaidData.removedKeywords
    removedAttrs = F13_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_RaidData.__init__(self, *args, **kwargs)

        self.cipher = kwargs.get("cipher", "")

    def _getArgsAsStr(self):
        retval = F13_RaidData._getArgsAsStr(self)

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher

        return retval

class F14_RaidData(F13_RaidData):
    pass

class F15_RaidData(F14_RaidData):
    removedKeywords = F14_RaidData.removedKeywords
    removedAttrs = F14_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_RaidData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.label = kwargs.get("label", "")

    def _getArgsAsStr(self):
        retval = F14_RaidData._getArgsAsStr(self)

        if self.label:
            retval += " --label=%s" % self.label

        return retval

class F18_RaidData(F15_RaidData):
    removedKeywords = F15_RaidData.removedKeywords
    removedAttrs = F15_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F15_RaidData.__init__(self, *args, **kwargs)

        self.cipher = kwargs.get("cipher", "")

    def _getArgsAsStr(self):
        retval = F15_RaidData._getArgsAsStr(self)

        if self.encrypted and self.cipher:
            retval += " --cipher=\"%s\"" % self.cipher

        return retval

class F23_RaidData(F18_RaidData):
    removedKeywords = F18_RaidData.removedKeywords
    removedAttrs = F18_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F18_RaidData.__init__(self, *args, **kwargs)
        self.mkfsopts = kwargs.get("mkfsoptions", "") or kwargs.get("mkfsopts", "")

    def _getArgsAsStr(self):
        retval = F18_RaidData._getArgsAsStr(self)

        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

class F25_RaidData(F23_RaidData):
    removedKeywords = F23_RaidData.removedKeywords
    removedAttrs = F23_RaidData.removedAttrs

    def __init__(self, *args, **kwargs):
        F23_RaidData.__init__(self, *args, **kwargs)
        self.chunk_size = kwargs.get("chunk_size", None)

    def _getArgsAsStr(self):
        retval = F23_RaidData._getArgsAsStr(self)

        if self.chunk_size:
            retval += " --chunksize=%d" % self.chunk_size

        return retval

class RHEL7_RaidData(F25_RaidData):
    pass

class F29_RaidData(F25_RaidData):
    def __init__(self, *args, **kwargs):
        F25_RaidData.__init__(self, *args, **kwargs)
        self.luks_version = kwargs.get("luks_version", "")
        self.pbkdf = kwargs.get("pbkdf", "")
        self.pbkdf_memory = kwargs.get("pbkdf_memory", 0)
        self.pbkdf_time = kwargs.get("pbkdf_time", 0)
        self.pbkdf_iterations = kwargs.get("pbkdf_iterations", 0)

    def _getArgsAsStr(self):
        retval = F25_RaidData._getArgsAsStr(self)

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

class RHEL8_RaidData(F29_RaidData):
    pass

class FC3_Raid(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=131, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        # A dict of all the RAID levels we support.  This means that if we
        # support more levels in the future, subclasses don't have to
        # duplicate too much.
        self.levelMap = {"RAID0": "RAID0", "0": "RAID0",
                         "RAID1": "RAID1", "1": "RAID1",
                         "RAID5": "RAID5", "5": "RAID5",
                         "RAID6": "RAID6", "6": "RAID6"}

        self.raidList = kwargs.get("raidList", [])
        self.op = self._getParser()

    def __str__(self):
        retval = ""

        for raid in self.raidList:
            retval += raid.__str__()

        return retval

    def _getParser(self):
        def device_cb(value):
            if value[0:2] == "md":
                return value[2:]
            else:
                return value

        def level_cb(value):
            if value.upper() in self.levelMap:
                return self.levelMap[value.upper()]
            else:
                raise KickstartParseError(_("Invalid raid level: %s") % value, lineno=self.lineno)

        op = KSOptionParser(prog="raid", description="""
                            Assembles a software RAID device.""",
                            epilog="""
                            The following example shows how to create a RAID
                            level 1 partition for /, and a RAID level 5 for
                            /usr, assuming there are three disks on the
                            system. It also creates three swap partitions, one
                            on each drive::

                                part raid.01 --size=6000 --ondisk=sda
                                part raid.02 --size=6000 --ondisk=sdb
                                part raid.03 --size=6000 --ondisk=sdc

                                part swap1 --size=512 --ondisk=sda
                                part swap2 --size=512 --ondisk=sdb
                                part swap3 --size=512 --ondisk=sdc

                                part raid.11 --size=6000 --ondisk=sda
                                part raid.12 --size=6000 --ondisk=sdb
                                part raid.13 --size=6000 --ondisk=sdc

                                raid / --level=1 --device=md0 raid.01 raid.02 raid.03
                                raid /usr --level=5 --device=md1 raid.11 raid.12 raid.13
                            """, version=FC3)
        op.add_argument("mntpoint", metavar="<mntpoint>", type=mountpoint, nargs=1,
                        version=FC3, help="""
                        Location where the RAID file system is mounted. If it
                        is /, the RAID level must be 1 unless a boot partition
                        (/boot) is present. If a boot partition is present, the
                        /boot partition must be level 1 and the root (/)
                        partition can be any of the available types.""")
        op.add_argument("partitions", metavar="<partitions*>", nargs="*",
                        version=FC3, help="""
                        The software raid partitions lists the RAID identifiers
                        to add to the RAID array.""")
        op.add_argument("--device", type=device_cb, required=True,
                        version=FC3, help="""
                        Name of the RAID device to use (such as 'fedora-root'
                        or 'home'). As of Fedora 19, RAID devices are no longer
                        referred to by names like 'md0'. If you have an old
                        (v0.90 metadata) array that you cannot assign a name to,
                        you can specify the array by a filesystem label or UUID
                        (eg: --device=LABEL=fedora-root).""")
        op.add_argument("--fstype", version=FC3, help="""
                        Sets the file system type for the RAID array. Valid
                        values include ext4, ext3, ext2, btrfs, swap, and vfat.
                        Other filesystems may be valid depending on command
                        line arguments passed to anaconda to enable other
                        filesystems.""")
        op.add_argument("--level", type=level_cb, version=FC3, help="""
                        RAID level to use %s.""" % set(self.levelMap.values()))
        op.add_argument("--noformat", dest="format", action="store_false",
                        default=True, version=FC3, help="""
                        Use an existing RAID device and do not format the RAID
                        array.""")
        op.add_argument("--spares", type=int, default=0, version=FC3, help="""
                        Specifies the number of spare drives allocated for the
                        RAID array. Spare drives are used to rebuild the array
                        in case of drive failure.""")
        op.add_argument("--useexisting", dest="preexist", action="store_true",
                        default=False, version=FC3, help="""
                        Use an existing RAID device and reformat it.""")
        return op

    def _getDevice(self, s):
        """ Convert the argument to --device= to its internal format. """
        # --device can't just take an int in the callback above, because it
        # could be specificed as "mdX", which causes optparse to error when
        # it runs int().
        return int(s)

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        if any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "raid", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        # because positional argumnets with variable number of values
        # don't parse very well
        if not ns.partitions and extra:
            ns.partitions = extra
            extra = []

        if not ns.format:
            ns.preexist = True

        assert len(ns.mntpoint) == 1
        if not ns.partitions and not ns.preexist:
            raise KickstartParseError(_("Partitions required for %s") % "raid", lineno=self.lineno)
        elif ns.partitions and ns.preexist:
            raise KickstartParseError(_("Members may not be specified for preexisting RAID device"), lineno=self.lineno)

        rd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, rd)
        rd.lineno = self.lineno

        # In older pykickstart --device was always specifying a minor, so
        # rd.device had to be an integer.
        # In newer pykickstart it has to be the array name since the minor
        # cannot be reliably predicted due to lack of mdadm.conf during boot.
        rd.device = self._getDevice(rd.device)
        rd.mountpoint = ns.mntpoint[0]

        if len(ns.partitions) > 0:
            rd.members = ns.partitions

        # Check for duplicates in the data list.
        if rd in self.dataList():
            warnings.warn(_("A RAID device with the name %s has already been defined.") % rd.device, KickstartParseWarning)

        if not rd.preexist and not rd.level:
            raise KickstartParseError("RAID Partition defined without RAID level", lineno=self.lineno)

        if rd.preexist and rd.device == "":
            raise KickstartParseError("Device required for preexisting RAID device", lineno=self.lineno)

        return rd

    def dataList(self):
        return self.raidList

    @property
    def dataClass(self):
        return self.handler.RaidData

class FC4_Raid(FC3_Raid):
    removedKeywords = FC3_Raid.removedKeywords
    removedAttrs = FC3_Raid.removedAttrs

    def _getParser(self):
        op = FC3_Raid._getParser(self)
        op.add_argument("--fsoptions", dest="fsopts", version=FC4, help="""
                        Specifies a free form string of options to be used when
                        mounting the filesystem. This string will be copied into
                        the /etc/fstab file of the installed system and should
                        be enclosed in quotes.""")
        return op

class FC5_Raid(FC4_Raid):
    removedKeywords = FC4_Raid.removedKeywords
    removedAttrs = FC4_Raid.removedAttrs

    def _getParser(self):
        op = FC4_Raid._getParser(self)
        op.add_argument("--bytes-per-inode", dest="bytesPerInode", type=int,
                        version=FC5, help="Specify the bytes/inode ratio.")
        return op

class RHEL5_Raid(FC5_Raid):
    removedKeywords = FC5_Raid.removedKeywords
    removedAttrs = FC5_Raid.removedAttrs

    def __init__(self, writePriority=131, *args, **kwargs):
        FC5_Raid.__init__(self, writePriority, *args, **kwargs)

        self.levelMap.update({"RAID10": "RAID10", "10": "RAID10"})

    def _getParser(self):
        op = FC5_Raid._getParser(self)
        for action in op._actions:
            if "--level" in action.option_strings:
                action.help += dedent("""

                .. versionchanged:: %s

                The "RAID10" level was added.""" % versionToLongString(RHEL5))
                break

        op.add_argument("--encrypted", action="store_true",
                        default=False, version=RHEL5, help="""
                        Specify that this RAID device should be encrypted.
                        """)
        op.add_argument("--passphrase", version=RHEL5, help="""
                        Specify the passphrase to use when encrypting this RAID
                        device. Without the above --encrypted option, this
                        option does nothing. If no passphrase is specified, the
                        default system-wide one is used, or the installer will
                        stop and prompt if there is no default.""")
        return op

class F7_Raid(FC5_Raid):
    removedKeywords = FC5_Raid.removedKeywords
    removedAttrs = FC5_Raid.removedAttrs

    def __init__(self, writePriority=131, *args, **kwargs):
        FC5_Raid.__init__(self, writePriority, *args, **kwargs)

        self.levelMap.update({"RAID10": "RAID10", "10": "RAID10"})

    def _getParser(self):
        op = FC5_Raid._getParser(self)
        for action in op._actions:
            if "--level" in action.option_strings:
                action.help += dedent("""

                .. versionchanged:: %s

                The "RAID10" level was added.""" % versionToLongString(F7))
                break
        return op

class F9_Raid(F7_Raid):
    removedKeywords = F7_Raid.removedKeywords
    removedAttrs = F7_Raid.removedAttrs

    def _getParser(self):
        op = F7_Raid._getParser(self)
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
                        Specify that this RAID device should be encrypted.""")
        op.add_argument("--passphrase", version=F9, help="""
                        Specify the passphrase to use when encrypting this RAID
                        device. Without the above --encrypted option, this option
                        does nothing. If no passphrase is specified, the default
                        system-wide one is used, or the installer will stop and
                        prompt if there is no default.""")
        return op

class F12_Raid(F9_Raid):
    removedKeywords = F9_Raid.removedKeywords
    removedAttrs = F9_Raid.removedAttrs

    def _getParser(self):
        op = F9_Raid._getParser(self)
        op.add_argument("--escrowcert", metavar="<url>", version=F12, help="""
                        Load an X.509 certificate from ``<url>``. Store the
                        data encryption key of this partition, encrypted using
                        the certificate, as a file in ``/root``. Only relevant
                        if ``--encrypted`` is specified as well.""")
        op.add_argument("--backuppassphrase", action="store_true",
                        default=False, version=F12, help="""
                        Only relevant if ``--escrowcert`` is specified as well.
                        In addition to storing the data encryption key, generate
                        a random passphrase and add it to this partition. Then
                        store the passphrase, encrypted using the certificate
                        specified by ``--escrowcert``, as a file in ``/root``.
                        If more than one LUKS volume uses ``--backuppassphrase``,
                        the same passphrase will be used for all such volumes.
                        """)
        return op

class F13_Raid(F12_Raid):
    removedKeywords = F12_Raid.removedKeywords
    removedAttrs = F12_Raid.removedAttrs

    def __init__(self, writePriority=131, *args, **kwargs):
        F12_Raid.__init__(self, writePriority, *args, **kwargs)

        self.levelMap.update({"RAID4": "RAID4", "4": "RAID4"})

    def _getParser(self):
        op = F12_Raid._getParser(self)
        for action in op._actions:
            if "--level" in action.option_strings:
                action.help += dedent("""

                .. versionchanged:: %s

                The "RAID4" level was added.""" % versionToLongString(F13))
                break
        return op

class RHEL6_Raid(F13_Raid):
    removedKeywords = F13_Raid.removedKeywords
    removedAttrs = F13_Raid.removedAttrs

    def _getParser(self):
        op = F13_Raid._getParser(self)
        op.add_argument("--cipher", version=RHEL6, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        return op

    def parse(self, args):
        # first call the overriden method
        retval = F13_Raid.parse(self, args)
        # the raid command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The raid and autopart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval

class F14_Raid(F13_Raid):
    removedKeywords = F13_Raid.removedKeywords
    removedAttrs = F13_Raid.removedAttrs

    def _getParser(self):
        op = F13_Raid._getParser(self)
        op.remove_argument("--bytes-per-inode", version=F14)
        return op

class F15_Raid(F14_Raid):
    removedKeywords = F14_Raid.removedKeywords
    removedAttrs = F14_Raid.removedAttrs

    def _getParser(self):
        op = F14_Raid._getParser(self)
        op.add_argument("--label", version=F15, help="""
                        Specify the label to give to the filesystem to be made.
                        If the given label is already in use by another
                        filesystem, a new label will be created.""")
        return op

class F18_Raid(F15_Raid):
    removedKeywords = F15_Raid.removedKeywords
    removedAttrs = F15_Raid.removedAttrs

    def _getParser(self):
        op = F15_Raid._getParser(self)
        op.add_argument("--cipher", version=F18, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        return op

class F19_Raid(F18_Raid):
    removedKeywords = F18_Raid.removedKeywords
    removedAttrs = F18_Raid.removedAttrs

    def _getDevice(self, s):
        return s

class F20_Raid(F19_Raid):
    removedKeywords = F19_Raid.removedKeywords
    removedAttrs = F19_Raid.removedAttrs

    def parse(self, args):
        # first call the overriden method
        retval = F19_Raid.parse(self, args)
        # the raid command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The raid and autopart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The raid and mount commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval

class F23_Raid(F20_Raid):
    removedKeywords = F20_Raid.removedKeywords
    removedAttrs = F20_Raid.removedAttrs

    def _getParser(self):
        op = F20_Raid._getParser(self)
        op.add_argument("--mkfsoptions", dest="mkfsopts", version=F23, help="""
                        Specifies additional parameters to be passed to the
                        program that makes a filesystem on this partition. No
                        processing is done on the list of arguments, so they
                        must be supplied in a format that can be passed directly
                        to the mkfs program. This means multiple options should
                        be comma-separated or surrounded by double quotes,
                        depending on the filesystem.""")
        return op

    def parse(self, args):
        retval = F20_Raid.parse(self, args)

        if not retval.format and retval.mkfsopts:
            raise KickstartParseError(_("--mkfsoptions with --noformat has no effect."), lineno=self.lineno)

        if retval.fsprofile and retval.mkfsopts:
            raise KickstartParseError(_("--mkfsoptions and --fsprofile cannot be used together."), lineno=self.lineno)

        return retval

class F25_Raid(F23_Raid):
    removedKeywords = F23_Raid.removedKeywords
    removedAttrs = F23_Raid.removedAttrs

    def _getParser(self):
        op = F23_Raid._getParser(self)
        op.add_argument("--chunksize", type=int, dest="chunk_size",
                        version=F25, help="""
                        Specify the chunk size (in KiB) for this RAID array.
                        """)
        return op

class RHEL7_Raid(F25_Raid):
    pass

class F29_Raid(F25_Raid):
    removedKeywords = F25_Raid.removedKeywords
    removedAttrs = F25_Raid.removedAttrs

    def _getParser(self):
        op = F25_Raid._getParser(self)
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
        retval = F25_Raid.parse(self, args)

        if retval.pbkdf_time and retval.pbkdf_iterations:
            msg = _("Only one of --pbkdf-time and --pbkdf-iterations can be specified.")
            raise KickstartParseError(msg, lineno=self.lineno)

        return retval

class RHEL8_Raid(F29_Raid):
    removedKeywords = F29_Raid.removedKeywords
    removedAttrs = F29_Raid.removedAttrs

    def parse(self, args):
        retval = F29_Raid.parse(self, args)
        if retval.fstype == "btrfs":
            raise KickstartParseError(_("Btrfs file system is not supported"), lineno=self.lineno)
        return retval

    def _getParser(self):
        "Only necessary for the type change documentation"
        op = F29_Raid._getParser(self)
        for action in op._actions:
            if "--fstype" in action.option_strings:
                action.help += """

                    .. versionchanged:: %s

                    Btrfs support was removed.""" % versionToLongString(RHEL8)
        return op
