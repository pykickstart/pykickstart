#
# Chris Lumens <clumens@redhat.com>
# David Lehman <dlehman@redhat.com>
#
# Copyright 2005, 2006, 2007, 2011 Red Hat, Inc.
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
from pykickstart.version import F17, F23, RHEL8, versionToLongString
from pykickstart.base import BaseData, KickstartCommand, DeprecatedCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser, mountpoint

import warnings
from pykickstart.i18n import _

class F17_BTRFSData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.format = kwargs.get("format", True)
        self.preexist = kwargs.get("preexist", False)
        self.label = kwargs.get("label", "")
        self.mountpoint = kwargs.get("mountpoint", "")
        self.devices = kwargs.get("devices", [])
        self.dataLevel = kwargs.get("data", None) or kwargs.get("dataLevel", None)
        self.metaDataLevel = kwargs.get("metadata", None) or kwargs.get("metaDataLevel", None)

        # subvolume-specific
        self.subvol = kwargs.get("subvol", False)
        self.parent = kwargs.get("parent", "")
        self.name = kwargs.get("name", None)        # required

    def __eq__(self, y):
        if not y:
            return False

        return self.mountpoint == y.mountpoint

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""
        if not self.format:
            retval += " --noformat"
        if self.preexist:
            retval += " --useexisting"
        if self.label:
            retval += " --label=%s" % self.label
        if self.dataLevel:
            retval += " --data=%s" % self.dataLevel.lower()
        if self.metaDataLevel:
            retval += " --metadata=%s" % self.metaDataLevel.lower()
        if self.subvol:
            retval += " --subvol --name=%s" % self.name

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "btrfs %s" % self.mountpoint
        retval += self._getArgsAsStr()
        return retval + " " + " ".join(self.devices) + "\n"

class F23_BTRFSData(F17_BTRFSData):
    removedKeywords = F17_BTRFSData.removedKeywords
    removedAttrs = F17_BTRFSData.removedAttrs

    def __init__(self, *args, **kwargs):
        F17_BTRFSData.__init__(self, *args, **kwargs)
        self.mkfsopts = kwargs.get("mkfsoptions", "") or kwargs.get("mkfsopts", "")

    def _getArgsAsStr(self):
        retval = F17_BTRFSData._getArgsAsStr(self)

        if self.mkfsopts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

class RHEL7_BTRFSData(F23_BTRFSData):
    pass

