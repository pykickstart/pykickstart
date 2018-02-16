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
from pykickstart.version import FC6
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser, commaSplit

from pykickstart.i18n import _

class FC6_Services(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.disabled = kwargs.get("disabled", [])
        self.enabled = kwargs.get("enabled", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        args = ""

        if self.disabled:
            args += " --disabled=\"%s\"" % ",".join(self.disabled)
        if self.enabled:
            args += " --enabled=\"%s\"" % ",".join(self.enabled)

        if args:
            retval += "# System services\nservices%s\n" % args

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="services", description="""
                            Modifies the default set of services that will run
                            under the default runlevel. The services listed in
                            the disabled list will be disabled before the
                            services listed in the enabled list are enabled.
                            """, epilog="""
                            One of ``--disabled`` or ``--enabled`` must be provided.
                            """, version=FC6)
        op.add_argument("--disabled", type=commaSplit, version=FC6,
                        metavar="<list>", help="""
                        Disable the services given in the comma separated list.
                        """)
        op.add_argument("--enabled", type=commaSplit, version=FC6,
                        metavar="<list>", help="""
                        Enable the services given in the comma separated list.
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if not (self.disabled or self.enabled):
            raise KickstartParseError(_("One of --disabled or --enabled must be provided."), lineno=self.lineno)

        return self
