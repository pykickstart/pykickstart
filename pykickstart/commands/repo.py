#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007, 2008, 2009 Red Hat, Inc.
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
from textwrap import dedent
from pykickstart.version import versionToLongString
from pykickstart.version import FC6, F8, F11, F13, F14, F15, F21, F27, F30, F33
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartError, KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser, commaSplit, ksboolean

import warnings
from pykickstart.i18n import _

class FC6_RepoData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.baseurl = kwargs.get("baseurl", "")
        self.mirrorlist = kwargs.get("mirrorlist", None)
        self.name = kwargs.get("name", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.name == y.name

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.baseurl:
            retval += "--baseurl=%s" % self.baseurl
        elif self.mirrorlist:
            retval += "--mirrorlist=%s" % self.mirrorlist

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "repo --name=\"%s\" %s\n" % (self.name, self._getArgsAsStr())
        return retval

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
            retval += " --includepkgs=\"%s\"" % ",".join(self.includepkgs)
        if self.excludepkgs:
            retval += " --excludepkgs=\"%s\"" % ",".join(self.excludepkgs)

        return retval

class F11_RepoData(F8_RepoData):
    removedKeywords = F8_RepoData.removedKeywords
    removedAttrs = F8_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F8_RepoData.__init__(self, *args, **kwargs)
        self.ignoregroups = kwargs.get("ignoregroups", None)

    def _getArgsAsStr(self):
        retval = F8_RepoData._getArgsAsStr(self)

        if self.ignoregroups:
            retval += " --ignoregroups=true"
        return retval

class F13_RepoData(F11_RepoData):
    removedKeywords = F11_RepoData.removedKeywords
    removedAttrs = F11_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F11_RepoData.__init__(self, *args, **kwargs)
        self.proxy = kwargs.get("proxy", "")

    def _getArgsAsStr(self):
        retval = F11_RepoData._getArgsAsStr(self)

        if self.proxy:
            retval += " --proxy=\"%s\"" % self.proxy

        return retval

class F14_RepoData(F13_RepoData):
    removedKeywords = F13_RepoData.removedKeywords
    removedAttrs = F13_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F13_RepoData.__init__(self, *args, **kwargs)
        self.noverifyssl = kwargs.get("noverifyssl", False)

    def _getArgsAsStr(self):
        retval = F13_RepoData._getArgsAsStr(self)

        if self.noverifyssl:
            retval += " --noverifyssl"

        return retval

class RHEL6_RepoData(F14_RepoData):
    pass

class F15_RepoData(F14_RepoData):
    pass

class F21_RepoData(F15_RepoData):
    removedKeywords = F15_RepoData.removedKeywords
    removedAttrs = F15_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F15_RepoData.__init__(self, *args, **kwargs)
        self.install = kwargs.get("install", False)

    def _getArgsAsStr(self):
        retval = F15_RepoData._getArgsAsStr(self)

        if self.install:
            retval += " --install"

        return retval

class F27_RepoData(F21_RepoData):
    removedKeywords = F21_RepoData.removedKeywords
    removedAttrs = F21_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_RepoData.__init__(self, *args, **kwargs)
        self.metalink = kwargs.get("metalink", False)

    def _getArgsAsStr(self):
        retval = F21_RepoData._getArgsAsStr(self)

        if self.metalink:
            retval += " --metalink=%s" % self.metalink

        return retval

class F30_RepoData(F27_RepoData):
    removedKeywords = F27_RepoData.removedKeywords
    removedAttrs = F27_RepoData.removedAttrs

    def __init__(self, *args, **kwargs):
        F27_RepoData.__init__(self, *args, **kwargs)
        self.sslcacert = kwargs.get("sslcacert", None)
        self.sslclientcert = kwargs.get("sslclientcert", None)
        self.sslclientkey = kwargs.get("sslclientkey", None)

    def _getArgsAsStr(self):
        retval = F27_RepoData._getArgsAsStr(self)

        if self.sslcacert:
            retval += " --sslcacert=\"%s\"" % self.sslcacert

        if self.sslclientcert:
            retval += " --sslclientcert=\"%s\"" % self.sslclientcert

        if self.sslclientkey:
            retval += " --sslclientkey=\"%s\"" % self.sslclientkey

        return retval

class RHEL7_RepoData(F21_RepoData):
    pass

class RHEL8_RepoData(F30_RepoData):
    pass

class FC6_Repo(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    urlRequired = True

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.repoList = kwargs.get("repoList", [])
        self.exclusive_required_options = [("mirrorlist", "--mirrorlist"),
                                           ("baseurl", "--baseurl")]

    def __str__(self):
        retval = ""
        for repo in self.repoList:
            retval += repo.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="repo", description="""
                            Configures additional yum repositories that may be
                            used as sources for package installation. Multiple
                            repo lines may be specified. By default, anaconda
                            has a configured set of repos taken from
                            /etc/anaconda.repos.d plus a special Installation
                            Repo in the case of a media install. The exact set
                            of repos in this directory changes from release to
                            release and cannot be listed here. There will
                            likely always be a repo named "updates".

                            Note: If you want to enable one of the repos in
                            /etc/anaconda.repos.d that is disabled by default
                            (like "updates"), you should use --name= but none
                            of the other options. anaconda will look for a repo
                            by this name automatically. Providing a baseurl or
                            mirrorlist URL will result in anaconda attempting
                            to add another repo by the same name, which will
                            cause a conflicting repo error.""",
                            version=FC6)
        op.add_argument("--name", required=True, version=FC6, help="""
                        The repo id. This option is required. The RepoId must 
                        not contain spaces (do not confuse with the optional name
                        used by yum). If a repo has a name that conflicts with a 
                        previously added one, the new repo will be ignored. 
                        Because anaconda has a populated list of repos when it 
                        starts, this means that users cannot create new repos 
                        that override these names.
                        Please check /etc/anaconda.repos.d from the operating
                        system you wish to install to see what names are not
                        available.""")
        op.add_argument("--baseurl", version=FC6, help="""
                        The URL for the repository. The variables that may be
                        used in yum repo config files are not supported here.
                        You may use one of either this option or
                        ``--mirrorlist``, not both. If an NFS repository is
                        specified, it should be of the form
                        ``nfs://host:/path/to/repo``. Note that there is a
                        colon after the host. Anaconda passes everything after
                        "nfs:// " directly to the mount command instead of
                        parsing URLs according to RFC 2224. Variable
                        substitution is done for $releasever and $basearch in
                        the url.""")
        op.add_argument("--mirrorlist", version=FC6, help="""
                        The URL pointing at a list of mirrors for the
                        repository. The variables that may be used in yum repo
                        config files are not supported here. You may use one of
                        either this option or ``--baseurl``, not both. Variable
                        substitution is done for $releasever and $basearch in
                        the url.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        # Check that just one of exclusive required options is specified
        used_options = [opt for attr, opt in self.exclusive_required_options
                        if getattr(ns, attr, None)]
        if self.urlRequired and not used_options:
            mapping = {"options_list": ", ".join((opt for attr, opt in self.exclusive_required_options))}
            raise KickstartParseError(_("One of -%(options_list)s options must be specified for repo command.") % mapping, lineno=self.lineno)
        if len(used_options) > 1:
            mapping = {"options_list": ", ".join((opt for opt in used_options))}
            raise KickstartParseError(_("Only one of %(options_list)s options may be specified for repo command.") % mapping, lineno=self.lineno)

        rd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, rd)
        rd.lineno = self.lineno

        # Check for duplicates in the data list.
        if rd in self.dataList():
            warnings.warn(_("A repo with the name %s has already been defined.") % rd.name, KickstartParseWarning)

        return rd

    def dataList(self):
        return self.repoList

    @property
    def dataClass(self):
        return self.handler.RepoData

class F8_Repo(FC6_Repo):
    removedKeywords = FC6_Repo.removedKeywords
    removedAttrs = FC6_Repo.removedAttrs

    def __str__(self):
        retval = ""
        for repo in self.repoList:
            retval += repo.__str__()

        return retval

    def _getParser(self):
        op = FC6_Repo._getParser(self)
        op.add_argument("--cost", type=int, version=F8, help="""
                        An integer value to assign a cost to this repository.
                        If multiple repositories provide the same packages,
                        this number will be used to prioritize which repository
                        will be used before another. Repositories with a lower
                        cost take priority over repositories with higher cost.
                        """)
        op.add_argument("--excludepkgs", type=commaSplit, version=F8, help="""
                        A comma-separated list of package names and globs that
                        must not be fetched from this repository. This is useful
                        if multiple repositories provide the same package and
                        you want to make sure it is not fetched from a particular
                        repository during installation.""")
        op.add_argument("--includepkgs", type=commaSplit, version=F8, help="""
                        A comma-separated list of package names and globs that
                        can be pulled from this repository. Any other packages
                        provided by the repository not on this list will be ignored.
                        This is useful if you want to install just a single package
                        or set of packages from a repository while including all
                        other packages the repository provides.""")
        return op

    def methodToRepo(self):
        if not self.handler.method.url:
            raise KickstartError(_("Method must be a url to be added to the repo list."), lineno=self.handler.method.lineno)
        reponame = "ks-method-url"
        repourl = self.handler.method.url
        rd = self.handler.RepoData(name=reponame, baseurl=repourl)
        return rd

class F11_Repo(F8_Repo):
    removedKeywords = F8_Repo.removedKeywords
    removedAttrs = F8_Repo.removedAttrs

    def _getParser(self):
        op = F8_Repo._getParser(self)
        op.add_argument("--ignoregroups", type=ksboolean, version=F11, help="""
                        This option is used when composing installation trees
                        and has no effect on the installation process itself.
                        It tells the compose tools to not look at the package
                        group information when mirroring trees so as to avoid
                        mirroring large amounts of unnecessary data.""")
        return op

class F13_Repo(F11_Repo):
    removedKeywords = F11_Repo.removedKeywords
    removedAttrs = F11_Repo.removedAttrs

    def _getParser(self):
        op = F11_Repo._getParser(self)
        op.add_argument("--proxy", version=F13, help="""
                        Specify an HTTP/HTTPS/FTP proxy to use just for this
                        repository. This setting does not affect any other
                        repositories, nor how the install.img is fetched on
                        HTTP installs. The various parts of the argument act
                        like you would expect. The syntax is::

                        ``--proxy=[protocol://][username[:password]@]host[:port]``
                        """)
        return op

class F14_Repo(F13_Repo):
    removedKeywords = F13_Repo.removedKeywords
    removedAttrs = F13_Repo.removedAttrs

    def _getParser(self):
        op = F13_Repo._getParser(self)
        op.add_argument("--noverifyssl", action="store_true", version=F14,
                        default=False, help="""
                        For a https repo do not check the server's certificate
                        with what well-known CA validate and do not check the
                        server's hostname matches the certificate's domain name.
                        """)
        return op

class RHEL6_Repo(F14_Repo):
    pass

class F15_Repo(F14_Repo):
    removedKeywords = F14_Repo.removedKeywords
    removedAttrs = F14_Repo.removedAttrs

    urlRequired = False

    def _getParser(self):
        op = F14_Repo._getParser(self)
        for action in op._actions:
            for option in ['--baseurl', '--mirrorlist']:
                if option in action.option_strings:
                    action.help += dedent("""

                    .. versionchanged:: %s

                    ``--mirrorlist`` and ``--baseurl`` are not required anymore!
                    """ % versionToLongString(F15))
        return op

class F21_Repo(F15_Repo):
    removedKeywords = F15_Repo.removedKeywords
    removedAttrs = F15_Repo.removedAttrs

    def _getParser(self):
        op = F15_Repo._getParser(self)
        op.add_argument("--install", action="store_true", version=F21,
                        default=False, help="""
                        Install this repository to the target system so that it
                        can be used after reboot.""")
        return op

class F27_Repo(F21_Repo):
    removedKeywords = F21_Repo.removedKeywords
    removedAttrs = F21_Repo.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_Repo.__init__(self, *args, **kwargs)
        self.exclusive_required_options.append(("metalink", "--metalink"))

    def _getParser(self):
        op = F21_Repo._getParser(self)
        op.add_argument("--metalink", version=F27, help="""
                        The URL pointing at a metalink for the repository. The
                        variables that may be used in yum repo config files are
                        not supported here. You may use only one of the
                        ``--baseurl``, ``--mirrorlist``, or ``--metalink``
                        options. Variable substitution is done for $releasever
                        and $basearch in the url.""")
        for action in op._actions:
            for option in ['--baseurl', '--mirrorlist']:
                if option in action.option_strings:
                    action.help += dedent("""

                    .. versionchanged:: %s

                    ``Another mutually exclusive option --metalink`` was added.
                    """ % versionToLongString(F27))
        return op

class F30_Repo(F27_Repo):
    removedKeywords = F27_Repo.removedKeywords
    removedAttrs = F27_Repo.removedAttrs

    def _getParser(self):
        op = F27_Repo._getParser(self)
        op.add_argument("--sslcacert", version=F30, help="""
                        Path to the file holding one or more SSL certificates
                        to verify the repository host with.

                        **Note** Usage of this parameter is discouraged. It is
                        designed for a specific image building tool use and
                        there are plans for a replacement.""")
        op.add_argument("--sslclientcert", version=F30, help="""
                        Path to the SSL client certificate (PEM file) which
                        should be used to connect to the repository.

                        **Note** Usage of this parameter is discouraged. It is
                        designed for a specific image building tool use and
                        there are plans for a replacement.""")
        op.add_argument("--sslclientkey", version=F30, help="""
                        Path to the private key file associated with the client
                        certificate given with --sslclientcert.

                        **Note** Usage of this parameter is discouraged. It is
                        designed for a specific image building tool use and
                        there are plans for a replacement.""")
        return op

class F33_Repo(F30_Repo):
    removedKeywords = F30_Repo.removedKeywords
    removedAttrs = F30_Repo.removedAttrs

    def _getParser(self):
        op = F30_Repo._getParser(self)
        op.add_argument("--ignoregroups", type=ksboolean, deprecated=F33)
        return op

class RHEL7_Repo(F21_Repo):
    pass

class RHEL8_Repo(F30_Repo):
    pass
