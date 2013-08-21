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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC3_HardDrive(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.biospart = kwargs.get("biospart", None)
        self.partition = kwargs.get("partition", None)
        self.dir = kwargs.get("dir", None)

        self.op = self._getParser()

    def __eq__(self, other):
        if not other:
            return False

        return self.biospart == other.biospart and self.partition == other.partition

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use hard drive installation media\n"

        if self.biospart is not None:
            retval += "harddrive --dir=%s --biospart=%s\n" % (self.dir, self.biospart)
        else:
            retval += "harddrive --dir=%s --partition=%s\n" % (self.dir, self.partition)

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--biospart", dest="biospart")
        op.add_option("--partition", dest="partition")
        op.add_option("--dir", dest="dir", required=1)

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        if self.biospart is None and self.partition is None or \
           self.biospart is not None and self.partition is not None:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified.")))

        return self
