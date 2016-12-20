#
# Chris Lumens <clumens@redhat.com>
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
from pykickstart.errors import KickstartParseWarning
from pykickstart.version import F12
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class F12_GroupData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.name = kwargs.get("name", "")
        self.gid = kwargs.get("gid", None)

    def __eq__(self, y):
        if not y:
            return False

        return self.name == y.name

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "group"

        if self.name:
            retval += " --name=%s" % self.name
        if self.gid:
            retval += " --gid=%s" % self.gid

        return retval + "\n"

class F12_Group(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.groupList = kwargs.get("groupList", [])

    def __str__(self):
        retval = ""
        for user in self.groupList:
            retval += user.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="group", description="""
            Creates a new user group on the system. If a group with the given
            name or GID already exists, this command will fail. In addition,
            the ``user`` command can be used to create a new group for the
            newly created user.""", version=F12)
        op.add_argument("--name", required=True, version=F12,
                        help="Provides the name of the new group.")
        op.add_argument("--gid", type=int, version=F12, help="""
                        The group's GID. If not provided, this defaults to the
                        next available non-system GID.""")
        return op

    def parse(self, args):
        gd = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_obj(ns, gd)
        gd.lineno = self.lineno

        # Check for duplicates in the data list.
        if gd in self.dataList():
            warnings.warn(_("A group with the name %s has already been defined.") % gd.name, KickstartParseWarning)

        return gd

    def dataList(self):
        return self.groupList

    @property
    def dataClass(self):
        return self.handler.GroupData
