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
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
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
        op = KSOptionParser()
        op.add_argument("--nomount", dest="nomount", action="store_true", default=False)
        op.add_argument("--romount", dest="romount", action="store_true", default=False)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        if ns.nomount and ns.romount:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Only one of --nomount and --romount may be specified for rescue command.")))

        self._setToSelf(ns)
        self.rescue = True
        return self
