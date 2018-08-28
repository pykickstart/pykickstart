#
# Martin Kolman <mkolman@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser
from pykickstart.version import RHEL8

from pykickstart.i18n import _

class RHEL8_Syspurpose(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.role = kwargs.get("role", None)
        self.sla = kwargs.get("sla", None)
        self.usage = kwargs.get("usage", None)
        self.addons = kwargs.get("addons", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not retval and not any([self.role, self.sla, self.usage, self.addons]):
            return ""

        retval += '# Intended system purpose\nsyspurpose'
        if self.role:
            retval+=' --role="%s"' % self.role
        if self.sla:
            retval+=' --sla="%s"' % self.sla
        if self.usage:
            retval+=' --usage="%s"' % self.usage
        if self.addons:
            for addon in self.addons:
                retval+=' --addon="%s"' % addon
        retval+='\n'
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="syspurpose", description="""
                            The syspurpose command is used to describe
                            how the system is intended to be used after the installation.

                            This information then can be used to apply the
                            correct subscription entitlement to the system.""", version=RHEL8)
        op.add_argument("--role", metavar="<role_name>", version=RHEL8, required=False,
                        help="""
                        The intended role of the system.""")
        op.add_argument("--sla", metavar="<sla_name>", version=RHEL8, required=False,
                        help="""
                        Name of the sla intended for the system.""")
        op.add_argument("--usage", metavar="<usage>", version=RHEL8, required=False,
                        help="""
                        The intended usage of the system.""")
        op.add_argument("--addon", metavar="<layered product or feature>", version=RHEL8, required=False,
                        action="append", dest="addons", help="""
                        Any additional layered products or features. To add multiple items specify
                        --addon multiple times, once per layered product/feature.""")
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) > 0:
            msg = _("The syspurpose command does not take positional arguments!")
            raise KickstartParseError(msg, lineno=self.lineno)

        self.set_to_self(ns)
        return self
