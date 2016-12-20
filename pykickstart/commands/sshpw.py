#
# Peter Jones <pjones@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
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
from pykickstart.version import F13, F24
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser
import warnings

from pykickstart.i18n import _

class F13_SshPwData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.username = kwargs.get("username", None)
        self.isCrypted = kwargs.get("isCrypted", False)
        self.password = kwargs.get("password", "")
        self.lock = kwargs.get("lock", False)

    def __eq__(self, y):
        if not y:
            return False

        return self.username == y.username

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)

        retval += "sshpw"
        retval += self._getArgsAsStr() + '\n'

        return retval

    def _getArgsAsStr(self):
        retval = ""

        retval += " --username=%s" % self.username
        if self.lock:
            retval += " --lock"
        if self.isCrypted:
            retval += " --iscrypted"
        else:
            retval += " --plaintext"

        retval += " %s" % self.password
        return retval

class F24_SshPwData(F13_SshPwData):
    removedKeywords = F13_SshPwData.removedKeywords
    removedAttrs = F13_SshPwData.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_SshPwData.__init__(self, *args, **kwargs)
        self.sshkey = kwargs.get("sshkey", False)

    def _getArgsAsStr(self):
        retval = ""

        retval += " --username=%s" % self.username
        if self.sshkey:
            retval += ' --sshkey'
        else:
            if self.lock:
                retval += " --lock"
            if self.isCrypted:
                retval += " --iscrypted"
            else:
                retval += " --plaintext"

        retval += " %s" % self.password
        return retval

class F13_SshPw(KickstartCommand):
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
        op = KSOptionParser(prog="sshpw", description="""
                            The installer can start up ssh to provide for
                            interactivity and inspection, just like it can with
                            telnet. The "inst.sshd" option must be specified on
                            the kernel command-line for Anaconda to start an ssh
                            daemon. The sshpw command is used to control the
                            accounts created in the installation environment that
                            may be remotely logged into. For each instance of
                            this command given, a user will be created. These
                            users will not be created on the final system -
                            they only exist for use while the installer is
                            running.

                            Note that by default, root has a blank password. If
                            you don't want any user to be able to ssh in and
                            have full access to your hardware, you must specify
                            sshpw for username root. Also note that if Anaconda
                            fails to parse the kickstart file, it will allow
                            anyone to login as root and have full access to
                            your hardware.""", version=F13)
        op.add_argument("--username", required=True, metavar="<name>",
                        version=F13, help="""
                        Provides the name of the user. This option is required.
                        """)
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true",
                        default=False, version=F13, help="""
                        If this is present, the password argument is assumed to
                        already be encrypted.""")
        op.add_argument("--plaintext", dest="isCrypted", action="store_false",
                        version=F13, help="""
                        If this is present, the password argument is assumed to
                        not be encrypted. This is the default.""")
        op.add_argument("--lock", action="store_true", default=False,
                        version=F13, help="""
                        If this is present, the new user account is locked by
                        default. That is, the user will not be able to login
                        from the console.""")
        op.add_argument("password", metavar="<password>", nargs="*",
                        version=F13, help="""
                        The password string to use.""")
        return op

    def parse(self, args):
        ud = self.dataClass()   # pylint: disable=not-callable
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if not ns.password:
            raise KickstartParseError(_("A single argument is expected for the %s command") % "sshpw", lineno=self.lineno)
        if extra:
            mapping = {"command": "sshpw", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_obj(ns, ud)
        ud.password = " ".join(ns.password)
        ud.lineno = self.lineno

        if ud in self.dataList():
            warnings.warn(_("An ssh user with the name %s has already been defined.") % ud.username, KickstartParseWarning)

        return ud

    def dataList(self):
        return self.sshUserList

    @property
    def dataClass(self):
        return self.handler.SshPwData

class F24_SshPw(F13_SshPw):
    removedKeywords = F13_SshPw.removedKeywords
    removedAttrs = F13_SshPw.removedAttrs

    def _getParser(self):
        op = F13_SshPw._getParser(self)
        op.add_argument("--sshkey", action="store_true", default=False,
                        version=F24, help="""
                        If this is used then the <password> string is
                        interpreted as an ssh key value.""")
        return op
