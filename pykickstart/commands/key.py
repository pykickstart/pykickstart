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
from pykickstart.version import RHEL5
from pykickstart.base import KickstartCommand
from pykickstart.constants import KS_INSTKEY_SKIP
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class RHEL5_Key(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.key = kwargs.get("key", "")
        self.skip = kwargs.get("skip", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.key == KS_INSTKEY_SKIP:
            retval += "key --skip\n"
        elif self.key:
            retval += "key %s\n" % self.key

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="key", description="", version=RHEL5)
        op.add_argument("--skip", action="store_true", default=False,
                        version=RHEL5, help="")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if self.skip:
            self.key = KS_INSTKEY_SKIP
        elif len(extra) != 1:
            raise KickstartParseError(_("Kickstart command %s requires one argument") % "key", lineno=self.lineno)
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "key", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)
        else:
            self.key = extra[0]

        return self
