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
from pykickstart.errors import KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

from pykickstart import _

class FC3_Url(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.url = kwargs.get("url", None)

        self.op = self._getParser()

    def __eq__(self, other):
        if not other:
            return False

        return self.url == other.url

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.seen:
            retval += "# Use network installation\nurl --url=\"%s\"\n" % self.url

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--url", dest="url", required=1)
        return op

    def parse(self, args):
        (opts, _extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        return self

class F13_Url(FC3_Url):
    removedKeywords = FC3_Url.removedKeywords
    removedAttrs = FC3_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_Url.__init__(self, *args, **kwargs)
        self.proxy = kwargs.get("proxy", "")

    def __eq__(self, other):
        if not FC3_Url.__eq__(self, other):
            return False

        return self.proxy == other.proxy

    def __str__(self):
        retval = FC3_Url.__str__(self)

        if self.seen and self.proxy:
            retval = retval.strip()
            retval += " --proxy=\"%s\"\n" % self.proxy

        return retval

    def _getParser(self):
        op = FC3_Url._getParser(self)
        op.add_option("--proxy")
        return op

class F14_Url(F13_Url):
    removedKeywords = F13_Url.removedKeywords
    removedAttrs = F13_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_Url.__init__(self, *args, **kwargs)
        self.noverifyssl = kwargs.get("noverifyssl", False)

    def __eq__(self, other):
        if not F13_Url.__eq__(self, other):
            return False

        return self.noverifyssl == other.noverifyssl

    def __str__(self):
        retval = F13_Url.__str__(self)

        if self.seen and self.noverifyssl:
            retval = retval.strip()
            retval += " --noverifyssl\n"

        return retval

    def _getParser(self):
        op = F13_Url._getParser(self)
        op.add_option("--noverifyssl", action="store_true", default=False)
        return op

RHEL6_Url = F14_Url

class F18_Url(F14_Url):
    removedKeywords = F14_Url.removedKeywords
    removedAttrs = F14_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_Url.__init__(self, *args, **kwargs)
        self.mirrorlist = kwargs.get("mirrorlist", None)

    def __eq__(self, other):
        if not F14_Url.__eq__(self, other):
            return False

        return self.mirrorlist == other.mirrorlist

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

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

    def _getParser(self):
        op = F14_Url._getParser(self)
        # This overrides the option set in the superclass's _getParser
        # method.  --url is no longer required because you could do
        # --mirrorlist instead.
        op.add_option("--url", dest="url")
        op.add_option("--mirrorlist", dest="mirrorlist")
        return op

    def parse(self, args):
        retval = F14_Url.parse(self, args)

        if self.url and self.mirrorlist:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Only one of --url and --mirrorlist may be specified for url command.")))

        if not self.url and not self.mirrorlist:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("One of --url or --mirrorlist must be specified for url command.")))

        return retval
