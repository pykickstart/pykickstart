#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2012, 2013 Red Hat, Inc.
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
from pykickstart.version import FC3, F16, F21
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class FC3_VolGroupData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.format = kwargs.get("format", True)
        self.pesize = kwargs.get("pesize", 32768)
        self.preexist = kwargs.get("preexist", False)
        self.vgname = kwargs.get("vgname", "")
        self.physvols = kwargs.get("physvols", [])

    def __eq__(self, y):
        if not y:
            return False

        return self.vgname == y.vgname

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""
        if not self.format:
            retval += " --noformat"
        if self.pesize:
            retval += " --pesize=%d" % self.pesize
        if self.preexist:
            retval += " --useexisting"

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "volgroup %s" % self.vgname
        retval += self._getArgsAsStr()

        # Do not output the physical volumes list if --preexist was passed in.
        # This would be invalid input according to the parse method.
        if not self.preexist:
            retval += " " + " ".join(self.physvols)

        return retval.strip() + "\n"

class F16_VolGroupData(FC3_VolGroupData):
    def __init__(self, *args, **kwargs):
        FC3_VolGroupData.__init__(self, *args, **kwargs)
        self.reserved_space = kwargs.get("reserved-space", None) or kwargs.get("reserved_space", None)
        self.reserved_percent = kwargs.get("reserved-percent", None) or kwargs.get("reserved_percent", None)

    def _getArgsAsStr(self):
        retval = FC3_VolGroupData._getArgsAsStr(self)
        if self.reserved_space:
            retval += " --reserved-space=%d" % self.reserved_space
        if self.reserved_percent:
            retval += " --reserved-percent=%d" % self.reserved_percent

        return retval

class F21_VolGroupData(F16_VolGroupData):
    def __init__(self, *args, **kwargs):
        F16_VolGroupData.__init__(self, *args, **kwargs)
        self.pesize = kwargs.get("pesize", 0)

class RHEL7_VolGroupData(F21_VolGroupData):
    pass

class RHEL8_VolGroupData(F21_VolGroupData):
    pass

class FC3_VolGroup(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=132, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.vgList = kwargs.get("vgList", [])

    def __str__(self):
        retval = ""
        for vg in self.vgList:
            retval += vg.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="volgroup", description="""
                            Creates a Logical Volume Management (LVM) group.
                            """, epilog="""
                            Create the partition first, create the logical
                            volume group, and then create the logical volume.
                            For example::

                                part pv.01 --size 3000
                                volgroup myvg pv.01
                                logvol / --vgname=myvg --size=2000 --name=rootvol
                            """, version=FC3)
        op.add_argument("name", metavar="<name>", nargs="*", version=FC3, help="""
                        Name given to the volume group. The (which denotes that
                        multiple partitions can be listed) lists the identifiers
                        to add to the volume group.""")
        op.add_argument("partitions", metavar="<partitions*>", nargs="*", help="""
                        Physical Volume partitions to be included in this
                        Volume Group""", version=FC3)
        op.add_argument("--noformat", dest="format", action="store_false",
                        default=True, version=FC3, help="""
                        Use an existing volume group. Do not specify partitions
                        when using this option.""")
        op.add_argument("--pesize", type=int, default=32768, version=FC3,
                        help="""
                        Set the size of the physical extents in KiB.""")
        op.add_argument("--useexisting", dest="preexist", action="store_true",
                        default=False, version=FC3, help="""
                        Use an existing volume group. Do not specify partitions
                        when using this option.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        # because positional arguments with variable number of values
        # don't parse very well
        if not ns.partitions:
            if extra:
                ns.partitions = extra
                extra = []
            elif ns.name:
                ns.partitions = ns.name[1:]
                ns.name = [ns.name[0]]

        if not ns.format:
            ns.preexist = True

        vg = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, vg)
        vg.lineno = self.lineno

        if not ns.name:
            raise KickstartParseError(_("volgroup must be given a VG name"), lineno=self.lineno)

        if not any([ns.partitions, ns.preexist]):
            raise KickstartParseError(_("volgroup must be given a list of partitions"), lineno=self.lineno)
        elif ns.partitions and ns.preexist:
            raise KickstartParseError(_("Members may not be specified for preexisting volgroup"), lineno=self.lineno)
        vg.vgname = ns.name[0]

        if ns.partitions:
            vg.physvols = ns.partitions

        # Check for duplicates in the data list.
        if vg in self.dataList():
            warnings.warn(_("A volgroup with the name %s has already been defined.") % vg.vgname, KickstartParseWarning)

        return vg

    def dataList(self):
        return self.vgList

    @property
    def dataClass(self):
        return self.handler.VolGroupData

class F16_VolGroup(FC3_VolGroup):
    def _getParser(self):
        op = FC3_VolGroup._getParser(self)
        op.add_argument("--reserved-space", dest="reserved_space", type=int,
                        version=F16, help="""
                        Specify an amount of space to leave unused in a volume
                        group, in MiB. Do not append any units. This option is
                        only used for new volume groups.""")
        op.add_argument("--reserved-percent", dest="reserved_percent", type=int,
                        version=F16, help="""
                        Specify a percentage of total volume group space to
                        leave unused (new volume groups only).""")
        return op

    def parse(self, args):
        # first call the overriden method
        retval = FC3_VolGroup.parse(self, args)

        # Check that any reserved space options are in their valid ranges.
        if retval.reserved_space is not None and retval.reserved_space < 0:
            raise KickstartParseError("Volume group reserved space must be a positive integer.", lineno=self.lineno)

        if retval.reserved_percent is not None and not 0 < retval.reserved_percent < 100:
            raise KickstartParseError("Volume group reserved space percentage must be between 1 and 99.", lineno=self.lineno)

        # the volgroup command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The volgroup and autopart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The volgroup and mount commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        return retval

class F21_VolGroup(F16_VolGroup):
    def _getParser(self):
        op = F16_VolGroup._getParser(self)
        op.add_argument("--pesize", type=int, default=0, version=F21, help="""
                        Set the size of the physical extents in KiB.""")
        return op

class RHEL7_VolGroup(F21_VolGroup):
    pass

class RHEL8_VolGroup(F21_VolGroup):
    pass
