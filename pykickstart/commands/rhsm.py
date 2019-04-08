#
# Copyright 2019 Red Hat, Inc.
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

class RHEL8_RHSM(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.organization = kwargs.get("organization", None)
        self.activation_keys = kwargs.get("activation_keys", None)
        self.connect_to_insights = kwargs.get("connect_to_insights", None)
        self.proxy = kwargs.get("proxy", None)
        self.server_hostname = kwargs.get("server_hostname", None)
        self.rhsm_baseurl = kwargs.get("rhsm_baseurl", None)


    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not retval and not any([self.organization, self.activation_keys,
                                   self.proxy, self.server_hostname,
                                   self.rhsm_baseurl]):
            return ""

        retval += '# Red Hat Subscription Manager\nrhsm'
        # TODO: check if including the organization name & activation key in
        #       the output kickstart is expected and safe
        if self.organization:
            retval+=' --organization="%s"' % self.organization
        for key in self.activation_keys:
            retval+=' --activation-key="%s"' % key
        if self.connect_to_insights:
            retval+=' --connect-to-insights'
        if self.proxy:
            retval += ' --proxy="%s"' % self.proxy
        if self.server_hostname:
            retval+=' --server-hostname="%s"' % self.server_hostname
        if self.rhsm_baseurl:
            retval+=' --rhsm-baseurl="%s"' % self.rhsm_baseurl
        retval+='\n'
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="rhsm", description="""
                            The rhsm command is used to configure a Red Hat subscription.
                            A Red Hat subscription is required for installing from
                            the Red Hat CDN installation source as well connecting the target
                            system to Red Hat Insights.

                            Subscription attached during the installation will also be available
                            on the target system after the installation.

                            System Purpose data specified via the syspurpose command may influence
                            what subscription will be attached to the system. System Purpose data
                            set via the syspurpose command will override system purpose data attached
                            to activation keys.

                            An organization id needs to be specified, as well as at least one activation key.
                            """, version=RHEL8)
        op.add_argument("--organization", metavar="<organization_name>", version=RHEL8, required=True,
                        help="Organization id.")
        op.add_argument("--activation-key", metavar="<activation_key>", action="append", dest="activation_keys",
                        version=RHEL8, required=True,
                        help="Activation key. Option can be used multiple times, once per activation key.")
        op.add_argument("--connect-to-insights", version=RHEL8, action="store_true", default=False,
                        help="Connect to Red Hat Insights.")
        op.add_argument("--proxy", version=RHEL8, help="""
                        Specify an HTTP proxy to use for subscription purposes.
                        The syntax is::

                        ``--proxy=[protocol://][username[:password]@]host[:port]``
                        """)
        op.add_argument("--server-hostname", metavar="<subscription_service_server_url>", version=RHEL8, required=False,
                        help="Red Hat subscription service server URL.")
        op.add_argument("--rhsm-baseurl", metavar="<content_base_url>", version=RHEL8, required=False,
                        help="Content base URL.")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        for key in ns.activation_keys:
            if key == "":
                raise KickstartParseError(_("Empty string is not a valid activation key."), lineno=self.lineno)

        self.set_to_self(ns)
        return self
