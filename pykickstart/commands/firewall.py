#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import string

from pykickstart.base import *
from pykickstart.options import *

class FC3_Firewall(KickstartCommand):
    def __init__(self, writePriority=0, enabled=True, ports=None, trusts=None):
        KickstartCommand.__init__(self, writePriority)
        self.enabled = enabled

        if ports == None:
            ports = []

        self.ports = ports

        if trusts == None:
            trusts = []

        self.trusts = trusts

    def __str__(self):
        extra = []
        filteredPorts = []

        if self.enabled:
            # It's possible we have words in the ports list instead of
            # port:proto (s-c-kickstart may do this).  So, filter those
            # out into their own list leaving what we expect.
            for port in self.ports:
                if port == "ssh":
                    extra.append("--ssh")
                elif port == "telnet":
                    extra.append("--telnet")
                elif port == "smtp":
                    extra.append("--smtp")
                elif port == "http":
                    extra.append("--http")
                elif port == "ftp":
                    extra.append("--ftp")
                else:
                    filteredPorts.append(port)

            # All the port:proto strings go into a comma-separated list.
            portstr = string.join (filteredPorts, ",")
            if len(portstr) > 0:
                portstr = "--port=" + portstr
            else:
                portstr = ""

            extrastr = string.join (extra, " ")

            truststr = string.join (self.trusts, ",")
            if len(truststr) > 0:
                truststr = "--trust=" + truststr

            # The output port list consists only of port:proto for
            # everything that we don't recognize, and special options for
            # those that we do.
            return "# Firewall configuration\nfirewall --enabled %s %s %s\n" % (extrastr, portstr, truststr)
        else:
            return "# Firewall configuration\nfirewall --disabled\n"

    def parse(self, args):
        def firewall_port_cb (option, opt_str, value, parser):
            for p in value.split(","):
                p = p.strip()
                if p.find(":") == -1:
                    p = "%s:tcp" % p
                parser.values.ensure_value(option.dest, []).append(p)

        op = KSOptionParser(map={"ssh":["22:tcp"], "telnet":["23:tcp"],
                             "smtp":["25:tcp"], "http":["80:tcp", "443:tcp"],
                             "ftp":["21:tcp"]}, lineno=self.lineno)

        op.add_option("--disable", "--disabled", dest="enabled",
                      action="store_false")
        op.add_option("--enable", "--enabled", dest="enabled",
                      action="store_true", default=True)
        op.add_option("--ftp", "--http", "--smtp", "--ssh", "--telnet",
                      dest="ports", action="map_extend")
        op.add_option("--high", deprecated=1)
        op.add_option("--medium", deprecated=1)
        op.add_option("--port", dest="ports", action="callback",
                      callback=firewall_port_cb, nargs=1, type="string")
        op.add_option("--trust", dest="trusts", action="append")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
