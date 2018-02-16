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
from pykickstart.version import F7
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class F7_Updates(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.url = kwargs.get("url", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.url == "floppy":
            retval += "updates\n"
        elif self.url:
            retval += "updates %s\n" % self.url

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="updates", description="""
                            Specify the location of an updates.img for use in
                            installation. See anaconda-release-notes.txt for a
                            description of how to make an updates.img.""",
                            version=F7)
        op.add_argument("updates", metavar="[URL]", nargs="*", version=F7,
                        help="""
                        If present, the URL for an updates image.

                        If not present, anaconda will attempt to load from a
                        floppy disk.""")
        return op

    def parse(self, args):
        (_ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(_ns.updates) > 1:
            raise KickstartParseError(_("Kickstart command %s only takes one argument") % "updates", lineno=self.lineno)
        elif extra:
            mapping = {"command": "updates", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)
        elif not _ns.updates:
            self.url = "floppy"
        else:
            self.url = _ns.updates[0]

        return self
