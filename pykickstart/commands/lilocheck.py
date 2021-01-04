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
from pykickstart.version import FC3, FC4, versionToLongString
from pykickstart.base import KickstartCommand, RemovedCommand
from pykickstart.options import KSOptionParser

class FC3_LiloCheck(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.check = kwargs.get("check", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.check:
            retval += "lilocheck\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="lilocheck", description="check LILO boot loader", version=FC3)
        return op

    def parse(self, args):
        self.op.parse_args(args=args, lineno=self.lineno)
        self.check = True
        return self

class FC4_LiloCheck(RemovedCommand, FC3_LiloCheck):
    def _getParser(self):
        op = FC3_LiloCheck._getParser(self)
        op.description += "\n\n.. versionremoved:: %s" % versionToLongString(FC4)
        return op
