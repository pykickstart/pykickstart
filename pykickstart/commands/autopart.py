#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC3_AutoPart(KickstartCommand):
    def __init__(self, writePriority=100, autopart=False):
        KickstartCommand.__init__(self, writePriority)
        self.autopart = autopart

    def __str__(self):
        if self.autopart:
            return "autopart\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "autopart")

        self.autopart = True

class F9_AutoPart(FC3_AutoPart):
    def __init__(self, writePriority=100, autopart=False, encrypted=False,
                 passphrase=""):
        FC3_AutoPart.__init__(self, writePriority=writePriority, autopart=autopart)
        self.op = self._getParser()

        self.encrypted = encrypted
        self.passphrase = passphrase

    def __str__(self):
        if self.autopart:
            retval = "autopart"
        else:
            return ""

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\""% self.passphrase

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)
        self._setToSelf(self.op, opts)
        self.autopart = True
