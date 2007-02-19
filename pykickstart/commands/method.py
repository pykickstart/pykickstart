#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3Method(KickstartCommand):
    def __init__(self, writePriority=0, method=""):
        KickstartCommand.__init__(self, writePriority)
        self.method = method

    def __str__(self):
        if self.method == "cdrom":
            return "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if hasattr(self, "biospart"):
                return msg + " --biospart=%s\n" % getattr(self, "biospart")
            else:
                return msg + " --partition=%s\n" % getattr(self, "partition")
        elif self.method == "nfs":
            return "# Use NFS installation media\nnfs --server=%s --dir=%s\n" % (self.server, self.dir)
        elif self.method == "url":
            return "# Use network installation\nurl --url=%s\n" % self.url
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)

        self.method = self.currentCmd

        if self.currentCmd == "cdrom":
            return
        elif self.currentCmd == "harddrive":
            op.add_option("--biospart", dest="biospart")
            op.add_option("--partition", dest="partition")
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "nfs":
            op.add_option("--server", dest="server", required=1)
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

        (opts, extra) = op.parse_args(args=args)

        if self.currentCmd == "harddrive":
            if (getattr(opts, "biospart") == None and getattr(opts, "partition") == None) or \
               (getattr(opts, "biospart") != None and getattr(opts, "partition") != None):

                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

        self._setToSelf(op, opts)

class FC6Method(FC3Method):
    def __init__(self, writePriority=0, method=""):
        FC3Method.__init__(self, writePriority, method)

    def __str__(self):
        if self.method == "cdrom":
            return "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if hasattr(self, "biospart"):
                return msg + " --biospart=%s\n" % getattr(self, "biospart")
            else:
                return msg + " --partition=%s\n" % getattr(self, "partition")
        elif self.method == "nfs":
            retval = "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.server, self.dir)
            if hasattr(self, "opts"):
                retval += " --opts=\"%s\"" % self.opts

            return retval + "\n"
        elif self.method == "url":
            return "# Use network installation\nurl --url=%s\n" % self.url
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)

        self.method = self.currentCmd

        if self.currentCmd == "cdrom":
            return
        elif self.currentCmd == "harddrive":
            op.add_option("--biospart", dest="biospart")
            op.add_option("--partition", dest="partition")
            op.add_option("--dir", dest="dir", required=1)
        elif self.currentCmd == "nfs":
            op.add_option("--server", dest="server", required=1)
            op.add_option("--dir", dest="dir", required=1)
            op.add_option("--opts", dest="opts")
        elif self.currentCmd == "url":
            op.add_option("--url", dest="url", required=1)

        (opts, extra) = op.parse_args(args=args)

        if self.currentCmd == "harddrive":
            if (getattr(opts, "biospart") == None and getattr(opts, "partition") == None) or \
               (getattr(opts, "biospart") != None and getattr(opts, "partition") != None):

                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

        self._setToSelf(op, opts)
