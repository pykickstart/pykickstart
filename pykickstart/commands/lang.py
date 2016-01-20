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

        if self.lang != "":
            retval += "# System language\nlang %s\n" % self.lang

        return retval

    def _getParser(self):
        op = KSOptionParser()
        return op

    def parse(self, args):
        (_opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        if len(extra) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Kickstart command %s requires one argument") % "lang"))

        self.lang = extra[0]
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
        def list_cb (option, opt_str, value, parser):
            for item in value.split(','):
                if item:
                    parser.values.ensure_value(option.dest, []).append(item)

        op = FC3_Lang._getParser(self)
        op.add_option("--addsupport", dest="addsupport", action="callback",
                      callback=list_cb, nargs=1, type="string")
        return op

    def parse(self, args):
        FC3_Lang.parse(self, args)
        (opts, _extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(self.op, opts)
        return self
