#
# Copyright 2023 Red Hat, Inc.
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
import warnings

from pykickstart.base import KickstartCommand, BaseData
from pykickstart.errors import KickstartParseWarning
from pykickstart.options import KSOptionParser
from pykickstart.i18n import _
from pykickstart.version import F39


class F39_StratisFsData(BaseData):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")
        self.pool = kwargs.get("pool", "")
        self.mount_point = kwargs.get("mount_point", "")
        self.size = kwargs.get("size", None)

    def __str__(self):
        retval = super().__str__()
        retval += "stratisfs %s" % self.mount_point
        retval += self._getArgsAsStr()
        return retval.strip() + "\n"

    def _getArgsAsStr(self):
        retval = ""

        if self.name:
            retval += " --name=%s" % self.name

        if self.pool:
            retval += " --pool=%s" % self.pool

        if self.size:
            retval += " --size=%d" % self.size

        return retval

    def __eq__(self, y):
        if not y:
            return False

        return self.pool == y.pool and self.name == y.name


class F39_StratisFs(KickstartCommand):

    def __init__(self, writePriority=133, *args, **kwargs):
        super().__init__(writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.filesystems = kwargs.get("filesystems", [])

    def __str__(self):
        return "".join(map(str, self.filesystems))

    def _getParser(self):
        op = KSOptionParser(prog="stratisfs", version=F39, description="""
                            Create a Stratis filesystem in a Stratis pool.
                            """, epilog="""
                            The following example shows how to create a Stratis
                            pool on three block devices and how to create filesystems
                            for the / and /home mount points::

                                stratispool mypool sda sdb sdc1
                                stratisfs / --pool=mypool --name=root --size=2000
                                stratisfs /home --pool=mypool --name=home --size=6000

                            """)
        op.add_argument("mount_point", metavar="<mount_point>", version=F39,
                        help="""Mount point for this Stratis filesystem.""")
        op.add_argument("--pool", metavar="<pool_name>", required=True, version=F39,
                        help="""Name of a Stratis pool this filesystem belongs to.""")
        op.add_argument("--name", metavar="<fs_name>", required=True, version=F39,
                        help="""Name given to this Stratis filesystem.""")
        op.add_argument("--size", type=int, version=F39,
                        help="""Size of this Stratis filesystem.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        fs = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, fs)
        fs.lineno = self.lineno

        # Check for duplicates in the data list.
        if fs in self.dataList():
            warnings.warn(
                _("A Stratis filesystem with the name %(fs_name)s has already been defined in "
                  "Stratis pool %(pool_name)s.") % {"fs_name": fs.name, "pool_name": fs.pool},
                KickstartParseWarning
            )

        return fs

    def dataList(self):
        return self.filesystems

    @property
    def dataClass(self):
        return self.handler.StratisFsData
