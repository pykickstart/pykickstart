#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2012, 2015 Red Hat, Inc.
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
__all__ = ["RHEL7Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import RHEL7

class RHEL7Handler(BaseHandler):
    version = RHEL7

    commandMap = {
        "auth": commands.authconfig.FC3_Authconfig,
        "authconfig": commands.authconfig.FC3_Authconfig,
        "autopart": commands.autopart.RHEL7_AutoPart,
        "autostep": commands.autostep.FC3_AutoStep,
        "bootloader": commands.bootloader.RHEL7_Bootloader,
        "btrfs": commands.btrfs.RHEL7_BTRFS,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.RHEL7_ClearPart,
        "cmdline": commands.displaymode.FC3_DisplayMode,
        "device": commands.device.F8_Device,
        "deviceprobe": commands.deviceprobe.FC3_DeviceProbe,
        "dmraid": commands.dmraid.FC6_DmRaid,
        "driverdisk": commands.driverdisk.F14_DriverDisk,
        "eula": commands.eula.F20_Eula,
        "fcoe": commands.fcoe.RHEL7_Fcoe,
        "firewall": commands.firewall.F20_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.FC3_DisplayMode,
        "group": commands.group.F12_Group,
        "halt": commands.reboot.F18_Reboot,
        "harddrive": commands.harddrive.FC3_HardDrive,
        "hmc": commands.hmc.RHEL7_Hmc,
        "ignoredisk": commands.ignoredisk.F14_IgnoreDisk,
        "install": commands.upgrade.F11_Upgrade,
        "iscsi": commands.iscsi.F17_Iscsi,
        "iscsiname": commands.iscsiname.FC6_IscsiName,
        "keyboard": commands.keyboard.F18_Keyboard,
        "lang": commands.lang.F19_Lang,
        "liveimg": commands.liveimg.F19_Liveimg,
        "logging": commands.logging.FC6_Logging,
        "logvol": commands.logvol.RHEL7_LogVol,
        "mediacheck": commands.mediacheck.FC4_MediaCheck,
        "method": commands.method.RHEL7_Method,
        "multipath": commands.multipath.FC6_MultiPath,
        "network": commands.network.RHEL7_Network,
        "nfs": commands.nfs.FC6_NFS,
        "nvdimm": commands.nvdimm.F28_Nvdimm,
        "ostreesetup": commands.ostreesetup.RHEL7_OSTreeSetup,
        "part": commands.partition.RHEL7_Partition,
        "partition": commands.partition.RHEL7_Partition,
        "poweroff": commands.reboot.F18_Reboot,
        "raid": commands.raid.RHEL7_Raid,
        "realm": commands.realm.F19_Realm,
        "reboot": commands.reboot.F18_Reboot,
        "repo": commands.repo.RHEL7_Repo,
        "reqpart": commands.reqpart.RHEL7_ReqPart,
        "rescue": commands.rescue.F10_Rescue,
        "rootpw": commands.rootpw.F18_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "services": commands.services.FC6_Services,
        "shutdown": commands.reboot.F18_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "snapshot": commands.snapshot.F26_Snapshot,
        "sshpw": commands.sshpw.F13_SshPw,
        "text": commands.displaymode.FC3_DisplayMode,
        "timezone": commands.timezone.RHEL7_Timezone,
        "unsupported_hardware": commands.unsupported_hardware.RHEL6_UnsupportedHardware,
        "updates": commands.updates.F7_Updates,
        "upgrade": commands.upgrade.F20_Upgrade,
        "url": commands.url.RHEL7_Url,
        "user": commands.user.F19_User,
        "vnc": commands.vnc.F9_Vnc,
        "volgroup": commands.volgroup.RHEL7_VolGroup,
        "xconfig": commands.xconfig.F14_XConfig,
        "zerombr": commands.zerombr.F9_ZeroMbr,
        "zfcp": commands.zfcp.F14_ZFCP,
    }

    dataMap = {
        "BTRFSData": commands.btrfs.RHEL7_BTRFSData,
        "DriverDiskData": commands.driverdisk.F14_DriverDiskData,
        "DeviceData": commands.device.F8_DeviceData,
        "DmRaidData": commands.dmraid.FC6_DmRaidData,
        "FcoeData": commands.fcoe.RHEL7_FcoeData,
        "GroupData": commands.group.F12_GroupData,
        "IscsiData": commands.iscsi.F17_IscsiData,
        "LogVolData": commands.logvol.RHEL7_LogVolData,
        "MultiPathData": commands.multipath.FC6_MultiPathData,
        "NetworkData": commands.network.RHEL7_NetworkData,
        "NvdimmData": commands.nvdimm.F28_NvdimmData,
        "PartData": commands.partition.RHEL7_PartData,
        "RaidData": commands.raid.RHEL7_RaidData,
        "RepoData": commands.repo.RHEL7_RepoData,
        "SnapshotData": commands.snapshot.F26_SnapshotData,
        "SshPwData": commands.sshpw.F13_SshPwData,
        "UserData": commands.user.F19_UserData,
        "VolGroupData": commands.volgroup.RHEL7_VolGroupData,
        "ZFCPData": commands.zfcp.F14_ZFCPData,
    }
