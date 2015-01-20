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

import gettext
from pykickstart import _

class FC3_Keyboard(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.keyboard = kwargs.get("keyboard", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.keyboard != "":
            retval += "# System keyboard\nkeyboard %s\n" % self.keyboard

        return retval

    def _getParser(self):
        op = KSOptionParser()
        return op

    def parse(self, args):
        (_opts, extra) = self.op.parse_args(args=args, lineno=self.lineno) 

        if len(extra) != 1:
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Kickstart command %s requires one argument") % "keyboard"))

        self.keyboard = extra[0]
        return self

class F18_Keyboard(FC3_Keyboard):
    # pylint: disable=super-init-not-called
    def __init__(self, writePriority=0, *args, **kwargs):
        # pylint: disable=non-parent-init-called
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self._keyboard = kwargs.get("_keyboard", "")
        self.vc_keymap = kwargs.get("vc_keymap", "")
        self.x_layouts = kwargs.get("x_layouts", [])
        self.switch_options = kwargs.get("switch_options", [])

    def __str__(self):
        if not any((self._keyboard, self.x_layouts, self.vc_keymap)):
            return ""

        retval = "# Keyboard layouts\n"
        if not self.vc_keymap and not self.x_layouts:
            retval += "keyboard '%s'\n" % self._keyboard
            return retval

        if self._keyboard:
            retval += "# old format: keyboard %s\n" % self._keyboard
            retval += "# new format:\n"
        retval += "keyboard" + self._getArgsAsStr() + "\n"

        return retval

    def _getArgsAsStr(self):
        retval = ""

        if self.vc_keymap:
            retval += " --vckeymap=%s" % self.vc_keymap

        if self.x_layouts:
            layouts_str = "'%s'" % self.x_layouts[0]
            for layout in self.x_layouts[1:]:
                layouts_str += ",'%s'" % layout
            retval += " --xlayouts=%s" % layouts_str

        if self.switch_options:
            switch_str = "'%s'" % self.switch_options[0]
            for opt in self.switch_options[1:]:
                switch_str += ",'%s'" % opt
            retval += " --switch=%s" % switch_str

        return retval

    def _getParser(self):
        def csv_parse_callback(option, _opt_str, value, parser):
            for item in value.split(","):
                if item:
                    parser.values.ensure_value(option.dest, []).append(item)

        op = FC3_Keyboard._getParser(self)
        op.add_option("--vckeymap", dest="vc_keymap", action="store", default="")
        op.add_option("--xlayouts", dest="x_layouts", action="callback",
                      callback=csv_parse_callback, nargs=1, type="string")
        op.add_option("--switch", dest="switch_options", action="callback",
                      callback=csv_parse_callback, nargs=1, type="string")

        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)

        if len(extra) > 1:
            message = _("A single argument is expected for the %s command") % \
                        "keyboard"
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        elif len(extra) == 0 and not self.vc_keymap and not self.x_layouts:
            message = _("One of --xlayouts, --vckeymap options with value(s) "
                        "or argument is expected for the keyboard command")
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=message))

        if len(extra) > 0:
            self._keyboard = extra[0]

        return self

    # property for backwards compatibility
    # pylint: disable=method-hidden
    @property
    def keyboard(self):
        if self.x_layouts:
            return self._keyboard or self.vc_keymap or self.x_layouts[0]
        else:
            return self._keyboard or self.vc_keymap or ""

    # pylint: disable=function-redefined,no-member
    @keyboard.setter
    def keyboard(self, value):
        self._keyboard = value

