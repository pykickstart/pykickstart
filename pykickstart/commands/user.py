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
import string

from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6_UserData(BaseData):
    def __init__(self, groups=None, homedir="", isCrypted=False, name="",
                 password="", shell="", uid=None):
        BaseData.__init__(self)

        if groups == None:
            groups = []

        self.groups = groups
        self.homedir = homedir
        self.isCrypted = isCrypted
        self.name = name
        self.password = password
        self.shell = shell
        self.uid = uid

    def __str__(self):
        retval = "user"

        if len(self.groups) > 0:
            retval += " --groups=%s" % string.join(self.groups, ",")
        if self.homedir:
            retval += " --homedir=%s" % self.homedir
        if self.name:
            retval += " --name=%s" % self.name
        if self.password:
            retval += " --password=%s" % self.password
        if self.isCrypted:
            retval += " --iscrypted"
        if self.shell:
            retval += " --shell=%s" % self.shell
        if self.uid:
            retval += " --uid=%s" % self.uid

        return retval + "\n"

class FC6_User(KickstartCommand):
    def __init__(self, writePriority=0, userList=None):
        KickstartCommand.__init__(self, writePriority)

        if userList == None:
            userList = []

        self.userList = userList

    def __str__(self):
        retval = ""
        for user in self.userList:
            retval += user.__str__()

        return retval

    def parse(self, args):
        def groups_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--groups", dest="groups", action="callback",
                      callback=groups_cb, nargs=1, type="string")
        op.add_option("--homedir")
        op.add_option("--iscrypted", dest="isCrypted", action="store_true",
                      default=False)
        op.add_option("--name", required=1)
        op.add_option("--password")
        op.add_option("--shell")
        op.add_option("--uid", type="int")

        ud = FC6_UserData()
        (opts, extra) = op.parse_args(args=args)
        self._setToObj(op, opts, ud)
        self.add(ud)

    def add(self, newObj):
        self.userList.append(newObj)
