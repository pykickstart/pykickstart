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
__all__ = ["F9Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import F9

class F9Handler(BaseHandler):
    version = F9

    commandMap = {
        "auth": commands.authconfig.FC3_Authconfig,
        "authconfig": commands.authconfig.FC3_Authconfig,
        "autopart": commands.autopart.F9_AutoPart,
        "autostep": commands.autostep.FC3_AutoStep,
        "bootloader": commands.bootloader.F8_Bootloader,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.FC3_ClearPart,
        "cmdline": commands.displaymode.FC3_DisplayMode,
        "device": commands.device.F8_Device,
        "deviceprobe": commands.deviceprobe.FC3_DeviceProbe,
        "dmraid": commands.dmraid.FC6_DmRaid,
        "driverdisk": commands.driverdisk.FC4_DriverDisk,
        "firewall": commands.firewall.F9_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.FC3_DisplayMode,
        "halt": commands.reboot.FC6_Reboot,
        "harddrive": commands.harddrive.FC3_HardDrive,
        "ignoredisk": commands.ignoredisk.F8_IgnoreDisk,
        "install": commands.upgrade.FC3_Upgrade,
        "interactive": commands.interactive.FC3_Interactive,
        "iscsi": commands.iscsi.FC6_Iscsi,
        "iscsiname": commands.iscsiname.FC6_IscsiName,
        "keyboard": commands.keyboard.FC3_Keyboard,
        "lang": commands.lang.FC3_Lang,
        "logging": commands.logging.FC6_Logging,
        "logvol": commands.logvol.F9_LogVol,
        "mediacheck": commands.mediacheck.FC4_MediaCheck,
        "method": commands.method.FC6_Method,
        "monitor": commands.monitor.FC6_Monitor,
        "multipath": commands.multipath.FC6_MultiPath,
        "network": commands.network.F9_Network,
        "nfs": commands.nfs.FC6_NFS,
        "part": commands.partition.F9_Partition,
        "partition": commands.partition.F9_Partition,
        "poweroff": commands.reboot.FC6_Reboot,
        "raid": commands.raid.F9_Raid,
        "reboot": commands.reboot.FC6_Reboot,
        "repo": commands.repo.F8_Repo,
        "rootpw": commands.rootpw.F8_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "services": commands.services.FC6_Services,
        "shutdown": commands.reboot.FC6_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "text": commands.displaymode.FC3_DisplayMode,
        "timezone": commands.timezone.FC6_Timezone,
        "updates": commands.updates.F7_Updates,
        "upgrade": commands.upgrade.FC3_Upgrade,
        "url": commands.url.FC3_Url,
        "user": commands.user.F8_User,
        "vnc": commands.vnc.F9_Vnc,
        "volgroup": commands.volgroup.FC3_VolGroup,
        "xconfig": commands.xconfig.F9_XConfig,
        "zerombr": commands.zerombr.F9_ZeroMbr,
        "zfcp": commands.zfcp.FC3_ZFCP,
    }

    dataMap = {
        "DriverDiskData": commands.driverdisk.FC4_DriverDiskData,
        "DeviceData": commands.device.F8_DeviceData,
        "DmRaidData": commands.dmraid.FC6_DmRaidData,
        "IscsiData": commands.iscsi.FC6_IscsiData,
        "LogVolData": commands.logvol.F9_LogVolData,
        "MultiPathData": commands.multipath.FC6_MultiPathData,
        "NetworkData": commands.network.F8_NetworkData,
        "PartData": commands.partition.F9_PartData,
        "RaidData": commands.raid.F9_RaidData,
        "RepoData": commands.repo.F8_RepoData,
        "UserData": commands.user.F8_UserData,
        "VolGroupData": commands.volgroup.FC3_VolGroupData,
        "ZFCPData": commands.zfcp.FC3_ZFCPData,
    }
