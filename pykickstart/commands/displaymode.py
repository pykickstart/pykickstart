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
from pykickstart.version import FC3, F26
from pykickstart.base import KickstartCommand
from pykickstart.constants import DISPLAY_MODE_CMDLINE, DISPLAY_MODE_GRAPHICAL, \
                                  DISPLAY_MODE_TEXT
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_DisplayMode(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.displayMode = kwargs.get("displayMode", None)
        self.op = self._getParser()

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

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if self.currentCmd == "cmdline":
            self.displayMode = DISPLAY_MODE_CMDLINE
        elif self.currentCmd == "graphical":
            self.displayMode = DISPLAY_MODE_GRAPHICAL
        elif self.currentCmd == "text":
            self.displayMode = DISPLAY_MODE_TEXT
        else:
            raise KickstartParseError(_("Unknown command %s") % self.currentCmd, lineno=self.lineno)

        return self

    def _getParser(self):
        op = KSOptionParser(prog="graphical|text|cmdline", version=FC3,
                            description="""
                            Controls which display mode will be used during
                            installation. If ``cmdline`` is chosen all required
                            installation options must be configured via kickstart
                            otherwise the installation will fail.""")
        return op

class F26_DisplayMode(FC3_DisplayMode):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_DisplayMode.__init__(self, writePriority, args, kwargs)
        self.nonInteractive = kwargs.get("nonInteractive", False)

    def __str__(self):
        retval = super(F26_DisplayMode, self).__str__()

        if self.nonInteractive:
            retval = retval.rstrip()
            retval += " --non-interactive\n"

        return retval

    def _getParser(self):
        op = FC3_DisplayMode._getParser(self)
        op.add_argument("--non-interactive", action="store_true", default=False,
                      dest="nonInteractive", version=F26, help="""
                       Perform the installation in a completely non-interactive mode.
                       This mode will kill the installation when user interaction will be
                       required. Can't be used with ``cmdline`` mode. This option is
                       especially useful for automated testing purpose.""")
        return op

    def parse(self, args):
        FC3_DisplayMode.parse(self, args)

        if self.currentCmd == "cmdline" and self.nonInteractive:
            msg = _("Kickstart command cmdline does not support --non-interactive parameter")
            raise KickstartParseError(msg, lineno=self.lineno)

        return self
