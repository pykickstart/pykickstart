#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from pykickstart.version import FC3, F8
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

import six

class FC3_RootPw(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.isCrypted = kwargs.get("isCrypted", False)
        self.password = kwargs.get("password", "")

    def _getArgsAsStr(self):
        retval = ""

        if self.isCrypted:
            retval += " --iscrypted"

        return retval

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.password:
            if isinstance(self.password, six.binary_type) and b'#' in self.password:
                password = '\"' + self.password + '\"'
            elif not isinstance(self.password, six.binary_type) and u'#' in self.password:
                password = '\"' + self.password + '\"'
            else:
                password = self.password

            retval += "# Root password\nrootpw%s %s\n" % (self._getArgsAsStr(), password)

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="rootpw", description="""
                            This required command sets the system's root
                            password.""", version=FC3)
        op.add_argument('password', metavar='<password>', nargs='?', version=FC3,
                        help="The desired root password.")
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true",
                        default=False, version=FC3, help="""
                        If this is present, the password argument is assumed to
                        already be encrypted. To create an encrypted password
                        you can use python::

                        ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Salt"))'``

                        This will generate sha512 crypt of your password using
                        your provided salt.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if not ns.password:
            raise KickstartParseError(_("A single argument is expected for the %s command") % "rootpw", lineno=self.lineno)
        elif extra:
            mapping = {"command": "rootpw", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_self(ns)
        return self

class F8_RootPw(FC3_RootPw):
    removedKeywords = FC3_RootPw.removedKeywords
    removedAttrs = FC3_RootPw.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_RootPw.__init__(self, writePriority, *args, **kwargs)
        self.lock = kwargs.get("lock", False)

    def _getArgsAsStr(self):
        retval = FC3_RootPw._getArgsAsStr(self)

        if self.lock:
            retval += " --lock"

        if not self.isCrypted:
            retval += " --plaintext"

        return retval

    def _getParser(self):
        op = FC3_RootPw._getParser(self)
        op.add_argument("--lock", action="store_true", default=False,
                        version=F8, help="""
                        If this is present, the root account is locked by
                        default. That is, the root user will not be able to
                        login from the console. When this option is present
                        the <password> argument is not required.""")
        op.add_argument("--plaintext", dest="isCrypted", action="store_false",
                        version=F8, help="""
                        The password argument is assumed to not be encrypted.
                        This is the default!""")
        return op

class F18_RootPw(F8_RootPw):
    removedKeywords = F8_RootPw.removedKeywords
    removedAttrs = F8_RootPw.removedAttrs

    def __str__(self):
        retval = F8_RootPw.__str__(self)

        if not retval and self.lock:
            retval = "#Root password\nrootpw --lock\n"

        return retval

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if not (ns.password or ns.lock):
            raise KickstartParseError(_("A single argument is expected for the %s command") % "rootpw", lineno=self.lineno)
        elif extra:
            mapping = {"command": "rootpw", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_self(ns)
        return self
