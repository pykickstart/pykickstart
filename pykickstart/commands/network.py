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
from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_NetworkData(BaseData):
    def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                 essid="", ethtool="", gateway="", hostname="", ip="",
                 mtu="", nameserver="", netmask="", nodns=False,
                 onboot=True, wepkey=""):
        BaseData.__init__(self)
        self.bootProto = bootProto
        self.dhcpclass = dhcpclass
        self.device = device
        self.essid = essid
        self.ethtool = ethtool
        self.gateway = gateway
        self.hostname = hostname
        self.ip = ip
        self.mtu = mtu
        self.nameserver = nameserver
        self.netmask = netmask
        self.nodns = nodns
        self.onboot = onboot
        self.wepkey = wepkey

    def __str__(self):
        retval = "network"

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
        if self.onboot:
            retval += " --onboot=on"
        if self.wepkey != "":
            retval += " --wepkey=%s" % self.wepkey

        return retval + "\n"

class FC4_NetworkData(FC3_NetworkData):
    def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                 essid="", ethtool="", gateway="", hostname="", ip="",
                 mtu="", nameserver="", netmask="", nodns=False,
                 notksdevice=False, onboot=True, wepkey=""):
        FC3_NetworkData.__init__(self, bootProto=bootProto,
                                dhcpclass=dhcpclass, device=device,
                                essid=essid, ethtool=ethtool,
                                gateway=gateway, hostname=hostname,
                                ip=ip, mtu=mtu, netmask=netmask,
                                nameserver=nameserver, nodns=nodns,
                                onboot=onboot, wepkey=wepkey)
        self.notksdevice = notksdevice

    def __str__(self):
        retval = FC3_NetworkData.__str__(self).strip()

        if self.notksdevice:
            retval += " --notksdevice"

        return retval + "\n"

class FC6_NetworkData(FC4_NetworkData):
    def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                 essid="", ethtool="", gateway="", hostname="", ip="",
                 noipv4=False, noipv6=False, mtu="", nameserver="", netmask="",
                 nodns=False, notksdevice=False, onboot=True, wepkey=""):
        FC4_NetworkData.__init__(self, bootProto=bootProto,
                                dhcpclass=dhcpclass, device=device,
                                essid=essid, ethtool=ethtool,
                                gateway=gateway, hostname=hostname,
                                ip=ip, mtu=mtu, netmask=netmask,
                                nameserver=nameserver, nodns=nodns,
                                notksdevice=notksdevice,
                                onboot=onboot, wepkey=wepkey)
        self.noipv4 = noipv4
        self.noipv6 = noipv6

    def __str__(self):
        retval = "network"

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
        if self.noipv4:
            retval += " --noipv4"
        if self.noipv6:
            retval += " --noipv6"
        if self.mtu != "":
            retval += " --mtu=%s" % self.mtu
        if self.nameserver != "":
            retval += " --nameserver=%s" % self.nameserver
        if self.netmask != "":
            retval += " --netmask=%s" % self.netmask
        if self.nodns:
            retval += " --nodns"
        if self.notksdevice:
            retval += " --notksdevice"
        if self.onboot:
            retval += " --onboot=on"
        if self.wepkey != "":
            retval += " --wepkey=%s" % self.wepkey

        return retval + "\n"

class F8_NetworkData(FC6_NetworkData):
    def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                 essid="", ethtool="", gateway="", hostname="", ip="", ipv6="",
                 noipv4=False, noipv6=False, mtu="", nameserver="", netmask="",
                 nodns=False, notksdevice=False, onboot=True, wepkey=""):
        FC6_NetworkData.__init__(self, bootProto=bootProto,
                                dhcpclass=dhcpclass, device=device,
                                essid=essid, ethtool=ethtool,
                                gateway=gateway, hostname=hostname,
                                ip=ip, mtu=mtu, netmask=netmask,
                                nameserver=nameserver, nodns=nodns,
                                notksdevice=notksdevice, noipv4=noipv4,
                                noipv6=noipv6, onboot=onboot, wepkey=wepkey)
        self.ipv6 = ipv6

    def __str__(self):
        retval = FC6_NetworkData.__str__(self).strip()

        if self.ipv6 != "":
            retval += " --ipv6" % self.ipv6

        return retval + "\n"

