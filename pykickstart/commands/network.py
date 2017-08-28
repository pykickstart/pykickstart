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
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.constants import BOOTPROTO_BOOTP, BOOTPROTO_DHCP, BOOTPROTO_IBFT, BOOTPROTO_QUERY, BOOTPROTO_STATIC, BIND_TO_MAC
from pykickstart.options import KSOptionParser
from pykickstart.errors import KickstartValueError, formatErrorMsg

import gettext
import warnings
_ = lambda x: gettext.ldgettext("pykickstart", x)

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

        return self.device and self.device == y.device

    def __ne__(self, y):
        return not self == y

    def _getArgsAsStr(self):
        retval = ""

        if self.bootProto != "":
            retval += " --bootproto=%s" % self.bootProto
        if self.dhcpclass != "":
            retval += " --dhcpclass=%s" % self.dhcpclass
        if self.device != "":
            retval += " --device=%s" % self.device
        if self.essid != "":
            retval += " --essid=\"%s\"" % self.essid
        if self.ethtool != "":
            retval += " --ethtool=\"%s\"" % self.ethtool
        if self.gateway != "":
            retval += " --gateway=%s" % self.gateway
        if self.hostname != "":
            retval += " --hostname=%s" % self.hostname
        if self.ip != "":
            retval += " --ip=%s" % self.ip
        if self.mtu != "":
            retval += " --mtu=%s" % self.mtu
        if self.nameserver != "":
            retval += " --nameserver=%s" % self.nameserver
        if self.netmask != "":
            retval += " --netmask=%s" % self.netmask
        if self.nodns:
            retval += " --nodns"
        if not self.onboot:
            retval += " --onboot=off"
        if self.wepkey != "":
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

        if self.ipv6 != "":
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
        if self.wpakey != "":
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

        if self.bondslaves != "":
            retval += " --bondslaves=%s" % self.bondslaves
        if self.bondopts != "":
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
                slavecfgs.append(slave+config)
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
        if self.bridgeslaves != "":
            retval += " --bridgeslaves=%s" % self.bridgeslaves
        if self.bridgeopts != "":
            retval += " --bridgeopts=%s" % self.bridgeopts

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
        if self.bridgeslaves != "":
            retval += " --bridgeslaves=%s" % self.bridgeslaves
        if self.bridgeopts != "":
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

        if retval != "":
            return "# Network information\n" + retval
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--bootproto", dest="bootProto",
                      default=BOOTPROTO_DHCP,
                      choices=self.bootprotoList)
        op.add_option("--dhcpclass", dest="dhcpclass")
        op.add_option("--device", dest="device")
        op.add_option("--essid", dest="essid")
        op.add_option("--ethtool", dest="ethtool")
        op.add_option("--gateway", dest="gateway")
        op.add_option("--hostname", dest="hostname")
        op.add_option("--ip", dest="ip")
        op.add_option("--mtu", dest="mtu")
        op.add_option("--nameserver", dest="nameserver")
        op.add_option("--netmask", dest="netmask")
        op.add_option("--nodns", dest="nodns", action="store_true",
                      default=False)
        op.add_option("--onboot", dest="onboot", action="store",
                      type="ksboolean")
        op.add_option("--wepkey", dest="wepkey")
        return op

    def parse(self, args):
        (opts, _extra) = self.op.parse_args(args=args, lineno=self.lineno)
        nd = self.handler.NetworkData()
        self._setToObj(self.op, opts, nd)
        nd.lineno = self.lineno

        # Check for duplicates in the data list.
        if nd in self.dataList():
            warnings.warn(_("A network device with the name %s has already been defined.") % nd.device)

        return nd

    def dataList(self):
        return self.network

class FC4_Network(FC3_Network):
    removedKeywords = FC3_Network.removedKeywords
    removedAttrs = FC3_Network.removedAttrs

    def _getParser(self):
        op = FC3_Network._getParser(self)
        op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                      default=False)
        return op

class FC6_Network(FC4_Network):
    removedKeywords = FC4_Network.removedKeywords
    removedAttrs = FC4_Network.removedAttrs

    def _getParser(self):
        op = FC4_Network._getParser(self)
        op.add_option("--noipv4", dest="noipv4", action="store_true",
                      default=False)
        op.add_option("--noipv6", dest="noipv6", action="store_true",
                      default=False)
        return op

class F8_Network(FC6_Network):
    removedKeywords = FC6_Network.removedKeywords
    removedAttrs = FC6_Network.removedAttrs

    def _getParser(self):
        op = FC6_Network._getParser(self)
        op.add_option("--ipv6", dest="ipv6")
        return op

class F9_Network(F8_Network):
    removedKeywords = F8_Network.removedKeywords
    removedAttrs = F8_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F8_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_QUERY)

    def _getParser(self):
        op = F8_Network._getParser(self)
        op.add_option("--bootproto", dest="bootProto",
                      default=BOOTPROTO_DHCP,
                      choices=self.bootprotoList)
        return op

class F16_Network(F9_Network):
    removedKeywords = F9_Network.removedKeywords
    removedAttrs = F9_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_IBFT)

    def _getParser(self):
        op = F9_Network._getParser(self)
        op.add_option("--activate", dest="activate", action="store_true",
                      default=None)
        op.add_option("--nodefroute", dest="nodefroute", action="store_true",
                      default=False)
        op.add_option("--wpakey", dest="wpakey", action="store", default="")
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
        op.add_option("--bondslaves", dest="bondslaves", action="store",
                default="")
        op.add_option("--bondopts", dest="bondopts", action="store",
                default="")
        op.add_option("--vlanid", dest="vlanid")
        op.add_option("--ipv6gateway", dest="ipv6gateway", action="store",
                default="")
        return op

