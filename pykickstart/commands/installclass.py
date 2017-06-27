#
# Vendula Poncova <vponcova@redhat.com>
#
# Copyright 2017 Red Hat, Inc.
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

from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser
from pykickstart.version import F26


class F26_InstallClass(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=-1, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.name = kwargs.get("name", "")

    def __str__(self):
        return "# Install class\ninstallclass%s\n" % self._getArgsAsStr()

    def _getArgsAsStr(self):
        retval = ""
        if self.name:
            retval += ' --name="%s"' % self.name
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="installclass", version=F26, description="""
                            Require the specified install class to be used for the installation.
                            Otherwise, the best available install class will be used.""")

        op.add_argument("--name", version=F26, required=True,
                        help="""
                        Name of the required install class.""")

        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self
