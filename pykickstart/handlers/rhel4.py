#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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
__all__ = ["RHEL4Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import RHEL4

class RHEL4Handler(BaseHandler):
    version = RHEL4

    commandMap = {
        "auth": commands.authconfig.FC3_Authconfig,
        "authconfig": commands.authconfig.FC3_Authconfig,
        "autopart": commands.autopart.FC3_AutoPart,
        "autostep": commands.autostep.FC3_AutoStep,
        "bootloader": commands.bootloader.FC3_Bootloader,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.FC3_ClearPart,
        "cmdline": commands.displaymode.FC3_DisplayMode,
        "device": commands.device.FC3_Device,
        "deviceprobe": commands.deviceprobe.FC3_DeviceProbe,
        "driverdisk": commands.driverdisk.FC4_DriverDisk,
        "firewall": commands.firewall.FC3_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.FC3_DisplayMode,
        "halt": commands.reboot.FC3_Reboot,
        "harddrive": commands.harddrive.FC3_HardDrive,
        "ignoredisk": commands.ignoredisk.F8_IgnoreDisk,
        "install": commands.upgrade.FC3_Upgrade,
        "interactive": commands.interactive.FC3_Interactive,
        "keyboard": commands.keyboard.FC3_Keyboard,
        "lang": commands.lang.FC3_Lang,
        "langsupport": commands.langsupport.FC3_LangSupport,
        "lilo": commands.bootloader.FC3_Lilo,
        "lilocheck": commands.lilocheck.FC3_LiloCheck,
        "logvol": commands.logvol.FC3_LogVol,
        "method": commands.method.FC3_Method,
        "monitor": commands.monitor.FC3_Monitor,
        "mouse": commands.mouse.FC3_Mouse,
        "network": commands.network.RHEL4_Network,
        "nfs": commands.nfs.FC3_NFS,
        "part": commands.partition.FC3_Partition,
        "partition": commands.partition.FC3_Partition,
        "poweroff": commands.reboot.FC3_Reboot,
        "raid": commands.raid.FC3_Raid,
        "reboot": commands.reboot.FC3_Reboot,
        "rootpw": commands.rootpw.FC3_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "shutdown": commands.reboot.FC3_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "text": commands.displaymode.FC3_DisplayMode,
        "timezone": commands.timezone.FC3_Timezone,
        "upgrade": commands.upgrade.FC3_Upgrade,
        "url": commands.url.FC3_Url,
        "vnc": commands.vnc.FC3_Vnc,
        "volgroup": commands.volgroup.FC3_VolGroup,
        "xconfig": commands.xconfig.FC3_XConfig,
        "zerombr": commands.zerombr.FC3_ZeroMbr,
        "zfcp": commands.zfcp.FC3_ZFCP,
    }

    dataMap = {
        "DriverDiskData": commands.driverdisk.FC4_DriverDiskData,
        "LogVolData": commands.logvol.FC3_LogVolData,
        "NetworkData": commands.network.RHEL4_NetworkData,
        "PartData": commands.partition.FC3_PartData,
        "RaidData": commands.raid.FC3_RaidData,
        "VolGroupData": commands.volgroup.FC3_VolGroupData,
        "ZFCPData": commands.zfcp.FC3_ZFCPData,
    }
