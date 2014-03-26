#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006, 2007 Red Hat, Inc.
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
__all__ = ["FC6Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import FC6

class FC6Handler(BaseHandler):
    version = FC6

    commandMap = {
        "auth": commands.authconfig.FC3_Authconfig,
        "authconfig": commands.authconfig.FC3_Authconfig,
        "autopart": commands.autopart.FC3_AutoPart,
        "autostep": commands.autostep.FC3_AutoStep,
        "bootloader": commands.bootloader.FC4_Bootloader,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.FC3_ClearPart,
        "cmdline": commands.displaymode.FC3_DisplayMode,
        "device": commands.device.FC3_Device,
        "deviceprobe": commands.deviceprobe.FC3_DeviceProbe,
        "dmraid": commands.dmraid.FC6_DmRaid,
        "driverdisk": commands.driverdisk.FC4_DriverDisk,
        "firewall": commands.firewall.FC3_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.FC3_DisplayMode,
        "halt": commands.reboot.FC6_Reboot,
        "harddrive": commands.harddrive.FC3_HardDrive,
        "ignoredisk": commands.ignoredisk.FC3_IgnoreDisk,
        "install": commands.upgrade.FC3_Upgrade,
        "interactive": commands.interactive.FC3_Interactive,
        "iscsi": commands.iscsi.FC6_Iscsi,
        "iscsiname": commands.iscsiname.FC6_IscsiName,
        "keyboard": commands.keyboard.FC3_Keyboard,
        "lang": commands.lang.FC3_Lang,
        "langsupport": commands.langsupport.FC5_LangSupport,
        "logging": commands.logging.FC6_Logging,
        "logvol": commands.logvol.FC4_LogVol,
        "mediacheck": commands.mediacheck.FC4_MediaCheck,
        "method": commands.method.FC6_Method,
        "monitor": commands.monitor.FC6_Monitor,
        "mouse": commands.mouse.FC3_Mouse,
        "multipath": commands.multipath.FC6_MultiPath,
        "network": commands.network.FC6_Network,
        "nfs": commands.nfs.FC6_NFS,
        "part": commands.partition.FC4_Partition,
        "partition": commands.partition.FC4_Partition,
        "poweroff": commands.reboot.FC6_Reboot,
        "raid": commands.raid.FC5_Raid,
        "reboot": commands.reboot.FC6_Reboot,
        "repo": commands.repo.FC6_Repo,
        "rootpw": commands.rootpw.FC3_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "services": commands.services.FC6_Services,
        "shutdown": commands.reboot.FC6_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "text": commands.displaymode.FC3_DisplayMode,
        "timezone": commands.timezone.FC6_Timezone,
        "upgrade": commands.upgrade.FC3_Upgrade,
        "user": commands.user.FC6_User,
        "url": commands.url.FC3_Url,
        "vnc": commands.vnc.FC6_Vnc,
        "volgroup": commands.volgroup.FC3_VolGroup,
        "xconfig": commands.xconfig.FC6_XConfig,
        "zerombr": commands.zerombr.FC3_ZeroMbr,
        "zfcp": commands.zfcp.FC3_ZFCP,
    }

    dataMap = {
        "DriverDiskData": commands.driverdisk.FC4_DriverDiskData,
        "DmRaidData": commands.dmraid.FC6_DmRaidData,
        "IscsiData": commands.iscsi.FC6_IscsiData,
        "LogVolData": commands.logvol.FC4_LogVolData,
        "MultiPathData": commands.multipath.FC6_MultiPathData,
        "NetworkData": commands.network.FC6_NetworkData,
        "PartData": commands.partition.FC4_PartData,
        "RaidData": commands.raid.FC5_RaidData,
        "RepoData": commands.repo.FC6_RepoData,
        "UserData": commands.user.FC6_UserData,
        "VolGroupData": commands.volgroup.FC3_VolGroupData,
        "ZFCPData": commands.zfcp.FC3_ZFCPData,
    }
