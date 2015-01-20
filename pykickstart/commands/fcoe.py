#
# Hans de Goede <hdegoede@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
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

import gettext
import warnings
from pykickstart import _

class F12_FcoeData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.nic = kwargs.get("nic", None)

    def __eq__(self, y):
        if not y:
            return False

        return self.nic == y.nic

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.nic:
            retval += " --nic=%s" % self.nic

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "fcoe%s\n" % self._getArgsAsStr()
        return retval

class F13_FcoeData(F12_FcoeData):
    removedKeywords = F12_FcoeData.removedKeywords
    removedAttrs = F12_FcoeData.removedAttrs

    def __init__(self, *args, **kwargs):
        F12_FcoeData.__init__(self, *args, **kwargs)
        self.dcb = kwargs.get("dcb", False)

    def _getArgsAsStr(self):
        retval = F12_FcoeData._getArgsAsStr(self)

        if self.dcb:
            retval += " --dcb"

        return retval

class RHEL7_FcoeData(F13_FcoeData):
    removedKeywords = F13_FcoeData.removedKeywords
    removedAttrs = F13_FcoeData.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_FcoeData.__init__(self, *args, **kwargs)
        self.autovlan = kwargs.get("autovlan", False)

    def _getArgsAsStr(self):
        retval = F13_FcoeData._getArgsAsStr(self)

        if self.autovlan:
            retval += " --autovlan"

        return retval

class F12_Fcoe(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=71, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.fcoe = kwargs.get("fcoe", [])

    def __str__(self):
        retval = ""
        for fcoe in self.fcoe:
            retval += fcoe.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--nic", dest="nic", required=1)
        return op

    def parse(self, args):
        zd = self.handler.FcoeData()
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        if len(extra) > 0:
            mapping = {"command": "fcoe", "options": extra}
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

        self._setToObj(self.op, opts, zd)
        zd.lineno = self.lineno

        # Check for duplicates in the data list.
        if zd in self.dataList():
            warnings.warn(_("A FCOE device with the name %s has already been defined.") % zd.nic)

        return zd

    def dataList(self):
        return self.fcoe

class F13_Fcoe(F12_Fcoe):
    removedKeywords = F12_Fcoe.removedKeywords
    removedAttrs = F12_Fcoe.removedAttrs

    def _getParser(self):
        op = F12_Fcoe._getParser(self)
        op.add_option("--dcb", dest="dcb", action="store_true", default=False)
        return op

class RHEL7_Fcoe(F13_Fcoe):
    removedKeywords = F13_Fcoe.removedKeywords
    removedAttrs = F13_Fcoe.removedAttrs

    def _getParser(self):
        op = F13_Fcoe._getParser(self)
        op.add_option("--autovlan", dest="autovlan", action="store_true", default=False)
        return op
