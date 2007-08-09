#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6_Logging(KickstartCommand):
    def __init__(self, writePriority=0, host="", level="", port=""):
        KickstartCommand.__init__(self, writePriority)
        self.host = host
        self.level = level
        self.port = port

    def __str__(self):
        if self.level != "":
            retval = "# Installation logging level\nlogging --level=%s" % self.level

            if self.host != "":
                retval += " --host=%s" % self.host

                if self.port != "":
                    retval += " --port=%s" % self.port

            return retval + "\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--host")
        op.add_option("--level", type="choice",
                      choices=["debug", "info", "warning", "error", "critical"])
        op.add_option("--port")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
