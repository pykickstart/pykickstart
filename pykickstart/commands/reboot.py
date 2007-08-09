#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Reboot(KickstartCommand):
    def __init__(self, writePriority=0, action=None):
        KickstartCommand.__init__(self, writePriority)
        self.action = action

    def __str__(self):
        if self.action == KS_REBOOT:
            return "# Reboot after installation\nreboot\n"
        elif self.action == KS_SHUTDOWN:
            return "# Shutdown after installation\nshutdown\n"
        else:
            return ""

    def parse(self, args):
        if self.currentCmd == "reboot":
            self.action = KS_REBOOT
        else:
            self.action = KS_SHUTDOWN

class FC6_Reboot(FC3_Reboot):
    def __init__(self, writePriority=0, action=None, eject=False):
        FC3_Reboot.__init__(self, writePriority, action=action)
        self.eject = eject

    def __str__(self):
        retval = ""

        if self.action == KS_REBOOT:
            retval = "# Reboot after installation\nreboot\n"
        elif self.action == KS_SHUTDOWN:
            retval = "# Shutdown after installation\nshutdown\n"
        else:
            return ""

        if self.eject:
            retval += " --eject"

        return retval

    def parse(self, args):
        if self.currentCmd == "reboot":
            self.action = KS_REBOOT
        else:
            self.action = KS_SHUTDOWN

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--eject", dest="eject", action="store_true",
                      default=False)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
