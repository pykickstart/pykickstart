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

class FC3_SELinux(KickstartCommand):
    def __init__(self, writePriority=0, selinux=None):
        KickstartCommand.__init__(self, writePriority)
        self.op = self._getParser()

        self.selinux = selinux

    def __str__(self):
        retval = "# SELinux configuration\n"

        if self.selinux == SELINUX_DISABLED:
            return retval + "selinux --disabled\n"
        elif self.selinux == SELINUX_ENFORCING:
            return retval + "selinux --enforcing\n"
        elif self.selinux == SELINUX_PERMISSIVE:
            return retval + "selinux --permissive\n"
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disabled", dest="sel", action="store_const",
                      const=SELINUX_DISABLED)
        op.add_option("--enforcing", dest="sel", action="store_const",
                      const=SELINUX_ENFORCING)
        op.add_option("--permissive", dest="sel", action="store_const",
                      const=SELINUX_PERMISSIVE)
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)
        self.selinux = opts.sel
