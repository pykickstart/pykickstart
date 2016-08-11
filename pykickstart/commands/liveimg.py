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
from pykickstart.version import F19
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class F19_Liveimg(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.checksum = kwargs.get("checksum", "")
        self.noverifyssl = kwargs.get("noverifyssl", None)
        self.proxy = kwargs.get("proxy", None)
        self.url = kwargs.get("url", None)

        self.op = self._getParser()

    def __eq__(self, other):
        if not other:
            return False

        return self.url == other.url and self.proxy == other.proxy and \
               self.noverifyssl == other.noverifyssl and \
               self.checksum == other.checksum

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use live disk image installation\n"

        retval += "liveimg --url=\"%s\"" % self.url

        if self.proxy:
            retval += " --proxy=\"%s\"" % self.proxy

        if self.noverifyssl:
            retval += " --noverifyssl"

        if self.checksum:
            retval += " --checksum=\"%s\"" % self.checksum

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(prog="liveimg", description="""
            Install a disk image instead of packages. The image can be the
            squashfs.img from a Live iso, or any filesystem mountable by the
            install media (eg. ext4). Anaconda expects the image to contain
            utilities it needs to complete the system install so the best way to
            create one is to use livemedia-creator to make the disk image. If
            the image contains /LiveOS/\\*.img (this is how squashfs.img is
            structured) the first \\*.img file inside LiveOS will be mounted and
            used to install the target system. The URL may also point to a
            tarfile of the root filesystem. The file must end in .tar, .tbz,
            .tgz, .txz, .tar.bz2, tar.gz, tar.xz""", version=F19)
        op.add_argument("--url", metavar="<url>", required=True, version=F19,
                        help="""
                        The URL to install from. http, https, ftp and file are
                        supported.""")
        op.add_argument("--proxy", metavar="<proxyurl>", version=F19, help="""
                        Specify an HTTP/HTTPS/FTP proxy to use while performing
                        the install. The various parts of the argument act like
                        you would expect. Syntax is::

                        ``--proxy=[protocol://][username[:password]@]host[:port]``
                        """)
        op.add_argument("--noverifyssl", action="store_true", version=F19,
                        default=False, help="""
                        For a tree on a HTTPS server do not check the server's
                        certificate with what well-known CA validate and do not
                        check the server's hostname matches the certificate's
                        domain name.""")
        op.add_argument("--checksum", metavar="<sha256>", version=F19,
                        help="Optional sha256 checksum of the image file")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self