class F17_BTRFS(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=132, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        # A dict of all the RAID levels we support.  This means that if we
        # support more levels in the future, subclasses don't have to
        # duplicate too much.
        self.levelMap = {"raid0": "raid0", "0": "raid0",
                         "raid1": "raid1", "1": "raid1",
                         "raid10": "raid10", "10": "raid10",
                         "single": "single"}

        self.btrfsList = kwargs.get("btrfsList", [])

    def __str__(self):
        retval = ""
        for btr in self.btrfsList:
            retval += btr.__str__()

        return retval

    def _getParser(self):
        def level_cb(value):
            if value.lower() in self.levelMap:
                return self.levelMap[value.lower()]
            else:
                raise KickstartParseError(_("Invalid btrfs level: %s") % value, lineno=self.lineno)

        op = KSOptionParser(prog="btrfs", description="""
                            Defines a BTRFS volume or subvolume. This command
                            is of the form:

                            ``btrfs <mntpoint> --data=<level> --metadata=<level> --label=<label> <partitions*>``

                            for volumes and of the form:

                            ``btrfs <mntpoint> --subvol --name=<path> <parent>``

                            for subvolumes.

                            The ``<partitions*>`` (which denotes that multiple
                            partitions can be listed) lists the BTRFS identifiers
                            to add to the BTRFS volume. For subvolumes, should be
                            the identifier of the subvolume's parent volume.

                            ``<mntpoint>``

                            Location where the file system is mounted.""",
                            epilog="""
                            The following example shows how to create a BTRFS
                            volume from member partitions on three disks with
                            subvolumes for root and home. The main volume is not
                            mounted or used directly in this example -- only
                            the root and home subvolumes::

                                part btrfs.01 --size=6000 --ondisk=sda
                                part btrfs.02 --size=6000 --ondisk=sdb
                                part btrfs.03 --size=6000 --ondisk=sdc

                                btrfs none --data=0 --metadata=1 --label=f17 btrfs.01 btrfs.02 btrfs.03
                                btrfs / --subvol --name=root LABEL=f17
                                btrfs /home --subvol --name=home f17""",
                            version=F17)
        op.add_argument("--noformat", dest="format", action="store_false",
                        default=True, version=F17, help="""
                        Use an existing BTRFS volume (or subvolume) and do not
                        reformat the filesystem.""")
        op.add_argument("--useexisting", dest="preexist", action="store_true",
                        default=False, help="Same as ``--noformat``.",
                        version=F17)

        # label, data, metadata
        op.add_argument("--label", default="", version=F17, help="""
                        Specify the label to give to the filesystem to be made.
                        If the given label is already in use by another
                        filesystem, a new label will be created. This option
                        has no meaning for subvolumes.""")
        op.add_argument("--data", dest="dataLevel", type=level_cb, help="""
                        RAID level to use (0, 1, 10) for filesystem data. Optional.
                        This option has no meaning for subvolumes.""",
                        version=F17)
        op.add_argument("--metadata", dest="metaDataLevel", type=level_cb,
                        version=F17, help="""
                        RAID level to use (0, 1, 10) for filesystem/volume
                        metadata. Optional. This option has no meaning for
                        subvolumes.""")

        #
        # subvolumes
        #
        op.add_argument("--subvol", action="store_true", default=False,
                        version=F17, help="Create BTRFS subvolume.")

        # parent must be a device spec (LABEL, UUID, &c)
        op.add_argument("--parent", default="", version=F17, help="BTRFS parent device")
        op.add_argument("--name", default="", version=F17, help="""
                        Subvolume name.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        data = self.dataClass()  # pylint: disable=not-callable
        self.set_to_obj(ns, data)
        data.lineno = self.lineno

        if not data.format:
            data.preexist = True
        elif data.preexist:
            data.format = False

        if not extra:
            raise KickstartParseError(_("btrfs must be given a mountpoint"), lineno=self.lineno)
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "btrfs", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        data.mountpoint = mountpoint(extra[0])
        data.devices = extra[1:]

        if not any([data.devices, data.subvol]):
            raise KickstartParseError(_("btrfs must be given a list of partitions"), lineno=self.lineno)
        elif not data.devices:
            raise KickstartParseError(_("btrfs subvol requires specification of parent volume"), lineno=self.lineno)

        if data.subvol and not data.name:
            raise KickstartParseError(_("btrfs subvolume requires a name"), lineno=self.lineno)

        # Check for duplicates in the data list.
        if data in self.dataList():
            warnings.warn(_("A btrfs volume with the mountpoint %s has already been defined.") % data.mountpoint, KickstartParseWarning)

        return data

    def dataList(self):
        return self.btrfsList

    @property
    def dataClass(self):
        return self.handler.BTRFSData

class F23_BTRFS(F17_BTRFS):
    removedKeywords = F17_BTRFS.removedKeywords
    removedAttrs = F17_BTRFS.removedAttrs

    def _getParser(self):
        op = F17_BTRFS._getParser(self)
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
        data = F17_BTRFS.parse(self, args)

        if (data.preexist or not data.format) and data.mkfsopts:
            raise KickstartParseError(_("--mkfsoptions with --noformat or --useexisting has no effect."), lineno=self.lineno)

        return data

class RHEL7_BTRFS(F23_BTRFS):
    pass

class RHEL8_BTRFS(DeprecatedCommand, F23_BTRFS):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = F23_BTRFS._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(RHEL8)
        return op
