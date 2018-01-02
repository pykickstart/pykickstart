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

from pykickstart.i18n import _

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
                if port == "ssh":
                    extra.append(" --ssh")
                elif port == "telnet":
                    extra.append(" --telnet")
                elif port == "smtp":
                    extra.append(" --smtp")
                elif port == "http":
                    extra.append(" --http")
                elif port == "ftp":
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
        def firewall_port_cb (option, opt_str, value, parser):
            for p in value.split(","):
                p = p.strip()
                if p.find(":") == -1:
                    p = "%s:tcp" % p
                parser.values.ensure_value(option.dest, []).append(p)

        op = KSOptionParser(mapping={"ssh":["22:tcp"], "telnet":["23:tcp"],
                             "smtp":["25:tcp"], "http":["80:tcp", "443:tcp"],
                             "ftp":["21:tcp"]})

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
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) != 0:
            mapping = {"command": "firewall", "options": extra}
            raise KickstartValueError(formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping))

        self.set_to_self(self.op, opts)
        return self

class F9_Firewall(FC3_Firewall):
    removedKeywords = FC3_Firewall.removedKeywords
    removedAttrs = FC3_Firewall.removedAttrs

    def _getParser(self):
        op = FC3_Firewall._getParser(self)
        op.remove_option("--high")
        op.remove_option("--medium")
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
        def service_cb (option, opt_str, value, parser):
            # python2.4 does not support action="append_const" that we were
            # using for these options.  Instead, we have to fake it by
            # appending whatever the option string is to the service list.
            if not value:
                parser.values.ensure_value(option.dest, []).append(opt_str[2:])
                return

            for p in value.split(","):
                p = p.strip()
                parser.values.ensure_value(option.dest, []).append(p)

        op = F9_Firewall._getParser(self)
        op.add_option("--service", dest="services", action="callback",
                      callback=service_cb, nargs=1, type="string")
        op.add_option("--ftp", dest="services", action="callback",
                      callback=service_cb)
        op.add_option("--http", dest="services", action="callback",
                      callback=service_cb)
        op.add_option("--smtp", dest="services", action="callback",
                      callback=service_cb)
        op.add_option("--ssh", dest="services", action="callback",
                      callback=service_cb)
        op.add_option("--telnet", deprecated=1)
        return op

class F14_Firewall(F10_Firewall):
    removedKeywords = F10_Firewall.removedKeywords + ["telnet"]
    removedAttrs = F10_Firewall.removedAttrs + ["telnet"]

    def _getParser(self):
        op = F10_Firewall._getParser(self)
        op.remove_option("--telnet")
        return op

class F20_Firewall(F14_Firewall):

    def __init__(self, writePriority=0, *args, **kwargs):
        F14_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.remove_services = kwargs.get("remove_services", [])

    def _getParser(self):
        def remove_service_cb(option, opt_str, value, parser):
            # python2.4 does not support action="append_const" that we were
            # using for these options.  Instead, we have to fake it by
            # appending whatever the option string is to the service list.
            if not value:
                parser.values.ensure_value(option.dest, []).append(opt_str[2:])
                return

            for p in value.split(","):
                p = p.strip()
                parser.values.ensure_value(option.dest, []).append(p)

        op = F14_Firewall._getParser(self)
        op.add_option("--remove-service", dest="remove_services",
                      action="callback", callback=remove_service_cb,
                      nargs=1, type="string")
        return op

    def __str__(self):
        if self.enabled is None:
            return ""

        retval = F10_Firewall.__str__(self)
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

class F28_Firewall(F20_Firewall):
    def __init__(self, writePriority=0, *args, **kwargs):
        F20_Firewall.__init__(self, writePriority, *args, **kwargs)
        self.use_system_defaults = kwargs.get("use_system_defaults", None)

    def _getParser(self):
        op = F20_Firewall._getParser(self)
        op.add_option("--use-system-defaults", dest="use_system_defaults",
                      action="store_true", default=False)
        return op

    def __str__(self):
        if self.use_system_defaults:
            return "# Firewall configuration\nfirewall --use-system-defaults\n"
        else:
            return F20_Firewall.__str__(self)
