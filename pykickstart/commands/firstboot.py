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
from pykickstart.version import FC3
from pykickstart.base import KickstartCommand
from pykickstart.constants import FIRSTBOOT_DEFAULT, FIRSTBOOT_SKIP, FIRSTBOOT_RECONFIG
from pykickstart.options import KSOptionParser

class FC3_Firstboot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.firstboot = kwargs.get("firstboot", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.firstboot is None:
            return retval

        if self.firstboot == FIRSTBOOT_SKIP:
            retval += "firstboot --disable\n"
        elif self.firstboot == FIRSTBOOT_DEFAULT:
            retval += "# Run the Setup Agent on first boot\nfirstboot --enable\n"
        elif self.firstboot == FIRSTBOOT_RECONFIG:
            retval += "# Run the Setup Agent on first boot\nfirstboot --reconfig\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="firstboot", description="""
                            Determine whether the Setup Agent starts the first
                            time the system is booted. If enabled, the
                            ``initial-setup`` package must be installed. If not
                            specified, the setup agent (initial-setup) is disabled
                            by default.""",
                            version=FC3)
        op.add_argument("--disable", "--disabled", dest="firstboot",
                        action="store_const", const=FIRSTBOOT_SKIP, version=FC3,
                        help="""The Setup Agent is not started the first time the
                        system boots.""")
        op.add_argument("--enable", "--enabled", dest="firstboot",
                        action="store_const", const=FIRSTBOOT_DEFAULT, version=FC3,
                        help="""The Setup Agent is started the first time the
                        system boots.""")
        op.add_argument("--reconfig", dest="firstboot", version=FC3,
                        action="store_const", const=FIRSTBOOT_RECONFIG,
                        help="""
                        Enable the Setup Agent to start at boot time in
                        reconfiguration mode. This mode enables the language,
                        mouse, keyboard, root password, security level,
                        time zone, and networking configuration options in
                        addition to the default ones.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.firstboot = ns.firstboot
        return self
