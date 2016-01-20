#
# Brian C. Lane <bcl@redhat.com>
#
# Copyright 2014 Red Hat, Inc.
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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser
import warnings

from pykickstart.i18n import _

class F22_SshKeyData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.username = kwargs.get("username", None)
        self.key = kwargs.get("key", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.username == y.username

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)

        retval += "sshkey"
        retval += self._getArgsAsStr() + '\n'

        return retval

    def _getArgsAsStr(self):
        retval = ""

        retval += " --username=%s" % self.username
        retval += ' "%s"' % self.key
        return retval

class F22_SshKey(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.sshUserList = kwargs.get("sshUserList", [])

    def __str__(self):
        retval = ""
        for user in self.sshUserList:
            retval += user.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--username", required=True)
        return op

    def parse(self, args):
        ud = self.handler.SshKeyData()
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) != 1:
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("A single argument is expected for the %s command") % "sshkey"))
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "sshkey", "options": extra}
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

        self.set_to_obj(ns, ud)
        ud.key = extra[0]
        ud.lineno = self.lineno

        if ud in self.dataList():
            warnings.warn(_("An ssh user with the name %s has already been defined.") % ud.username)

        return ud

    def dataList(self):
        return self.sshUserList
