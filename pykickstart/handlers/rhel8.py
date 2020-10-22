#
# Radek Vykydal <rvykydal@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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
__all__ = ["RHEL8Handler"]

from pykickstart import commands
from pykickstart.base import BaseHandler
from pykickstart.version import RHEL8

class RHEL8Handler(BaseHandler):
    version = RHEL8

    commandMap = {
        "auth": commands.authconfig.F28_Authconfig,
        "authconfig": commands.authconfig.F28_Authconfig,
        "authselect": commands.authselect.F28_Authselect,
        "autopart": commands.autopart.RHEL8_AutoPart,
        "autostep": commands.autostep.RHEL8_AutoStep,
        "bootloader": commands.bootloader.RHEL8_Bootloader,
        "btrfs": commands.btrfs.RHEL8_BTRFS,
        "cdrom": commands.cdrom.FC3_Cdrom,
        "clearpart": commands.clearpart.F28_ClearPart,
        "cmdline": commands.displaymode.F26_DisplayMode,
        "device": commands.device.F24_Device,
        "deviceprobe": commands.deviceprobe.F29_DeviceProbe,
        "dmraid": commands.dmraid.F24_DmRaid,
        "driverdisk": commands.driverdisk.F14_DriverDisk,
        "module" : commands.module.RHEL8_Module,
        "eula": commands.eula.F20_Eula,
        "fcoe": commands.fcoe.RHEL8_Fcoe,
        "firewall": commands.firewall.F28_Firewall,
        "firstboot": commands.firstboot.FC3_Firstboot,
        "graphical": commands.displaymode.F26_DisplayMode,
        "group": commands.group.F12_Group,
        "halt": commands.reboot.F23_Reboot,
        "harddrive": commands.harddrive.FC3_HardDrive,
        "hmc" : commands.hmc.F28_Hmc,
        "ignoredisk": commands.ignoredisk.F29_IgnoreDisk,
        "install": commands.install.F29_Install,
        "iscsi": commands.iscsi.F17_Iscsi,
        "iscsiname": commands.iscsiname.FC6_IscsiName,
        "keyboard": commands.keyboard.F18_Keyboard,
        "lang": commands.lang.F19_Lang,
        "liveimg": commands.liveimg.F19_Liveimg,
        "logging": commands.logging.FC6_Logging,
        "logvol": commands.logvol.RHEL8_LogVol,
        "mediacheck": commands.mediacheck.FC4_MediaCheck,
        "method": commands.method.F28_Method,
        "mount": commands.mount.F27_Mount,
        "multipath": commands.multipath.F24_MultiPath,
        "network": commands.network.F27_Network,
        "nfs": commands.nfs.FC6_NFS,
        "nvdimm": commands.nvdimm.F28_Nvdimm,
        "ostreesetup": commands.ostreesetup.RHEL8_OSTreeSetup,
        "part": commands.partition.RHEL8_Partition,
        "partition": commands.partition.RHEL8_Partition,
        "poweroff": commands.reboot.F23_Reboot,
        "raid": commands.raid.RHEL8_Raid,
        "realm": commands.realm.F19_Realm,
        "reboot": commands.reboot.F23_Reboot,
        "repo": commands.repo.RHEL8_Repo,
        "reqpart": commands.reqpart.F23_ReqPart,
        "rescue": commands.rescue.F10_Rescue,
        "rhsm": commands.rhsm.RHEL8_RHSM,
        "rootpw": commands.rootpw.F18_RootPw,
        "selinux": commands.selinux.FC3_SELinux,
        "services": commands.services.FC6_Services,
        "shutdown": commands.reboot.F23_Reboot,
        "skipx": commands.skipx.FC3_SkipX,
        "snapshot": commands.snapshot.F26_Snapshot,
        "sshpw": commands.sshpw.F24_SshPw,
        "sshkey": commands.sshkey.F22_SshKey,
        "syspurpose" : commands.syspurpose.RHEL8_Syspurpose,
        "text": commands.displaymode.F26_DisplayMode,
        "timezone": commands.timezone.F25_Timezone,
        "updates": commands.updates.F7_Updates,
        "url": commands.url.RHEL8_Url,
        "user": commands.user.F24_User,
        "vnc": commands.vnc.F9_Vnc,
        "volgroup": commands.volgroup.RHEL8_VolGroup,
        "xconfig": commands.xconfig.F14_XConfig,
        "zerombr": commands.zerombr.F9_ZeroMbr,
        "zfcp": commands.zfcp.F14_ZFCP,
        "zipl": commands.zipl.RHEL8_Zipl,
    }

    dataMap = {
        "BTRFSData": commands.btrfs.F23_BTRFSData,
        "DriverDiskData": commands.driverdisk.F14_DriverDiskData,
        "DeviceData": commands.device.F8_DeviceData,
        "DmRaidData": commands.dmraid.FC6_DmRaidData,
        "ModuleData" : commands.module.RHEL8_ModuleData,
        "FcoeData": commands.fcoe.RHEL8_FcoeData,
        "GroupData": commands.group.F12_GroupData,
        "IscsiData": commands.iscsi.F17_IscsiData,
        "LogVolData": commands.logvol.RHEL8_LogVolData,
        "MountData": commands.mount.F27_MountData,
        "MultiPathData": commands.multipath.FC6_MultiPathData,
        "NetworkData": commands.network.F27_NetworkData,
        "NvdimmData": commands.nvdimm.F28_NvdimmData,
        "PartData": commands.partition.RHEL8_PartData,
        "RaidData": commands.raid.RHEL8_RaidData,
        "RepoData": commands.repo.RHEL8_RepoData,
        "SnapshotData": commands.snapshot.F26_SnapshotData,
        "SshPwData": commands.sshpw.F24_SshPwData,
        "SshKeyData": commands.sshkey.F22_SshKeyData,
        "UserData": commands.user.F19_UserData,
        "VolGroupData": commands.volgroup.RHEL8_VolGroupData,
        "ZFCPData": commands.zfcp.F14_ZFCPData,
    }