class F20_Network(F19_Network):

    def _getParser(self):
        # see the tests for teamslaves option
        def teamslaves_cb(option, opt_str, value, parser):
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
                    # "eth1,eth2'{"prio":100"}'"
                    if not parts[-1]:
                        # just remove it
                        parts = parts[:-1]
                    # if not (our example), add empty config for the last device
                    else:
                        parts.append('')
                        # parts == ['eth1,eth2', '{"prio": 100}', ',eth3', '']
                # zip devices with their configs
                it = iter(parts)
                for devs, cfg in zip(it,it):
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
            parser.values.teamslaves = teamslaves

        op = F19_Network._getParser(self)
        op.add_option("--teamslaves", dest="teamslaves", action="callback",
                callback=teamslaves_cb, nargs=1, type="string")
        op.add_option("--teamconfig", dest="teamconfig", action="store",
                default="")
        return op

class F21_Network(F20_Network):
    def _getParser(self):
        op = F20_Network._getParser(self)
        op.add_option("--interfacename", dest="interfacename", action="store",
                default="")
        return op

class F22_Network(F21_Network):
    def _getParser(self):
        op = F21_Network._getParser(self)
        op.add_option("--bridgeslaves", dest="bridgeslaves", action="store",
                default="")
        op.add_option("--bridgeopts", dest="bridgeopts", action="store",
                default="")
        return op

    def parse(self, args):
        # call the overridden command to do it's job first
        retval = F21_Network.parse(self, args)

        if retval.bridgeopts:
            if not retval.bridgeslaves:
                msg = formatErrorMsg(self.lineno, msg=_("Option --bridgeopts requires "\
                                        "--bridgeslaves to be specified"))
                raise KickstartValueError(msg)
            opts = retval.bridgeopts.split(",")
            for opt in opts:
                _key, _sep, value = opt.partition("=")
                if not value or "=" in value:
                    msg = formatErrorMsg(self.lineno, msg=_("Bad format of --bridgeopts, expecting key=value options separated by ','"))
                    raise KickstartValueError(msg)

        return retval

class RHEL4_Network(FC3_Network):
    removedKeywords = FC3_Network.removedKeywords
    removedAttrs = FC3_Network.removedAttrs

    def _getParser(self):
        op = FC3_Network._getParser(self)
        op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                      default=False)
        return op

class RHEL5_Network(FC6_Network):
    removedKeywords = FC6_Network.removedKeywords
    removedAttrs = FC6_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC6_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_QUERY)

    def _getParser(self):
        op = FC6_Network._getParser(self)
        op.add_option("--bootproto", dest="bootProto",
                      default=BOOTPROTO_DHCP,
                      choices=self.bootprotoList)
        return op

class RHEL6_Network(F9_Network):
    removedKeywords = F9_Network.removedKeywords
    removedAttrs = F9_Network.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_Network.__init__(self, writePriority, *args, **kwargs)
        self.bootprotoList.append(BOOTPROTO_IBFT)

    def _getParser(self):
        op = F9_Network._getParser(self)
        op.add_option("--activate", dest="activate", action="store_true",
                      default=None)
        op.add_option("--nodefroute", dest="nodefroute", action="store_true",
                      default=False)
        op.add_option("--vlanid", dest="vlanid")
        op.add_option("--bondslaves", dest="bondslaves")
        op.add_option("--bondopts", dest="bondopts")
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
            return _("The vlan id out of the %d-%d vlan id range.") % (MIN_VLAN_ID, MAX_VLAN_ID)

    # network interface name seems to be valid (no error found)
    return None

class RHEL7_Network(F21_Network):
    def __init__(self, writePriority=0, *args, **kwargs):
        self.bind_to_choices = [BIND_TO_MAC]
        F21_Network.__init__(self, writePriority, *args, **kwargs)

    def _getParser(self):
        op = F21_Network._getParser(self)
        op.add_option("--bridgeslaves", dest="bridgeslaves", action="store",
                default="")
        op.add_option("--bridgeopts", dest="bridgeopts", action="store",
                default="")
        op.add_option("--no-activate", dest="activate", action="store_false",
                      default=None)
        op.add_option("--bindto", dest="bindto", default=None,
                      choices=self.bind_to_choices)
        return op

    def parse(self, args):
        # call the overridden command to do it's job first
        retval = F21_Network.parse(self, args)

        # validate the network interface name
        error_message = validate_network_interface_name(retval.interfacename)
        # something is wrong with the interface name
        if error_message is not None:
            raise KickstartValueError(formatErrorMsg(self.lineno,msg=error_message))

        if retval.bridgeopts:
            if not retval.bridgeslaves:
                msg = formatErrorMsg(self.lineno, msg=_("Option --bridgeopts requires "\
                                        "--bridgeslaves to be specified"))
                raise KickstartValueError(msg)
            opts = retval.bridgeopts.split(",")
            for opt in opts:
                _key, _sep, value = opt.partition("=")
                if not value or "=" in value:
                    msg = formatErrorMsg(self.lineno, msg=_("Bad format of --bridgeopts, expecting key=value options separated by ','"))
                    raise KickstartValueError(msg)

        if retval.bindto == BIND_TO_MAC:
            if retval.vlanid and not retval.bondopts:
                msg = formatErrorMsg(self.lineno, msg=_("--bindto=%s is not supported for this type of device") % BIND_TO_MAC)
                raise KickstartValueError(msg)

        return retval
