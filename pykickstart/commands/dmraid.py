#
# Chris Lumens <clumens@redhat.com>
# Peter Jones <pjones@redhat.com>
#
# Copyright 2006, 2007 Red Hat, Inc.
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
from pykickstart.errors import KickstartParseWarning
from pykickstart.version import versionToLongString, FC6, F24
from pykickstart.base import BaseData, DeprecatedCommand, KickstartCommand
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class FC6_DmRaidData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)

        self.name = kwargs.get("name", "")
        self.devices = kwargs.get("devices", [])
        self.dmset = kwargs.get("dmset", None)

    def __eq__(self, y):
        if not y:
            return False

        return self.name == y.name and self.devices == y.devices

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "dmraid --name=%s" % self.name

        for dev in self.devices:
            retval += " --dev=\"%s\"" % dev

        return retval + "\n"

class FC6_DmRaid(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=60, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.dmraids = kwargs.get("dmraids", [])

    def __str__(self):
        retval = ""
        for dm in self.dmraids:
            retval += dm.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="dmraid", description="", version=FC6)
        op.add_argument("--name", required=True, version=FC6, help="")
        op.add_argument("--dev", dest="devices", action="append",
                        required=True, version=FC6, help="")
        return op

    def parse(self, args):
        dm = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        dm.name = dm.name.split('/')[-1]
        self.set_to_obj(ns, dm)
        dm.lineno = self.lineno

        # Check for duplicates in the data list.
        if dm in self.dataList():
            warnings.warn(_("A DM RAID device with the name %(name)s and devices %(devices)s has already been defined.") % {"name": dm.name, "devices": dm.devices}, KickstartParseWarning)

        return dm

    def dataList(self):
        return self.dmraids

    @property
    def dataClass(self):
        return self.handler.DmRaidData

class F24_DmRaid(DeprecatedCommand, FC6_DmRaid):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = FC6_DmRaid._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F24)
        return op
