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
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser
from pykickstart.constants import SNAPSHOT_WHEN_POST_INSTALL, SNAPSHOT_WHEN_PRE_INSTALL
from pykickstart.version import F26

from pykickstart.i18n import _


class F26_SnapshotData(BaseData):
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


class F26_Snapshot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=140, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)

        self.snapshotList = kwargs.get("snapshotList", [])
        self.whenMap = { "post-install": SNAPSHOT_WHEN_POST_INSTALL,
                         "pre-install": SNAPSHOT_WHEN_PRE_INSTALL }
        self.op = self._getParser()

    def __str__(self):
        retval = ""

        for snapshot in self.snapshotList:
            retval += snapshot.__str__()

        return retval

    def _when_cb(self, value):
        if value.lower() in self.whenMap:
            return self.whenMap[value.lower()]
        else:
            msg = _("Invalid snapshot when parameter: %s") % value
            raise KickstartParseError(msg, lineno=self.lineno)

    def _getParser(self):
        op = KSOptionParser(prog="snapshot", version=F26, description="""
                            Create an LVM snapshot for devices on an LVM thin pool.""")
        op.add_argument("--name", metavar="<snapshot_name>", version=F26, required=True,
                        help="""
                        Name of the newly created snapshot.""")
        # Show all possible options in meta message
        meta_msg = "<%s>" % ("|".join(self.whenMap.keys()))
        op.add_argument("--when", metavar=meta_msg, type=self._when_cb, version=F26,
                        required=True, help="""
                        You can specify two possible values: ``pre-install`` and ``post-install``.
                        When the ``pre-install`` value is used the snapshot is created before
                        the installation but after the ``%%pre`` section is run.
                        When the ``post-install`` value is used the snapshot is created after
                        the installation is done and after the ``%%post`` section is run.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) == 0:
            msg = _("Snapshot origin must be specified!")
            raise KickstartParseError(msg, lineno=self.lineno)
        elif len(extra) > 1:
            msg = _("Snapshot origin can be specified only once!")
            raise KickstartParseError(msg, lineno=self.lineno)

        snap_data = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, snap_data)
        snap_data.lineno = self.lineno
        snap_data.origin = extra[0]

        # Check for duplicates
        if snap_data.name in [snap.name for snap in self.dataList()]:
            msg = (_("Snapshot with the name %s has been already defined!") % snap_data.name)
            raise KickstartParseError(msg, lineno=self.lineno)

        if snap_data.when is None:
            msg = _("Snapshot \"when\" parameter must be specified!")
            raise KickstartParseError(msg, lineno=self.lineno)

        groups = snap_data.origin.split('/')
        if len(groups) != 2 or len(groups[0]) == 0 or len(groups[1]) == 0:
            msg = (_("Snapshot origin %s must be specified by VG/LV!") % snap_data.origin)
            raise KickstartParseError(msg, lineno=self.lineno)

        # Check if value in a '--when' param is valid
        if snap_data.when != "" and snap_data.when not in self.whenMap.values():
            msg = (_("Snapshot when param must have one of these values %s!") % self.whenMap.keys())
            raise KickstartParseError(msg, lineno=self.lineno)
        return snap_data

    def dataList(self):
        return self.snapshotList

    @property
    def dataClass(self):
        return self.handler.SnapshotData
