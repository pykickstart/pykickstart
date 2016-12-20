#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.version import versionToLongString, RHEL4, RHEL5, RHEL6, RHEL7
from pykickstart.version import FC3, FC4, FC6, F8, F9, F16, F19, F20, F21, F22, F25, F27
from pykickstart.constants import BOOTPROTO_BOOTP, BOOTPROTO_DHCP, BOOTPROTO_IBFT, BOOTPROTO_QUERY, BOOTPROTO_STATIC, BIND_TO_MAC
from pykickstart.options import KSOptionParser, ksboolean
from pykickstart.errors import KickstartParseError, KickstartParseWarning

import warnings
from pykickstart.i18n import _

MIN_VLAN_ID = 0
MAX_VLAN_ID = 4095

class FC3_NetworkData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.bootProto = kwargs.get("bootProto", BOOTPROTO_DHCP)
        self.dhcpclass = kwargs.get("dhcpclass", "")
        self.device = kwargs.get("device", "")
        self.essid = kwargs.get("essid", "")
        self.ethtool = kwargs.get("ethtool", "")
        self.gateway = kwargs.get("gateway", "")
        self.hostname = kwargs.get("hostname", "")
        self.ip = kwargs.get("ip", "")
        self.mtu = kwargs.get("mtu", "")
        self.nameserver = kwargs.get("nameserver", "")
        self.netmask = kwargs.get("netmask", "")
        self.nodns = kwargs.get("nodns", False)
        self.onboot = kwargs.get("onboot", True)
        self.wepkey = kwargs.get("wepkey", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.device == y.device

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.bootProto:
            retval += " --bootproto=%s" % self.bootProto
        if self.dhcpclass:
            retval += " --dhcpclass=%s" % self.dhcpclass
        if self.device:
            retval += " --device=%s" % self.device
        if self.essid:
            retval += " --essid=\"%s\"" % self.essid
        if self.ethtool:
            retval += " --ethtool=\"%s\"" % self.ethtool
        if self.gateway:
            retval += " --gateway=%s" % self.gateway
        if self.hostname:
            retval += " --hostname=%s" % self.hostname
        if self.ip:
            retval += " --ip=%s" % self.ip
        if self.mtu:
            retval += " --mtu=%s" % self.mtu
        if self.nameserver:
            retval += " --nameserver=%s" % self.nameserver
        if self.netmask:
            retval += " --netmask=%s" % self.netmask
        if self.nodns:
            retval += " --nodns"
        if not self.onboot:
            retval += " --onboot=off"
        if self.wepkey:
            retval += " --wepkey=%s" % self.wepkey

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "network %s\n" % self._getArgsAsStr()
        return retval

class FC4_NetworkData(FC3_NetworkData):
    removedKeywords = FC3_NetworkData.removedKeywords
    removedAttrs = FC3_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_NetworkData.__init__(self, *args, **kwargs)
        self.notksdevice = kwargs.get("notksdevice", False)

    def _getArgsAsStr(self):
        retval = FC3_NetworkData._getArgsAsStr(self)

        if self.notksdevice:
            retval += " --notksdevice"

        return retval

class FC6_NetworkData(FC4_NetworkData):
    removedKeywords = FC4_NetworkData.removedKeywords
    removedAttrs = FC4_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC4_NetworkData.__init__(self, *args, **kwargs)
        self.noipv4 = kwargs.get("noipv4", False)
        self.noipv6 = kwargs.get("noipv6", False)

    def _getArgsAsStr(self):
        retval = FC4_NetworkData._getArgsAsStr(self)

        if self.noipv4:
            retval += " --noipv4"
        if self.noipv6:
            retval += " --noipv6"

        return retval

class F8_NetworkData(FC6_NetworkData):
    removedKeywords = FC6_NetworkData.removedKeywords
    removedAttrs = FC6_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC6_NetworkData.__init__(self, *args, **kwargs)
        self.ipv6 = kwargs.get("ipv6", "")

    def _getArgsAsStr(self):
        retval = FC6_NetworkData._getArgsAsStr(self)

        if self.ipv6:
            retval += " --ipv6=%s" % self.ipv6

        return retval

class F16_NetworkData(F8_NetworkData):
    removedKeywords = F8_NetworkData.removedKeywords
    removedAttrs = F8_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F8_NetworkData.__init__(self, *args, **kwargs)
        self.activate = kwargs.get("activate", None)
        self.nodefroute = kwargs.get("nodefroute", False)
        self.wpakey = kwargs.get("wpakey", "")

    def _getArgsAsStr(self):
        retval = F8_NetworkData._getArgsAsStr(self)

        if self.activate:
            retval += " --activate"
        if self.nodefroute:
            retval += " --nodefroute"
        if self.wpakey:
            retval += " --wpakey=%s" % self.wpakey

        return retval

class F19_NetworkData(F16_NetworkData):
    removedKeywords = F16_NetworkData.removedKeywords
    removedAttrs = F16_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F16_NetworkData.__init__(self, *args, **kwargs)
        self.bondslaves = kwargs.get("bondslaves", "")
        self.bondopts = kwargs.get("bondopts", "")
        self.vlanid = kwargs.get("vlanid", "")
        self.ipv6gateway = kwargs.get("ipv6gateway", "")

    def _getArgsAsStr(self):
        retval = F16_NetworkData._getArgsAsStr(self)

        if self.bondslaves:
            retval += " --bondslaves=%s" % self.bondslaves
        if self.bondopts:
            retval += " --bondopts=%s" % self.bondopts
        if self.vlanid:
            retval += " --vlanid=%s" % self.vlanid
        if self.ipv6gateway:
            retval += " --ipv6gateway=%s" % self.ipv6gateway

        return retval

class F20_NetworkData(F19_NetworkData):
    removedKeywords = F19_NetworkData.removedKeywords
    removedAttrs = F19_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F19_NetworkData.__init__(self, *args, **kwargs)
        self.teamslaves = kwargs.get("teamslaves", [])
        self.teamconfig = kwargs.get("teamconfig", "")

    def _getArgsAsStr(self):
        retval = F19_NetworkData._getArgsAsStr(self)

        # see the tests for format description
        if self.teamslaves:
            slavecfgs = []
            for slave, config in self.teamslaves:
                if config:
                    config = "'" + config + "'"
                slavecfgs.append(slave + config)
            slavecfgs = ",".join(slavecfgs).replace('"', r'\"')
            retval += ' --teamslaves="%s"' % slavecfgs
        if self.teamconfig:
            retval += ' --teamconfig="%s"' % self.teamconfig.replace('"', r'\"')
        return retval

class F21_NetworkData(F20_NetworkData):
    removedKeywords = F20_NetworkData.removedKeywords
    removedAttrs = F20_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F20_NetworkData.__init__(self, *args, **kwargs)
        self.interfacename = kwargs.get("interfacename", "")

    def _getArgsAsStr(self):
        retval = F20_NetworkData._getArgsAsStr(self)
        if self.interfacename:
            retval += " --interfacename=%s" % self.interfacename

        return retval

class F22_NetworkData(F21_NetworkData):
    removedKeywords = F21_NetworkData.removedKeywords
    removedAttrs = F21_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_NetworkData.__init__(self, *args, **kwargs)
        self.bridgeslaves = kwargs.get("bridgeslaves", "")
        self.bridgeopts = kwargs.get("bridgeopts", "")

    def _getArgsAsStr(self):
        retval = F21_NetworkData._getArgsAsStr(self)
        if self.bridgeslaves:
            retval += " --bridgeslaves=%s" % self.bridgeslaves
        if self.bridgeopts:
            retval += " --bridgeopts=%s" % self.bridgeopts

        return retval

class F25_NetworkData(F22_NetworkData):
    removedKeywords = F22_NetworkData.removedKeywords
    removedAttrs = F22_NetworkData.removedAttrs

    def _getArgsAsStr(self):
        retval = F22_NetworkData._getArgsAsStr(self)
        if self.activate == False:
            retval += " --no-activate"
        return retval

class F27_NetworkData(F25_NetworkData):
    removedKeywords = F25_NetworkData.removedKeywords
    removedAttrs = F25_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F25_NetworkData.__init__(self, *args, **kwargs)
        self.bindto = kwargs.get("bindto", None)

    def _getArgsAsStr(self):
        retval = F25_NetworkData._getArgsAsStr(self)
        if self.bindto == BIND_TO_MAC:
            retval += " --bindto=%s" % self.bindto
        return retval

class RHEL4_NetworkData(FC3_NetworkData):
    removedKeywords = FC3_NetworkData.removedKeywords
    removedAttrs = FC3_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        FC3_NetworkData.__init__(self, *args, **kwargs)
        self.notksdevice = kwargs.get("notksdevice", False)

    def _getArgsAsStr(self):
        retval = FC3_NetworkData._getArgsAsStr(self)

        if self.notksdevice:
            retval += " --notksdevice"

        return retval

class RHEL6_NetworkData(F8_NetworkData):
    removedKeywords = F8_NetworkData.removedKeywords
    removedAttrs = F8_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F8_NetworkData.__init__(self, *args, **kwargs)
        self.activate = kwargs.get("activate", None)
        self.nodefroute = kwargs.get("nodefroute", False)
        self.vlanid = kwargs.get("vlanid", "")
        self.bondslaves = kwargs.get("bondslaves", "")
        self.bondopts = kwargs.get("bondopts", "")

    def _getArgsAsStr(self):
        retval = F8_NetworkData._getArgsAsStr(self)

        if self.activate:
            retval += " --activate"
        if self.nodefroute:
            retval += " --nodefroute"
        if self.vlanid:
            retval += " --vlanid=%s" % self.vlanid
        if self.bondslaves:
            retval += " --bondslaves=%s" % self.bondslaves
        if self.bondopts:
            retval += " --bondopts=%s" % self.bondopts

        return retval

class RHEL7_NetworkData(F21_NetworkData):
    removedKeywords = F21_NetworkData.removedKeywords
    removedAttrs = F21_NetworkData.removedAttrs

    def __init__(self, *args, **kwargs):
        F21_NetworkData.__init__(self, *args, **kwargs)
        self.bridgeslaves = kwargs.get("bridgeslaves", "")
        self.bridgeopts = kwargs.get("bridgeopts", "")
        self.bindto = kwargs.get("bindto", None)

    def _getArgsAsStr(self):
        retval = F21_NetworkData._getArgsAsStr(self)
        if self.bridgeslaves:
            retval += " --bridgeslaves=%s" % self.bridgeslaves
        if self.bridgeopts:
            retval += " --bridgeopts=%s" % self.bridgeopts
        if self.activate == False:
            retval += " --no-activate"
        if self.bindto == BIND_TO_MAC:
            retval += " --bindto=%s" % self.bindto

        return retval

class FC3_Network(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList = [BOOTPROTO_DHCP, BOOTPROTO_BOOTP,
                              BOOTPROTO_STATIC]

        self.op = self._getParser()

        self.network = kwargs.get("network", [])

    def __str__(self):
        retval = ""

        for nic in self.network:
            retval += nic.__str__()

        if retval:
            return "# Network information\n" + retval
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser(prog="network", description="""
                            Configures network information for target system
                            and activates network devices in installer
                            environment. The device specified in the first
                            network command is activated automatically.
                            Activation of the device can be also explicitly
                            required by ``--activate`` option""", version=FC3)
        op.add_argument("--bootproto", dest="bootProto", version=FC3,
                        default=BOOTPROTO_DHCP, choices=self.bootprotoList,
                        help="""
                        The method of IPv4 configuration. For IPv6
                        configuration use ``--ipv6`` option.

                        The default setting is ``dhcp``. To turn IPv4
                        configuration off use ``--noipv4`` option.

                        - The ``dhcp`` method uses a DHCP server system to
                          obtain its networking configuration.

                        - The ``static`` method requires that you specify at
                          least IP address and netmask with ``--ip`` and
                          ``--netmask`` options. For example::

                              ``network --device=link --bootproto=static --ip=10.0.2.15 --netmask=255.255.255.0 --gateway=10.0.2.254 --nameserver=10.0.2.1``

                        - ``ibft`` setting is for reading the configuration
                          from iBFT table.""")
        op.add_argument("--dhcpclass", version=FC3, help="""
                        Specifies the DHCP vendor class identifier. The dhcpd
                        service will see this value as vendor-class-identifier.""")
        op.add_argument("--device", version=FC3, help="""
                        Specifies the device to be configured (and eventually
                        activated in Anaconda) with the network command.

                        You can specify a device to be activated in any of the
                        following ways:
                        - the device name of the interface, for example, ``em1``
                        - the MAC address of the interface, for example,
                          ``01:23:45:67:89:ab``
                        - the keyword ``link``, which specifies the first
                          interface with its link in the up state
                        - the keyword ``bootif``, which uses the MAC address
                          that pxelinux set in the ``BOOTIF`` variable. Set
                          ``IPAPPEND 2`` in your pxelinux.cfg file to have
                          pxelinux set the ``BOOTIF`` variable.

                        For example::

                            ``network --bootproto=dhcp --device=ens3``

                        If the ``--device=`` option is missing on the first use
                        of the network command, the value of the ``ksdevice=``
                        Anaconda boot option is used, if available. If
                        ``ksdevice=`` is not set, ``link`` value is used. Note
                        that this is considered deprecated behavior; in most
                        cases, you should always specify a ``--device=`` for
                        every network command. The behavior of any subsequent
                        network command in the same Kickstart file is
                        unspecified if its ``--device=`` option is missing.
                        Make sure you specify this option for any network
                        command beyond the first.
                        """)
        op.add_argument("--essid", version=FC3,
                        help="The network ID for wireless networks.")
        op.add_argument("--ethtool", version=FC3, help="""
                        Specifies additional low-level settings for the network
                        device which will be passed to the ethtool program.""")
        op.add_argument("--gateway", version=FC3,
                        help="Default gateway, as a single IPv4 address.")
        op.add_argument("--hostname", version=FC3,
                        help="""
                        The host name for the installed system.

                        The host name can either be a fully-qualified domain
                        name (FQDN) in the format hostname.domainname, or a
                        short host name with no domain. Many networks have a
                        DHCP service which automatically supplies connected
                        systems with a domain name; to allow DHCP to assign the
                        domain name, only specify a short host name.""")
        op.add_argument("--ip", version=FC3,
                        help="IPv4 address for the interface.")
        op.add_argument("--mtu", version=FC3, help="The MTU of the device.")
        op.add_argument("--nameserver", version=FC3, help="""
                        Primary nameserver, as an IP address. Multiple
                        nameservers must be comma separated.""")
        op.add_argument("--netmask", version=FC3,
                        help="IPv4 network mask of the device.")
        op.add_argument("--nodns", action="store_true", default=False,
                        version=FC3, help="Do not configure any DNS server.")
        op.add_argument("--onboot", type=ksboolean, version=FC3, help="""
                        Whether or not to enable the device a boot time.""")
        op.add_argument("--wepkey", version=FC3,
                        help="The WEP encryption key for wireless networks.")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        nd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, nd)
        nd.lineno = self.lineno

        # Check for duplicates in the data list.
        if nd in self.dataList():
            warnings.warn(_("A network device with the name %s has already been defined.") % nd.device, KickstartParseWarning)

        return nd

    def dataList(self):
        return self.network

    @property
    def dataClass(self):
        return self.handler.NetworkData

class FC4_Network(FC3_Network):
    removedKeywords = FC3_Network.removedKeywords
    removedAttrs = FC3_Network.removedAttrs

    def _getParser(self):
        op = FC3_Network._getParser(self)
        op.add_argument("--notksdevice", action="store_true", default=False,
                        version=FC4, help="""
                        This network device is not used for kickstart.""")
        return op

class FC6_Network(FC4_Network):
    removedKeywords = FC4_Network.removedKeywords
    removedAttrs = FC4_Network.removedAttrs

    def _getParser(self):
        op = FC4_Network._getParser(self)
        op.add_argument("--noipv4", action="store_true", default=False,
                        version=FC6, help="Disable IPv4 configuration of this device.")
        op.add_argument("--noipv6", action="store_true", default=False,
                        version=FC6, help="Disable IPv6 configuration of this device.")
        return op

class F8_Network(FC6_Network):
    removedKeywords = FC6_Network.removedKeywords
    removedAttrs = FC6_Network.removedAttrs

    def _getParser(self):
        op = FC6_Network._getParser(self)
        op.add_argument("--ipv6", version=F8, help="""
                        IPv6 address for the interface. This can be:
                        - the static address in form
                          ``<IPv6 address>[/<prefix length>]``, e.g.
                          ``3ffe:ffff:0:1::1/128``
                          (if prefix is omitted 64 is assumed),
                        - ``auto`` for stateless automatic address
                          autoconfiguration, or
                        - ``dhcp`` for DHCPv6-only configuration (no router
                          advertisements).
                        """)
        return op

class F9_Network(F8_Network):
    removedKeywords = F8_Network.removedKeywords
    removedAttrs = F8_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F8_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_QUERY)

    def _getParser(self):
        op = F8_Network._getParser(self)
        for action in op._actions:
            if "--bootproto" in action.option_strings:
                action.help += dedent("""

                        .. versionchanged:: %s

                        The 'query' value was added.""" % versionToLongString(F9))
                break
        return op

