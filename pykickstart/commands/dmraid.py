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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC6_DmRaidData(BaseData):
    def __init__(self, name="", devices=None, dmset=None):
        BaseData.__init__(self)
        self.name = name

        if devices == None:
            devices = []

        self.devices = devices
        self.dmset = dmset

    def __str__(self):
        retval = "dmraid --name=%s" % self.name

        for dev in self.devices:
            retval += " --dev=\"%s\"" % dev

        return retval + "\n"

class FC6_DmRaid(KickstartCommand):
    def __init__(self, writePriority=60, dmraids=None):
        KickstartCommand.__init__(self, writePriority)
        self.op = self._getParser()

        if dmraids == None:
            dmraids = []

        self.dmraids = dmraids

    def __str__(self):
        retval = ""
        for dm in self.dmraids:
            retval += dm.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", action="store", type="string",
                      required=1)
        op.add_option("--dev", dest="devices", action="append", type="string",
                      required=1)
        return op

    def parse(self, args):
        dm = FC6_DmRaidData()
        (opts, extra) = self.op.parse_args(args=args)
        dm.name = dm.name.split('/')[-1]
        self._setToObj(self.op, opts, dm)
        self.add(dm)

    def add(self, newObj):
        self.dmraids.append(newObj)
