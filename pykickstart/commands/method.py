#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007, 2009 Red Hat, Inc.
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

    def __eq__(self, other):
        if not other:
            return False

        if self.method != other.method:
            return False

        if self.method == "harddrive":
            return self.biospart == other.biospart and self.partition == other.partition
        elif self.method == "nfs":
            return self.server == other.server and self.dir == other.dir
        elif self.method == "url":
            return self.url == other.url
        else:
            return True

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.method == "cdrom":
            retval += "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if self.biospart is not None:
                retval += msg + " --biospart=%s\n" % self.biospart
            else:
                retval += msg + " --partition=%s\n" % self.partition
        elif self.method == "nfs":
            retval += "# Use NFS installation media\nnfs --server=%s --dir=%s\n" % (self.server, self.dir)
        elif self.method == "url":
            retval += "# Use network installation\nurl --url=\"%s\"\n" % self.url

        return retval

    def _getParser(self):
        op = KSOptionParser()

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
        (opts, extra) = op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(op, opts)

        if self.currentCmd == "harddrive":
            if self.biospart is None and self.partition is None or \
               self.biospart is not None and self.partition is not None:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of biospart or partition options must be specified."))

        return self

class FC6_Method(FC3_Method):
    removedKeywords = FC3_Method.removedKeywords
    removedAttrs = FC3_Method.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Method.__init__(self, writePriority, *args, **kwargs)

        # Same reason for this attribute as the comment in FC3_Method.
        self.opts = None

    def __eq__(self, other):
        if not FC3_Method.__eq__(self, other):
            return False

        if self.method == "nfs":
            return self.opts == other.opts
        else:
            return True

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.method == "cdrom":
            retval += "# Use CDROM installation media\ncdrom\n"
        elif self.method == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.dir

            if self.biospart is not None:
                retval += msg + " --biospart=%s\n" % self.biospart
            else:
                retval += msg + " --partition=%s\n" % self.partition
        elif self.method == "nfs":
            retval += "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.server, self.dir)
            if self.opts is not None:
                retval += " --opts=\"%s\"" % self.opts
            retval += "\n"
        elif self.method == "url":
            retval += "# Use network installation\nurl --url=\"%s\"\n" % self.url

        return retval

    def _getParser(self):
        op = FC3_Method._getParser(self)

        if self.currentCmd == "nfs":
            op.add_option("--opts", dest="opts")

        return op

class F13_Method(FC6_Method):
    removedKeywords = FC6_Method.removedKeywords
    removedAttrs = FC6_Method.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_Method.__init__(self, *args, **kwargs)

        # And same as all the other __init__ methods.
        self.proxy = ""

    def __eq__(self, other):
        if not FC6_Method.__eq__(self, other):
            return False

        if self.method == "url":
            return self.proxy == other.proxy
        else:
            return True

    def __str__(self):
        retval = FC6_Method.__str__(self)

        if self.method == "url" and self.proxy:
            retval = retval.strip()
            retval += " --proxy=\"%s\"\n" % self.proxy

        return retval

    def _getParser(self):
        op = FC6_Method._getParser(self)

        if self.currentCmd == "url":
            op.add_option("--proxy")

        return op

class F14_Method(F13_Method):
    removedKeywords = F13_Method.removedKeywords
    removedAttrs = F13_Method.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_Method.__init__(self, *args, **kwargs)

        self.noverifyssl = False

    def __eq__(self, other):
        if not F13_Method.__eq__(self, other):
            return False

        if self.method == "url":
            return self.noverifyssl == other.noverifyssl
        else:
            return True

    def __str__(self):
        retval = F13_Method.__str__(self)

        if self.method == "url" and self.noverifyssl:
            retval = retval.strip()
            retval += " --noverifyssl\n"

        return retval

    def _getParser(self):
        op = F13_Method._getParser(self)

        if self.currentCmd == "url":
            op.add_option("--noverifyssl", action="store_true", default=False)

        return op

RHEL6_Method = F14_Method

class F18_Method(F14_Method):
    removedKeywords = F14_Method.removedKeywords
    removedAttrs = F14_Method.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_Method.__init__(self, *args, **kwargs)
        self.mirrorlist = None

    def __eq__(self, other):
        if not F14_Method.__eq__(self, other):
            return False

        if self.method == "url":
            return self.mirrorlist == other.mirrorlist
        else:
            return True

    def __str__(self):
        if self.method == "url":
            retval = KickstartCommand.__str__(self)
            retval += "# Use network installation\n"

            if self.url:
                retval += "url --url=\"%s\"" % self.url
            elif self.mirrorlist:
                retval += "url --mirrorlist=\"%s\"" % self.mirrorlist

            if self.proxy:
                retval += " --proxy=\"%s\"" % self.proxy

            if self.noverifyssl:
                retval += " --noverifyssl"

            return retval + "\n"
        else:
            retval = F14_Method.__str__(self)

        return retval

    def _getParser(self):
        op = F14_Method._getParser(self)

        if self.currentCmd == "url":
            # This overrides the option set in the superclass's _getParser
            # method.  --url is no longer required because you could do
            # --mirrorlist instead.
            op.add_option("--url", dest="url")
            op.add_option("--mirrorlist", dest="mirrorlist")

        return op

    def parse(self, args):
        retval = F14_Method.parse(self, args)

        if self.currentCmd == "url":
            if self.url and self.mirrorlist:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Only one of --url and --mirrorlist may be specified for url command."))

            if not self.url and not self.mirrorlist:
                raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of --url or --mirrorlist must be specified for url command."))

        return retval

class F19_Method(F18_Method):
    removedKeywords = F18_Method.removedKeywords
    removedAttrs = F18_Method.removedAttrs

    def __init__(self, *args, **kwargs):
        F18_Method.__init__(self, *args, **kwargs)
        self.checksum = ""

    def __eq__(self, other):
        if not F18_Method.__eq__(self, other):
            return False

        if self.method == "liveimg":
            return self.url == other.url and self.proxy == other.proxy and \
                   self.noverifyssl == other.noverifyssl and \
                   self.checksum == other.checksum
        else:
            return True

    def __str__(self):
        if self.method == "liveimg":
            retval = KickstartCommand.__str__(self)
            retval += "# Use live disk image installation\n"

            retval += "liveimg --url=\"%s\"" % self.url

            if self.proxy:
                retval += " --proxy=\"%s\"" % self.proxy

            if self.noverifyssl:
                retval += " --noverifyssl"

            if self.checksum:
                retval += " --checksum=\"%s\"" % self.checksum

            return retval + "\n"
        else:
            retval = F18_Method.__str__(self)

        return retval

    def _getParser(self):
        op = F18_Method._getParser(self)

        if self.currentCmd == "liveimg":
            op.add_option("--url", required=1)
            op.add_option("--proxy")
            op.add_option("--noverifyssl", action="store_true", default=False)
            op.add_option("--checksum")

        return op
