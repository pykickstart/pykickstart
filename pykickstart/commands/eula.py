#
# Copyright (C) 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Vratislav Podzimek <vpodzime@redhat.com>
#
from pykickstart.version import F20
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class F20_Eula(KickstartCommand):
    """The 'eula' kickstart command"""

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.agreed = kwargs.get("agreed", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.agreed:
            retval += "# License agreement\n"
            retval += "eula %s\n" % self._getArgsAsStr()

        return retval

    def _getArgsAsStr(self):
        if self.agreed:
            return "--agreed"
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser(prog="eula", version=F20, description="""
                            Automatically accept Red Hat's EULA""")
        # people would struggle remembering the exact word
        op.add_argument("--agreed", "--agree", "--accepted", "--accept",
                        dest="agreed", action="store_true", default=False,
                        version=F20, help="Accept the EULA. This is mandatory option!")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        self.set_to_self(ns)

        if extra:
            raise KickstartParseError(_("Kickstart command %s does not take any arguments") % "eula", lineno=self.lineno)

        if not self.agreed:
            raise KickstartParseError(_("Kickstart command eula expects the --agreed option"), lineno=self.lineno)

        return self
