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
from textwrap import dedent

from pykickstart.errors import KickstartParseWarning, KickstartParseError
from pykickstart.version import FC3, F12, F14, RHEL8, versionToLongString
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class FC3_ZFCPData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.devnum = kwargs.get("devnum", "")
        self.wwpn = kwargs.get("wwpn", "")
        self.fcplun = kwargs.get("fcplun", "")
        self.scsiid = kwargs.get("scsiid", "")
        self.scsilun = kwargs.get("scsilun", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.devnum == y.devnum and self.wwpn == y.wwpn and \
               self.fcplun == y.fcplun and self.scsiid == y.scsiid and \
               self.scsilun == y.scsilun

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "zfcp"

        if self.devnum:
            retval += " --devnum=%s" % self.devnum
        if self.wwpn:
            retval += " --wwpn=%s" % self.wwpn
        if self.fcplun:
            retval += " --fcplun=%s" % self.fcplun
        if hasattr(self, "scsiid") and self.scsiid:
            retval += " --scsiid=%s" % self.scsiid
        if hasattr(self, "scsilun") and self.scsilun:
            retval += " --scsilun=%s" % self.scsilun

        return retval + "\n"

class F12_ZFCPData(FC3_ZFCPData):
    removedKeywords = FC3_ZFCPData.removedKeywords + ["scsiid", "scsilun"]
    removedAttrs = FC3_ZFCPData.removedAttrs + ["scsiid", "scsilun"]

    def __init__(self, *args, **kwargs):
        FC3_ZFCPData.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

    def __eq__(self, y):
        if not y:
            return False

        return self.devnum == y.devnum and self.wwpn == y.wwpn and \
               self.fcplun == y.fcplun

class F14_ZFCPData(F12_ZFCPData):
    pass

class RHEL8_ZFCPData(F14_ZFCPData):
    pass

class FC3_ZFCP(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=71, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.zfcp = kwargs.get("zfcp", [])

    def __str__(self):
        retval = ""
        for zfcp in self.zfcp:
            retval += zfcp.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="zfcp", version=FC3, description="""
                        Define a Fibre channel device. This option only applies
                        on IBM System z.""")
        op.add_argument("--devnum", required=True, version=FC3, help="""
                        The device number (zFCP adaptor device bus ID).""")
        op.add_argument("--fcplun", required=True, version=FC3, help="""
                        The device's Logical Unit Number (LUN). Takes the form
                        of a 16-digit number, preceded by 0x.""")
        op.add_argument("--wwpn", required=True, version=FC3, help="""
                        The device's World Wide Port Name (WWPN). Takes the form
                        of a 16-digit number, preceded by 0x.""")
        op.add_argument("--scsiid", required=True, version=FC3, help="SCSI ID")
        op.add_argument("--scsilun", required=True, version=FC3, help="SCSI LUN")
        return op

    def parse(self, args):
        zd = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_obj(ns, zd)
        zd.lineno = self.lineno

        # Check for duplicates in the data list.
        if zd in self.dataList():
            warnings.warn(_("A zfcp with this information has already been defined."), KickstartParseWarning)

        return zd

    def dataList(self):
        return self.zfcp

    @property
    def dataClass(self):
        return self.handler.ZFCPData

class F12_ZFCP(FC3_ZFCP):
    removedKeywords = FC3_ZFCP.removedKeywords
    removedAttrs = FC3_ZFCP.removedAttrs + ["scsiid", "scsilun"]

    def __init__(self, *args, **kwargs):
        FC3_ZFCP.__init__(self, *args, **kwargs)
        self.deleteRemovedAttrs()

    def _getParser(self):
        op = FC3_ZFCP._getParser(self)
        op.add_argument("--scsiid", deprecated=F12)
        op.add_argument("--scsilun", deprecated=F12)
        return op

class F14_ZFCP(F12_ZFCP):
    removedKeywords = F12_ZFCP.removedKeywords
    removedAttrs = F12_ZFCP.removedAttrs

    def _getParser(self):
        op = F12_ZFCP._getParser(self)
        op.remove_argument("--scsiid", version=F14)
        op.remove_argument("--scsilun", version=F14)
        return op

class RHEL8_ZFCP(F14_ZFCP):
    removedKeywords = F14_ZFCP.removedKeywords
    removedAttrs = F14_ZFCP.removedAttrs

    def _getParser(self):
        op = F14_ZFCP._getParser(self)
        op.description += dedent("""

            .. versionchanged:: %s

            It is sufficient to specify an FCP device bus ID if automatic LUN scanning
            is available. Otherwise all three parameters are required.

            ``zfcp --devnum=<devnum> [--wwpn=<wwpn> --fcplun=<lun>]``

            Automatic LUN scanning is available for FCP devices operating in NPIV mode
            if it is not disabled through the `zfcp.allow_lun_scan` module parameter
            (enabled by default). It provides access to all SCSI devices, that is, WWPNs
            and FCP LUNs, found in the storage area network attached to the FCP device
            with the specified bus ID.

        """ % versionToLongString(RHEL8))

        op.epilog += dedent("""
        For example::

            zfcp --devnum=0.0.6000
            zfcp --devnum=0.0.4000 --wwpn=0x5005076300C213e9 --fcplun=0x5022000000000000

        """)

        op.add_argument("--wwpn", default="", required=False, version=RHEL8, help="""
                        The argument is optional.""")
        op.add_argument("--fcplun", default="", required=False, version=RHEL8, help="""
                        The argument is optional.""")
        return op

    def parse(self, args):
        data = F14_ZFCP.parse(self, args)

        if not ((data.devnum and not data.wwpn and not data.fcplun)
                or (data.devnum and data.wwpn and data.fcplun)):
            msg = _("Only --devnum or --devnum with --wwpn and --fcplun are allowed.")
            raise KickstartParseError(msg, lineno=self.lineno)

        return data
