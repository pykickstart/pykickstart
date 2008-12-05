#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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

class FC3_Method(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.method = kwargs.get("method", "")

        # Set all these attributes so calls to this command's __call__
        # method can set them.  However we don't want to provide them as
        # arguments to __init__ because method is special.
        self.biospart = None
        self.partition = None
        self.server = None
        self.dir = None
        self.url = None

    def __str__(self):
        if self.method == "cdrom":
            return "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if self.biospart is not None:
                return msg + " --biospart=%s\n" % self.biospart
            else:
                return msg + " --partition=%s\n" % self.partition
        elif self.method == "nfs":
            return "# Use NFS installation media\nnfs --server=%s --dir=%s\n" % (self.server, self.dir)
        elif self.method == "url":
            return "# Use network installation\nurl --url=%s\n" % self.url
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)

        # method = "cdrom" falls through to the return
        if self.currentCmd == "harddrive":
            op.add_option("--biospart", dest="biospart")
            op.add_option("--partition", dest="partition")
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "nfs":
            op.add_option("--server", dest="server", required=1)
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

        return op

    def parse(self, args):
        self.method = self.currentCmd

        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if self.currentCmd == "harddrive":
            if self.biospart is None and self.partition is None or \
               self.biospart is not None and self.partition is not None:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

class FC6_Method(FC3_Method):
    removedKeywords = FC3_Method.removedKeywords
    removedAttrs = FC3_Method.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Method.__init__(self, writePriority, *args, **kwargs)

        # Same reason for this attribute as the comment in FC3_Method.
        self.opts = None

    def __str__(self):
        if self.method == "cdrom":
            return "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if self.biospart is not None:
                return msg + " --biospart=%s\n" % self.biospart
            else:
                return msg + " --partition=%s\n" % self.partition
        elif self.method == "nfs":
            retval = "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.server, self.dir)
            if self.opts is not None:
                retval += " --opts=\"%s\"" % self.opts

            return retval + "\n"
        elif self.method == "url":
            return "# Use network installation\nurl --url=%s\n" % self.url
        else:
            return ""

    def _getParser(self):
        op = FC3_Method._getParser(self)

        if self.currentCmd == "nfs":
            op.add_option("--opts", dest="opts")

        return op
