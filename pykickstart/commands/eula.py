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

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class F20_Eula(KickstartCommand):
    """The 'eula' kickstart command"""

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
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
        op = KSOptionParser()
        # people would struggle remembering the exact word
        op.add_option("--agreed", "--agree", "--accepted", "--accept",
                      dest="agreed", action="store_true", default=False)

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        if len(extra) != 0:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "eula"))

        if not self.agreed:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Kickstart command eula expects the --agreed option")))

        return self

