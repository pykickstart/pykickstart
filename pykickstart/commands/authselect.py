#
# Vendula Poncova <vponcova@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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
from pykickstart.options import KSOptionParser
from pykickstart.version import F28


class F28_Authselect(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.authselect = kwargs.get("authselect", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.authselect:
            retval += "# System authorization information\nauthselect %s\n" % self.authselect

        return retval

    def parse(self, args):
        self.authselect = self.currentLine[len(self.currentCmd):].strip()
        return self

    def _getParser(self):
        op = KSOptionParser(prog="authselect",  description="""
                            This command sets up the authentication options
                            for the system. This is just a wrapper around the
                            authselect program, so all options recognized by
                            that program are valid for this command. See the
                            manual page for authselect for a complete list.""",
                            version=F28)

        op.add_argument("options", metavar="[options]", help="""
                        See ``man authselect``.""", version=F28)
        return op
