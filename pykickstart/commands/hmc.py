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
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser
from pykickstart.i18n import _


class RHEL7_Hmc(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use installation media via SE/HMC\nhmc\n"
        return retval

    def _getParser(self):
        op = KSOptionParser()
        return op

    def parse(self, args):
        (_opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) > 0:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % self.currentCmd))

        return self

class F28_Hmc(RHEL7_Hmc):
    pass
