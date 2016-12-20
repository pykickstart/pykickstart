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
from pykickstart.errors import KickstartParseWarning
from pykickstart.version import FC6, F8, F12, F19, F24
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser, commaSplit

import warnings
import six
from pykickstart.i18n import _

class FC6_UserData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.groups = kwargs.get("groups", [])
        self.homedir = kwargs.get("homedir", "")
        self.isCrypted = kwargs.get("isCrypted", False)
        self.name = kwargs.get("name", "")
        self.password = kwargs.get("password", "")
        self.shell = kwargs.get("shell", "")
        self.uid = kwargs.get("uid", None)

    def __eq__(self, y):
        if not y:
            return False

        return self.name == y.name

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)

        args = self._getArgsAsStr()
        if args:
            retval += "user%s\n" % args

        return retval

    def _getArgsAsStr(self):
        retval = ""

        if self.groups:
            retval += " --groups=%s" % ",".join(self.groups)
        if self.homedir:
            retval += " --homedir=%s" % self.homedir
        if self.name:
            retval += " --name=%s" % self.name
        if self.password:
            if isinstance(self.password, six.binary_type) and b'#' in self.password:
                retval += " --password=\"%s\"" % self.password
            elif not isinstance(self.password, six.binary_type) and u'#' in self.password:
                retval += " --password=\"%s\"" % self.password
            else:
                retval += " --password=%s" % self.password
        if self.isCrypted:
            retval += " --iscrypted"
        if self.shell:
            retval += " --shell=%s" % self.shell
        if self.uid:
            retval += " --uid=%s" % self.uid

        return retval

class F8_UserData(FC6_UserData):
    removedKeywords = FC6_UserData.removedKeywords
    removedAttrs = FC6_UserData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_UserData.__init__(self, *args, **kwargs)
        self.lock = kwargs.get("lock", False)

    def _getArgsAsStr(self):
        retval = FC6_UserData._getArgsAsStr(self)

        if self.lock:
            retval += " --lock"

        return retval

class F12_UserData(F8_UserData):
    removedKeywords = F8_UserData.removedKeywords
    removedAttrs = F8_UserData.removedAttrs

    def __init__(self, *args, **kwargs):
        F8_UserData.__init__(self, *args, **kwargs)
        self.gecos = kwargs.get("gecos", "")

    def _getArgsAsStr(self):
        retval = F8_UserData._getArgsAsStr(self)

        if self.gecos:
            retval += " --gecos=\"%s\"" % (self.gecos,)

        return retval

class F19_UserData(F12_UserData):
    removedKeywords = F12_UserData.removedKeywords
    removedAttrs = F12_UserData.removedAttrs

    def __init__(self, *args, **kwargs):
        F12_UserData.__init__(self, *args, **kwargs)
        self.gid = kwargs.get("gid", None)

    def _getArgsAsStr(self):
        retval = F12_UserData._getArgsAsStr(self)

        if self.gid:
            retval += " --gid=%d" % (self.gid,)

        return retval


class FC6_User(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.userList = kwargs.get("userList", [])

    def __str__(self):
        retval = ""
        for user in self.userList:
            retval += user.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="user", description="""
                            Creates a new user on the system.""",
                            version=FC6)
        op.add_argument("--groups", type=commaSplit, version=FC6, help="""
                        In addition to the default group, a comma separated
                        list of group names the user should belong to. Any groups
                        that do not already exist will be created. If the group
                        already exists with a different GID, an error will
                        be raised.""",
                        metavar="<group1>,<group2>,...,<groupN>")
        op.add_argument("--homedir", version=FC6, help="""
                        The home directory for the user. If not provided, this
                        defaults to /home/.""")
        op.add_argument("--iscrypted", dest="isCrypted", action="store_true",
                        default=False, version=FC6, help="""
                        If specified, consider the password provided by
                        ``--password`` already encrypted. This is the default.
                        """)
        op.add_argument("--name", required=True, version=FC6, help="""
                        Provides the name of the user. This option is required.
                        """)
        op.add_argument("--password", version=FC6, help="""
                        The new user's password. If not provided, the account
                        will be locked by default. If this is present, the
                        password argument is assumed to already be encrypted.
                        ``--plaintext`` has the opposite effect - the password
                        argument is assumed to not be encrypted. To create an
                        encrypted password you can use python::

                        ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Sault"))'``

                        This will generate sha512 crypt of your password using
                        your provided salt.""")
        op.add_argument("--shell", version=FC6, help="""
                        The user's login shell. If not provided, this defaults
                        to the system default.""")
        op.add_argument("--uid", type=int, metavar="INT", version=FC6, help="""
                        The user's UID. If not provided, this defaults to the
                        next available non-system UID.""")
        return op

    def parse(self, args):
        ud = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_obj(ns, ud)
        ud.lineno = self.lineno

        # Check for duplicates in the data list.
        if ud in self.dataList():
            warnings.warn(_("A user with the name %s has already been defined.") % ud.name, KickstartParseWarning)

        return ud

    def dataList(self):
        return self.userList

    @property
    def dataClass(self):
        return self.handler.UserData

class F8_User(FC6_User):
    removedKeywords = FC6_User.removedKeywords
    removedAttrs = FC6_User.removedAttrs

    def _getParser(self):
        op = FC6_User._getParser(self)
        op.add_argument("--lock", action="store_true", default=False,
                        version=F8, help="""
                        If this is present, the new user account is locked by
                        default. That is, the user will not be able to login
                        from the console.""")
        op.add_argument("--plaintext", dest="isCrypted", version=F8,
                        action="store_false", help="""
                        If specified, consider the password provided by
                        ``--password`` to be plain text.""")
        return op

class F12_User(F8_User):
    removedKeywords = F8_User.removedKeywords
    removedAttrs = F8_User.removedAttrs

    def _getParser(self):
        op = F8_User._getParser(self)
        op.add_argument("--gecos", version=F12, help="""
                        Provides the GECOS information for the user. This is a
                        string of various system-specific fields separated by a
                        comma. It is frequently used to specify the user's full
                        name, office number, and the like. See ``man 5 passwd``
                        for more details.""")
        return op

class F19_User(F12_User):
    removedKeywords = F12_User.removedKeywords
    removedAttrs = F12_User.removedAttrs

    def _getParser(self):
        op = F12_User._getParser(self)
        op.add_argument("--gid", type=int, metavar="INT", version=F19, help="""
                        The GID of the user's primary group. If not provided,
                        this defaults to the next available non-system GID.""")
        return op

class F24_User(F19_User):
    removedKeywords = F19_User.removedKeywords
    removedAttrs = F19_User.removedAttrs

    def _getParser(self):
        op = F19_User._getParser(self)
        op.add_argument("--groups", type=commaSplit, version=F24, help="""
                        The group name can optionally be followed by a GID in
                        parenthesis, for example, ``newgroup(5002)``.""")
        return op
