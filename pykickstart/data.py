#
# data.py:  Kickstart data representation.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from constants import *

class KickstartData:
    def __init__(self):
        # Set by command handlers.
        self.authconfig = ""
        self.autopart = False
        self.autostep = {"autoscreenshot": False}
        self.bootloader = {"appendLine": "", "driveorder": [],
                           "forceLBA": False, "location": "mbr", "md5pass": "",
                           "password": "", "upgrade": False, "hvArgs": ""}
        self.dmraids = []
        self.encrypted = False
        self.mpaths = []
        self.clearpart = {"drives": [], "initAll": False,
                          "type": CLEARPART_TYPE_NONE}
        self.device = ""
        self.deviceprobe = ""
        self.displayMode = DISPLAY_MODE_GRAPHICAL
        self.driverdisk = ""
        self.firewall = {"enabled": True, "ports": [], "trusts": [], "disableSsh": False}
        self.firstboot = FIRSTBOOT_SKIP
        self.ignoredisk = {"drives": [], "onlyuse": []}
        self.interactive = False
        self.iscsi = []
        self.iscsiname = ""
        self.key = ""
        self.keyboard = ""
        self.lang = ""
        self.logging = {"host": "", "level": "info", "port": ""}
        self.mediacheck = False
        self.method = {"method": ""}
        self.monitor = {"hsync": "", "monitor": "", "probe": True, "vsync": ""}
        self.network = []
        self.platform = ""
        self.reboot = {"action": KS_WAIT, "eject": False}
        self.rootpw = {"isCrypted": False, "password": ""}
        self.selinux = SELINUX_ENFORCING
        self.services = {"disabled": [], "enabled": []}
        self.skipx = False
        self.timezone = {"isUtc": False, "timezone": ""}
        self.upgrade = False
        self.vnc = {"enabled": False, "password": "", "host": "", "port": ""}
        self.xconfig = {"driver": "", "defaultdesktop": "", "depth": 0,
                        "resolution": "", "startX": False, "videoRam": ""}
        self.zerombr = False
        self.zfcp = []

        self.lvList = []
        self.partitions = []
        self.raidList = []
        self.vgList = []

        self.repoList = []
        self.userList = []

        # Set by %package header.
        self.excludeDocs = False
        self.addBase = True
        self.handleMissing = KS_MISSING_PROMPT

        # Set by sections.
        self.groupList = []
        self.packageList = []
        self.excludedList = []
        self.excludedGroupList = []
        self.scripts = []

class KickstartLogVolData:
    def __init__(self):
        self.bytesPerInode = 4096
        self.fsopts = ""
        self.fstype = ""
        self.grow = False
        self.maxSizeMB = 0
        self.name = ""
        self.format = True
        self.percent = 0
        self.recommended = False
        self.size = None
        self.preexist = False
        self.vgname = ""
        self.mountpoint = ""
        self.encrypted = False

class KickstartNetworkData:
    def __init__(self):
        self.bootProto = "dhcp"
        self.dhcpclass = ""
        self.device = ""
        self.essid = ""
        self.ethtool = ""
        self.gateway = ""
        self.hostname = ""
        self.ip = ""
        self.ipv4 = True
        self.ipv6 = True
        self.mtu = ""
        self.nameserver = ""
        self.netmask = ""
        self.nodns = False
        self.notksdevice = False
        self.onboot = True
        self.wepkey = ""

class KickstartPartData:
    def __init__ (self):
        self.active = False
        self.primOnly = False
        self.bytesPerInode = 4096
        self.end = 0
        self.fsopts = ""
        self.fstype = ""
        self.grow = False
        self.label = ""
        self.maxSizeMB = 0
        self.format = True
        self.onbiosdisk = ""
        self.disk = ""
        self.onPart = ""
        self.recommended = False
        self.size = None
        self.start = 0
        self.mountpoint = ""
        self.encrypted = False

class KickstartRaidData:
    def __init__ (self):
        self.device = None
        self.fsopts = ""
        self.fstype = ""
        self.level = ""
        self.format = True
        self.spares = 0
        self.preexist = False
        self.mountpoint = ""
        self.members = []
        self.bytesPerInode = 4096
        self.encrypted = False

class KickstartRepoData:
    def __init__ (self):
        self.baseurl = ""
        self.mirrorlist = ""
        self.name = ""

class KickstartUserData:
    def __init__ (self):
        self.groups = []
        self.homedir = ""
        self.isCrypted = False
        self.name = ""
        self.password = ""
        self.shell = ""
        self.uid = None

class KickstartVolGroupData:
    def __init__(self):
        self.format = True
        self.pesize = 32768
        self.preexist = False
        self.vgname = ""
        self.physvols = []

class KickstartDmRaidData:
    def __init__(self):
        self.name = ""
        self.devices = []
        self.dmset = None

class KickstartMpPathData:
    def __init__(self):
        self.mpdev = ""
        self.device = ""
        self.rule = ""

class KickstartMultiPathData:
    def __init__(self):
        self.name = ""
        self.paths = []

class KickstartIscsiData:
    def __init__(self):
        self.ipaddr = ""
        self.port = "3260"
        self.target = ""
        self.user = None
        self.password = None
        self.user_in = None
        self.password_in = None

class KickstartZFCPData:
    def __init__(self):
        self.devnum = ""
        self.wwpn = ""
        self.fcplun = ""
        self.scsiid = ""
        self.scsilun = ""