class F16_Network(F9_Network):
    removedKeywords = F9_Network.removedKeywords
    removedAttrs = F9_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_IBFT)

    def _getParser(self):
        op = F9_Network._getParser(self)
        for action in op._actions:
            if "--bootproto" in action.option_strings:
                action.help += dedent("""

                        .. versionchanged:: %s

                        The 'ibft' value was added.""" % versionToLongString(F16))
                break
        op.add_argument("--activate", action="store_true", version=F16,
                        default=None, help="""
                        As noted above, using this option ensures any matching
                        devices beyond the first will also be activated.""")
        op.add_argument("--nodefroute", action="store_true", version=F16,
                        default=False, help="""
                        Prevents grabbing of the default route by the device.
                        It can be useful when activating additional devices in
                        installer using ``--activate`` option.""")
        op.add_argument("--wpakey", default="", version=F16, help="""
                        The WPA encryption key for wireless networks.""")
        return op

class F18_Network(F16_Network):

    @property
    def hostname(self):
        for nd in self.dataList():
            if nd.hostname:
                return nd.hostname
        return None

class F19_Network(F18_Network):

    def _getParser(self):
        op = F18_Network._getParser(self)
        op.add_argument("--bondslaves", default="", version=F19, help="""
                        Bonded device with name specified by ``--device`` option
                        will be created using slaves specified in this option.
                        Example::

                            ``network --device bond0 --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --bondslaves=ens7,ens8 --bondopts=mode=active-backup,primary=ens7 --activate``
                        """)
        op.add_argument("--bondopts", default="", version=F19, help="""
                        A comma-separated list of optional parameters for bonded
                        interface specified by ``--bondslaves`` and ``--device``
                        options. Example::

                            ``--bondopts=mode=active-backup,primary=eth1``

                        If an option itself contains comma as separator use
                        semicolon to separate the options. Example::

                            ``--bondopts=mode=active-backup,balance-rr;primary=eth1``
                        """)
        op.add_argument("--vlanid", version=F19, help="""
                        Id (802.1q tag) of vlan device to be created using parent
                        device specified by ``--device`` option. For example::

                            ``network --device=eth0 --vlanid=171``

                        will create vlan device ``eth0.171``.""")
        op.add_argument("--ipv6gateway", default="", version=F19, help="""
                        Default gateway, as a single IPv6 address.
                        """)
        return op

