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
from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6_RepoData(BaseData):
    def __init__(self, baseurl="", mirrorlist="", name=""):
        BaseData.__init__(self)
        self.baseurl = baseurl
        self.mirrorlist = mirrorlist
        self.name = name

    def __str__(self):
        if self.baseurl:
            urlopt = "--baseurl=%s" % self.baseurl
        elif self.mirrorlist:
            urlopt = "--mirrorlist=%s" % self.mirrorlist

        return "repo --name=%s %s\n" % (self.name, urlopt)

class FC6_Repo(KickstartCommand):
    def __init__(self, writePriority=0, repoList=None):
        KickstartCommand.__init__(self, writePriority)

        if repoList == None:
            repoList = []

        self.repoList = repoList

    def __str__(self):
        retval = ""
        for repo in self.repoList:
            retval += repo.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", required=1)
        op.add_option("--baseurl")
        op.add_option("--mirrorlist")

        (opts, extra) = op.parse_args(args=args)

        # This is lame, but I can't think of a better way to make sure only
        # one of these two is specified.
        if opts.baseurl and opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Only one of --baseurl and --mirrorlist may be specified for repo command."))

        if not opts.baseurl and not opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of --baseurl or --mirrorlist must be specified for repo command."))

        rd = FC6_RepoData()
        self._setToObj(op, opts, rd)
        self.add(rd)

    def add(self, newObj):
        self.repoList.append(newObj)
