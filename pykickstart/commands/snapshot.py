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
from pykickstart.constants import SNAPSHOT_WHEN_POST_INSTALL, SNAPSHOT_WHEN_PRE_INSTALL

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class RHEL7_SnapshotData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.name = kwargs.get("name", "")
        self.origin = kwargs.get("origin", "")
        self.when = kwargs.get("when", None)

    def __eq__(self, y):
        if not y:
            return False
        return (self.name == y.name and
                self.origin == y.origin and
                self.when == y.when)

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.when == SNAPSHOT_WHEN_POST_INSTALL:
            retval += "--when=post-install"
        elif self.when == SNAPSHOT_WHEN_PRE_INSTALL:
            retval += "--when=pre-install"

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += ("snapshot %s --name=%s %s" % (self.origin, self.name, self._getArgsAsStr()))
        return retval.strip() + "\n"


class RHEL7_Snapshot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=140, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.snapshotList = kwargs.get("snapshotList", [])
        self.whenMap = { "post-install": SNAPSHOT_WHEN_POST_INSTALL,
                         "pre-install": SNAPSHOT_WHEN_PRE_INSTALL }

    def __str__(self):
        retval = ""

        for part in self.snapshotList:
            retval += part.__str__()

        return retval

    def _getParser(self):
        def when_cb(option, opt_str, value, parser):
            if value.lower() in self.whenMap:
                parser.values.ensure_value(option.dest, self.whenMap[value.lower()])
        op = KSOptionParser()

        op.add_option("--name", dest="name", required=True, type="string")
        op.add_option("--when", action="callback", callback=when_cb,
                      dest="when", required=True, type="string")

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) == 0:
            msg = _("Snapshot origin must be specified!")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))
        elif len(extra) > 1:
            msg = _("Snapshot origin can be specified only once!")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))

        snap_data = self.handler.SnapshotData()
        self._setToObj(self.op, opts, snap_data)
        snap_data.lineno = self.lineno
        snap_data.origin = extra[0]

        # Check for duplicates
        if snap_data.name in [snap.name for snap in self.dataList()]:
            msg = (_("Snapshot with the name %s has been already defined!") % snap_data.name)
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))

        if snap_data.when is None:
            msg = _("Snapshot \"when\" parameter must be specified!")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))

        groups = snap_data.origin.split('/')
        if len(groups) != 2 or len(groups[0]) == 0 or len(groups[1]) == 0:
            msg = (_("Snapshot origin %s must be specified by VG/LV!") % snap_data.origin)
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))

        # Check if value in a '--when' param is valid
        if snap_data.when != "" and snap_data.when not in self.whenMap.values():
            msg = (_("Snapshot when param must have one of these values %s!") % self.whenMap.keys())
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=msg))
        return snap_data

    def dataList(self):
        return self.snapshotList


F26_SnapshotData = RHEL7_SnapshotData
F26_Snapshot = RHEL7_Snapshot