class F20_Network(F19_Network):

    def _getParser(self):
        # see the tests for teamslaves option
        def teamslaves_cb(value):
            # value is of: "<DEV1>['<JSON_CONFIG1>'],<DEV2>['<JSON_CONFIG2>'],..."
            # for example: "eth1,eth2'{"prio": 100}',eth3"
            teamslaves = []
            if value:
                # Although slaves, having optional config, are separated by ","
                # first extract json configs because they can contain the ","
                parts = value.split("'")
                # parts == ['eth1,eth2', '{"prio": 100}', ',eth3']
                # ensure the list has even number of items for further zipping,
                # for odd number of items
                if len(parts) % 2 == 1:
                    # if the list ends with an empty string which must be a leftover
                    # from splitting string not ending with device eg
                    # "eth1,eth2'{"prio":100}'"
                    if not parts[-1]:
                        # just remove it
                        parts = parts[:-1]
                    # if not (our example), add empty config for the last device
                    else:
                        parts.append('')
                        # parts == ['eth1,eth2', '{"prio": 100}', ',eth3', '']
                # zip devices with their configs
                it = iter(parts)
                for devs, cfg in zip(it, it):
                    # first loop:
                    # devs == "eth1,eth2", cfg == '{"prio": 100}'
                    devs = devs.strip(',').split(',')
                    # devs == ["eth1", "eth2"]
                    # initialize config of all devs but the last one to empty
                    for d in devs[:-1]:
                        teamslaves.append((d, ''))
                    # teamslaves == [("eth1", '')]
                    # and set config of the last device
                    teamslaves.append((devs[-1], cfg))
                    # teamslaves == [('eth1', ''), ('eth2', '{"prio": 100}']

            return teamslaves

        op = F19_Network._getParser(self)
        op.add_argument("--teamslaves", type=teamslaves_cb, version=F20,
                        help="""
                        Team device with name specified by ``--device`` option
                        will be created using slaves specified in this option.
                        Slaves are separated by comma. A slave can be followed
                        by its configuration which is a single-quoted json format
                        string with double qoutes escaped by ``'\'`` character.
                        Example::

                            ``--teamslaves="p3p1'{\"prio\": -10, \"sticky\": true}',p3p2'{\"prio\": 100}'"``.

                        See also ``--teamconfig`` option.""")
        op.add_argument("--teamconfig", default="", version=F20, help="""
                        Double-quoted team device configuration which is a json
                        format string with double quotes escaped with ``'\'``
                        character. The device name is specified by ``--device``
                        option and its slaves and their configuration by
                        ``--teamslaves`` option. Example::

                        ``network --device team0 --activate --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --teamslaves="p3p1'{\"prio\": -10, \"sticky\": true}',p3p2'{\"prio\": 100}'" --teamconfig="{\"runner\": {\"name\": \"activebackup\"}}"``
                        """)
        return op

