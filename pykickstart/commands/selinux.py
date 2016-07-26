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
from pykickstart.constants import SELINUX_DISABLED, SELINUX_ENFORCING, SELINUX_PERMISSIVE
from pykickstart.options import KSOptionParser

class FC3_SELinux(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.selinux = kwargs.get("selinux", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not retval and self.selinux is None:
            return ""

        retval += "# SELinux configuration\n"

        if self.selinux == SELINUX_DISABLED:
            retval += "selinux --disabled\n"
        elif self.selinux == SELINUX_ENFORCING:
            retval += "selinux --enforcing\n"
        elif self.selinux == SELINUX_PERMISSIVE:
            retval += "selinux --permissive\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="selinux", description="""
                            Sets the state of SELinux on the installed system.
                            SELinux defaults to enforcing in anaconda.""",
                            epilog="""
                            Only one of ``--disabled``, ``--enabled`` or
                            ``--permissive`` must be specified!""",
                            version=FC3)
        op.add_argument("--disabled", dest="selinux", version=FC3,
                        action="store_const", const=SELINUX_DISABLED,
                        help="If this is present, SELinux is disabled.")
        op.add_argument("--enforcing", dest="selinux", version=FC3,
                        action="store_const", const=SELINUX_ENFORCING,
                        help="""
                        If this is present, SELinux is set to enforcing mode.
                        """)
        op.add_argument("--permissive", dest="selinux", version=FC3,
                        action="store_const", const=SELINUX_PERMISSIVE,
                        help="""
                        If this is present, SELinux is enabled, but only logs
                        things that would be denied in enforcing mode.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self
