#
# writer.py:  Kickstart file writer.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005 Red Hat, Inc.
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

                         self.doAuthconfig, self.doAutoPart, self.doAutoStep,
                         self.doBootloader, self.doClearPart, self.doDevice,
                         self.doDeviceProbe, self.doDisplayMode,
                         self.doDriverDisk, self.doFirewall, self.doFirstboot,
                         self.doIgnoreDisk, self.doInteractive, self.doKeyboard,
                         self.doLang, self.doMediaCheck, self.doMethod,
                         self.doMonitor, self.doNetwork, self.doReboot,
                         self.doRootPw, self.doSELinux, self.doSkipX,
                         self.doTimezone, self.doUpgrade, self.doVnc,
                         self.doXConfig, self.doZeroMbr, self.doZFCP,

                         self.doPartition, self.doLogicalVolume,
                         self.doVolumeGroup, self.doRaid,

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
        if self.ksdata.authconfig != "" and self.ksdata.upgrade == False:
            return "# System authorization information\nauth %s" % self.ksdata.authconfig

    def doAutoPart(self):
        if self.ksdata.autopart:
            return "autopart"

    def doAutoStep(self):
        if self.ksdata.autostep["autoscreenshot"]:
            return "autostep --autoscreenshot"

    def doBootloader(self):
        str = "# System bootloader configuration\nbootloader"

        if self.ksdata.bootloader["appendLine"] != "":
            str = str + " --append=\"%s\"" % self.ksdata.bootloader["appendLine"]
        if self.ksdata.bootloader["location"]:
            str = str + " --location=%s" % self.ksdata.bootloader["location"]
        if self.ksdata.bootloader["forceLBA"] == True:
            str = str + " --lba32"
        if self.ksdata.bootloader["password"] != "":
            str = str + " --password=%s" % self.ksdata.bootloader["password"]
        if self.ksdata.bootloader["md5pass"] != "":
            str = str + " --md5pass=%s" % self.ksdata.bootloader["md5pass"]
        if self.ksdata.bootloader["upgrade"] == True:
            str = str + " --upgrade"
        if len(self.ksdata.bootloader["driveorder"]) > 0:
            str = str + " --driveorder=%s" % \
                        string.join(self.ksdata.bootloader["driveorder"], ",")

        if str != "bootloader":
            return str

    def doClearPart(self):
        if self.ksdata.clearpart["type"] == CLEARPART_TYPE_NONE:
            clearstr = "--none"
        elif self.ksdata.clearpart["type"] == CLEARPART_TYPE_LINUX:
            clearstr = "--linux"
        elif self.ksdata.clearpart["type"] == CLEARPART_TYPE_ALL:
            clearstr = "--all"
        else:
            clearstr = ""

        if self.ksdata.clearpart["initAll"] == True:
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
        if self.ksdata.upgrade == True:
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
                portstr = "--ports=" + portstr
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
        str = "# Run the Setup Agent on first boot\n"

        if self.ksdata.firstboot == FIRSTBOOT_SKIP:
            return str + "firstboot --disable"
        elif self.ksdata.firstboot == FIRSTBOOT_DEFAULT:
            return str + "firstboot --enable"
        elif self.ksdata.firstboot == FIRSTBOOT_RECONFIG:
            return str + "firstboot --reconfig"

    def doIgnoreDisk(self):
        if len(self.ksdata.ignoredisk) > 0:
            str = string.join (self.ksdata.ignoredisk, ",")
            return "ignoredisk --drives= %s" % str

    def doInteractive(self):
        if self.ksdata.interactive == True:
            return "# Use interactive kickstart installation method\ninteractive"

    def doKeyboard(self):
        if self.ksdata.keyboard != "":
            return "# System keyboard\nkeyboard %s" % self.ksdata.keyboard

    def doLang(self):
        if self.ksdata.lang != "":
            return "# System language\nlang %s" % self.ksdata.lang

    def doLogicalVolume(self):
        if self.ksdata.upgrade == True:
            return

        str = ""

        for part in self.ksdata.lvList:
            str = str + "logvol %s" % part.mountpoint

            if part.bytesPerInode > 0:
                str = str + " --bytes-per-inode= %d" % part.bytesPerInode
            if part.fsopts != "":
                str = str + " --fsoptions=\"%s\"" % part.fsopts
            if part.fstype != "":
                str = str + " --fstype=\"%s\"" % part.fstype
            if part.grow == True:
                str = str + " --grow"
            if part.maxSizeMB > 0:
                str = str + " --maxsize=%d" % part.maxSizeMB
            if part.format == False:
                str = str + " --noformat"
            if part.percent > 0:
                str = str + " --percent=%d" % part.percent
            if part.recommended == True:
                str = str + " --recommended"
            if part.size > 0:
                str = str + " --size=%d" % part.size
            if part.preexist == True:
                str = str + " --useexisting"

            str = str + " --name=%s --vgname=%s\n" % (part.name, part.vgname)

        return str.rstrip()

    def doMediaCheck(self):
        if self.ksdata.mediacheck == True:
            return "mediacheck"

    def doMethod(self):
        if self.ksdata.method["method"] == "cdrom":
            return "# Use CDROM installation media\ncdrom"
        elif self.ksdata.method["method"] == "harddrive":
            return "# Use hard drive installation media\nharddrive --partition=%s --dir=%s" % (self.ksdata.method["partition"], self.ksdata.method["dir"])
        elif self.ksdata.method["method"] == "nfs":
            return "# Use NFS installation media\nnfs --server=%s --dir=%s" % (self.ksdata.method["server"], self.ksdata.method["dir"])
        elif self.ksdata.method["method"] == "url":
            return "# Use network installation\nurl --url=%s" % self.ksdata.method["url"]

    def doMonitor(self):
        str = "monitor"

        if self.ksdata.monitor["hsync"] != "":
            str = str + " --hsync=%s" % self.ksdata.monitor["hsync"]
        if self.ksdata.monitor["monitor"] != "":
            str = str + " --monitor=%s" % self.ksdata.monitor["monitor"]
        if self.ksdata.monitor["vsync"] != "":
            str = str + " --vsync=%s" % self.ksdata.monitor["vsync"]

        if str != "monitor":
            return str

    def doNetwork(self):
        if self.ksdata.network == []:
            return

        str = "# Network information\n"

        for nic in self.ksdata.network:
            str = str + "network"

            if nic.bootProto != "":
                str = str + " --bootproto=%s" % nic.bootProto
            if nic.dhcpclass != "":
                str = str + " --dhcpclass=%s" % nic.dhcpclass
            if nic.device != "":
                str = str + " --device=%s" % nic.device
            if nic.essid != "":
                str = str + " --essid=\"%s\"" % nic.essid
            if nic.ethtool != "":
                str = str + " --ethtool=%s" % nic.ethtool
            if nic.gateway != "":
                str = str + " --gateway=%s" % nic.gateway
            if nic.hostname != "":
                str = str + " --hostname=%s" % nic.hostname
            if nic.ip != "":
                str = str + " --ip=%s" % nic.ip
            if nic.nameserver != "":
                str = str + " --nameserver=%s" % nic.nameserver
            if nic.netmask != "":
                str = str + " --netmask=%s" % nic.netmask
            if nic.nodns == True:
                str = str + " --nodns"
            if nic.notksdevice == True:
                str = str + " --notksdevice"
            if nic.onboot == True:
                str = str + " --onboot"
            if nic.wepkey != "":
                str = str + " --wepkey=%s" % nic.wepkey

            str = str + "\n"

        return str.rstrip()

    def doPartition(self):
        if self.ksdata.upgrade == True or self.ksdata.partitions == []:
            return

        str = "# Disk partitioning information\n"

        for part in self.ksdata.partitions:
            str = str + "part %s" % part.mountpoint

            if part.active == True:
                str = str + " --active"
            if part.primOnly == True:
                str = str + " --asprimary"
            if part.bytesPerInode != 0:
                str = str + " --bytes-per-inode=%d" % part.bytesPerInode
            if part.end != 0:
                str = str + " --end=%d" % part.end
            if part.fsopts != "":
                str = str + " --fsoptions=\"%s\"" % part.fsopts
            if part.fstype != "":
                str = str + " --fstype=\"%s\"" % part.fstype
            if part.grow == True:
                str = str + " --grow"
            if part.label != "":
                str = str + " --label=%s" % part.label
            if part.maxSizeMB > 0:
                str = str + " --maxsize=%d" % part.maxSizeMB
            if part.format == False:
                str = str + " --noformat"
            if part.onbiosdisk != "":
                str = str + " --onbiosdisk=%s" % part.onbiosdisk
            if part.disk != "":
                str = str + " --ondisk=%s" % part.disk
            if part.onPart != "":
                str = str + " --onpart=%s" % part.onPart
            if part.recommended == True:
                str = str + " --recommended"
            if part.size != 0:
                str = str + " --size=%d" % part.size
            if part.start != 0:
                str = str + " --start=%d" % part.start

            str = str + "\n"

        return str.rstrip()

    def doReboot(self):
        if self.ksdata.reboot == True:
            return "# Reboot after installation\nreboot"

    def doRaid(self):
        if self.ksdata.upgrade == True:
            return

        str = ""

        for raid in self.ksdata.raidList:
            str = str + "raid %s" % raid.mountpoint

            if raid.device != "":
                str = str + " --device=%s" % raid.device
            if raid.fsopts != "":
                str = str + " --fsoptions=\"%s\"" % raid.fsopts
            if raid.fstype != "":
                str = str + " --fstype=\"%s\"" % raid.fstype
            if raid.level != "":
                str = str + " --level=%s" % raid.level
            if raid.format == False:
                str = str + " --noformat"
            if raid.spares != 0:
                str = str + " --spares=%d" % raid.spares
            if raid.preexist == True:
                str = str + " --useexisting"

            str = str + " %s\n" % string.join(raid.members)

        return str.rstrip()

    def doRootPw(self):
        if self.ksdata.rootpw["password"] != "":
            if self.ksdata.rootpw["isCrypted"] == True:
                crypted = "--iscrypted"
            else:
                crypted = ""

            return "#Root password\nrootpw %s %s" % (crypted, self.ksdata.rootpw["password"])

    def doSELinux(self):
        str = "# SELinux configuration\n"

        if self.ksdata.selinux == SELINUX_DISABLED:
            return str + "selinux --disabled"
        elif self.ksdata.selinux == SELINUX_ENFORCING:
            return str + "selinux --enforcing"
        elif self.ksdata.selinux == SELINUX_PERMISSIVE:
            return str + "selinux --permissive"

    def doSkipX(self):
        if self.ksdata.skipx == True and self.ksdata.upgrade == False:
            return "# Do not configure the X Window System\nskipx"

    def doTimezone(self):
        if self.ksdata.timezone["timezone"] != "":
            if self.ksdata.timezone["isUtc"] == True:
                utc = "--isUtc"
            else:
                utc = ""

            return "# System timezone\ntimezone %s %s" %(utc, self.ksdata.timezone["timezone"])

    def doUpgrade(self):
        if self.ksdata.upgrade == True:
            return "# Upgrade existing installation\nupgrade"
        else:
            return "# Install OS instead of upgrade\ninstall"

    def doVnc(self):
        if self.ksdata.vnc["enabled"] == True:
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
        if self.ksdata.upgrade == True:
            return

        str = ""

        for vg in self.ksdata.vgList:
            str = str + "volgroup %s" % vg.vgname

            if vg.format == False:
                str = str + " --noformat"
            if vg.pesize != 0:
                str = str + " --pesize=%d" % vg.pesize
            if vg.preexist == True:
                str = str + " --useexisting"

            str = str + " %s\n" % string.join(vg.physvols, ",")

        return str.rstrip()

    def doXConfig(self):
        if self.ksdata.upgrade == True or self.ksdata.skipx == True:
            return

        str = "# X Window System configuration information\nxconfig"

        if self.ksdata.xconfig["driver"] != "":
            str = str + " --driver=%s" % self.ksdata.xconfig["driver"]
        if self.ksdata.xconfig["defaultdesktop"] != "":
            str = str + " --defaultdesktop=%s" % self.ksdata.xconfig["defaultdesktop"]
        if self.ksdata.xconfig["depth"] != 0:
            str = str + " --depth=%d" % self.ksdata.xconfig["depth"]
        if self.ksdata.xconfig["hsync"] != "":
            str = str + " --hsync=%s" % self.ksdata.xconfig["hsync"]
        if self.ksdata.xconfig["monitor"] != "":
            str = str + " --monitor=\"%s\"" % self.ksdata.xconfig["monitor"]
        if self.ksdata.xconfig["probe"] == False:
            str = str + " --noprobe"
        if self.ksdata.xconfig["resolution"] != "":
            str = str + " --resolution=%s" % self.ksdata.xconfig["resolution"]
        if self.ksdata.xconfig["startX"] == True:
            str = str + " --startxonboot"
        if self.ksdata.xconfig["videoRam"] != "":
            str = str + " --videoram=%s" % self.ksdata.xconfig["videoRam"]
        if self.ksdata.xconfig["vsync"] != "":
            str = str + " --vsync=%s" % self.ksdata.xconfig["vsync"]

        if str != "xconfig":
            return str

    def doZeroMbr(self):
        if self.ksdata.zerombr == True:
            return "# Clear the Master Boot Record\nzerombr"

    def doZFCP(self):
        if self.ksdata.zfcp["devnum"] != "":
            return "zfcp --devnum=%(devnum)s --fcplun=%(fcplun)s --scsiid=%(scsiid)s --scsilun=%(scsilun)s --wwpn=%(wwpn)s" % self.ksdata.zfcp

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
        if self.ksdata.upgrade == True:
            return

        str = "\n%packages\n"

        for pkg in self.ksdata.packageList:
            str = str + "%s\n" % pkg

        for pkg in self.ksdata.excludedList:
            str = str + "-%s\n" % pkg

        for grp in self.ksdata.groupList:
            str = str + "@%s\n" % grp

        return str.rstrip()