class F21_Network(F20_Network):
    def _getParser(self):
        op = F20_Network._getParser(self)
        op.add_argument("--interfacename", default="", version=F21, help="""
                        Specify a custom interface name for a virtual LAN
                        device. This option should be used when the default
                        name generated by the ``--vlanid=`` option is not
                        desirable. This option must be used along with
                        ``--vlanid=``. For example::

                            ``network --device=em1 --vlanid=171 --interfacename=vlan171``

                        The above command creates a virtual LAN interface named
                        ``vlan171`` on the em1 device with an ID of 171. The
                        interface name can be arbitrary (for example,
                        ``my-vlan``), but in specific cases, the following
                        conventions must be followed:

                        If the name contains a dot (.), it must take the form
                        of NAME.ID. The NAME is arbitrary, but the ID must be
                        the VLAN ID. For example: ``em1.171`` or
                        ``my-vlan.171``.  Names starting with vlan must take
                        the form of vlanID - for example: ``vlan171``.""")
        return op

class F22_Network(F21_Network):
    def _getParser(self):
        op = F21_Network._getParser(self)
        op.add_argument("--bridgeslaves", default="", version=F22, help="""
                        When this option is used, the network bridge with
                        device name specified using the ``--device=`` option
                        will be created and devices defined in the
                        ``--bridgeslaves=`` option will be added to the bridge.
                        For example::

                            ``network --device=bridge0 --bridgeslaves=em1``""")
        op.add_argument("--bridgeopts", default="", version=F22, help="""
                        An optional comma-separated list of parameters for the
                        bridged interface.  Available values are ``stp``,
                        ``priority``, ``forward-delay``, ``hello-time``,
                        ``max-age``, and ``ageing-time``. For information about
                        these parameters, see the bridge setting table in the
                        nm-settings(5) man page or at
                        https://developer.gnome.org/NetworkManager/0.9/ref-settings.html.
                        """)
        return op

    def parse(self, args):
        # call the overridden command to do it's job first
        retval = F21_Network.parse(self, args)

        if retval.bridgeopts:
            if not retval.bridgeslaves:
                msg = _("Option --bridgeopts requires --bridgeslaves to be specified")
                raise KickstartParseError(msg, lineno=self.lineno)
            opts = retval.bridgeopts.split(",")
            for opt in opts:
                _key, _sep, value = opt.partition("=")
                if not value or "=" in value:
                    msg = _("Bad format of --bridgeopts, expecting key=value options separated by ','")
                    raise KickstartParseError(msg, lineno=self.lineno)

        return retval

