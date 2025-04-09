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
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

class F43_BootcSetup(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.op = self._getParser()
        self.osname = kwargs.get('osname', None)
        self.remote = kwargs.get("remote", self.osname)
        self.url = kwargs.get('url', None)
        self.ref = kwargs.get('ref', None)
        self.nogpg = kwargs.get('nogpg', False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        if self.osname:
            retval += "# Bootc setup\n"
            retval += "bootcsetup %s\n" % self._getArgsAsStr()

        return retval

    def _getArgsAsStr(self):
        retcmd = []
        if self.osname:
            retcmd.append('--osname="%s"' % self.osname)
        if self.remote:
            retcmd.append('--remote="%s"' % self.remote)
        if self.url:
            retcmd.append('--url="%s"' % self.url)
        if self.ref:
            retcmd.append('--ref="%s"' % self.ref)
        if self.nogpg:
            retcmd.append('--nogpg')
        return ' '.join(retcmd)

    def _getParser(self):
        op = KSOptionParser(prog="bootcsetup", description="""
                            Used for Bootc installations. See
                            https://docs.fedoraproject.org/en-US/bootc/
                            for more information about Bootc.
                            """, version=F43, conflicts=self.conflictingCommands)
        op.add_argument("--osname", required=True, version=F43, help="""
                        Management root for OS installation.""")
        op.add_argument("--remote", version=F43, help="""
                        Management root for OS installation.""")
        op.add_argument("--url", required=True, version=F43, help="""
                        Repository URL.""")
        op.add_argument("--ref", required=True, version=F43, help="""
                        Name of branch inside the repository.""")
        op.add_argument("--nogpg", action="store_true", version=F43, help="""
                        Disable GPG key verification.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        if not self.remote:
            self.remote = self.osname

        if not self.url.startswith(("file:", "http:", "https:")):
            raise KickstartParseError("bootc repos must use file, HTTP or HTTPS protocol.", lineno=self.lineno)

        return self

