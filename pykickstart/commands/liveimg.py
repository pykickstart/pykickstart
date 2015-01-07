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
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

import gettext
from pykickstart import _

class F19_Liveimg(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.checksum = kwargs.get("checksum", "")
        self.noverifyssl = kwargs.get("noverifyssl", None)
        self.proxy = kwargs.get("proxy", None)
        self.url = kwargs.get("url", None)

        self.op = self._getParser()

    def __eq__(self, other):
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
        op = KSOptionParser()
        op.add_option("--url", required=1)
        op.add_option("--proxy")
        op.add_option("--noverifyssl", action="store_true", default=False)
        op.add_option("--checksum")
        return op

    def parse(self, args):
        (opts, _extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        return self
