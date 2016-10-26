#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007, 2009, 2013 Red Hat, Inc.
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
from pykickstart.version import FC3, FC6
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class FC3_NFS(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.server = kwargs.get("server", None)
        self.dir = kwargs.get("dir", None)

        self.op = self._getParser()

    def __eq__(self, other):
        if not other:
            return False

        return self.server == other.server and self.dir == other.dir

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use NFS installation media\nnfs --server=%s --dir=%s\n" % (self.server, self.dir)
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="nfs", description="""
                            Install from the NFS server specified. This can
                            either be an exploded installation tree or a
                            directory of ISO images. In the latter case, the
                            install.img must also be provided subject to the
                            same rules as with the harddrive installation
                            method described above.""", version=FC3)
        op.add_argument("--server", metavar="<hostname>", required=True,
                        version=FC3, help="""
                        Server from which to install (hostname or IP).""")
        op.add_argument("--dir", metavar="<directory>", required=True,
                        version=FC3, help="""
                        Directory containing the ``Packages/`` directory of the
                        installation tree. If doing an ISO install, this
                        directory must also contain images/install.img.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class FC6_NFS(FC3_NFS):
    removedKeywords = FC3_NFS.removedKeywords
    removedAttrs = FC3_NFS.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_NFS.__init__(self, writePriority, *args, **kwargs)
        self.opts = kwargs.get("opts", None)

    def __eq__(self, other):
        if not FC3_NFS.__eq__(self, other):
            return False

        return self.opts == other.opts

    def __str__(self):
        retval = FC3_NFS.__str__(self)

        if self.seen and self.opts:
            retval = retval.rstrip()
            retval += " --opts=\"%s\"\n" % self.opts

        return retval

    def _getParser(self):
        op = FC3_NFS._getParser(self)
        op.add_argument("--opts", metavar="<options>", version=FC6, help="""
                        Mount options to use for mounting the NFS export. Any
                        options that can be specified in ``/etc/fstab`` for an NFS
                        mount are allowed. The options are listed in the ``nfs(5)``
                        man page. Multiple options are separated with a comma.
                        """)
        return op
