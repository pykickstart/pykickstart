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

class RHEL3_Mouse(KickstartCommand):
    def __init__(self, writePriority=0, device="", emulthree=False, mouse=""):
        KickstartCommand.__init__(self, writePriority)
        self.device = device
        self.emulthree = emulthree
        self.mouse = mouse

    def __str__(self):
        opts = ""
        if self.device:
            opts += "--device=%s " % self.device
        if self.emulthree:
            opts += "--emulthree " 

        retval = ""
        if self.mouse:
            retval = "# System mouse\nmouse %s%s\n" % (opts, self.mouse)
        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--device", dest="device", default="")
        op.add_option("--emulthree", dest="emulthree", default=False, action="store_true")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
        self.mouse = extra

class FC3_Mouse(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)
