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
from textwrap import dedent
from pykickstart.base import KickstartCommand
from pykickstart.version import FC3, F18, versionToLongString
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser, commaSplit

from pykickstart.i18n import _


class FC3_Keyboard(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.keyboard = kwargs.get("keyboard", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.keyboard:
            retval += "# System keyboard\nkeyboard %s\n" % self.keyboard

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="keyboard", description="""
            This required command sets system keyboard type.""", version=FC3)
        op.add_argument("kbd", nargs='*', help="Keyboard type", version=FC3)
        return op

    def parse(self, args):
        (_ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(_ns.kbd) != 1:
            raise KickstartParseError(_("Kickstart command %s requires one argument") % "keyboard", lineno=self.lineno)
        elif extra:
            mapping = {"command": "keyboard", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.keyboard = _ns.kbd[0]
        return self

class F18_Keyboard(FC3_Keyboard):
    def __init__(self, writePriority=0, *args, **kwargs):                # pylint: disable=super-init-not-called
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)  # pylint: disable=non-parent-init-called
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
        op = FC3_Keyboard._getParser(self)
        op.description += dedent("""

        .. versionchanged:: %s

        See the documentation of ``--vckeymap`` option and the tip at the end
        of this section for a guide how to get values accepted by this command.

        Either ``--vckeymap`` or ``--xlayouts`` must be used.

        Alternatively, use the older format, ``arg``, which is still supported.
        ``arg`` can be an X layout or VConsole keymap name.

        Missing values will be automatically converted from the given one(s).
        """ % versionToLongString(F18))

        op.add_argument("--vckeymap", dest="vc_keymap", default="", help="""
                        Specify VConsole keymap that should be used. is a keymap
                        name which is the same as the filename under
                        ``/usr/lib/kbd/keymaps/`` without the ``.map.gz`` extension.
                        """, version=F18)
        op.add_argument("--xlayouts", dest="x_layouts", type=commaSplit,
                        version=F18, help="""
                        Specify a list of X layouts that should be used
                        (comma-separated list without spaces). Accepts the same
                        values as ``setxkbmap(1)``, but uses either the layout format
                        (such as cz) or the 'layout (variant)' format (such as
                        'cz (qwerty)'). For example::

                        ``keyboard --xlayouts=cz,'cz (qwerty)'`""")
        op.add_argument("--switch", dest="switch_options", type=commaSplit,
                        version=F18, help="""
                        Specify a list of layout switching options that should
                        be used (comma-separated list without spaces). Accepts
                        the same values as ``setxkbmap(1)`` for layout switching.
                        For example::

                        ``keyboard --xlayouts=cz,'cz (qwerty)' --switch=grp:alt_shift_toggle``
                        """)
        op.epilog = dedent("""
        *If you know only the description of the layout (e.g. Czech (qwerty)),
        you can use http://vpodzime.fedorapeople.org/layouts_list.py to list
        all available layouts and find the one you want to use. The string in
        square brackets is the valid layout specification as Anaconda accepts
        it. The same goes for switching options and
        http://vpodzime.fedorapeople.org/switching_list.py*""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if len(ns.kbd) > 1:
            message = _("A single argument is expected for the %s command") % "keyboard"
            raise KickstartParseError(message, lineno=self.lineno)
        elif extra:
            mapping = {"command": "keyboard", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)
        elif not any([ns.kbd, self.vc_keymap, self.x_layouts]):
            message = _("One of --xlayouts, --vckeymap options with value(s) "
                        "or argument is expected for the keyboard command")
            raise KickstartParseError(message, lineno=self.lineno)

        if ns.kbd:
            self._keyboard = ns.kbd[0]

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
