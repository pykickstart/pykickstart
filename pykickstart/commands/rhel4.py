#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import string
import warnings

from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *
from pykickstart.version import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

### INHERIT FROM A PREVIOUS RELEASE
from fc3 import *

class RHEL4Handler(FC3Handler):
    ##
    ## DATA CLASSES
    ##
    class NetworkData(FC3Handler.NetworkData):
        def __init__(self, bootProto="dhcp", dhcpclass="", device="", essid="",
                     ethtool="", gateway="", hostname="", ip="", mtu="",
                     nameserver="", netmask="", nodns=False, notksdevice=False,
                     onboot=True, wepkey=""):
            FC3Handler.NetworkData.__init__(self, bootProto=bootProto,
                                            dhcpclass=dhcpclass, device=device,
                                            essid=essid, ethtool=ethtool,
                                            gateway=gateway, hostname=hostname,
                                            ip=ip, mtu=mtu, netmask=netmask,
                                            nameserver=nameserver, nodns=nodns,
                                            onboot=onboot, wepkey=wepkey)
            self.notksdevice = notksdevice

        def __str__(self):
            retval = FC3Handler.NetworkData.__str__().strip()

            if self.notksdevice:
                retval += " --notksdevice"

            return retval + "\n"

    ###
    ### COMMAND CLASSES
    ###
    class Network(FC3Handler.Network):
        def __init__(self, writePriority=0, network=None):
            FC3Handler.Network.__init__(self, writePriority, network)

        def parse(self, args):
            op = KSOptionParser(lineno=self.lineno)
            op.add_option("--bootproto", dest="bootProto", default="dhcp",
                          choices=["dhcp", "bootp", "static"])
            op.add_option("--class", dest="dhcpclass")
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
            op.add_option("--notksdevice", dest="notksdevice", action="store_true",
                          default=False)
            op.add_option("--onboot", dest="onboot", action="store",
                          type="ksboolean")
            op.add_option("--wepkey", dest="wepkey")

            (opts, extra) = op.parse_args(args=args)
            nd = self.handler.NetworkData()
            self._setToObj(op, opts, nd)
            self.add(nd)


    ##
    ## MAIN
    ##
    def __init__(self):
        FC3Handler.__init__(self)
        self.version = RHEL4

        self.overrideCommand(self.Network())