class RHEL4_NetworkData(FC3_NetworkData):
    def __init__(self, bootProto=BOOTPROTO_DHCP, dhcpclass="", device="",
                 essid="", ethtool="", gateway="", hostname="", ip="",
                 mtu="", nameserver="", netmask="", nodns=False,
                 notksdevice=False, onboot=True, wepkey=""):
        FC3_NetworkData.__init__(self, bootProto=bootProto,
                                dhcpclass=dhcpclass, device=device,
                                essid=essid, ethtool=ethtool,
                                gateway=gateway, hostname=hostname,
                                ip=ip, mtu=mtu, netmask=netmask,
                                nameserver=nameserver, nodns=nodns,
                                onboot=onboot, wepkey=wepkey)
        self.notksdevice = notksdevice

    def __str__(self):
        retval = FC3_NetworkData.__str__(self).strip()

        if self.notksdevice:
            retval += " --notksdevice"

        return retval + "\n"

class FC3_Network(KickstartCommand):
    def __init__(self, writePriority=0, network=None):
        KickstartCommand.__init__(self, writePriority)

        if network == None:
            network = []

        self.network = network

    def __str__(self):
        retval = ""

        for nic in self.network:
            retval += nic.__str__()

        if retval != "":
            return "# Network information\n" + retval
        else:
            return ""

    def _populateParser(self, op):
        op.add_option("--bootproto", dest="bootProto",
                      default=BOOTPROTO_DHCP,
                      choices=[BOOTPROTO_DHCP, BOOTPROTO_BOOTP,
                               BOOTPROTO_STATIC])
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

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        self._populateParser(op)

        (opts, extra) = op.parse_args(args=args)
        nd = FC3_NetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)

    def add(self, newObj):
        self.network.append(newObj)

class FC4_Network(FC3_Network):
    def __init__(self, writePriority=0, network=None):
        FC3_Network.__init__(self, writePriority, network)

    def _populateParser(self, op):
        FC3_Network._populateParser(self, op)
        op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                      default=False)

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        self._populateParser(op)

        (opts, extra) = op.parse_args(args=args)
        nd = FC4_NetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)

class FC6_Network(FC4_Network):
    def __init__(self, writePriority=0, network=None):
        FC4_Network.__init__(self, writePriority, network)

    def _populateParser(self, op):
        FC4_Network._populateParser(self, op)
        op.add_option("--noipv4", dest="noipv4", action="store_true",
                      default=False)
        op.add_option("--noipv6", dest="noipv6", action="store_true",
                      default=False)

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        self._populateParser(op)

        (opts, extra) = op.parse_args(args=args)
        nd = FC6_NetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)

class F8_Network(FC6_Network):
    def __init__(self, writePriority=0, network=None):
        FC6_Network.__init__(self, writePriority, network)

    def _populateParser(self, op):
        FC6_Network._populateParser(self, op)
        op.add_option("--ipv6", dest="ipv6")

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        self._populateParser(op)

        (opts, extra) = op.parse_args(args=args)
        nd = F8_NetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)

class RHEL4_Network(FC3_Network):
    def __init__(self, writePriority=0, network=None):
        FC3_Network.__init__(self, writePriority, network)

    def _populateParser(self, op):
        FC3_Network._populateParser(self, op)
        op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                      default=False)

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        self._populateParser(op)

        (opts, extra) = op.parse_args(args=args)
        nd = RHEL4_NetworkData()
        self._setToObj(op, opts, nd)
        self.add(nd)
