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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

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
        self.dataLevel = kwargs.get("data", None)
        self.metaDataLevel = kwargs.get("metadata", None)

        # subvolume-specific
        self.subvol = kwargs.get("subvol", False)
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
        self.mkfsopts = kwargs.get("mkfsoptions", "")

    def _getArgsAsStr(self):
        retval = F17_BTRFSData._getArgsAsStr(self)

        if self.mkfsopts != "":
            retval += " --mkfsoptions=\"%s\"" % self.mkfsopts

        return retval

RHEL7_BTRFSData = F23_BTRFSData

class F17_BTRFS(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=132, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        # A dict of all the RAID levels we support.  This means that if we
        # support more levels in the future, subclasses don't have to
        # duplicate too much.
        self.levelMap = { "raid0": "raid0", "0": "raid0",
                          "raid1": "raid1", "1": "raid1",
                          "raid10": "raid10", "10": "raid10",
                          "single": "single" }

        self.btrfsList = kwargs.get("btrfsList", [])

    def __str__(self):
        retval = ""
        for btr in self.btrfsList:
            retval += btr.__str__()

        return retval

    def _getParser(self):
        # Have to be a little more complicated to set two values.
        def btrfs_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        def level_cb (option, opt_str, value, parser):
            if value.lower() in self.levelMap:
                parser.values.ensure_value(option.dest, self.levelMap[value.lower()])

        op = KSOptionParser()
        op.add_option("--noformat", action="callback", callback=btrfs_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--useexisting", action="callback", callback=btrfs_cb,
                      dest="preexist", default=False, nargs=0)

        # label, data, metadata
        op.add_option("--label", dest="label", default="")
        op.add_option("--data", dest="dataLevel", action="callback",
                      callback=level_cb, type="string", nargs=1)
        op.add_option("--metadata", dest="metaDataLevel", action="callback",
                      callback=level_cb, type="string", nargs=1)

        #
        # subvolumes
        #
        op.add_option("--subvol", dest="subvol", action="store_true",
                      default=False)

        # parent must be a device spec (LABEL, UUID, &c)
        op.add_option("--parent", dest="parent", default="")
        op.add_option("--name", dest="name", default="")

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        data = self.handler.BTRFSData()
        self._setToObj(self.op, opts, data)
        data.lineno = self.lineno

        if len(extra) == 0:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("btrfs must be given a mountpoint")))

        if len(extra) == 1 and not data.subvol:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("btrfs must be given a list of partitions")))
        elif len(extra) == 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("btrfs subvol requires specification of parent volume")))

        if data.subvol and not data.name:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("btrfs subvolume requires a name")))

        data.mountpoint = extra[0]
        data.devices = extra[1:]

        # Check for duplicates in the data list.
        if data in self.dataList():
            warnings.warn(_("A btrfs volume with the mountpoint %s has already been defined.") % data.label)

        return data

    def dataList(self):
        return self.btrfsList

class F23_BTRFS(F17_BTRFS):
    removedKeywords = F17_BTRFS.removedKeywords
    removedAttrs = F17_BTRFS.removedAttrs

    def _getParser(self):
        op = F17_BTRFS._getParser(self)
        op.add_option("--mkfsoptions", dest="mkfsopts")

        return op

    def parse(self, args):
        data = F17_BTRFS.parse(self, args)

        if (data.preexist or not data.format) and data.mkfsopts:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("--mkfsoptions with --noformat or --useexisting has no effect.")))

        return data

RHEL7_BTRFS = F23_BTRFS
