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
import warnings

from pykickstart.errors import KickstartDeprecationWarning
from pykickstart.version import FC3
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_ZeroMbr(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=110, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.zerombr = kwargs.get("zerombr", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.zerombr:
            retval += "# Clear the Master Boot Record\nzerombr\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="zerombr", description="""
                            If zerombr is specified, any disks whose formatting
                            is unrecognized are initialized. This will destroy
                            all of the contents of disks with invalid partition
                            tables or other formatting unrecognizable to the
                            installer. It is useful so that the installation
                            program does not ask if it should initialize the
                            disk label if installing to a brand new hard drive.
                            """, version=FC3)
        return op

    def parse(self, args):
        extra = self.op.parse_known_args(args=args, lineno=self.lineno)[1]

        if extra:
            warnings.warn(_("Ignoring deprecated option on line %s:  The zerombr command no longer takes any options.  In future releases, this will result in a fatal error from kickstart.  Please modify your kickstart file to remove any options.") % self.lineno, KickstartDeprecationWarning)

        self.zerombr = True
        return self

class F9_ZeroMbr(FC3_ZeroMbr):
    removedKeywords = FC3_ZeroMbr.removedKeywords
    removedAttrs = FC3_ZeroMbr.removedAttrs

    def parse(self, args):
        self.op.parse_args(args=args, lineno=self.lineno)
        self.zerombr = True
        return self
