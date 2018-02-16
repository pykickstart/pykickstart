#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
from pykickstart.version import FC3, FC4, F12, F14
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_DriverDiskData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)

        self.partition = kwargs.get("partition", "")
        self.source = kwargs.get("source", "")
        self.type = kwargs.get("type", "")

    def _getArgsAsStr(self):
        retval = ""

        if self.partition:
            retval += "%s" % self.partition

            if hasattr(self, "type") and self.type:
                retval += " --type=%s" % self.type
        elif self.source:
            retval += "--source=%s" % self.source
        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "driverdisk %s\n" % self._getArgsAsStr()
        return retval

class FC4_DriverDiskData(FC3_DriverDiskData):
    removedKeywords = FC3_DriverDiskData.removedKeywords
    removedAttrs = FC3_DriverDiskData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_DriverDiskData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.biospart = kwargs.get("biospart", "")

    def _getArgsAsStr(self):
        retval = ""

        if self.partition:
            retval += "%s" % self.partition

            if hasattr(self, "type") and self.type:
                retval += " --type=%s" % self.type
        elif self.source:
            retval += "--source=%s" % self.source
        elif self.biospart:
            retval += "--biospart=%s" % self.biospart

        return retval

class F12_DriverDiskData(FC4_DriverDiskData):
    removedKeywords = FC4_DriverDiskData.removedKeywords + ["type"]
    removedAttrs = FC4_DriverDiskData.removedAttrs + ["type"]

    def __init__(self, *args, **kwargs):
        FC4_DriverDiskData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

class F14_DriverDiskData(F12_DriverDiskData):
    pass

class FC3_DriverDisk(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.driverdiskList = kwargs.get("driverdiskList", [])

    def __str__(self):
        retval = ""
        for dd in self.driverdiskList:
            retval += dd.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="driverdisk", description="""
                            Driver diskettes can be used during kickstart
                            installations. You need to copy the driver disk's
                            contents to the root directory of a partition on
                            the system's hard drive. Then you need to use the
                            driverdisk command to tell the installation program
                            where to look for the driver disk.""",
                            version=FC3)
        op.add_argument("partition", nargs="*", version=FC3,
                        help="Partition containing the driver disk.")
        op.add_argument("--source", version=FC3, help="""
                        Specify a URL for the driver disk. NFS locations can be
                        given with ``nfs:host:/path/to/img``.""")
        op.add_argument("--type", version=FC3, help="")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(ns.partition) > 1:
            raise KickstartParseError(_("Only one partition may be specified for driverdisk command."), lineno=self.lineno)
        elif extra:
            mapping = {"command": "driverdisk", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        if len(ns.partition) == 1 and ns.source:
            raise KickstartParseError(_("Only one of --source and partition may be specified for driverdisk command."), lineno=self.lineno)

        if not ns.partition and not ns.source:
            raise KickstartParseError(_("One of --source or partition must be specified for driverdisk command."), lineno=self.lineno)

        ddd = self.dataClass()  # pylint: disable=not-callable
        self.set_to_obj(ns, ddd)
        ddd.lineno = self.lineno
        if len(ns.partition) == 1:
            ddd.partition = ns.partition[0]

        return ddd

    def dataList(self):
        return self.driverdiskList

    @property
    def dataClass(self):
        return self.handler.DriverDiskData

class FC4_DriverDisk(FC3_DriverDisk):
    removedKeywords = FC3_DriverDisk.removedKeywords
    removedAttrs = FC3_DriverDisk.removedKeywords

    def _getParser(self):
        op = FC3_DriverDisk._getParser(self)
        op.add_argument("--biospart", version=FC4, help="""
                        BIOS partition containing the driver disk (such as 82p2).
                        """)
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(ns.partition) > 1:
            raise KickstartParseError(_("Only one partition may be specified for driverdisk command."), lineno=self.lineno)
        elif extra:
            mapping = {"command": "driverdisk", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        if len(ns.partition) == 1 and ns.source:
            raise KickstartParseError(_("Only one of --source and partition may be specified for driverdisk command."), lineno=self.lineno)
        elif len(ns.partition) == 1 and ns.biospart:
            raise KickstartParseError(_("Only one of --biospart and partition may be specified for driverdisk command."), lineno=self.lineno)
        elif ns.source and ns.biospart:
            raise KickstartParseError(_("Only one of --biospart and --source may be specified for driverdisk command."), lineno=self.lineno)

        if not ns.partition and not ns.source and not ns.biospart:
            raise KickstartParseError(_("One of --source, --biospart, or partition must be specified for driverdisk command."), lineno=self.lineno)

        ddd = self.dataClass()  # pylint: disable=not-callable
        self.set_to_obj(ns, ddd)
        ddd.lineno = self.lineno
        if len(ns.partition) == 1:
            ddd.partition = ns.partition[0]

        return ddd

class F12_DriverDisk(FC4_DriverDisk):
    removedKeywords = FC4_DriverDisk.removedKeywords
    removedAttrs = FC4_DriverDisk.removedKeywords

    def _getParser(self):
        op = FC4_DriverDisk._getParser(self)
        op.add_argument("--type", deprecated=F12)
        return op

class F14_DriverDisk(F12_DriverDisk):
    removedKeywords = F12_DriverDisk.removedKeywords
    removedAttrs = F12_DriverDisk.removedKeywords

    def _getParser(self):
        op = F12_DriverDisk._getParser(self)
        op.remove_argument("--type", version=F14)
        return op
