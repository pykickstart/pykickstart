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
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartValueError, formatErrorMsg
from pykickstart.options import KSOptionParser

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

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

        if self.password != "":
            retval += "# Root password\nrootpw%s %s\n" % (self._getArgsAsStr(), self.password)

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        if len(extra) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw"))

        self.password = extra[0]
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
        op.add_option("--lock", dest="lock", action="store_true", default=False)
        op.add_option("--plaintext", dest="isCrypted", action="store_false")
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
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        if len(extra) != 1 and not self.lock:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "rootpw"))

        if len(extra) == 1:
            self.password = extra[0]

        return self
