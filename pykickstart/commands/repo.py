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
from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6RepoData(BaseData):
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

class FC6Repo(KickstartCommand):
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

        rd = FC6RepoData()
        self._setToObj(op, opts, rd)
        self.add(rd)

    def add(self, newObj):
        self.repoList.append(newObj)
