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
            if len(portstr) > 0:
                portstr = " --port=" + portstr
            else:
                portstr = ""

            extrastr = "".join(extra)
            truststr = ",".join(self.trusts)

            if len(truststr) > 0:
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

        op = KSOptionParser()
        op.add_argument("--disable", "--disabled", dest="enabled", action="store_false")
        op.add_argument("--enable", "--enabled", dest="enabled", action="store_true", default=True)
        op.add_argument("--ftp", dest="ports", action="append_const", const="21:tcp")
        op.add_argument("--http", dest="ports", action=ExtendConstAction, const=["80:tcp", "443:tcp"], nargs=0)
        op.add_argument("--smtp", dest="ports", action="append_const", const="25:tcp")
        op.add_argument("--ssh", dest="ports", action="append_const", const="22:tcp")
        op.add_argument("--telnet", dest="ports", action="append_const", const="23:tcp")
        op.add_argument("--high", deprecated=True)
        op.add_argument("--medium", deprecated=True)
        op.add_argument("--port", dest="ports", action=ExtendAction, type=firewall_port_cb)
        op.add_argument("--trust", dest="trusts", action="append")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(ns)
        return self

class F9_Firewall(FC3_Firewall):
    removedKeywords = FC3_Firewall.removedKeywords
    removedAttrs = FC3_Firewall.removedAttrs

    def _getParser(self):
        op = FC3_Firewall._getParser(self)
        op.remove_argument("--high")
        op.remove_argument("--medium")
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
            if len(svcstr) > 0:
                svcstr = " --service=" + svcstr
            else:
                svcstr = ""

            return retval + "%s\n" % svcstr
        else:
            return retval

    def _getParser(self):
        op = F9_Firewall._getParser(self)
        op.add_argument("--service", dest="services", action=ExtendAction, type=commaSplit)
        op.add_argument("--ftp", dest="services", action="append_const", const="ftp")
        op.add_argument("--http", dest="services", action="append_const", const="http")
        op.add_argument("--smtp", dest="services", action="append_const", const="smtp")
        op.add_argument("--ssh", dest="services", action="append_const", const="ssh")
        op.add_argument("--telnet", deprecated=True)
        return op

class F14_Firewall(F10_Firewall):
    removedKeywords = F10_Firewall.removedKeywords + ["telnet"]
    removedAttrs = F10_Firewall.removedAttrs + ["telnet"]

    def _getParser(self):
        op = F10_Firewall._getParser(self)
        op.remove_argument("--telnet")
        return op

class F20_Firewall(F14_Firewall):
    def __init__(self, writePriority=0, *args, **kwargs):
        F14_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.remove_services = kwargs.get("remove_services", [])

    def _getParser(self):
        op = F14_Firewall._getParser(self)
        op.add_argument("--remove-service", dest="remove_services", action=ExtendAction, type=commaSplit)
        return op

    def __str__(self):
        if self.enabled is None:
            return ""

        retval = F14_Firewall.__str__(self)
        if self.enabled:
            retval = retval.strip()

            svcstr = ",".join(self.remove_services)
            if len(svcstr) > 0:
                svcstr = " --remove-service=" + svcstr
            else:
                svcstr = ""

            return retval + "%s\n" % svcstr
        else:
            return retval
