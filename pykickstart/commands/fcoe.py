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
from pykickstart.version import F12, F13, F28, RHEL7
from pykickstart.errors import KickstartParseWarning
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

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

class F28_FcoeData(F13_FcoeData):
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

class RHEL8_FcoeData(F28_FcoeData):
    pass

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
        op = KSOptionParser(prog="fcoe", description="""
                            Discover and attach FCoE storage devices accessible via
                            specified network interface
                            """, version=F12)
        op.add_argument("--nic", required=True, version=F12, help="""
                        Name of the network device connected to the FCoE switch""")
        return op

    def parse(self, args):
        zd = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        self.set_to_obj(ns, zd)
        zd.lineno = self.lineno

        # Check for duplicates in the data list.
        if zd in self.dataList():
            warnings.warn(_("A FCOE device with the name %s has already been defined.") % zd.nic, KickstartParseWarning)

        return zd

    def dataList(self):
        return self.fcoe

    @property
    def dataClass(self):
        return self.handler.FcoeData

class F13_Fcoe(F12_Fcoe):
    removedKeywords = F12_Fcoe.removedKeywords
    removedAttrs = F12_Fcoe.removedAttrs

    def _getParser(self):
        op = F12_Fcoe._getParser(self)
        op.add_argument("--dcb", action="store_true", default=False, version=F13, help="""
                        Enable Data Center Bridging awareness in installer. This option
                        should only be enabled for network interfaces that
                        require a host-based DCBX client. Configurations on
                        interfaces that implement a hardware DCBX client should
                        not use it.
                        """)
        return op

class RHEL7_Fcoe(F13_Fcoe):
    removedKeywords = F13_Fcoe.removedKeywords
    removedAttrs = F13_Fcoe.removedAttrs

    def _getParser(self):
        op = F13_Fcoe._getParser(self)
        op.add_argument("--autovlan", action="store_true", default=False, version=RHEL7, help="""
                        Perform automatic VLAN discovery and setup. This option is enabled
                        by default.
                        """)
        return op

class F28_Fcoe(F13_Fcoe):
    removedKeywords = F13_Fcoe.removedKeywords
    removedAttrs = F13_Fcoe.removedAttrs

    def _getParser(self):
        op = F13_Fcoe._getParser(self)
        op.add_argument("--autovlan", action="store_true", default=False, version=F28, help="""
                        Perform automatic VLAN discovery and setup. This option is enabled
                        by default.
                        """)
        return op

class RHEL8_Fcoe(F28_Fcoe):
    pass
