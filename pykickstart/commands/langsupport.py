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
from pykickstart.version import FC3, FC5, versionToLongString
from pykickstart.base import DeprecatedCommand, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.i18n import _
from pykickstart.options import KSOptionParser

class FC3_LangSupport(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.deflang = kwargs.get("deflang", "")
        self.supported = kwargs.get("supported", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.deflang:
            retval += "langsupport --default=%s" % self.deflang

            if self.supported:
                retval += " %s" % " ".join(self.supported)

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(prog="langsupport", description="""
            Install the support packages for the given locales.""", version=FC3)
        op.add_argument("--default", dest="deflang", default="en_US.UTF-8",
                        version=FC3, help="Default locale")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        if any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "langsupport", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_self(ns)
        self.supported = extra
        return self

class FC5_LangSupport(DeprecatedCommand, FC3_LangSupport):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = FC3_LangSupport._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(FC5)
        return op
