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


class F39_StratisPoolData(BaseData):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", None)
        self.devices = kwargs.get("devices", [])

    def __str__(self):
        retval = super().__str__()
        retval += "stratispool %s" % self.name
        retval += self._getArgsAsStr()
        retval += " " + " ".join(self.devices)
        return retval.strip() + "\n"

    def _getArgsAsStr(self):
        retval = ""

        if self.encrypted:
            retval += " --encrypted"

        if self.passphrase:
            retval += " --passphrase=\"%s\"" % self.passphrase

        return retval

    def __eq__(self, y):
        return y and self.name == y.name


class F39_StratisPool(KickstartCommand):

    def __init__(self, writePriority=132, *args, **kwargs):
        super().__init__(writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.pools = kwargs.get("pools", [])

    def __str__(self):
        return "".join(map(str, self.pools))

    def _getParser(self):
        op = KSOptionParser(prog="stratispool", version=F39, description="""
                            Create a Stratis pool from one or more block devices.
                            A pool has a fixed total size, equal to the size of
                            the block devices.
                            """, epilog="""
                            The following example shows how to create a Stratis
                            pool on three block devices and how to create filesystems
                            for the / and /home mount points::

                                stratispool mypool sda sdb sdc1
                                stratisfs / --pool=mypool --name=root --size=2000
                                stratisfs /home --pool=mypool --name=home --size=6000

                            """)
        op.add_argument("name", metavar="<pool_name>", version=F39,
                        help="""Name given to this Stratis pool.""")
        op.add_argument("--encrypted", action="store_true", default=False,
                        version=F39, help="""
                        Specify that this Stratis pool should be encrypted.""")
        op.add_argument("--passphrase", version=F39, help="""
                        Specify the passphrase to use when encrypting this
                        Stratis pool. Without the above ``--encrypted``
                        option, this option does nothing. If no passphrase is
                        specified, the default system-wide one is used, or the
                        installer will stop and prompt if there is no default.""")
        op.add_argument("devices", metavar="<block_devices*>", version=F39,
                        nargs="+", help="""
                        Block devices to be included in this Stratis pool""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        pool = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, pool)
        pool.lineno = self.lineno

        # Check for duplicates in the data list.
        if pool in self.dataList():
            warnings.warn(
                _("A Stratis pool with the name %s has already been defined.") %
                pool.name, KickstartParseWarning
            )

        return pool

    def dataList(self):
        return self.pools

    @property
    def dataClass(self):
        return self.handler.StratisPoolData