class F24_Network(F22_Network):
    removedKeywords = F22_Network.removedKeywords
    removedAttrs = F22_Network.removedAttrs

    def parse(self, args):
        retval = F22_Network.parse(self, args)

        # If we specify noipv4 then we need to make sure bootproto is zero'ed
        # out
        if retval.noipv4:
            retval.bootProto = ""
        return retval

class F25_Network(F24_Network):
    removedKeywords = F24_Network.removedKeywords
    removedAttrs = F24_Network.removedAttrs

    def _getParser(self):
        op = F24_Network._getParser(self)
        op.add_argument("--no-activate", default=None, version=F25, dest="activate",
                action="store_false", help="""
                Use this option with first network command to prevent
                activation of the device in istaller environment""")
        return op

class F27_Network(F25_Network):
    removedKeywords = F25_Network.removedKeywords
    removedAttrs = F25_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        self.bind_to_choices = [BIND_TO_MAC]
        F25_Network.__init__(self, writePriority, *args, **kwargs)

    def _getParser(self):
        op = F25_Network._getParser(self)
        op.add_argument("--bindto", dest="bindto", default=None, version=F27,
                        choices=self.bind_to_choices, help="""
                        Optionally allows to specify how the connection
                        configuration created for the device should be bound. If
                        the option is not used, the connection binds to
                        interface name (``DEVICE`` value in ifcfg file). For
                        virtual devices (bond, team, bridge) it configures
                        binding of slaves. Not applicable to vlan devices.

                        Note that this option is independent of how the
                        ``--device`` is specified.

                        Currently only the value ``mac`` is suported.
                        ``--bindto=mac`` will bind the connection to MAC address
                        of the device (``HWADDR`` value in ifcfg file).

                        For example::

                            ``network --device=01:23:45:67:89:ab --bootproto=dhcp --bindto=mac``

                        will bind the configuration of the device specified by
                        MAC address ``01:23:45:67:89:ab`` to its MAC address.

                            ``network --device=01:23:45:67:89:ab --bootproto=dhcp``

                        will bind the configuration of the device specified by
                        MAC address ``01:23:45:67:89:ab`` to its interface name
                        (eg ``ens3``).

                            ``network --device=ens3 --bootproto=dhcp --bindto=mac``

                        will bind the configuration of the device specified by
                        interface name ``ens3`` to its MAC address.
                       """)
        return op

    def parse(self, args):
        # call the overridden command to do it's job first
        retval = F25_Network.parse(self, args)

        if retval.bindto == BIND_TO_MAC:
            if retval.vlanid and not retval.bondopts:
                msg = _("--bindto=%s is not supported for this type of device") % BIND_TO_MAC
                raise KickstartParseError(msg, lineno=self.lineno)

        return retval

