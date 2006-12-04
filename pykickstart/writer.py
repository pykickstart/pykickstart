#
# writer.py:  Kickstart file writer.
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
import string
from constants import *

class KickstartWriter:
    def __init__(self, ksdata):
        # All the printing handlers in the order they should be called.
        self.handlers = [self.doPlatform,

                         self.doAuthconfig, self.doMultiPath, self.doDmRaid,
                         self.doAutoPart, self.doAutoStep, self.doBootloader,
                         self.doZeroMbr, self.doClearPart, self.doDevice,
                         self.doDeviceProbe, self.doDisplayMode,
                         self.doDriverDisk, self.doFirewall, self.doFirstboot,
                         self.doIgnoreDisk, self.doInteractive, self.doIscsi,
                         self.doIscsiName, self.doKey, self.doKeyboard,
                         self.doLang, self.doLogging, self.doMediaCheck,
                         self.doMethod, self.doNetwork, self.doReboot,
                         self.doRepo, self.doRootPw, self.doSELinux,
                         self.doServices, self.doSkipX, self.doTimezone,
                         self.doUpgrade, self.doUser, self.doVnc,
                         self.doXConfig, self.doMonitor, self.doZFCP,

                         self.doPartition, self.doVolumeGroup,
                         self.doLogicalVolume, self.doRaid,

                         self.doScripts, self.doPackages]

        self.ksdata = ksdata

    # Return a string representation of the ksdata suitable for writing to
    # a file.
    def write(self):
        return string.join(filter (lambda str: str != None and str != "",
                                  map (lambda fn: fn(), self.handlers)), "\n")

    def doPlatform(self):
        if self.ksdata.platform != "":
            return "#platform=%s" % self.ksdata.platform

    def doAuthconfig(self):
        if self.ksdata.authconfig != "" and not self.ksdata.upgrade:
            return "# System authorization information\nauth %s" % self.ksdata.authconfig

    def doMultiPath(self):
        rets = []

        for mpath in self.ksdata.mpaths:
            for path in mpath.paths:
                rets.append("multipath --mpdev=%s --device=%s --rule=\"%s\"" \
                    % (mpath.name, path.device, path.rule))

        return string.join(rets, "\n")

    def doDmRaid(self):
        retval = ""

        for raid in self.ksdata.dmraids:
            retval = retval + "dmraid --name=%s" % (raid.name,)

            for dev in raid.devices:
                retval = retval + "--dev=\"%s\"" % (dev,)

            retval = retval + "\n"
        return retval

    def doAutoPart(self):
        if self.ksdata.autopart:
            return "autopart"

    def doAutoStep(self):
        if self.ksdata.autostep["autoscreenshot"]:
            return "autostep --autoscreenshot"

    def doBootloader(self):
        retval = "# System bootloader configuration\nbootloader"

        if self.ksdata.bootloader["appendLine"] != "":
            retval = retval + " --append=\"%s\"" % self.ksdata.bootloader["appendLine"]
        if self.ksdata.bootloader["location"]:
            retval = retval + " --location=%s" % self.ksdata.bootloader["location"]
        if self.ksdata.bootloader["forceLBA"]:
            retval = retval + " --lba32"
        if self.ksdata.bootloader["password"] != "":
            retval = retval + " --password=%s" % self.ksdata.bootloader["password"]
        if self.ksdata.bootloader["md5pass"] != "":
            retval = retval + " --md5pass=%s" % self.ksdata.bootloader["md5pass"]
        if self.ksdata.bootloader["upgrade"]:
            retval = retval + " --upgrade"
        if len(self.ksdata.bootloader["driveorder"]) > 0:
            retval = retval + " --driveorder=%s" % \
                     string.join(self.ksdata.bootloader["driveorder"], ",")

        if retval != "bootloader":
            return retval

    def doClearPart(self):
        if self.ksdata.clearpart["type"] == CLEARPART_TYPE_NONE:
            clearstr = "--none"
        elif self.ksdata.clearpart["type"] == CLEARPART_TYPE_LINUX:
            clearstr = "--linux"
        elif self.ksdata.clearpart["type"] == CLEARPART_TYPE_ALL:
            clearstr = "--all"
        else:
            clearstr = ""

        if self.ksdata.clearpart["initAll"]:
            initstr = "--initlabel"
        else:
            initstr = ""

        if len(self.ksdata.clearpart["drives"]) > 0:
            drivestr = "--drives=" + \
                       string.join (self.ksdata.clearpart["drives"], ",")
        else:
            drivestr = ""

        return "# Partition clearing information\nclearpart %s %s %s" % (clearstr, initstr, drivestr)

    def doDevice(self):
        if self.ksdata.device != "":
            return "device %s" % self.ksdata.device

    def doDeviceProbe(self):
        if self.ksdata.deviceprobe != "":
            return "deviceprobe %s" % self.ksdata.deviceprobe

    def doDisplayMode(self):
        if self.ksdata.displayMode == DISPLAY_MODE_CMDLINE:
            return "cmdline"
        elif self.ksdata.displayMode == DISPLAY_MODE_GRAPHICAL:
            return "# Use graphical install\ngraphical"
        elif self.ksdata.displayMode == DISPLAY_MODE_TEXT:
            return "# Use text mode install\ntext"

    def doDriverDisk(self):
        if self.ksdata.driverdisk != "":
            return "driverdisk %s" % self.ksdata.driverdisk

    def doFirewall(self):
        if self.ksdata.upgrade:
            return

        extra = []
        filteredPorts = []

        if self.ksdata.firewall["enabled"]:
            # It's possible we have words in the ports list instead of
            # port:proto (s-c-kickstart may do this).  So, filter those
            # out into their own list leaving what we expect.
            for port in self.ksdata.firewall["ports"]:
                if port == "ssh":
                    extra.append("--ssh")
                elif port == "telnet":
                    extra.append("--telnet")
                elif port == "smtp":
                    extra.append("--smtp")
                elif port == "http":
                    extra.append("--http")
                elif port == "ftp":
                    extra.append("--ftp")
                else:
                    filteredPorts.append(port)

            # All the port:proto strings go into a comma-separated list.
            portstr = string.join (filteredPorts, ",")
            if len(portstr) > 0:
                portstr = "--port=" + portstr
            else:
                portstr = ""

            extrastr = string.join (extra, " ")

            truststr = string.join (self.ksdata.firewall["trusts"], ",")
            if len(truststr) > 0:
                truststr = "--trust=" + truststr

            # The output port list consists only of port:proto for
            # everything that we don't recognize, and special options for
            # those that we do.
            return "# Firewall configuration\nfirewall --enabled %s %s %s" % (extrastr, portstr, truststr)
        else:
            return "# Firewall configuration\nfirewall --disabled"

    def doFirstboot(self):
        retval = "# Run the Setup Agent on first boot\n"

        if self.ksdata.firstboot == FIRSTBOOT_SKIP:
            return retval + "firstboot --disable"
        elif self.ksdata.firstboot == FIRSTBOOT_DEFAULT:
            return retval + "firstboot --enable"
        elif self.ksdata.firstboot == FIRSTBOOT_RECONFIG:
            return retval + "firstboot --reconfig"

    def doIgnoreDisk(self):
        if len(self.ksdata.ignoredisk) > 0:
            retval = string.join (self.ksdata.ignoredisk, ",")
            return "ignoredisk --drives=%s" % retval

    def doInteractive(self):
        if self.ksdata.interactive:
            return "# Use interactive kickstart installation method\ninteractive"

    def doIscsi(self):
        if self.ksdata.iscsi == []:
            return

        retval = ""

        for i in self.ksdata.iscsi:
            retval += "iscsi"

            if i.target != "":
                retval += " --target=%s" % i.target
            if i.ipaddr != "":
                retval += " --ipaddr=%s" % i.ipaddr
            if i.port != "":
                retval += " --port=%s" % i.port
            if i.user is not None:
                retval += " --user=%s" % i.user
            if i.password is not None:
                retval += " --password=%s" % i.password

            retval += "\n"

        return retval.rstrip()

    def doIscsiName(self):
        if self.ksdata.iscsiname != "":
            return "iscsiname %s" % self.ksdata.iscsiname

    def doKey(self):
        if self.ksdata.key == KS_INSTKEY_SKIP:
            return "key --skip"
        elif self.ksdata.key != "":
            return "key %s" % self.ksdata.key

    def doKeyboard(self):
        if self.ksdata.keyboard != "":
            return "# System keyboard\nkeyboard %s" % self.ksdata.keyboard

    def doLang(self):
        if self.ksdata.lang != "":
            return "# System language\nlang %s" % self.ksdata.lang

    def doLogging(self):
        retval = "# Installation logging level\nlogging --level=%s" % self.ksdata.logging["level"]

        if self.ksdata.logging["host"] != "":
            retval = retval + " --host=%s" % self.ksdata.logging["host"]

            if self.ksdata.logging["port"] != "":
                retval = retval + " --port=%s" % self.ksdata.logging["port"]

        return retval

    def doLogicalVolume(self):
        if self.ksdata.upgrade:
            return

        retval = ""

        for part in self.ksdata.lvList:
            retval = retval + "logvol %s" % part.mountpoint

            if part.bytesPerInode > 0:
                retval = retval + " --bytes-per-inode=%d" % part.bytesPerInode
            if part.fsopts != "":
                retval = retval + " --fsoptions=\"%s\"" % part.fsopts
            if part.fstype != "":
                retval = retval + " --fstype=\"%s\"" % part.fstype
            if part.grow:
                retval = retval + " --grow"
            if part.maxSizeMB > 0:
                retval = retval + " --maxsize=%d" % part.maxSizeMB
            if not part.format:
                retval = retval + " --noformat"
            if part.percent > 0:
                retval = retval + " --percent=%d" % part.percent
            if part.recommended:
                retval = retval + " --recommended"
            if part.size > 0:
                retval = retval + " --size=%d" % part.size
            if part.preexist:
                retval = retval + " --useexisting"

            retval = retval + " --name=%s --vgname=%s\n" % (part.name, part.vgname)

        return retval.rstrip()

    def doMediaCheck(self):
        if self.ksdata.mediacheck:
            return "mediacheck"

    def doMethod(self):
        if self.ksdata.method["method"] == "cdrom":
            return "# Use CDROM installation media\ncdrom"
        elif self.ksdata.method["method"] == "harddrive":
            msg = "# Use hard drive installation media\nharddrive --dir=%s" % self.ksdata.method["dir"]

            if self.ksdata.method.has_key("biospart"):
                return msg + " --biospart=%s" % self.ksdata.method["biospart"]
            else:
                return msg + " --partition=%s" % self.ksdata.method["partition"]
        elif self.ksdata.method["method"] == "nfs":
            return "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.ksdata.method["server"], self.ksdata.method["dir"])
        elif self.ksdata.method["method"] == "url":
            return "# Use network installation\nurl --url=%s" % self.ksdata.method["url"]

    def doMonitor(self):
        retval = "monitor"

        if self.ksdata.monitor["hsync"] != "":
            retval = retval + " --hsync=%s" % self.ksdata.monitor["hsync"]
        if self.ksdata.monitor["monitor"] != "":
            retval = retval + " --monitor=\"%s\"" % self.ksdata.monitor["monitor"]
        if not self.ksdata.monitor["probe"]:
            retval = retval + " --noprobe"
        if self.ksdata.monitor["vsync"] != "":
            retval = retval + " --vsync=%s" % self.ksdata.monitor["vsync"]

        if retval != "monitor":
            return retval

    def doNetwork(self):
        if self.ksdata.network == []:
            return

        retval = "# Network information\n"

        for nic in self.ksdata.network:
            retval = retval + "network"

            if nic.bootProto != "":
                retval = retval + " --bootproto=%s" % nic.bootProto
            if nic.dhcpclass != "":
                retval = retval + " --dhcpclass=%s" % nic.dhcpclass
            if nic.device != "":
                retval = retval + " --device=%s" % nic.device
            if nic.essid != "":
                retval = retval + " --essid=\"%s\"" % nic.essid
            if nic.ethtool != "":
                retval = retval + " --ethtool=\"%s\"" % nic.ethtool
            if nic.gateway != "":
                retval = retval + " --gateway=%s" % nic.gateway
            if nic.hostname != "":
                retval = retval + " --hostname=%s" % nic.hostname
            if nic.ip != "":
                retval = retval + " --ip=%s" % nic.ip
            if not nic.ipv4:
                retval += " --noipv4"
            if not nic.ipv6:
                retval += " --noipv6"
            if nic.mtu != "":
                retval = retval + " --mtu=%s" % nic.mtu
            if nic.nameserver != "":
                retval = retval + " --nameserver=%s" % nic.nameserver
            if nic.netmask != "":
                retval = retval + " --netmask=%s" % nic.netmask
            if nic.nodns:
                retval = retval + " --nodns"
            if nic.notksdevice:
                retval = retval + " --notksdevice"
            if nic.onboot:
                retval = retval + " --onboot=on"
            if nic.wepkey != "":
                retval = retval + " --wepkey=%s" % nic.wepkey

            retval = retval + "\n"

        return retval.rstrip()

    def doPartition(self):
        if self.ksdata.upgrade or self.ksdata.partitions == []:
            return

        retval = "# Disk partitioning information\n"

        for part in self.ksdata.partitions:
            retval = retval + "part %s" % part.mountpoint

            if part.active:
                retval = retval + " --active"
            if part.primOnly:
                retval = retval + " --asprimary"
            if part.bytesPerInode != 0:
                retval = retval + " --bytes-per-inode=%d" % part.bytesPerInode
            if part.end != 0:
                retval = retval + " --end=%d" % part.end
            if part.fsopts != "":
                retval = retval + " --fsoptions=\"%s\"" % part.fsopts
            if part.fstype != "":
                retval = retval + " --fstype=\"%s\"" % part.fstype
            if part.grow:
                retval = retval + " --grow"
            if part.label != "":
                retval = retval + " --label=%s" % part.label
            if part.maxSizeMB > 0:
                retval = retval + " --maxsize=%d" % part.maxSizeMB
            if not part.format:
                retval = retval + " --noformat"
            if part.onbiosdisk != "":
                retval = retval + " --onbiosdisk=%s" % part.onbiosdisk
            if part.disk != "":
                retval = retval + " --ondisk=%s" % part.disk
            if part.onPart != "":
                retval = retval + " --onpart=%s" % part.onPart
            if part.recommended:
                retval = retval + " --recommended"
            if part.size and part.size != 0:
                retval = retval + " --size=%d" % int(part.size)
            if part.start != 0:
                retval = retval + " --start=%d" % part.start

            retval = retval + "\n"

        return retval.rstrip()

    def doReboot(self):
        retval = ""

        if self.ksdata.reboot["action"] == KS_REBOOT:
            retval = "# Reboot after installation\nreboot"
        elif self.ksdata.reboot["action"] == KS_SHUTDOWN:
            retval = "# Shutdown after installation\nshutdown"

        if self.ksdata.reboot["eject"]:
            retval = retval + " --eject"

        return retval

    def doRepo(self):
        retval = ""

        for repo in self.ksdata.repoList:
            if repo.baseurl:
                urlopt = "--baseurl=%s" % repo.baseurl
            elif repo.mirrorlist:
                urlopt = "--mirrorlist=%s" % repo.mirrorlist

            retval = retval + "repo --name=%s %s\n" % (repo.name, urlopt)

        return retval

    def doRaid(self):
        if self.ksdata.upgrade:
            return

        retval = ""

        for raid in self.ksdata.raidList:
            retval = retval + "raid %s" % raid.mountpoint

            if raid.bytesPerInode != 0:
                retval = retval + " --bytes-per-inode=%d" % raid.bytesPerInode
            if raid.device != "":
                retval = retval + " --device=%s" % raid.device
            if raid.fsopts != "":
                retval = retval + " --fsoptions=\"%s\"" % raid.fsopts
            if raid.fstype != "":
                retval = retval + " --fstype=\"%s\"" % raid.fstype
            if raid.level != "":
                retval = retval + " --level=%s" % raid.level
            if not raid.format:
                retval = retval + " --noformat"
            if raid.spares != 0:
                retval = retval + " --spares=%d" % raid.spares
            if raid.preexist:
                retval = retval + " --useexisting"

            retval = retval + " %s\n" % string.join(raid.members)

        return retval.rstrip()

    def doRootPw(self):
        if self.ksdata.rootpw["password"] != "":
            if self.ksdata.rootpw["isCrypted"]:
                crypted = "--iscrypted"
            else:
                crypted = ""

            return "#Root password\nrootpw %s %s\n" % (crypted, self.ksdata.rootpw["password"])

    def doSELinux(self):
        retval = "# SELinux configuration\n"

        if self.ksdata.selinux == SELINUX_DISABLED:
            return retval + "selinux --disabled"
        elif self.ksdata.selinux == SELINUX_ENFORCING:
            return retval + "selinux --enforcing"
        elif self.ksdata.selinux == SELINUX_PERMISSIVE:
            return retval + "selinux --permissive"

    def doServices(self):
        retval = ""

        if len(self.ksdata.services["disabled"]) > 0:
            retval = retval + " --disabled=%s" % string.join(self.ksdata.services["disabled"], ",")
        if len(self.ksdata.services["enabled"]) > 0:
            retval = retval + " --enabled=%s" % string.join(self.ksdata.services["enabled"], ",")

        if retval != "":
            return "# System services\nservices %s\n" % retval

    def doSkipX(self):
        if self.ksdata.skipx and not self.ksdata.upgrade:
            return "# Do not configure the X Window System\nskipx"

    def doTimezone(self):
        if self.ksdata.timezone["timezone"] != "":
            if self.ksdata.timezone["isUtc"]:
                utc = "--isUtc"
            else:
                utc = ""

            return "# System timezone\ntimezone %s %s" %(utc, self.ksdata.timezone["timezone"])

    def doUpgrade(self):
        if self.ksdata.upgrade:
            return "# Upgrade existing installation\nupgrade"
        else:
            return "# Install OS instead of upgrade\ninstall"

    def doUser(self):
        retval = ""

        for user in self.ksdata.userList:
            retval = retval + "user"

            if len(user.groups) > 0:
                retval = retval + " --groups=%s" % string.join(user.groups, ",")
            if user.homedir:
                retval = retval + " --homedir=%s" % user.homedir
            if user.name:
                retval = retval + " --name=%s" % user.name
            if user.password:
                retval = retval + " --password=%s" % user.password
            if user.isCrypted:
                retval = retval + " --isCrypted"
            if user.shell:
                retval = retval + " --shell=%s" % user.shell
            if user.uid:
                retval = retval + " --uid=%s" % user.uid

            retval = retval + "\n"

        return retval.rstrip()

    def doVnc(self):
        if self.ksdata.vnc["enabled"]:
            if self.ksdata.vnc["password"] != "":
                password = "--password=%s" % self.ksdata.vnc["password"]
            else:
                password = ""

            if self.ksdata.vnc["port"] != "":
                port = ":%s" % self.ksdata.vnc["port"]
            else:
                port = ""

            return "vnc --enabled %s %s%s" % (password, self.ksdata.vnc["host"],
                                              port)

    def doVolumeGroup(self):
        if self.ksdata.upgrade:
            return

        retval = ""

        for vg in self.ksdata.vgList:
            retval = retval + "volgroup %s" % vg.vgname

            if not vg.format:
                retval = retval + " --noformat"
            if vg.pesize != 0:
                retval = retval + " --pesize=%d" % vg.pesize
            if vg.preexist:
                retval = retval + " --useexisting"

            retval = retval + " %s\n" % string.join(vg.physvols, ",")

        return retval.rstrip()

    def doXConfig(self):
        if self.ksdata.upgrade or self.ksdata.skipx:
            return

        retval = ""

        if self.ksdata.xconfig["driver"] != "":
            retval = retval + " --driver=%s" % self.ksdata.xconfig["driver"]
        if self.ksdata.xconfig["defaultdesktop"] != "":
            retval = retval + " --defaultdesktop=%s" % self.ksdata.xconfig["defaultdesktop"]
        if self.ksdata.xconfig["depth"] != 0:
            retval = retval + " --depth=%d" % self.ksdata.xconfig["depth"]
        if self.ksdata.xconfig["resolution"] != "":
            retval = retval + " --resolution=%s" % self.ksdata.xconfig["resolution"]
        if self.ksdata.xconfig["startX"]:
            retval = retval + " --startxonboot"
        if self.ksdata.xconfig["videoRam"] != "":
            retval = retval + " --videoram=%s" % self.ksdata.xconfig["videoRam"]

        if retval != "":
            return "# X Window System configuration information\nxconfig %s" % retval

    def doZeroMbr(self):
        if self.ksdata.zerombr:
            return "# Clear the Master Boot Record\nzerombr"

    def doZFCP(self):
        if self.ksdata.zfcp == []:
            return

        retval = ""

        for i in self.ksdata.zfcp:
            retval += "zfcp"

            if i.devnum != "":
                retval += " --devnum=%s" % i.devnum
            if i.wwpn != "":
                retval += " --wwpn=%s" % i.wwpn
            if i.fcplun != "":
                retval += " --fcplun=%s" % i.fcplun
            if i.scsiid != "":
                retval += " --scsiid=%s" % i.scsiid
            if i.scsilun != "":
                retval += " --scsilun=%s" % i.scsilun

            retval += "\n"

        return retval.rstrip()

    def doScripts(self):
        preStr = ""
        postStr = ""
        tracebackStr = ""

        for script in self.ksdata.scripts:
            if script.type == KS_SCRIPT_PRE:
                preStr = preStr + "%%pre %s" % script.write()
            elif script.type == KS_SCRIPT_POST:
                postStr = postStr + "%%post %s" % script.write()
            elif script.type == KS_SCRIPT_TRACEBACK:
                tracebackStr = tracebackStr + "%%traceback %s" % script.write()

        return preStr + postStr + tracebackStr.rstrip()

    def doPackages(self):
        if self.ksdata.upgrade:
            return

        pkgs = ""

        for grp in self.ksdata.groupList:
            pkgs += "@%s\n" % grp

        for pkg in self.ksdata.packageList:
            pkgs += "%s\n" % pkg

        for pkg in self.ksdata.excludedList:
            pkgs += "-%s\n" % pkg

        if pkgs == "":
            return

        retval = "\n%packages"

        if self.ksdata.excludeDocs:
            retval += " --excludedocs"
        if not self.ksdata.addBase:
            retval += " --nobase"
        if self.ksdata.handleMissing == KS_MISSING_IGNORE:
            retval += " --ignoremissing"

        return retval + "\n" + pkgs
