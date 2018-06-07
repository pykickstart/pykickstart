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
from pykickstart.version import RHEL5, RHEL6, versionToLongString
from pykickstart.version import FC3, FC4, F8, F12, F14, F15, F17, F18, F19, F21, F29
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
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

        if self.appendLine:
            retval += " --append=\"%s\"" % self.appendLine
        if self.linear:
            retval += " --linear"
        if self.location:
            retval += " --location=%s" % self.location
        if hasattr(self, "forceLBA") and self.forceLBA:
            retval += " --lba32"
        if self.password:
            retval += " --password=\"%s\"" % self.password
        if self.md5pass:
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

        if self.location:
            retval += "# System bootloader configuration\nbootloader"
            retval += self._getArgsAsStr() + "\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="bootloader", description="""
                            This required command specifies how the boot loader
                            should be installed.

                            There must be a biosboot partition for the bootloader
                            to be installed successfully onto a disk that contains
                            a GPT/GUID partition table, which includes disks
                            initialized by anaconda. This partition may be created
                            with the kickstart command
                            ``part biosboot --fstype=biosboot --size=1``. However,
                            in the case that a disk has an existing biosboot
                            partition, adding a ``part biosboot`` option is
                            unnecessary.""", version=FC3)
        op.add_argument("--append", dest="appendLine", version=FC3, help="""
                        Specifies kernel parameters. The default set of bootloader
                        arguments is "rhgb quiet". You will get this set of
                        arguments regardless of what parameters you pass to
                        --append, or if you leave out --append entirely.
                        For example::

                        ``bootloader --location=mbr --append="hdd=ide-scsi ide=nodma"``
                        """)
        op.add_argument("--linear", action="store_true", default=True,
                        version=FC3, help="")
        op.add_argument("--nolinear", dest="linear", action="store_false",
                        version=FC3, help="")
        op.add_argument("--location", default="mbr", version=FC3,
                        choices=["mbr", "partition", "none", "boot"],
                        help="""
                        Specifies where the boot record is written. Valid values
                        are the following: mbr (the default), partition
                        (installs the boot loader on the first sector of the
                        partition containing the kernel), or none
                        (do not install the boot loader).

                         **Note** `bootloader --location=none` is different from
                         `bootloader --location=none --disabled`.
                         `--location=none` prevents extra installation steps
                         that makes the target machine bootable, e.g. write to
                         MBR on x86 BIOS systems. However, the corresponding RPM
                         packages are still installed, and `--disabled` can be
                         appended to prevent it. `bootloader --disabled` only
                         does not prevent the installation of the bootloader and
                         Anaconda will complain if no other options are
                         provided.
                        """)
        op.add_argument("--lba32", dest="forceLBA", action="store_true",
                        default=False, version=FC3, help="")
        op.add_argument("--password", default="", version=FC3, help="""
                        If using GRUB, sets the GRUB boot loader password. This
                        should be used to restrict access to the GRUB shell,
                        where arbitrary kernel options can be passed.""")
        op.add_argument("--md5pass", default="", version=FC3, help="""
                        If using GRUB, similar to ``--password=`` except the
                        password should already be encrypted.""")
        op.add_argument("--upgrade", action="store_true", default=False,
                        version=FC3, help="")
        op.add_argument("--useLilo", action="store_true", default=False,
                        version=FC3, help="")
        op.add_argument("--driveorder", type=commaSplit, version=FC3, help="")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if self.currentCmd == "lilo":
            self.useLilo = True

        return self


class FC3_Lilo(FC3_Bootloader):
    """
        This is for backwards compatibility and docs generation.
        Used only in FC3, RHEL3 and RHEL4.
    """
    def _getParser(self):
        op = super(FC3_Lilo, self)._getParser()
        op.prog = "lilo"
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(FC4)
        return op


class FC4_Bootloader(FC3_Bootloader):
    removedKeywords = FC3_Bootloader.removedKeywords + ["linear", "useLilo"]
    removedAttrs = FC3_Bootloader.removedAttrs + ["linear", "useLilo"]

    def __init__(self, writePriority=10, *args, **kwargs):
        FC3_Bootloader.__init__(self, writePriority, *args, **kwargs)

    def _getArgsAsStr(self):
        retval = ""
        if self.appendLine:
            retval += " --append=\"%s\"" % self.appendLine
        if self.location:
            retval += " --location=%s" % self.location
        if hasattr(self, "forceLBA") and self.forceLBA:
            retval += " --lba32"
        if self.password:
            retval += " --password=\"%s\"" % self.password
        if self.md5pass:
            retval += " --md5pass=\"%s\"" % self.md5pass
        if self.upgrade:
            retval += " --upgrade"
        if len(self.driveorder) > 0:
            retval += " --driveorder=\"%s\"" % ",".join(self.driveorder)
        return retval

    def _getParser(self):
        op = FC3_Bootloader._getParser(self)
        op.remove_argument("--linear", version=FC4)
        op.remove_argument("--nolinear", version=FC4)
        op.remove_argument("--useLilo", version=FC4)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
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
            ret += " --timeout=%d" % (self.timeout,)
        if self.default:
            ret += " --default=%s" % (self.default,)

        return ret

    def _getParser(self):
        op = FC4_Bootloader._getParser(self)
        op.add_argument("--timeout", type=int, version=F8, help="""
                        Specify the number of seconds before the bootloader
                        times out and boots the default option.""")
        op.add_argument("--default", version=F8, help="""
                        Sets the default boot image in the bootloader
                        configuration.""")
        return op

class F12_Bootloader(F8_Bootloader):
    removedKeywords = F8_Bootloader.removedKeywords
    removedAttrs = F8_Bootloader.removedAttrs

    def _getParser(self):
        op = F8_Bootloader._getParser(self)
        op.add_argument("--lba32", dest="forceLBA", action="store_true",
                        deprecated=F12)
        return op

class F14_Bootloader(F12_Bootloader):
    removedKeywords = F12_Bootloader.removedKeywords + ["forceLBA"]
    removedAttrs = F12_Bootloader.removedKeywords + ["forceLBA"]

    def _getParser(self):
        op = F12_Bootloader._getParser(self)
        op.remove_argument("--lba32", version=F14)
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
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true",
                        default=False, version=F15, help="""
                        If given, the password specified by ``--password=`` is
                        already encrypted and should be passed to the bootloader
                        configuration without additional modification.""")
        op.add_argument("--md5pass", dest="_md5pass", version=F15, help="""
                        If using GRUB, similar to ``--password=`` except the password
                        should already be encrypted.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        # argparse doesn't give us a way to set two things at once, so we need to check if
        # _md5pass was given and if so, set everything now.
        if getattr(ns, "_md5pass", None):
            ns.password = ns._md5pass
            ns.isCrypted = True
            del ns._md5pass

        self.set_to_self(ns)
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
        op.add_argument("--boot-drive", dest="bootDrive", default="",
                        version=F17, help="""
                        Specifies which drive the bootloader should be written
                        to and thus, which drive the computer will boot from.""")
        return op

    def parse(self, args):
        retval = F15_Bootloader.parse(self, args)

        if "," in retval.bootDrive:     # pylint: disable=no-member
            raise KickstartParseError(_("--boot-drive accepts only one argument"), lineno=self.lineno)

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
        op.add_argument("--leavebootorder", action="store_true", default=False,
                        version=F18, help="""
                        On EFI or ISeries/PSeries machines, this option prevents
                        the installer from making changes to the existing list
                        of bootable images.""")
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
            ret += " --hvargs=\"%s\"" % (self.hvArgs,)

        return ret

    def _getParser(self):
        op = FC4_Bootloader._getParser(self)
        # todo: this is only in RHEL5 and nowhere else
        # possibly shadowed by the way we implement commands
        # inheritance
        op.add_argument("--hvargs", dest="hvArgs", version=RHEL5, help="")
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
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true",
                        default=False, version=RHEL6, help="""
                        If given, the password specified by ``--password=`` is
                        already encrypted and should be passed to the bootloader
                        configuration without additional modification.""")
        op.add_argument("--md5pass", dest="_md5pass", version=RHEL6, help="""
                        If using GRUB, similar to ``--password=`` except the
                        password should already be encrypted.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        # argparse doesn't give us a way to set two things at once, so we need to check if
        # _md5pass was given and if so, set everything now.
        if getattr(ns, "_md5pass", None):
            ns.password = ns._md5pass
            ns.isCrypted = True
            del ns._md5pass

        self.set_to_self(ns)
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
        op.add_argument("--extlinux", action="store_true", default=False,
                        version=F19, help="""
                        Use the extlinux bootloader instead of GRUB. This option
                        only works on machines that are supported by extlinux.""")
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
        op.add_argument("--disabled", action="store_true", default=False,
                        version=F21, help="""
                        Do not install the boot loader.

                         **Note** `bootloader --location=none` is different from
                         `bootloader --location=none --disabled`.
                         `--location=none` prevents extra installation steps
                         that makes the target machine bootable, e.g. write to
                         MBR on x86 BIOS systems. However, the corresponding RPM
                         packages are still installed, and `--disabled` can be
                         appended to prevent it. `bootloader --disabled` only
                         does not prevent the installation of the bootloader and
                         Anaconda will complain if no other options are
                         provided.
                        """)
        op.add_argument("--nombr", action="store_true", default=False,
                        version=F21, help="")
        return op

class RHEL7_Bootloader(F21_Bootloader):
    pass

class F29_Bootloader(F21_Bootloader):
    removedKeywords = F21_Bootloader.removedKeywords
    removedAttrs = F21_Bootloader.removedAttrs

    def _getParser(self):
        op = F21_Bootloader._getParser(self)
        op.add_argument("--upgrade", action="store_true", default=False,
                        deprecated=F29, help="")
        return op

class RHEL8_Bootloader(F29_Bootloader):
    pass
