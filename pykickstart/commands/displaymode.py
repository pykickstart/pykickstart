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
from pykickstart.constants import DISPLAY_MODE_CMDLINE, DISPLAY_MODE_GRAPHICAL, \
                                  DISPLAY_MODE_TEXT
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_DisplayMode(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.displayMode = kwargs.get("displayMode", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.displayMode is None:
            return retval

        if self.displayMode == DISPLAY_MODE_CMDLINE:
            retval += "cmdline\n"
        elif self.displayMode == DISPLAY_MODE_GRAPHICAL:
            retval += "# Use graphical install\ngraphical\n"
        elif self.displayMode == DISPLAY_MODE_TEXT:
            retval += "# Use text mode install\ntext\n"

        return retval

    def _getParser(self):
        op = KSOptionParser()
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(self.op, opts)

        if len(extra) > 0:
            msg = _("Kickstart command %s does not take any arguments") % self.currentCmd
            raise KickstartParseError(formatErrorMsg(self.lineno, msg))

        if self.currentCmd == "cmdline":
            self.displayMode = DISPLAY_MODE_CMDLINE
        elif self.currentCmd == "graphical":
            self.displayMode = DISPLAY_MODE_GRAPHICAL
        elif self.currentCmd == "text":
            self.displayMode = DISPLAY_MODE_TEXT

        return self

class F26_DisplayMode(FC3_DisplayMode):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_DisplayMode.__init__(self, writePriority, args, kwargs)
        self.op = self._getParser()
        self.nonInteractive = kwargs.get("nonInteractive", False)

    def __str__(self):
        retval = super(F26_DisplayMode, self).__str__()

        if self.nonInteractive:
            retval = retval.rstrip()
            retval += " --non-interactive\n"

        return retval

    def _getParser(self):
        op = FC3_DisplayMode._getParser(self)
        op.add_option("--non-interactive", action="store_true", default=False,
                      dest="nonInteractive")
        return op

    def parse(self, args):
        FC3_DisplayMode.parse(self, args)

        if self.currentCmd == "cmdline" and self.nonInteractive:
            msg = _("Kickstart command cmdline does not support --non-interactive parameter")
            raise KickstartParseError(formatErrorMsg(self.lineno, msg))

        return self
