#
# Jiri Konecny <jkonecny@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008, 2012, 2016, 2017 Red Hat, Inc.
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
_ = lambda x: gettext.ldgettext("pykickstart", x)

class RHEL7_SnapshotData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.name = kwargs.get("name", "")
        self.origin = kwargs.get("origin", "")

    def __eq__(self, y):
        if not y:
            return False
        return (self.name == y.name and
                self.origin == y.origin)

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "snapshot %s --name=%s" % (self.origin, self.name)
        return retval + "\n"


class RHEL7_Snapshot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=140, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.snapshotList = kwargs.get("snapshotList", [])

    def __str__(self):
        retval = ""

        for part in self.snapshotList:
            retval += part.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--name", dest="name", required=True, type="string")

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) == 0:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Snapshot origin must be specified!")))
        elif len(extra) > 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Snapshot origin can be specified only once")))

        snap_data = self.handler.SnapshotData()
        self._setToObj(self.op, opts, snap_data)
        snap_data.lineno = self.lineno
        snap_data.origin = extra[0]

        # Check for duplicates
        if snap_data in self.dataList():
            warnings.warn(_("Snapshot with the name %s has been already defined") % snap_data.name)

        return snap_data

    def dataList(self):
        return self.snapshotList
