#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007, 2009 Red Hat, Inc.
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

class FC6_Logging(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.host = kwargs.get("host", "")
        self.level = kwargs.get("level", "")
        self.port = kwargs.get("port", "")

        self._levelProvided = self.level != ""
        if not self._levelProvided:
            self.level = "info"

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.level and self._levelProvided:
            retval += "# Installation logging level\nlogging --level=%s" % self.level

            if self.host != "":
                retval += " --host=%s" % self.host

                if self.port != "":
                    retval += " --port=%s" % self.port

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--host")
        op.add_argument("--level", choices=["debug", "info", "warning", "error", "critical"])
        op.add_argument("--port")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if self.port and not self.host:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Can't specify --port without --host.")))

        self._levelProvided = self.level != ""
        if not self._levelProvided:
            self.level = "info"

        return self
