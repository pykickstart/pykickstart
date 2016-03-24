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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
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
        if self.pesize != 0:
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

class FC16_VolGroupData(FC3_VolGroupData):
    def __init__(self, *args, **kwargs):
        FC3_VolGroupData.__init__(self, *args, **kwargs)
        self.reserved_space = kwargs.get("reserved-space", None)
        self.reserved_percent = kwargs.get("reserved-percent", None)

    def _getArgsAsStr(self):
        retval = FC3_VolGroupData._getArgsAsStr(self)
        if self.reserved_space is not None and self.reserved_space > 0:
            retval += " --reserved-space=%d" % self.reserved_space
        if self.reserved_percent is not None and self.reserved_percent > 0:
            retval += " --reserved-percent=%d" % self.reserved_percent

        return retval

class F21_VolGroupData(FC16_VolGroupData):
    def __init__(self, *args, **kwargs):
        FC16_VolGroupData.__init__(self, *args, **kwargs)
        self.pesize = kwargs.get("pesize", 0)

RHEL7_VolGroupData = F21_VolGroupData

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
        op = KSOptionParser()
        op.add_argument("--noformat", dest="format", action="store_false", default=True)
        op.add_argument("--pesize", type=int, default=32768)
        op.add_argument("--useexisting", dest="preexist", action="store_true", default=False)
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if not ns.format:
            ns.preexist = True

        vg = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, vg)
        vg.lineno = self.lineno

        if len(extra) == 0:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("volgroup must be given a VG name")))
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "volgroup", "options": extra}
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

        if len(extra) == 1 and not ns.preexist:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("volgroup must be given a list of partitions")))
        elif len(extra) > 1 and ns.preexist:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Members may not be specified for preexisting volgroup")))

        vg.vgname = extra[0]

        if len(extra) > 1:
            vg.physvols = extra[1:]

        # Check for duplicates in the data list.
        if vg in self.dataList():
            warnings.warn(_("A volgroup with the name %s has already been defined.") % vg.vgname)

        return vg

    def dataList(self):
        return self.vgList

    @property
    def dataClass(self):
        return self.handler.VolGroupData

class FC16_VolGroup(FC3_VolGroup):
    def _getParser(self):
        op = FC3_VolGroup._getParser(self)
        op.add_argument("--reserved-space", dest="reserved_space", type=int)
        op.add_argument("--reserved-percent", dest="reserved_percent", type=int)
        return op

    def parse(self, args):
        # first call the overriden method
        retval = FC3_VolGroup.parse(self, args)

        # Check that any reserved space options are in their valid ranges.
        if getattr(retval, "reserved_space", None) is not None and retval.reserved_space < 0:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg="Volume group reserved space must be a positive integer."))

        if getattr(retval, "reserved_percent", None) is not None and not 0 < retval.reserved_percent < 100:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg="Volume group reserved space percentage must be between 1 and 99."))

        # the volgroup command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The volgroup and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        return retval

class F21_VolGroup(FC16_VolGroup):
    def _getParser(self):
        op = FC16_VolGroup._getParser(self)
        op.add_argument("--pesize", type=int, default=0)

        return op

RHEL7_VolGroup = F21_VolGroup