class RHEL4_Network(FC3_Network):
    removedKeywords = FC3_Network.removedKeywords
    removedAttrs = FC3_Network.removedAttrs

    def _getParser(self):
        op = FC3_Network._getParser(self)
        op.add_argument("--notksdevice", action="store_true", default=False,
                        version=RHEL4, help="")
        return op

class RHEL5_Network(FC6_Network):
    removedKeywords = FC6_Network.removedKeywords
    removedAttrs = FC6_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC6_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_QUERY)

    def _getParser(self):
        op = FC6_Network._getParser(self)
        for action in op._actions:
            if "--bootproto" in action.option_strings:
                action.help += dedent("""

                        .. versionchanged:: %s

                        The 'query' value was added.""" % versionToLongString(RHEL5))
                break
        return op

class RHEL6_Network(F9_Network):
    removedKeywords = F9_Network.removedKeywords
    removedAttrs = F9_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_IBFT)

    def _getParser(self):
        op = F9_Network._getParser(self)
        for action in op._actions:
            if "--bootproto" in action.option_strings:
                action.help += dedent("""

                        .. versionchanged:: %s

                        The 'ibft' value was added.""" % versionToLongString(RHEL6))
                break
        op.add_argument("--activate", action="store_true", version=RHEL6,
                        default=None, help="""
                        Activate this device in the installation environment.

                        If the device has already been activated (for example,
                        an interface you configured with boot options so that
                        the system could retrieve the Kickstart file) the
                        device is reactivated to use the configuration
                        specified in the Kickstart file.""")
        op.add_argument("--nodefroute", action="store_true", version=RHEL6,
                        default=False, help="""
                        Prevents the interface being set as the default route.
                        Use this option when you activate additional devices
                        with the ``--activate=`` option, for example, a NIC on
                        a separate subnet for an iSCSI target.""")
        op.add_argument("--vlanid", version=RHEL6, help="""
                        Id (802.1q tag) of vlan device to be created using parent
                        device specified by ``--device`` option. For example::

                            ``network --device=eth0 --vlanid=171``

                        will create vlan device ``eth0.171``.""")
        op.add_argument("--bondslaves", version=RHEL6, help="""
                        Bonded device with name specified by ``--device`` option
                        will be created using slaves specified in this option.
                        Example::

                           ``network --device bond0 --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --bondslaves=eth0,eth1 --bondopts=mode=active-backup,primary=eth0 --activate``

                        """)
        op.add_argument("--bondopts", version=RHEL6, help="""
                        A comma-separated list of optional parameters for bonded
                        interface specified by ``--bondslaves`` and ``--device``
                        options. Example::

                            ``--bondopts=mode=active-backup,primary=eth1``

                        If an option itself contains comma as separator use
                        semicolon to separate the options. Example::

                            ``--bondopts=mode=active-backup,balance-rr;primary=eth1``
                        """)
        return op

