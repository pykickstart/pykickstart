#
# Copyright 2021 Red Hat, Inc.
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
__all__ = ["F36Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import F36

class F36Handler(BaseHandler):
    version = F36

    commandMap = {
        "auth": commands.authconfig.F35_Authconfig, # RemovedCommand
        "authconfig": commands.authconfig.F35_Authconfig, # RemovedCommand
        "authselect": commands.authselect.F28_Authselect,
        "autopart": commands.autopart.F29_AutoPart,
        "autostep": commands.autostep.F34_AutoStep,
        "bootloader": commands.bootloader.F34_Bootloader,
        "btrfs": commands.btrfs.F23_BTRFS,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.F28_ClearPart,
        "cmdline": commands.displaymode.F26_DisplayMode,
        "device": commands.device.F34_Device,
        "deviceprobe": commands.deviceprobe.F34_DeviceProbe,
        "dmraid": commands.dmraid.F34_DmRaid,
        "driverdisk": commands.driverdisk.F14_DriverDisk,
        "module": commands.module.F31_Module,
        "eula": commands.eula.F20_Eula,
        "fcoe": commands.fcoe.F28_Fcoe,
        "firewall": commands.firewall.F28_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.F26_DisplayMode,
        "group": commands.group.F12_Group,
        "halt": commands.reboot.F23_Reboot,
        "harddrive": commands.harddrive.F33_HardDrive,
        "hmc": commands.hmc.F28_Hmc,
        "ignoredisk": commands.ignoredisk.F34_IgnoreDisk,
        "install": commands.install.F34_Install,
        "iscsi": commands.iscsi.F17_Iscsi,
        "iscsiname": commands.iscsiname.FC6_IscsiName,
        "keyboard": commands.keyboard.F18_Keyboard,
        "lang": commands.lang.F19_Lang,
        "liveimg": commands.liveimg.F19_Liveimg,
        "logging": commands.logging.F34_Logging,
        "logvol": commands.logvol.F29_LogVol,
        "mediacheck": commands.mediacheck.FC4_MediaCheck,
        "method": commands.method.F34_Method,
        "mount": commands.mount.F27_Mount,
        "multipath": commands.multipath.F34_MultiPath,
        "network": commands.network.F27_Network,
        "nfs": commands.nfs.FC6_NFS,
        "nvdimm": commands.nvdimm.F28_Nvdimm,
        "timesource": commands.timesource.F33_Timesource,
        "ostreesetup": commands.ostreesetup.F21_OSTreeSetup,
        "part": commands.partition.F34_Partition,
        "partition": commands.partition.F34_Partition,
        "poweroff": commands.reboot.F23_Reboot,
        "raid": commands.raid.F29_Raid,
        "realm": commands.realm.F19_Realm,
        "reboot": commands.reboot.F23_Reboot,
        "repo": commands.repo.F33_Repo,
        "reqpart": commands.reqpart.F23_ReqPart,
        "rescue": commands.rescue.F10_Rescue,
        "rootpw": commands.rootpw.F18_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "services": commands.services.FC6_Services,
        "shutdown": commands.reboot.F23_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "snapshot": commands.snapshot.F26_Snapshot,
        "sshpw": commands.sshpw.F24_SshPw,
        "sshkey": commands.sshkey.F22_SshKey,
        "text": commands.displaymode.F26_DisplayMode,
        "timezone": commands.timezone.F33_Timezone,
        "updates": commands.updates.F34_Updates,
        "url": commands.url.F30_Url,
        "user": commands.user.F24_User,
        "vnc": commands.vnc.F9_Vnc,
        "volgroup": commands.volgroup.F21_VolGroup,
        "xconfig": commands.xconfig.F14_XConfig,
        "zerombr": commands.zerombr.F9_ZeroMbr,
        "zfcp": commands.zfcp.F14_ZFCP,
        "zipl": commands.zipl.F32_Zipl,
    }

    dataMap = {
        "BTRFSData": commands.btrfs.F23_BTRFSData,
        "DriverDiskData": commands.driverdisk.F14_DriverDiskData,
        "DeviceData": commands.device.F8_DeviceData,
        "DmRaidData": commands.dmraid.FC6_DmRaidData,
        "ModuleData": commands.module.F31_ModuleData,
        "TimesourceData": commands.timesource.F33_TimesourceData,
        "FcoeData": commands.fcoe.F28_FcoeData,
        "GroupData": commands.group.F12_GroupData,
        "IscsiData": commands.iscsi.F17_IscsiData,
        "LogVolData": commands.logvol.F29_LogVolData,
        "MountData": commands.mount.F27_MountData,
        "MultiPathData": commands.multipath.FC6_MultiPathData,
        "NetworkData": commands.network.F27_NetworkData,
        "NvdimmData": commands.nvdimm.F28_NvdimmData,
        "PartData": commands.partition.F29_PartData,
        "RaidData": commands.raid.F29_RaidData,
        "RepoData": commands.repo.F30_RepoData,
        "SnapshotData": commands.snapshot.F26_SnapshotData,
        "SshPwData": commands.sshpw.F24_SshPwData,
        "SshKeyData": commands.sshkey.F22_SshKeyData,
        "UserData": commands.user.F19_UserData,
        "VolGroupData": commands.volgroup.F21_VolGroupData,
        "ZFCPData": commands.zfcp.F14_ZFCPData,
    }
