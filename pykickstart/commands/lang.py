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
from pykickstart.version import FC3, F19
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser, commaSplit

from pykickstart.i18n import _

class FC3_Lang(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.lang = kwargs.get("lang", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.lang:
            retval += "# System language\nlang %s\n" % self.lang

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="lang", description="""
            This required command sets the language to use during installation
            and the default language to use on the installed system to ``<id>``.
            This can be the same as any recognized setting for the ``$LANG``
            environment variable, though not all languages are supported during
            installation.

            Certain languages (mainly Chinese, Japanese, Korean, and Indic
            languages) are not supported during text mode installation. If one
            of these languages is specified using the lang command, installation
            will continue in English though the running system will have the
            specified langauge by default.

            The file ``/usr/share/system-config-language/locale-list`` provides a
            list the valid language codes in the first column of each line and
            is part of the system-config-languages package.""", version=FC3)
        op.add_argument("lang", metavar="<lang>", nargs=1, version=FC3,
                        help="Language ID.")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        assert len(ns.lang) == 1

        if extra:
            mapping = {"command": "lang", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.set_to_self(ns)
        self.lang = ns.lang[0]
        return self

class F19_Lang(FC3_Lang):
    removedKeywords = FC3_Lang.removedKeywords
    removedAttrs = FC3_Lang.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Lang.__init__(self, writePriority, *args, **kwargs)
        self.addsupport = kwargs.get("addsupport", [])

        self.op = self._getParser()

    def __str__(self):
        s = FC3_Lang.__str__(self)
        if s and self.addsupport:
            s = s.rstrip()
            s += " --addsupport=%s\n" % ",".join(self.addsupport)
        return s

    def _getParser(self):
        op = FC3_Lang._getParser(self)
        op.add_argument("--addsupport", type=commaSplit,
                        metavar="LOCALE", help="""
                        Install the support packages for the given locales,
                        specified as a comma-separated list. Each locale may be
                        specified in the same ways as the primary language may
                        be, as described above.""", version=F19)
        return op