def validate_network_interface_name(name):
    """Check if the given network interface name is valid, return an error message
    if an error is found or None if no errors are found

    :param str name: name to validate
    :returns: error message or None if no error is found
    :rtype: str or NoneType
    """
    # (for reference see the NetworkManager source code:
    #  NetworkManager/src/settings/plugins/ifcfg-rh/reader.c
    #  and the make_vlan_setting function)

    vlan_id = None

    # if it contains '.', vlan id should follow (eg 'ens7.171', 'mydev.171')
    (vlan, dot, id_candidate) = name.partition(".")
    if dot:
        # 'vlan' can't be followed by a '.'
        if vlan == "vlan":
            return _("When using the <prefix>.<vlan id> interface name notation, <prefix> can't be equal to 'vlan'.")
        try:
            vlan_id = int(id_candidate)
        except ValueError:
            return _("If network --interfacename contains a '.', valid vlan id should follow.")

    # if it starts with 'vlan', vlan id should follow ('vlan171')
    (empty, sep, id_candidate) = name.partition("vlan")
    if sep and empty == "":
        # if we checked only for empty == "", we would evaluate missing interface name as an error
        try:
            vlan_id = int(id_candidate)
        except ValueError:
            return _("If network --interfacename starts with 'vlan', valid vlan id should follow.")

    # check if the vlan id is in range
    if vlan_id is not None:
        if not(MIN_VLAN_ID <= vlan_id <= MAX_VLAN_ID):
            return _("The vlan id is out of the %(minimum)d-%(maximum)d vlan id range.") % {"minimum": MIN_VLAN_ID, "maximum": MAX_VLAN_ID}

    # network interface name seems to be valid (no error found)
    return None

