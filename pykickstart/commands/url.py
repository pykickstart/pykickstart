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
from pykickstart.version import FC3, F13, F14, F18, RHEL7, F27, RHEL8
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

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
        op = KSOptionParser(prog="url", description="""
                            Install from an installation tree on a remote server
                            via FTP or HTTP.""", version=FC3)
        op.add_argument("--url", required=True, version=FC3, help="""
                        The URL to install from. Variable substitution is done
                        for $releasever and $basearch in the url.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
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
        op.add_argument("--proxy", metavar="URL", version=F13,
                        help="""
                        Specify an HTTP/HTTPS/FTP proxy to use while performing
                        the install. The various parts of the argument act like
                        you would expect. The syntax is::

                            [protocol://][username[:password]@]host[:port]
                        """)
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
        op.add_argument("--noverifyssl", action="store_true", version=F14,
                        default=False, help="""
                        For a tree on a HTTPS server do not check the server's
                        certificate with what well-known CA validate and do not
                        check the server's hostname matches the certificate's
                        domain name.""")
        return op

class RHEL6_Url(F14_Url):
    pass

class F18_Url(F14_Url):
    removedKeywords = F14_Url.removedKeywords
    removedAttrs = F14_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F14_Url.__init__(self, *args, **kwargs)
        self.mirrorlist = kwargs.get("mirrorlist", None)
        self.exclusive_required_options = [("mirrorlist", "--mirrorlist"),
                                           ("url", "--url")]

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
        op.add_argument("--url", version=F18, help="""
                        This parameter is no longer required because you could
                        use ``--mirrorlist`` instead.""")
        op.add_argument("--mirrorlist", metavar="URL", version=F18, help="""
                        The mirror URL to install from. Variable substitution
                        is done for $releasever and $basearch in the url.""")
        return op

    def parse(self, args):
        retval = F14_Url.parse(self, args)

        ns = self.op.parse_args(args=args, lineno=self.lineno)
        # Check that just one of exclusive required options is specified
        used_options = [opt for attr, opt in self.exclusive_required_options
                        if getattr(ns, attr, None)]
        if len(used_options) == 0:
            mapping = {"options_list": ", ".join((opt for attr, opt in self.exclusive_required_options))}
            raise KickstartParseError(_("One of -%(options_list)s options must be specified for url command.") % mapping, lineno=self.lineno)
        if len(used_options) > 1:
            mapping = {"options_list": ", ".join((opt for opt in used_options))}
            raise KickstartParseError(_("Only one of %(options_list)s options may be specified for url command.") % mapping, lineno=self.lineno)

        return retval

class RHEL7_Url(F18_Url):
    removedKeywords = F18_Url.removedKeywords
    removedAttrs = F18_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F18_Url.__init__(self, *args, **kwargs)
        self.sslcacert = kwargs.get("sslcacert", None)
        self.sslclientcert = kwargs.get("sslclientcert", None)
        self.sslclientkey = kwargs.get("sslclientkey", None)

    def __str__(self):
        retval = F18_Url.__str__(self)
        if not self.seen:
            return retval

        retval = retval[:-1]  # strip '\n'

        if self.sslcacert:
            retval += " --sslcacert=\"%s\"" % self.sslcacert

        if self.sslclientcert:
            retval += " --sslclientcert=\"%s\"" % self.sslclientcert

        if self.sslclientkey:
            retval += " --sslclientkey=\"%s\"" % self.sslclientkey

        return retval + "\n"

    def _getParser(self):
        op = F18_Url._getParser(self)
        op.add_argument("--sslcacert", version=RHEL7, help="""
                        Path to the file holding one or more SSL certificates
                        to verify the repository host with.""")
        op.add_argument("--sslclientcert", version=RHEL7, help="""
                        Path to the SSL client certificate (PEM file) which
                        should be used to connect to the repository.""")
        op.add_argument("--sslclientkey", version=RHEL7, help="""
                        Path to the private key file associated with the client
                        certificate given with --sslclientcert.""")
        return op

class F27_Url(F18_Url):
    removedKeywords = F18_Url.removedKeywords
    removedAttrs = F18_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F18_Url.__init__(self, *args, **kwargs)
        self.metalink = kwargs.get("metalink", None)
        self.exclusive_required_options.append(("metalink", "--metalink"))

    def __eq__(self, other):
        if not F18_Url.__eq__(self, other):
            return False

        return self.metalink == other.metalink

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use network installation\n"

        if self.url:
            retval += "url --url=\"%s\"" % self.url
        elif self.mirrorlist:
            retval += "url --mirrorlist=\"%s\"" % self.mirrorlist
        elif self.metalink:
            retval += "url --metalink=\"%s\"" % self.metalink

        if self.proxy:
            retval += " --proxy=\"%s\"" % self.proxy

        if self.noverifyssl:
            retval += " --noverifyssl"

        return retval + "\n"

    def _getParser(self):
        op = F18_Url._getParser(self)
        op.add_argument("--metalink", metavar="URL", version=F27, help="""
                        The metalink URL to install from. Variable substitution
                        is done for $releasever and $basearch in the url.""")
        return op

class RHEL8_Url(F27_Url):
    removedKeywords = F27_Url.removedKeywords
    removedAttrs = F27_Url.removedAttrs

    def __init__(self, *args, **kwargs):
        F27_Url.__init__(self, *args, **kwargs)
        self.sslcacert = kwargs.get("sslcacert", None)
        self.sslclientcert = kwargs.get("sslclientcert", None)
        self.sslclientkey = kwargs.get("sslclientkey", None)

    def __str__(self):
        retval = F27_Url.__str__(self)
        if not self.seen:
            return retval

        retval = retval[:-1]  # strip '\n'

        if self.sslcacert:
            retval += " --sslcacert=\"%s\"" % self.sslcacert

        if self.sslclientcert:
            retval += " --sslclientcert=\"%s\"" % self.sslclientcert

        if self.sslclientkey:
            retval += " --sslclientkey=\"%s\"" % self.sslclientkey

        return retval + "\n"

    def _getParser(self):
        op = F27_Url._getParser(self)
        op.add_argument("--sslcacert", version=RHEL8, help="""
                        Path to the file holding one or more SSL certificates
                        to verify the repository host with.""")
        op.add_argument("--sslclientcert", version=RHEL8, help="""
                        Path to the SSL client certificate (PEM file) which
                        should be used to connect to the repository.""")
        op.add_argument("--sslclientkey", version=RHEL8, help="""
                        Path to the private key file associated with the client
                        certificate given with --sslclientcert.""")
        return op
