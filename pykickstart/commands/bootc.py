#
# Copyright (C) 2025  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from pykickstart.version import F43
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class F43_Bootc(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs
    conflictingCommands = ["ostreesetup", "ostreecontainer"]

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)

        self.op = self._getParser()

        self.stateroot = kwargs.get('stateroot', None)
        self.sourceImgRef = kwargs.get("sourceImgRef", None)
        self.targetImgRef = kwargs.get("targetImgRef", self.sourceImgRef)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not self.seen:
            return retval

        retval += "# Bootc setup\n"
        retval += "bootc %s\n" % self._getArgsAsStr()

        return retval

    def _getArgsAsStr(self):
        retcmd = []

        if self.stateroot:
            retcmd.append('--stateroot="%s"' % self.stateroot)
        if self.sourceImgRef:
            retcmd.append('--source-imgref="%s"' % self.sourceImgRef)
        if self.targetImgRef:
            retcmd.append('--target-imgref="%s"' % self.targetImgRef)

        return ' '.join(retcmd)

    def _getParser(self):
        op = KSOptionParser(prog="bootc", description="""
                            Used for Bootc installations from native container. See
                            https://bootc-dev.github.io/bootc//man/bootc-install-to-filesystem.html
                            for more information about Bootc install to filesystem.

                            **Experimental. Use on your own risk.**
                            """, version=F43, conflicts=self.conflictingCommands)
        # Rename the osname to stateroot and set default as proposed by
        # https://github.com/ostreedev/ostree/issues/2794
        op.add_argument("--stateroot",
                        version=F43,
                        default="default",
                        help="""
                        Name for the state directory, also known as "osname".
                        """)
        op.add_argument("--source-imgref",
                        dest="sourceImgRef",
                        required=True,
                        version=F43,
                        help="""
                        Install the system from an explicitly given source.
                        """)
        op.add_argument("--target-imgref",
                        dest="targetImgRef",
                        version=F43,
                        help="""
                        Specify the image to fetch for subsequent updates.
                        If not presented defaults to '--source-imgref' value.
                        """)

        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if not self.targetImgRef:
            self.targetImgRef = self.sourceImgRef

        return self

