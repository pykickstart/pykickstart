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

import string

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC6_RepoData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.baseurl = kwargs.get("baseurl", "")
        self.mirrorlist = kwargs.get("mirrorlist", None)
        self.name = kwargs.get("name", "")

    def _getArgsAsStr(self):
        retval = ""

        if self.baseurl:
            retval += "--baseurl=%s" % self.baseurl
        elif self.mirrorlist:
            retval += "--mirrorlist=%s" % self.mirrorlist

        return retval

    def __str__(self):
        return "repo --name=%s %s\n" % (self.name, self._getArgsAsStr())

class F8_RepoData(FC6_RepoData):
    removedKeywords = FC6_RepoData.removedKeywords
    removedAttrs = FC6_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_RepoData.__init__(self, *args, **kwargs)
        self.cost = kwargs.get("cost", None)
        self.includepkgs = kwargs.get("includepkgs", [])
        self.excludepkgs = kwargs.get("excludepkgs", [])

    def _getArgsAsStr(self):
        retval = FC6_RepoData._getArgsAsStr(self)

        if self.cost:
            retval += " --cost=%s" % self.cost
        if self.includepkgs:
            retval += " --includepkgs=\"%s\"" % string.join(self.includepkgs, ",")
        if self.excludepkgs:
            retval += " --excludepkgs=\"%s\"" % string.join(self.excludepkgs, ",")

        return retval

class FC6_Repo(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.repoList = kwargs.get("repoList", [])

    def __str__(self):
        retval = ""
        for repo in self.repoList:
            retval += repo.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--name", dest="name", required=1)
        op.add_option("--baseurl")
        op.add_option("--mirrorlist")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)

        # This is lame, but I can't think of a better way to make sure only
        # one of these two is specified.
        if opts.baseurl and opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Only one of --baseurl and --mirrorlist may be specified for repo command."))

        if not opts.baseurl and not opts.mirrorlist:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of --baseurl or --mirrorlist must be specified for repo command."))

        rd = self.handler.RepoData()
        self._setToObj(self.op, opts, rd)
        self.add(rd)

    def add(self, newObj):
        self.repoList.append(newObj)

class F8_Repo(FC6_Repo):
    removedKeywords = FC6_Repo.removedKeywords
    removedAttrs = FC6_Repo.removedAttrs

    def __str__(self):
        retval = ""
        for repo in self.repoList:
            retval += repo.__str__()

        return retval

    def _getParser(self):
        def list_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = FC6_Repo._getParser(self)
        op.add_option("--cost", action="store", type="int")
        op.add_option("--excludepkgs", action="callback", callback=list_cb,
                      nargs=1, type="string")
        op.add_option("--includepkgs", action="callback", callback=list_cb,
                      nargs=1, type="string")
        return op

    def methodToRepo(self):
        if not self.handler.method.url:
            raise KickstartError, formatErrorMsg(self.handler.method.lineno, msg=_("Method must be a url to be added to the repo list."))
        reponame = "ks-method-url"
        repourl = self.handler.method.url
        rd = self.handler.RepoData(name=reponame, baseurl=repourl)
        self.add(rd)