class RHEL7_Network(F21_Network):
    def __init__(self, writePriority=0, *args, **kwargs):
        self.bind_to_choices = [BIND_TO_MAC]
        F21_Network.__init__(self, writePriority, *args, **kwargs)

    def _getParser(self):
        op = F21_Network._getParser(self)
        op.add_argument("--bridgeslaves", default="", version=RHEL7, help="""
                        When this option is used, the network bridge with
                        device name specified using the ``--device=`` option
                        will be created and devices defined in the
                        ``--bridgeslaves=`` option will be added to the bridge.
                        For example::

                            ``network --device=bridge0 --bridgeslaves=em1``""")
        op.add_argument("--bridgeopts", default="", version=RHEL7, help="""
                        An optional comma-separated list of parameters for the
                        bridged interface.  Available values are ``stp``,
                        ``priority``, ``forward-delay``, ``hello-time``,
                        ``max-age``, and ``ageing-time``. For information about
                        these parameters, see the bridge setting table in the
                        nm-settings(5) man page or at
                        https://developer.gnome.org/NetworkManager/0.9/ref-settings.html.
                        """)
        op.add_argument("--no-activate", default=None, version=RHEL7, dest="activate",
                action="store_false", help="""
                Use this option with first network command to prevent
                activation of the device in istaller environment""")
        op.add_argument("--bindto", dest="bindto", default=None, version=RHEL7,
                        choices=self.bind_to_choices, help="""
                        Optionally allows to specify how the connection
                        configuration created for the device should be bound. If
                        the option is not used, the connection binds to
                        interface name (``DEVICE`` value in ifcfg file). For
                        virtual devices (bond, team, bridge) it configures
                        binding of slaves. Not applicable to vlan devices.

                        Note that this option is independent of how the
                        ``--device`` is specified.

                        Currently only the value ``mac`` is suported.
                        ``--bindto=mac`` will bind the connection to MAC address
                        of the device (``HWADDR`` value in ifcfg file).

                        For example::

                            ``network --device=01:23:45:67:89:ab --bootproto=dhcp --bindto=mac``

                        will bind the configuration of the device specified by
                        MAC address ``01:23:45:67:89:ab`` to its MAC address.

                            ``network --device=01:23:45:67:89:ab --bootproto=dhcp``

                        will bind the configuration of the device specified by
                        MAC address ``01:23:45:67:89:ab`` to its interface name
                        (eg ``ens3``).

                            ``network --device=ens3 --bootproto=dhcp --bindto=mac``

                        will bind the configuration of the device specified by
                        interface name ``ens3`` to its MAC address.
                       """)
        return op

    def parse(self, args):
        # call the overridden command to do it's job first
        retval = F21_Network.parse(self, args)

        # validate the network interface name
        error_message = validate_network_interface_name(retval.interfacename)
        # something is wrong with the interface name
        if error_message:
            raise KickstartParseError(error_message, lineno=self.lineno)

        if retval.bridgeopts:
            if not retval.bridgeslaves:
                msg = _("Option --bridgeopts requires --bridgeslaves to be specified")
                raise KickstartParseError(msg, lineno=self.lineno)
            opts = retval.bridgeopts.split(",")
            for opt in opts:
                _key, _sep, value = opt.partition("=")
                if not value or "=" in value:
                    msg = _("Bad format of --bridgeopts, expecting key=value options separated by ','")
                    raise KickstartParseError(msg, lineno=self.lineno)

        if retval.bindto == BIND_TO_MAC:
            if retval.vlanid and not retval.bondopts:
                msg = _("--bindto=%s is not supported for this type of device") % BIND_TO_MAC
                raise KickstartParseError(msg, lineno=self.lineno)

        return retval
