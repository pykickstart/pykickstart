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
from pykickstart.base import KickstartCommand
from pykickstart.version import versionToLongString, RHEL6, RHEL7, RHEL8
from pykickstart.version import FC3, F9, F12, F16, F17, F18, F20, F21, F26, F29
from pykickstart.constants import AUTOPART_TYPE_BTRFS, AUTOPART_TYPE_LVM, AUTOPART_TYPE_LVM_THINP, AUTOPART_TYPE_PLAIN
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_AutoPart(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.autopart = kwargs.get("autopart", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.autopart:
            retval += "autopart\n"

        return retval

    def parse(self, args):
        if len(args) > 0:
            raise KickstartParseError(_("Kickstart command %s does not take any arguments") % "autopart", lineno=self.lineno)

        self.autopart = True
        return self

    def _getParser(self):
        return KSOptionParser(prog="autopart", description="""
                            Automatically create partitions -- a root (``/``) partition,
                            a swap partition, and an appropriate boot partition
                            for the architecture. On large enough drives, this
                            will also create a /home partition.

                            The ``autopart`` command can't be used with the logvol,
                            part/partition, raid, reqpart, or volgroup in the same
                            kickstart file.""", version=FC3)

class F9_AutoPart(FC3_AutoPart):
    removedKeywords = FC3_AutoPart.removedKeywords
    removedAttrs = FC3_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        FC3_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

        self.op = self._getParser()

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not self.autopart:
            return retval

        retval += "autopart"

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase:
                retval += " --passphrase=\"%s\""% self.passphrase

        retval += "\n"
        return retval

    def _getParser(self):
        op = FC3_AutoPart._getParser(self)
        op.add_argument("--encrypted", action="store_true", default=False,
                        version=F9, help="""
                        Should all devices with support be encrypted by default?
                        This is equivalent to checking the "Encrypt" checkbox on
                        the initial partitioning screen.""")
        op.add_argument("--passphrase", version=F9, help="""
                        Only relevant if ``--encrypted`` is specified. Provide
                        a default system-wide passphrase for all encrypted
                        devices.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        self.autopart = True
        return self

class F12_AutoPart(F9_AutoPart):
    removedKeywords = F9_AutoPart.removedKeywords
    removedAttrs = F9_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F9_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)

        self.escrowcert = kwargs.get("escrowcert", "")
        self.backuppassphrase = kwargs.get("backuppassphrase", False)

    def __str__(self):
        retval = F9_AutoPart.__str__(self)

        if not self.autopart:
            return retval

        if self.encrypted and self.escrowcert:
            retval = retval.strip()

            retval += " --escrowcert=\"%s\"" % self.escrowcert

            if self.backuppassphrase:
                retval += " --backuppassphrase"

            retval += "\n"

        return retval

    def _getParser(self):
        op = F9_AutoPart._getParser(self)
        op.add_argument("--escrowcert", metavar="<url>", version=F12, help="""
                        Only relevant if ``--encrypted`` is specified. Load an
                        X.509 certificate from ``<url>``. Store the data
                        encryption keys of all encrypted volumes created during
                        installation, encrypted using the certificate, as files
                        in ``/root``.""")
        op.add_argument("--backuppassphrase", action="store_true",
                        default=False, version=F12, help="""
                        Only relevant if ``--escrowcert`` is specified. In
                        addition to storing the data encryption keys, generate
                        a random passphrase and add it to all encrypted volumes
                        created during installation. Then store the passphrase,
                        encrypted using the certificate specified by
                        ``--escrowcert``, as files in ``/root`` (one file for
                        each encrypted volume).""")
        return op

class RHEL6_AutoPart(F12_AutoPart):
    removedKeywords = F12_AutoPart.removedKeywords
    removedAttrs = F12_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F12_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.cipher = kwargs.get("cipher", "")

    def __str__(self):
        retval = F12_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.encrypted and self.cipher:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --cipher=\"%s\"" % self.cipher
            retval += "\n"

        return retval

    def _getParser(self):
        op = F12_AutoPart._getParser(self)
        op.add_argument("--cipher", version=RHEL6, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        return op

    def parse(self, args):
        # call the overriden command to do its job first
        retval = F12_AutoPart.parse(self, args)

        # Using autopart together with other partitioning command such as
        # part/partition, raid, logvol or volgroup can lead to hard to debug
        # behavior that might among other result into an unbootable system.
        #
        # Therefore if any of those commands is detected in the same kickstart
        # together with autopart, an error is raised and installation is
        # aborted.
        conflicting_command = ""

        # seen indicates that the corresponding
        # command has been seen in kickstart
        if self.handler.partition.seen:
            conflicting_command = "part/partition"
        elif self.handler.raid.seen:
            conflicting_command = "raid"
        elif self.handler.volgroup.seen:
            conflicting_command = "volgroup"
        elif self.handler.logvol.seen:
            conflicting_command = "logvol"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The %s and autopart commands can't be used at the same time") % conflicting_command
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval


class F16_AutoPart(F12_AutoPart):
    removedKeywords = F12_AutoPart.removedKeywords
    removedAttrs = F12_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F12_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.lvm = kwargs.get("lvm", True)

    def __str__(self):
        retval = F12_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        # If requested, disable LVM autopart
        if not self.lvm:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --nolvm"
            retval += "\n"

        return retval

    def _getParser(self):
        op = F12_AutoPart._getParser(self)
        op.add_argument("--nolvm", action="store_false", dest="lvm",
                        default=True, version=F16,
                        help="Don't use LVM when partitioning.")
        return op

class F17_AutoPart(F16_AutoPart):
    def __init__(self, writePriority=100, *args, **kwargs):
        self.typeMap = {"lvm": AUTOPART_TYPE_LVM,
                        "btrfs": AUTOPART_TYPE_BTRFS,
                        "plain": AUTOPART_TYPE_PLAIN,
                        "partition": AUTOPART_TYPE_PLAIN}
        F16_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.type = kwargs.get("type", None)

    def _typeAsStr(self):
        retval = None

        for (key, value) in list(self.typeMap.items()):
            if value == self.type:
                retval = key
                break

        if retval == "partition":
            retval = "plain"

        return retval

    def __str__(self):
        retval = F16_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        ty = self._typeAsStr()
        if ty:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --type=%s\n" % ty

        return retval

    def _type_cb(self, value):
        if value.lower() in self.typeMap:
            return self.typeMap[value.lower()]
        else:
            raise KickstartParseError(_("Invalid autopart type: %s") % value, lineno=self.lineno)

    def _getParser(self):
        op = F16_AutoPart._getParser(self)
        op.add_argument("--nolvm", action="store_const", version=F17,
                        const=AUTOPART_TYPE_PLAIN, dest="type",
                        help="The same as ``--type=plain``")
        op.add_argument("--type", type=self._type_cb, version=F17, help="""
                        Select automatic partitioning scheme. Must be one of the
                        following: %s. Plain means regular
                        partitions with no btrfs or lvm.""" % list(self.typeMap.keys()))
        return op

    def parse(self, args):
        retval = F16_AutoPart.parse(self, args)

        # make this always True to avoid writing --nolvm
        self.lvm = True

        return retval

class F18_AutoPart(F17_AutoPart):
    removedKeywords = F17_AutoPart.removedKeywords
    removedAttrs = F17_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F17_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.cipher = kwargs.get("cipher", "")

    def __str__(self):
        retval = F17_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.encrypted and self.cipher:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --cipher=\"%s\"" % self.cipher
            retval += "\n"

        return retval

    def _getParser(self):
        op = F17_AutoPart._getParser(self)
        op.add_argument("--cipher", version=F18, help="""
                        Only relevant if ``--encrypted`` is specified. Specifies
                        which encryption algorithm should be used to encrypt the
                        filesystem.""")
        return op

class F20_AutoPart(F18_AutoPart):
    def __init__(self, writePriority=100, *args, **kwargs):
        F18_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.typeMap["thinp"] = AUTOPART_TYPE_LVM_THINP

    def parse(self, args):
        # call the overriden command to do its job first
        retval = F18_AutoPart.parse(self, args)

        # Using autopart together with other partitioning command such as
        # part/partition, raid, logvol or volgroup can lead to hard to debug
        # behavior that might among other result into an unbootable system.
        #
        # Therefore if any of those commands is detected in the same kickstart
        # together with autopart, an error is raised and installation is
        # aborted.
        conflicting_command = ""

        # seen indicates that the corresponding
        # command has been seen in kickstart
        if self.handler.partition.seen:
            conflicting_command = "part/partition"
        elif self.handler.raid.seen:
            conflicting_command = "raid"
        elif self.handler.volgroup.seen:
            conflicting_command = "volgroup"
        elif self.handler.logvol.seen:
            conflicting_command = "logvol"
        elif hasattr(self.handler, "mount") and self.handler.mount.seen:
            conflicting_command = "mount"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The %s and autopart commands can't be used at the same time") % conflicting_command
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval

    def _getParser(self):
        "Only necessary for the type change documentation"
        op = F18_AutoPart._getParser(self)
        for action in op._actions:
            if "--type" in action.option_strings:
                action.help += """

                    .. versionchanged:: %s

                    Partitioning scheme 'thinp' was added.""" % versionToLongString(F20)
        return op

class F21_AutoPart(F20_AutoPart):
    removedKeywords = F20_AutoPart.removedKeywords
    removedAttrs = F20_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F20_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.fstype = kwargs.get("fstype", "")

    def __str__(self):
        retval = F20_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.fstype:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --fstype=%s" % self.fstype
            retval += "\n"

        return retval

    def _getParser(self):
        op = F20_AutoPart._getParser(self)
        op.add_argument("--fstype", version=F21, help="""
                        Use the specified filesystem type on the partitions.
                        Note that it cannot be used with ``--type=btrfs`` since
                        btrfs is both a partition scheme and a filesystem. eg.
                        ``--fstype=ext4``.""")
        return op

    def parse(self, args):
        # call the overriden command to do its job first
        retval = F20_AutoPart.parse(self, args)

        # btrfs is not a valid filesystem type
        if self.fstype == "btrfs":
            raise KickstartParseError(_("autopart --fstype=btrfs is not valid fstype, use --type=btrfs instead"), lineno=self.lineno)

        if self._typeAsStr() == "btrfs" and self.fstype:
            raise KickstartParseError(_("autopart --fstype cannot be used with --type=btrfs"), lineno=self.lineno)

        return retval

class F23_AutoPart(F21_AutoPart):
    def parse(self, args):
        # call the overriden command to do its job first
        retval = F21_AutoPart.parse(self, args)

        conflicting_command = ""
        if hasattr(self.handler, "reqpart") and self.handler.reqpart.seen:
            conflicting_command = "reqpart"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The %s and autopart commands can't be used at the same time") % conflicting_command
            raise KickstartParseError(errorMsg, lineno=self.lineno)

        return retval

class RHEL7_AutoPart(F21_AutoPart):

    def __init__(self, writePriority=100, *args, **kwargs):
        F21_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.nohome = kwargs.get("nohome", False)

    def __str__(self):
        retval = F21_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.nohome:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --nohome"
            retval += "\n"

        return retval

    def _getParser(self):
        op = F21_AutoPart._getParser(self)
        op.add_argument("--nohome", action="store_true", default=False,
                        version=RHEL7, help="""
                        Do not create a /home partition.""")
        return op

    def parse(self, args):
        # call the overriden command to do its job first
        retval = F21_AutoPart.parse(self, args)

        conflicting_command = ""
        if hasattr(self.handler, "reqpart") and self.handler.reqpart.seen:
            conflicting_command = "reqpart"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The %s and autopart commands can't be used at the same time") % conflicting_command
            raise KickstartParseError(errorMsg, lineno=self.lineno)

        return retval

class F26_AutoPart(F23_AutoPart):
    removedKeywords = F23_AutoPart.removedKeywords
    removedAttrs = F23_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F23_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.nohome = kwargs.get("nohome", False)
        self.noboot = kwargs.get("noboot", False)
        self.noswap = kwargs.get("noswap", False)

    def __str__(self):
        retval = F23_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.nohome:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --nohome"
            retval += "\n"

        if self.noboot:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --noboot"
            retval += "\n"

        if self.noswap:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --noswap"
            retval += "\n"

        return retval

    def _getParser(self):
        op = F23_AutoPart._getParser(self)
        op.add_argument("--nohome", action="store_true", default=False,
                        version=F26, help="""
                        Do not create a /home partition.""")
        op.add_argument("--noboot", action="store_true", default=False,
                        version=F26, help="""
                        Do not create a /boot partition.""")
        op.add_argument("--noswap", action="store_true", default=False,
                        version=F26, help="""
                        Do not create a swap partition.""")
        return op

class F29_AutoPart(F26_AutoPart):
    removedKeywords = F26_AutoPart.removedKeywords
    removedAttrs = F26_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F26_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.luks_version = kwargs.get("luks_version", "")
        self.pbkdf = kwargs.get("pbkdf", "")
        self.pbkdf_memory = kwargs.get("pbkdf_memory", 0)
        self.pbkdf_time = kwargs.get("pbkdf_time", 0)
        self.pbkdf_iterations = kwargs.get("pbkdf_iterations", 0)

    def __str__(self):
        retval = F26_AutoPart.__str__(self)
        if not self.autopart:
            return retval

        if self.encrypted and self.luks_version:
            retval = retval.strip()
            retval += " --luks-version=%s" % self.luks_version
            retval += "\n"

        if self.encrypted and self.pbkdf:
            retval = retval.strip()
            retval += " --pbkdf=%s" % self.pbkdf
            retval += "\n"

        if self.encrypted and self.pbkdf_memory:
            retval = retval.strip()
            retval += " --pbkdf-memory=%s" % self.pbkdf_memory
            retval += "\n"

        if self.encrypted and self.pbkdf_time:
            retval = retval.strip()
            retval += " --pbkdf-time=%s" % self.pbkdf_time
            retval += "\n"

        if self.encrypted and self.pbkdf_iterations:
            retval = retval.strip()
            retval += " --pbkdf-iterations=%s" % self.pbkdf_iterations
            retval += "\n"

        return retval

    def _getParser(self):
        op = F26_AutoPart._getParser(self)
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
        retval = F26_AutoPart.parse(self, args)

        if self.pbkdf_time and self.pbkdf_iterations:
            msg = _("Only one of --pbkdf-time and --pbkdf-iterations can be specified.")
            raise KickstartParseError(msg, lineno=self.lineno)

        return retval

class RHEL8_AutoPart(F29_AutoPart):
    removedKeywords = F29_AutoPart.removedKeywords
    removedAttrs = F29_AutoPart.removedAttrs

    def parse(self, args):
        # call the overriden command to do it's job first
        retval = F29_AutoPart.parse(self, args)

        # btrfs is no more supported
        if self._typeAsStr() == "btrfs":
            raise KickstartParseError(_("autopart --type=btrfs is not supported"),
                                      lineno=self.lineno)

        return retval

    def _getParser(self):
        "Only necessary for the type change documentation"
        op = F29_AutoPart._getParser(self)
        for action in op._actions:
            if "--type" in action.option_strings:
                action.help += """

                    .. versionchanged:: %s

                    Partitioning scheme 'btrfs' was removed.""" % versionToLongString(RHEL8)
            if "--fstype" in action.option_strings:
                action.help += """

                    .. versionchanged:: %s

                    Partitioning scheme 'btrfs' was removed.""" % versionToLongString(RHEL8)
        return op
