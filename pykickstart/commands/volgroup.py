#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
import warnings
_ = lambda x: gettext.ldgettext("pykickstart", x)

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
        return retval + " " + " ".join(self.physvols) + "\n"

class FC16_VolGroupData(FC3_VolGroupData):
    def __init__(self, *args, **kwargs):
        FC3_VolGroupData.__init__(self, *args, **kwargs)
        self.reserved_space = kwargs.get("reserved-space", 0)
        self.reserved_percent = kwargs.get("reserved-percent", 0)

    def _getArgsAsStr(self):
        retval = FC3_VolGroupData._getArgsAsStr(self)
        if self.reserved_space > 0:
            retval += " --reserved-space=%d" % self.reserved_space
        if self.reserved_percent > 0:
            retval += " --reserved-percent=%d" % self.reserved_percent

        return retval

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
        # Have to be a little more complicated to set two values.
        def vg_cb (option, opt_str, value, parser):
            parser.values.format = False
            parser.values.preexist = True

        op = KSOptionParser()
        op.add_option("--noformat", action="callback", callback=vg_cb,
                      dest="format", default=True, nargs=0)
        op.add_option("--pesize", dest="pesize", type="int", nargs=1,
                      default=32768)
        op.add_option("--useexisting", dest="preexist", action="store_true",
                      default=False)
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        vg = self.handler.VolGroupData()
        self._setToObj(self.op, opts, vg)
        vg.lineno = self.lineno

        if len(extra) == 0:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("volgroup must be given a VG name")))

        if len(extra) == 1:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("volgroup must be given a list of partitions")))

        vg.vgname = extra[0]
        vg.physvols = extra[1:]

        # Check for duplicates in the data list.
        if vg in self.dataList():
            warnings.warn(_("A volgroup with the name %s has already been defined.") % vg.vgname)

        return vg

    def dataList(self):
        return self.vgList

class FC16_VolGroup(FC3_VolGroup):
    def _getParser(self):
        def space_cb(option, opt_str, value, parser):
            if value < 0:
                raise KickstartValueError(formatErrorMsg(self.lineno, msg="Volume group reserved space must be a positive integer."))

            parser.values.reserved_space = value

        def percent_cb(option, opt_str, value, parser):
            if not 0 < value < 100:
                raise KickstartValueError(formatErrorMsg(self.lineno, msg="Volume group reserved space percentage must be between 1 and 99."))

            parser.values.reserved_percent = value

        op = FC3_VolGroup._getParser(self)
        op.add_option("--reserved-space", action="callback", callback=space_cb,
                      dest="reserved_space", type="int", nargs=1, default=0)
        op.add_option("--reserved-percent", action="callback", callback=percent_cb,
                      dest="reserved_percent", type="int", nargs=1, default=0)
        return op


class RHEL6_VolGroup(FC3_VolGroup):

    def parse(self, args):
        # first call the overriden method
        retval = FC3_VolGroup.parse(self, args)
        # the volgroup command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The volgroup and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        return retval


class F20_VolGroup(FC16_VolGroup):

    def parse(self, args):
        # first call the overriden method
        retval = FC16_VolGroup.parse(self, args)
        # the volgroup command can't be used together with the autopart command
        # due to the hard to debug behavior their combination introduces
        if self.handler.autopart.seen:
            errorMsg = _("The volgroup and autopart commands can't be used at the same time")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))
        return retval
