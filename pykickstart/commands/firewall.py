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
from pykickstart.version import FC3, F9, F10, F14, F20, F28
from pykickstart.base import KickstartCommand
from pykickstart.options import ExtendAction, ExtendConstAction, KSOptionParser, commaSplit

class FC3_Firewall(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.enabled = kwargs.get("enabled", None)
        self.ports = kwargs.get("ports", [])
        self.trusts = kwargs.get("trusts", [])

    def __str__(self):
        extra = []
        filteredPorts = []

        retval = KickstartCommand.__str__(self)

        if self.enabled is None:
            return retval

        if self.enabled:
            # It's possible we have words in the ports list instead of
            # port:proto (s-c-kickstart may do this).  So, filter those
            # out into their own list leaving what we expect.
            for port in self.ports:
                if port == "ssh:tcp":
                    extra.append(" --ssh")
                elif port == "telnet:tcp":
                    extra.append(" --telnet")
                elif port == "smtp:tcp":
                    extra.append(" --smtp")
                elif port == "http:tcp":
                    extra.append(" --http")
                elif port == "ftp:tcp":
                    extra.append(" --ftp")
                else:
                    filteredPorts.append(port)

            # All the port:proto strings go into a comma-separated list.
            portstr = ",".join(filteredPorts)
            if portstr:
                portstr = " --port=" + portstr

            extrastr = "".join(extra)
            truststr = ",".join(self.trusts)

            if truststr:
                truststr = " --trust=" + truststr

            # The output port list consists only of port:proto for
            # everything that we don't recognize, and special options for
            # those that we do.
            retval += "# Firewall configuration\nfirewall --enabled%s%s%s\n" % (extrastr, portstr, truststr)
        else:
            retval += "# Firewall configuration\nfirewall --disabled\n"

        return retval

    def _getParser(self):
        def firewall_port_cb(value):
            retval = []
            for p in value.split(","):
                p = p.strip()
                if p.find(":") == -1:
                    p = "%s:tcp" % p

                retval.append(p)

            return retval

        op = KSOptionParser(prog="firewall", description="""
                            This option corresponds to the Firewall Configuration
                            screen in the installation program""",
                            version=FC3)
        op.add_argument("--disable", "--disabled", dest="enabled",
                        action="store_false", version=FC3,
                        help="Do not configure any iptables rules.")
        op.add_argument("--enable", "--enabled", dest="enabled",
                        action="store_true", default=True, help="""
                        Reject incoming connections that are not in response
                        to outbound requests, such as DNS replies or DHCP
                        requests. If access to services running on this machine
                        is needed, you can choose to allow specific services
                        through the firewall.""", version=FC3)
        op.add_argument("--ftp", dest="ports", action="append_const",
                        const="21:tcp", version=FC3, help="")
        op.add_argument("--http", dest="ports", action=ExtendConstAction,
                        const=["80:tcp", "443:tcp"], nargs=0, version=FC3,
                        help="")
        op.add_argument("--smtp", dest="ports", action="append_const",
                        const="25:tcp", version=FC3, help="")
        op.add_argument("--ssh", dest="ports", action="append_const",
                        const="22:tcp", version=FC3, help="")
        op.add_argument("--telnet", dest="ports", action="append_const",
                        const="23:tcp", version=FC3, help="")
        op.add_argument("--high", deprecated=FC3, help="")
        op.add_argument("--medium", deprecated=FC3, help="")
        op.add_argument("--port", dest="ports", action=ExtendAction,
                        type=firewall_port_cb, help="""
                        You can specify that ports be allowed through the firewall
                        using the port:protocol format. You can also specify ports
                        numerically. Multiple ports can be combined into one option
                        as long as they are separated by commas. For example::

                        ``firewall --port=imap:tcp,1234:ucp,47``""",
                        version=FC3)
        op.add_argument("--trust", dest="trusts", action="append", help="""
                        Listing a device here, such as eth0, allows all traffic
                        coming from that device to go through the firewall. To
                        list more than one device, use --trust eth0 --trust eth1.
                        Do NOT use a comma-separated format such as
                        --trust eth0, eth1.""", version=FC3)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class F9_Firewall(FC3_Firewall):
    removedKeywords = FC3_Firewall.removedKeywords
    removedAttrs = FC3_Firewall.removedAttrs

    def _getParser(self):
        op = FC3_Firewall._getParser(self)
        op.remove_argument("--high", version=F9)
        op.remove_argument("--medium", version=F9)
        return op

class F10_Firewall(F9_Firewall):
    removedKeywords = F9_Firewall.removedKeywords
    removedAttrs = F9_Firewall.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.services = kwargs.get("services", [])

    def __str__(self):
        if self.enabled is None:
            return ""

        retval = F9_Firewall.__str__(self)
        if self.enabled:
            retval = retval.strip()

            svcstr = ",".join(self.services)
            if svcstr:
                svcstr = " --service=" + svcstr

            return retval + "%s\n" % svcstr
        else:
            return retval

    def _getParser(self):
        op = F9_Firewall._getParser(self)
        op.add_argument("--service", dest="services", action=ExtendAction,
                        type=commaSplit, help="""
                        This option provides a higher-level way to allow services
                        through the firewall. Some services (like cups, avahi, etc.)
                        require multiple ports to be open or other special
                        configuration in order for the service to work. You could
                        specify each individual service with the ``--port`` option,
                        or specify ``--service=`` and open them all at once.

                        Valid options are anything recognized by the
                        firewall-cmd program in the firewalld package.
                        If firewalld is running::

                        ``firewall-cmd --get-services``

                        will provide a list of known service names.""",
                        version=F10)
        op.add_argument("--ftp", dest="services", action="append_const",
                        const="ftp", version=F10, help="")
        op.add_argument("--http", dest="services", action="append_const",
                        const="http", version=F10, help="")
        op.add_argument("--smtp", dest="services", action="append_const",
                        const="smtp", version=F10, help="")
        op.add_argument("--ssh", dest="services", action="append_const",
                        const="ssh", version=F10, help="")
        op.add_argument("--telnet", deprecated=F10)
        return op

class F14_Firewall(F10_Firewall):
    removedKeywords = F10_Firewall.removedKeywords + ["telnet"]
    removedAttrs = F10_Firewall.removedAttrs + ["telnet"]

    def _getParser(self):
        op = F10_Firewall._getParser(self)
        op.remove_argument("--telnet", version=F14)
        return op

class F20_Firewall(F14_Firewall):
    def __init__(self, writePriority=0, *args, **kwargs):
        F14_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.remove_services = kwargs.get("remove_services", [])

    def _getParser(self):
        op = F14_Firewall._getParser(self)
        op.add_argument("--remove-service", dest="remove_services", help="",
                        action=ExtendAction, type=commaSplit, version=F20)
        return op

    def __str__(self):
        if self.enabled is None:
            return ""

        retval = F14_Firewall.__str__(self)
        if self.enabled:
            retval = retval.strip()

            svcstr = ",".join(self.remove_services)
            if svcstr:
                svcstr = " --remove-service=" + svcstr

            return retval + "%s\n" % svcstr
        else:
            return retval

class F28_Firewall(F20_Firewall):
    def __init__(self, writePriority=0, *args, **kwargs):
        F20_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.use_system_defaults = kwargs.get("use_system_defaults", None)

    def _getParser(self):
        op = F20_Firewall._getParser(self)
        op.add_argument("--use-system-defaults", dest="use_system_defaults",
                        action="store_true", default=False, version=F28, help="""
                        Don't configure the firewall at all. This instructs anaconda
                        to do nothing and allows the system to rely on the defaults
                        that were provided with the package or ostree.  If this option
                        is used with other options then all other options will be
                        ignored.""")
        return op

    def __str__(self):
        if self.use_system_defaults:
            return "# Firewall configuration\nfirewall --use-system-defaults\n"
        else:
            return F20_Firewall.__str__(self)
