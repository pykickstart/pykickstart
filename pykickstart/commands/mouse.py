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
from pykickstart.version import versionToLongString, RHEL3, FC3
from pykickstart.base import DeprecatedCommand, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class RHEL3_Mouse(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.device = kwargs.get("device", "")
        self.emulthree = kwargs.get("emulthree", False)
        self.mouse = kwargs.get("mouse", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        opts = ""
        if self.device:
            opts += "--device=%s " % self.device
        if self.emulthree:
            opts += "--emulthree "

        if self.mouse:
            retval += "# System mouse\nmouse %s%s\n" % (opts, self.mouse)
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="mouse", description="""
                            Configure the system mouse""", version=RHEL3)
        op.add_argument("--device", default="", version=RHEL3,
                        help="Which device node to use for mouse")
        op.add_argument("--emulthree", default=False, action="store_true",
                        version=RHEL3, help="If set emulate 3 mouse buttons")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) != 1:
            raise KickstartParseError(_("Kickstart command %s requires one argument") % "mouse", lineno=self.lineno)
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "mouse", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_self(ns)
        self.mouse = extra[0]
        return self

class FC3_Mouse(DeprecatedCommand, RHEL3_Mouse):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = RHEL3_Mouse._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(FC3)
        return op
