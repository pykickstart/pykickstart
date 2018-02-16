#
# Alexander Todorov <atodorov@redhat.com>
#
# Copyright 2008 Red Hat, Inc.
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
from pykickstart.version import F10
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class F10_Rescue(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.rescue = False
        self.nomount = kwargs.get("nomount", False)
        self.romount = kwargs.get("romount", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.rescue:
            retval += "rescue"

            if self.nomount:
                retval += " --nomount"
            if self.romount:
                retval += " --romount"

            retval = "# Start rescue mode\n%s\n" % retval

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="rescue", description="""
                            Automatically enter the installer's rescue mode.
                            This gives you a chance to repair the system should
                            something catastrophic happen.""", epilog="""
                            By default, the installer will find your system and
                            mount it in read-write mode, telling you where it has
                            performed this mount. You may optionally choose to
                            not mount anything or mount in read-only mode. Only
                            one of these two options may be given at any one
                            time.""", version=F10)
        op.add_argument("--nomount", action="store_true", version=F10,
                        default=False, help="""
                        Don't mount the installed system.""")
        op.add_argument("--romount", action="store_true", version=F10,
                        default=False, help="""
                        Mount the installed system in read-only mode.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        if ns.nomount and ns.romount:
            raise KickstartParseError(_("Only one of --nomount and --romount may be specified for rescue command."), lineno=self.lineno)

        self.set_to_self(ns)
        self.rescue = True
        return self
