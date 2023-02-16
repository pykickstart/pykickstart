#
# Copyright (C) 2023  Red Hat, Inc.
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
from pykickstart.version import F38
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class F38_OSTreeContainer(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs
    conflictingCommands = ["ostreesetup"]

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.op = self._getParser()
        self.stateroot = kwargs.get('stateroot', None)
        self.url = kwargs.get('url', None)
        self.transport = kwargs.get("transport", None)
        self.remote = kwargs.get("remote", self.stateroot)
        self.noSignatureVerification = kwargs.get('noSignatureVerification', False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not self.seen:
            return retval

        retval += "# OSTree container setup\n"
        retval += "ostreecontainer %s\n" % self._getArgsAsStr()

        return retval

    def _getArgsAsStr(self):
        retcmd = []
        if self.stateroot:
            retcmd.append('--stateroot="%s"' % self.stateroot)
        if self.remote:
            retcmd.append('--remote="%s"' % self.remote)
        if self.noSignatureVerification:
            retcmd.append('--no-signature-verification')
        if self.transport:
            retcmd.append('--transport="%s"' % self.transport)
        if self.url:
            retcmd.append('--url="%s"' % self.url)
        return ' '.join(retcmd)

    def _getParser(self):
        op = KSOptionParser(prog="ostreecontainer", description="""
                            Used for OSTree installations from native container. See
                            https://coreos.github.io/rpm-ostree/container/
                            for more information about OSTree.

                            **Experimental. Use on your own risk.**
                            """, version=F38, conflicts=self.conflictingCommands)
        # Rename the osname to stateroot and set default as proposed by
        # https://github.com/ostreedev/ostree/issues/2794
        op.add_argument("--stateroot", version=F38, help="""
                        Name for the state directory, also known as "osname".
                        Default value will be `default`.""")
        op.add_argument("--url", required=True, version=F38, help="""
                        Name of the container image; for the `registry` transport.
                        This would be e.g. `quay.io/exampleos/foo:latest`.""")
        op.add_argument("--transport", version=F38, help="""
                        The transport; e.g. registry, oci, oci-archive.
                        The default is `registry`.""")
        op.add_argument("--remote", version=F38, help="""
                        Name of the OSTree remote.""")
        op.add_argument("--no-signature-verification",
                        dest="noSignatureVerification",
                        action="store_true",
                        version=F38,
                        help="""Disable verification via an ostree remote.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        if not self.remote:
            self.remote = self.stateroot

        return self
