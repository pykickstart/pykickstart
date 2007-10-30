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
from pykickstart.options import *

class FC3_Firstboot(KickstartCommand):
    def __init__(self, writePriority=0, firstboot=None):
        KickstartCommand.__init__(self, writePriority)
        self.op = self._getParser()

        self.firstboot = firstboot

    def __str__(self):
        if self.firstboot is None:
            return ""

        if self.firstboot == FIRSTBOOT_SKIP:
            return "firstboot --disable\n"
        elif self.firstboot == FIRSTBOOT_DEFAULT:
            return "# Run the Setup Agent on first boot\nfirstboot --enable\n"
        elif self.firstboot == FIRSTBOOT_RECONFIG:
            return "# Run the Setup Agent on first boot\nfirstboot --reconfig\n"

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disable", "--disabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_SKIP)
        op.add_option("--enable", "--enabled", dest="firstboot",
                      action="store_const", const=FIRSTBOOT_DEFAULT)
        op.add_option("--reconfig", dest="firstboot", action="store_const",
                      const=FIRSTBOOT_RECONFIG)
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)
        self.firstboot = opts.firstboot
