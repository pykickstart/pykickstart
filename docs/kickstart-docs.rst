Kickstart Documentation
************************

:Authors:
   Chris Lumens <clumens@redhat.com>
   and other members of the *Anaconda installer team*

.. contents::
   :depth: 3

Chapter 1. Introduction
=======================

What are Kickstart Installations?
---------------------------------

Many system administrators would prefer to use an automated installation
method to install Fedora or Red Hat Enterprise Linux on their machines.
To answer this need, Red Hat created the kickstart installation method.
Using kickstart, a system administrator can create a single file
containing the answers to all the questions that would normally be asked
during a typical installation.

Kickstart files can be kept on a server system and read by individual
computers during the installation. This installation method can support
the use of a single kickstart file to install Fedora or Red Hat
Enterprise Linux on multiple machines, making it ideal for network and
system administrators.

The Fedora installation guide at
http://docs.fedoraproject.org/en-US/index.html has a detailed section on
kickstart.


How Do You Perform a Kickstart Installation?
--------------------------------------------

Kickstart installations can be performed using a local CD-ROM, a local
hard drive, or via NFS, FTP, or HTTP.

To use kickstart, you must:

#. Create a kickstart file.
#. Create a boot diskette with the kickstart file or make the kickstart
   file available on the network.
#. Make the installation tree available.
#. Start the kickstart installation.

This chapter explains these steps in detail.


Creating the Kickstart File
---------------------------

The kickstart file is a simple text file, containing a list of items,
each identified by a keyword. You can create it by using the Kickstart
Configurator application or by writing it from scratch. The Fedora or
Red Hat Enterprise Linux installation program also creates a sample
kickstart file based on the options that you selected during
installation. It is written to the file /root/anaconda-ks.cfg. You
should be able to edit it with any text editor or word processor that
can save files as ASCII text.

First, be aware of the following issues when you are creating your
kickstart file:

-  While not strictly required, there is a natural order for sections
   that should be followed. Items within the sections do not have to be
   in a specific order unless otherwise noted. The section order is:

   #. Command section -- Refer to Chapter 2 for a list of kickstart
      options. You must include the required options.
   #. The %packages section -- Refer to Chapter 3 for details.
   #. The %pre, %pre-install, %post, and %traceback sections -- These
      sections can be in any order and are not required. Refer to Chapter
      4 and Chapter 5 for details.

-  The %packages, %pre, %pre-install, %post and %traceback sections are all
   required to be closed with %end
-  Items that are not required can be omitted.
-  Omitting any required item will result in the installation program
   prompting the user for an answer to the related item, just as the
   user would be prompted during a typical installation. Once the answer
   is given, the installation will continue unattended unless it finds
   another missing item.
-  Lines starting with a pound sign (#) are treated as comments and are
   ignored.
-  If deprecated commands, options, or syntax are used during a
   kickstart installation, a warning message will be logged to the
   anaconda log. Since deprecated items are usually removed within a
   release or two, it makes sense to check the installation log to make
   sure you haven't used any of them. When using ksvalidator, deprecated
   items will cause an error.


Special Notes for Referring to Disks
------------------------------------

Traditionally, disks have been referred to throughout Kickstart by a
device node name (such as ``sda``). The Linux kernel has moved to a more
dynamic method where device names are not guaranteed to be consistent
across reboots, so this can complicate usage in Kickstart scripts. To
accommodate stable device naming, you can use any item from
``/dev/disk`` in place of a device node name. For example, instead of:

``part / --fstype=ext4 --onpart=sda1``

You could use an entry similar to one of the following:

::

    part / --fstype=ext4 --onpart=/dev/disk/by-path/pci-0000:00:05.0-scsi-0:0:0:0-part1
    part / --fstype=ext4 --onpart=/dev/disk/by-id/ata-ST3160815AS_6RA0C882-part1

This provides a consistent way to refer to disks that is more meaningful
than just ``sda``. This is especially useful in large storage
environments.

You can also use shell-like entries to refer to disks. This is primarily
intended to make it easier to use the ``clearpart`` and ``ignoredisk``
commands in large storage environments. For example, instead of:

``ignoredisk --drives=sdaa,sdab,sdac``

You could use an entry similar to the following:

``ignoredisk --drives=/dev/disk/by-path/pci-0000:00:05.0-scsi-*``

Finally, anywhere you want to refer to an existing partition or
filesystem (say, in the ``part --ondisk=``) option, you may also refer
to the device by its filesystem label or UUID. This is done as follows:

::

    part /data --ondisk=LABEL=data
    part /misc --ondisk=UUID=819ff6de-0bd6-4bf4-8b72-dbe41033a85b


Chapter 2. Kickstart Options
============================

The following options can be placed in a kickstart file. If you prefer
to use a graphical interface for creating your kickstart file, you can
use the Kickstart Configurator application.

**If the option is followed by an equals mark (``==``), a value must be specified after it.

In the example commands, options in '''[square brackets]''' are optional arguments for the command.**

**pykickstart processes arguments to commands just like the shell does:**

::

   If a list of arguments can be passed in, the arguments must be separated by
   commas and not include any extra spaces.  If extra spaces are required in the
   list of arguments, the entire argument must be surrounded by double quotes.  If
   quotes, spaces, or other special characters need to be added to the argumens
   list, they must be escaped.


auth or authconfig
------------------

This required command sets up the authentication options for the system.
This is just a wrapper around the authconfig program, so all options
recognized by that program are valid for this command. See the manual
page for authconfig for a complete list.

By default, passwords are normally encrypted and are not shadowed.


autopart
--------

Automatically create partitions -- a root (/) partition, a swap
partition, and an appropriate boot partition for the architecture. On
large enough drives, this will also create a /home partition.

**The ``autopart`` command can't be used together with the ``part``/``partition``, ``raid``, ``volgroup`` or ``logvol`` commands in the same kickstart file.**

``--type=<type>``

    Select automatic partitioning scheme. Must be one of the following:
    lvm, btrfs, plain, thinp. Plain means regular partitions with no
    btrfs or lvm.

``--nolvm``

    Same as ``--type=plain``

``--encrypted``

    Should all devices with support be encrypted by default? This is
    equivalent to checking the "Encrypt" checkbox on the initial
    partitioning screen.

``--passphrase=``

    Only relevant if ``--encrypted`` is specified. Provide a default
    system-wide passphrase for all encrypted devices.

``--escrowcert=<url>``

    Only relevant if ``--encrypted`` is specified. Load an X.509
    certificate from ``<url>``. Store the data encryption keys of all
    encrypted volumes created during installation, encrypted using the
    certificate, as files in ``/root``.

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified. In addition to
    storing the data encryption keys, generate a random passphrase and
    add it to all encrypted volumes created during installation. Then
    store the passphrase, encrypted using the certificate specified by
    ``--escrowcert``, as files in ``/root`` (one file for each encrypted
    volume).

``--cipher``

    Only relevant if ``--encrypted`` is specified. Specifies which
    encryption algorithm should be used to encrypt the filesystem.

``--fstype=<filesystem>``

    Use the specified filesystem type on the partitions. Note that it
    cannot be used with --type=btrfs since btrfs is both a partition
    scheme and a filesystem. eg. --fstype=ext4. Added in
    anaconda-21.46-1


autostep
--------

Kickstart installs normally skip unnecessary screens. This makes the
installer step through every screen, displaying each briefly.

This is mostly used for debugging.

``--autoscreenshot``

    Take a screenshot at every step during installation and copy the
    images over to /root/anaconda-screenshots after installation is
    complete. This is most useful for documentation.


bootloader
----------

This required command specifies how the boot loader should be installed.

**As of Fedora 16 there must be a biosboot partition for the bootloader to be installed successfully onto a disk that contains a GPT/GUID partition table, which includes disks initialized by anaconda. This partition may be created with the kickstart option ``part biosboot --fstype=biosboot --size=1``. However, in the case that a disk has an existing biosboot partition, adding a "part biosboot" option is unnecessary.**

``--append=``

    Specifies kernel parameters. The default set of bootloader arguments
    is "rhgb quiet". You will get this set of arguments regardless of
    what parameters you pass to --append, or if you leave out --append
    entirely. For example:

    ``bootloader --location=mbr --append="hdd=ide-scsi ide=nodma"``

``--boot-drive=``

    Specifies which drive the bootloader should be written to and thus,
    which drive the computer will boot from.

``--disabled``

    Do not install the boot loader.

``--leavebootorder``

    On EFI or ISeries/PSeries machines, this option prevents the
    installer from making changes to the existing list of bootable
    images.

``--driveorder``

    Specify which drive is first in the BIOS boot order. For example:

    ``bootloader --driveorder=sda,hda``

``--location=``

    Specifies where the boot record is written. Valid values are the
    following: mbr (the default), partition (installs the boot loader on
    the first sector of the partition containing the kernel), or none
    (do not install the boot loader).

``--nombr``

    Install the boot loader configuration and support files, but do not
    modify the MBR. Since Fedora 21.

``--password=``

    If using GRUB, sets the GRUB boot loader password. This should be
    used to restrict access to the GRUB shell, where arbitrary kernel
    options can be passed.

``--iscrypted``

    If given, the password specified by ``--password=`` is already
    encrypted and should be passed to the bootloader configuration
    without additional modification.

``--md5pass=``

    If using GRUB, similar to ``--password=`` except the password should
    already be encrypted.

``--timeout=<secs>``

    Specify the number of seconds before the bootloader times out and
    boots the default option.

``--default=``

    Sets the default boot image in the bootloader configuration.

``--extlinux``

    Use the extlinux bootloader instead of GRUB. This option only works
    on machines that are supported by extlinux.


btrfs
-----

Defines a BTRFS volume or subvolume. This command is of the form:

``btrfs <mntpoint> --data=<level> --metadata=<level> --label=<label> <partitions*>``

for volumes and of the form:

``btrfs <mntpoint> --subvol --name=<path> <parent>``

for subvolumes.

The ``<partitions*>`` (which denotes that multiple partitions can be
listed) lists the BTRFS identifiers to add to the BTRFS volume. For
subvolumes, should be the identifier of the subvolume's parent volume.

``<mntpoint>``

    Location where the file system is mounted.

``--data=``

    RAID level to use (0, 1, 10) for filesystem data. Optional. This
    option has no meaning for subvolumes.

``--metadata=``

    RAID level to use (0, 1, 10) for filesystem/volume metadata.
    Optional. This option has no meaning for subvolumes.

``--label=``

    Specify the label to give to the filesystem to be made. If the given
    label is already in use by another filesystem, a new label will be
    created. This option has no meaning for subvolumes.

``--noformat``

    Use an existing BTRFS volume (or subvolume) and do not reformat the
    filesystem.

``--useexisting``

    Same as --noformat, above.

``--mkfsoptions=``

    Specifies additional parameters to be passed to the program that makes
    a filesystem on this partition. No processing is done on the list of arguments,
    so they must be supplied in a format that can be passed directly to the mkfs
    program.  This means multiple options should be comma-separated or surrounded
    by double quotes, depending on the filesystem.

The following example shows how to create a BTRFS volume from member
partitions on three disks with subvolumes for root and home. The main
volume is not mounted or used directly in this example -- only the root
and home subvolumes.

::

    part btrfs.01 --size=6000 --ondisk=sda
    part btrfs.02 --size=6000 --ondisk=sdb
    part btrfs.03 --size=6000 --ondisk=sdc

    btrfs none --data=0 --metadata=1 --label=f17 btrfs.01 btrfs.02 btrfs.03
    btrfs / --subvol --name=root LABEL=f17
    btrfs /home --subvol --name=home f17


clearpart
---------

Removes partitions from the system, prior to creation of new partitions.
By default, no partitions are removed.

**If the clearpart command is used, then the ``--onpart`` command cannot be used on a logical partition.**

``--all``

    Erases all partitions from the system.

``--drives=``

    Specifies which drives to clear partitions from. For example, the
    following clears the partitions on the first two drives on the
    primary IDE controller:

    ``clearpart --all --drives=sda,sdb``

``--list=``

    Specifies which partitions to clear. If given, this supercedes any
    of the ``--all`` and ``--linux`` options. This can be across
    different drives:

    ``clearpart --list=sda2,sda3,sdb1``

``--initlabel``

    Initializes the disk label to the default for your architecture (for
    example msdos for x86 and gpt for Itanium). This is only meaningful
    in combination with the '--all' option.

``--linux``

    Erases all Linux partitions.

``--none`` (default)

    Do not remove any partitions.

``--disklabel=<supported label>``

    Set the default disklabel to use. Only disklabels supported for the
    platform will be accepted. eg. msdos and gpt for x86\_64 but not
    dasd. Added in anaconda-21.43-1


cmdline
-------

Perform the installation in a completely non-interactive command line
mode. Any prompts for interaction will halt the install. This mode is
useful on S/390 systems with the x3270 console.


driverdisk
----------

Driver diskettes can be used during kickstart installations. You need to
copy the driver disk's contents to the root directory of a partition on
the system's hard drive. Then you need to use the driverdisk command to
tell the installation program where to look for the driver disk.

``driverdisk <partition>|--source=<url>|--biospart=<part>``

``<partition>``

    Partition containing the driver disk.

``--source=<url>``

    Specify a URL for the driver disk. NFS locations can be given with
    ``nfs:host:/path/to/img``.

``--biospart=<part>``

    BIOS partition containing the driver disk (such as 82p2).


fcoe
----


firewall
--------

This option corresponds to the Firewall Configuration screen in the
installation program:

``firewall --enabled|--disabled <device> [options]``

``--enabled`` or ``--enable``

    Reject incoming connections that are not in response to outbound
    requests, such as DNS replies or DHCP requests. If access to
    services running on this machine is needed, you can choose to allow
    specific services through the firewall.

``--disabled`` or ``--disable``

    Do not configure any iptables rules.

``--trust=``

    Listing a device here, such as eth0, allows all traffic coming from
    that device to go through the firewall. To list more than one
    device, use --trust eth0 --trust eth1. Do NOT use a comma-separated
    format such as --trust eth0, eth1.

``<incoming>``

    Replace with none or more of the following to allow the specified
    services through the firewall.

        ``--ssh`` - The ssh option is enabled by default, regardless of
        the presence of this flag.

        ``--smtp``

        ``--http``

        ``--ftp``

``--port=``

    You can specify that ports be allowed through the firewall using the
    port:protocol format. You can also specify ports numerically.
    Multiple ports can be combined into one option as long as they are
    separated by commas. For example:

    ``firewall --port=imap:tcp,1234:ucp,47``

``--service=``

    This option provides a higher-level way to allow services through
    the firewall. Some services (like cups, avahi, etc.) require
    multiple ports to be open or other special configuration in order
    for the service to work. You could specify each individual service
    with the ``--port`` option, or specify ``--service=`` and open them
    all at once.

    Valid options are anything recognized by the firewall-offline-cmd
    program in the firewalld package. If firewalld is running,
    ``firewall-cmd --get-services`` will provide a list of known service
    names.


firstboot
---------

Determine whether the Setup Agent starts the first time the system is
booted. If enabled, the ``initial-setup`` package must be installed. If
not specified, the setup agent (initial-setup) is disabled by default.

``firstboot --enable|--disable|--reconfig``

``--enable`` or ``--enabled``

    The Setup Agent is started the first time the system boots.

``--disable`` or ``--disabled``

    The Setup Agent is not started the first time the system boots.

``--reconfig``

    Enable the Setup Agent to start at boot time in reconfiguration
    mode. This mode enables the language, mouse, keyboard, root
    password, security level, time zone, and networking configuration
    options in addition to the default ones.


group
-----

Creates a new user group on the system. If a group with the given name
or GID already exists, this command will fail. In addition, the ``user``
command can be used to create a new group for the newly created user.

``group --name=<name> [--gid=<gid>]``

``--name=``

    Provides the name of the new group.

``--gid=``

    The group's GID. If not provided, this defaults to the next
    available non-system GID.


graphical
---------

Perform the kickstart installation in graphical mode. This is the
default.


halt
----

At the end of installation, display a message and wait for the user to
press a key before rebooting. This is the default action.


ignoredisk
----------

Controls anaconda's access to disks attached to the system. By default,
all disks will be available for partitioning. Only one of the following
three options may be used.

``ignoredisk --drives=[disk1,disk2,...]``

    Specifies those disks that anaconda should not touch when
    partitioning, formatting, and clearing.

``ignoredisk --only-use=[disk1,disk2,...]``

    Specifies the opposite - only disks listed here will be used during
    installation.

``ignoredisk --interactive``

    Allow the user manually navigate the advanced storage screen.


install
-------

Tells the system to install a fresh system rather than upgrade an
existing system. This is the default mode. For installation, you must
specify the type of installation from one of cdrom, harddrive, nfs, or
url (for ftp or http installations). The install command and the
installation method command must be on separate lines.

**Note that from F18 onward, upgrades are no longer supported in anaconda and should be done with FedUp, the Fedora update tool.**

**If using F21 or later, the DNF system-upgrade plugin is recommended instead.**


cdrom
~~~~~

``cdrom``

    Install from the first CD-ROM/DVD drive on the system.


harddrive
~~~~~~~~~

``harddrive [--biospart=<bios partition> | --partition=<partition>] [--dir=<directory>]``

    Install from a directory of ISO images on a local drive, which must
    be either vfat or ext2. In addition to this directory, you must also
    provide the install.img in some way. You can either do this by
    booting off the boot.iso or by creating an images/ directory in the
    same directory as the ISO images and placing install.img in there.

    ``--biospart=``

        BIOS partition to install from (such as 82p2).

    ``--partition=``

        Partition to install from (such as, sdb2).

    ``--dir=``

        Directory containing both the ISO images and the
        images/install.img. For example:

    ``harddrive --partition=hdb2 --dir=/tmp/install-tree``


liveimg
~~~~~~~

``liveimg --url=<url> [--proxy=<proxyurl>] [--checksum=<sha256>] [--noverifyssl]``

    Install a disk image instead of packages. The image can be the
    squashfs.img from a Live iso, or any filesystem mountable by the
    install media (eg. ext4). Anaconda expects the image to contain
    utilities it needs to complete the system install so the best way to
    create one is to use livemedia-creator to make the disk image. If
    the image contains /LiveOS/\*.img (this is how squashfs.img is
    structured) the first \*img file inside LiveOS will be mounted and
    used to install the target system. As of Anaconda 21.29 the URL may
    point to a tarfile of the root filesystem. The file must end in
    .tar, .tbz, .tgz, .txz, .tar.bz2, tar.gz, tar.xz

    ``--url=``

        The URL to install from. http, https, ftp and file are
        supported.

    ``--proxy=[protocol://][username[:password]@]host[:port]``

        Specify an HTTP/HTTPS/FTP proxy to use while performing the
        install. The various parts of the argument act like you would
        expect.

    ``--checksum=``

        Optional sha256 checksum of the image file

    ``--noverifyssl``

        For a tree on a HTTPS server do not check the server's
        certificate with what well-known CA validate and do not check
        the server's hostname matches the certificate's domain name.


nfs
~~~

``nfs --server=<hostname> --dir=<directory> [--opts=<nfs options>]``

    Install from the NFS server specified. This can either be an
    exploded installation tree or a directory of ISO images. In the
    latter case, the install.img must also be provided subject to the
    same rules as with the harddrive installation method described
    above.

    ``--server=``

        Server from which to install (hostname or IP).

    ``--dir=``

        Directory containing the Packages/ directory of the installation
        tree. If doing an ISO install, this directory must also contain
        images/install.img.

    ``--opts=``

        Mount options to use for mounting the NFS export. Any options
        that can be specified in /etc/fstab for an NFS mount are
        allowed. The options are listed in the nfs(5) man page. Multiple
        options are separated with a comma.

        For example:

        ``nfs --server=nfsserver.example.com --dir=/tmp/install-tree``


url
~~~

``url --url=<url>|--mirrorlist=<url> [--proxy=<proxy url>] [--noverifyssl]``

    Install from an installation tree on a remote server via FTP or
    HTTP.

    ``--url=``

        The URL to install from. Variable substitution is done for
        $releasever and $basearch in the url (added in F19).

    ``--mirrorlist=``

        The mirror URL to install from. Variable substitution is done
        for $releasever and $basearch in the url (added in F19).

    ``--proxy=[protocol://][username[:password]@]host[:port]``

        Specify an HTTP/HTTPS/FTP proxy to use while performing the
        install. The various parts of the argument act like you would
        expect.

    ``--noverifyssl``

        For a tree on a HTTPS server do not check the server's
        certificate with what well-known CA validate and do not check
        the server's hostname matches the certificate's domain name.


iscsi
-----

Specifies additional iSCSI storage to be attached during installation.
If you use the iscsi parameter, you must also assign a name to the iSCSI
node, using the iscsiname parameter. The iscsiname parameter must appear
before the iscsi parameter in the kickstart file.

``iscsi --ipaddr= [options]``

We recommend that wherever possible you configure iSCSI storage in the
system BIOS or firmware (iBFT for Intel systems) rather than use the
iscsi parameter. \*Anaconda\* automatically detects and uses disks
configured in BIOS or firmware and no special configuration is necessary
in the kickstart file.

If you must use the iscsi parameter, ensure that networking is activated
at the beginning of the installation, and that the iscsi parameter
appears in the kickstart file before you refer to iSCSI disks with
parameters such as clearpart or ignoredisk.

``--ipaddr=`` (mandatory)

    The IP address of the target to connect to.

``--port=``

    The port number to connect to (default, --port=3260).

``--target=``

    The target iqn.

``--iface=``

    Bind connection to specific network interface instead of using the
    default one determined by network layer. Once used, it must be
    specified for all iscsi commands.

``--user=``

    The username required to authenticate with the target.

``--password=``

    The password that corresponds with the username specified for the
    target.

``--reverse-user=``

    The username required to authenticate with the initiator from a
    target that uses reverse CHAP authentication.

``--reverse-password=``

    The password that corresponds with the username specified for the
    initiator.


iscsiname
---------

Assigns an initiator name to the computer. If you use the iscsi
parameter in your kickstart file, this parameter is mandatory, and you
must specify iscsiname in the kickstart file before you specify iscsi.

``iscsiname <iqn>``


keyboard
--------

This required command sets system keyboard type. See the documentation
of ``--vckeymap`` option and the tip at the end of this section for a
guide how to get values accepted by this command.

**Starting with Fedora 18 the ``keyboard`` command has three new options:**

``keyboard [--vckeymap=<keymap>] [--xlayouts=<layout1>,<layout2>,...,<layoutN>] [--switch=<option1>...<optionN>] [arg]``

    Either ``--vckeymap`` or ``--xlayouts`` must be used.

    Alternatively, use the older format, ``arg``, which is still
    supported. ``arg`` can be an X layout or VConsole keymap name.

    Missing values will be automatically converted from the given
    one(s).

``--vckeymap=<keymap>``

    Specify VConsole keymap that should be used. is a keymap name which
    is the same as the filename under /usr/lib/kbd/keymaps/ without the
    ".map.gz" extension.

``--xlayouts=<layout1>,<layout2>,...,<layoutN>``

    Specify a list of X layouts that should be used (comma-separated
    list without spaces).
    Accepts the same values as setxkbmap(1), but uses either the layout
    format (such as cz) or the 'layout (variant)' format (such as 'cz
    (qwerty)').

    For example:
    ``keyboard --xlayouts=cz,'cz (qwerty)'``

``--switch=<option1>,...,<optionN>``

    Specify a list of layout switching options that should be used
    (comma-separated list without spaces).
    Accepts the same values as setxkbmap(1) for layout switching.
    For example
    ``keyboard --xlayouts=cz,'cz (qwerty)' --switch=grp:alt_shift_toggle``

*If you know only the description of the layout (e.g. Czech (qwerty)), you can use http://vpodzime.fedorapeople.org/layouts_list.py to list all available layouts and find the one you want to use. The string in square brackets is the valid layout specification as Anaconda accepts it. The same goes for switching options and http://vpodzime.fedorapeople.org/switching_list.py*


lang
----

``lang <id>``

This required command sets the language to use during installation and
the default language to use on the installed system to ``<id>``. This
can be the same as any recognized setting for the $LANG environment
variable, though not all languages are supported during installation.

Certain languages (mainly Chinese, Japanese, Korean, and Indic
languages) are not supported during text mode installation. If one of
these languages is specified using the lang command, installation will
continue in English though the running system will have the specified
langauge by default.

The file /usr/share/system-config-language/locale-list provides a list
the valid language codes in the first column of each line and is part of
the system-config-languages package.

``--addsupport=``

    Install the support packages for the given locales, specified as a
    comma-separated list. Each locale may be specified in the same ways
    as the primary language may be, as described above.


logvol
------

Create a logical volume for Logical Volume Management (LVM).

``logvol <mntpoint> --vgname=<name> --size=<size> --name=<name> <options>``

``--noformat``

    Use an existing logical volume and do not format it.

``--useexisting``

    Use an existing logical volume and reformat it.

``--fstype=``

    Sets the file system type for the logical volume. Valid values
    include ext4, ext3, ext2, btrfs, swap, and vfat. Other filesystems
    may be valid depending on command line arguments passed to anaconda
    to enable other filesystems. Btrfs is a experimental filesystem. Do
    take regular backups if you are using it.

``--fsoptions=``

    Specifies a free form string of options to be used when mounting the
    filesystem. This string will be copied into the /etc/fstab file of
    the installed system and should be enclosed in quotes.

``--mkfsoptions=``

    Specifies additional parameters to be passed to the program that makes
    a filesystem on this partition. No processing is done on the list of arguments,
    so they must be supplied in a format that can be passed directly to the mkfs
    program.  This means multiple options should be comma-separated or surrounded
    by double quotes, depending on the filesystem.

``--grow``

    Tells the logical volume to grow to fill available space (if any),
    or up to the maximum size setting. Note that --grow is not supported
    for logical volumes containing a RAID volume on top of them.

``--maxsize=``

    The maximum size in megabytes when the logical volume is set to
    grow. Specify an integer value here, and do not append the number
    with MB.

``--recommended``

    Determine the size of the logical volume automatically.

``--percent``

    Specify the size of the logical volume as a percentage of available
    space in the volume group. Without the above --grow option, this may
    not work.

``--encrypted``

    Specify that this logical volume should be encrypted.

``--passphrase=``

    Specify the passphrase to use when encrypting this logical volume.
    Without the above --encrypted option, this option does nothing. If
    no passphrase is specified, the default system-wide one is used, or
    the installer will stop and prompt if there is no default.

``--escrowcert=<url>``

    Load an X.509 certificate from ``<url>``. Store the data encryption
    key of this logical volume, encrypted using the certificate, as a
    file in ``/root``. Only relevant if ``--encrypted`` is specified as
    well.

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well. In addition
    to storing the data encryption key, generate a random passphrase and
    add it to this logical volume. Then store the passphrase, encrypted
    using the certificate specified by ``--escrowcert``, as a file in
    ``/root``. If more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

``--thinpool``

    Create a thin pool logical volume. (Use a mountpoint of "none")

``--profile=<profile_name>``

    Specify an LVM profile for the thin pool (see lvm(8), standard
    profiles are 'default' and 'thin-performance' defined in the
    /etc/lvm/profile/ directory)

``--metadatasize=<size>``

    Specify the metadata area size (in MiB) for a new thin pool device.

``--chunksize=<size>``

    Specify the chunk size (in KiB) for a new thin pool device.

``--thin``

    Create a thin logical volume. (Requires use of --poolname)

``--poolname=<name>``

    Specify the name of the thin pool in which to create a thin logical
    volume. (Requires --thin)

``--resize``

    Attempt to resize this logical volume to the size given by
    ``--size=``. This option must be used with
    ``--useexisting --size=``, or an error will be raised.

``--cachesize``

    Requested size (in MiB) of cache attached to the logical volume. (Requires
    --cachepvs)

``--cachepvs``

    Comma-separated list of (fast) physical volumes that should be used for the
    cache.

``--cachemode``

    Mode that should be used for the cache. Either ``writeback`` or ``writethrough``.

Create the partition first, create the logical volume group, and then
create the logical volume. For example:

::

    part pv.01 --size 3000
    volgroup myvg pv.01
    logvol / --vgname=myvg --size=2000 --name=rootvol


logging
-------

This command controls the error logging of anaconda during installation.
It has no effect on the installed system.

``--host=``

    Send logging information to the given remote host, which must be
    running a syslogd process configured to accept remote logging.

``--port=``

    If the remote syslogd process uses a port other than the default, it
    may be specified with this option.

``--level=``

    One of debug, info, warning, error, or critical.

    Specify the minimum level of messages that appear on tty3. All
    messages will still be sent to the log file regardless of this
    level, however.


mediacheck
----------

If given, this will force anaconda to run mediacheck on the installation
media. This command requires that installs be attended, so it is
disabled by default.


monitor
-------

If the monitor command is not given, anaconda will use X to
automatically detect your monitor settings. Please try this before
manually configuring your monitor.

``--hsync=``

    Specifies the horizontal sync frequency of the monitor.

``--monitor=``

    Use specified monitor; monitor name should be from the list of
    monitors in /usr/share/hwdata/MonitorsDB from the hwdata package.
    The list of monitors can also be found on the X Configuration screen
    of the Kickstart Configurator. This is ignored if --hsync or --vsync
    is provided. If no monitor information is provided, the installation
    program tries to probe for it automatically.

``--noprobe``

    Do not probe the monitor.

``--vsync=``

    Specifies the vertical sync frequency of the monitor.


network
-------

Configures network information for target system and activates network
devices in installer environment. Device of the first network command is
activated if network is required, e.g. in case of network installation
or using vnc. Activation of the device can be also explicitly required
by ``--activate`` option. If the device has already been activated to
get kickstart file (e.g. using configuration provided with boot options
or entered in loader UI) it is re-activated with configuration from
kickstart file.

In F15, the device of first network command is activated also in case of
non-network installs, and device is not re-activated using kickstart
configuration.

``--activate``

    As noted above, using this option ensures any matching devices
    beyond the first will also be activated.

    Since F16.

``--bootproto=[dhcp|bootp|static|ibft]``

    The default setting is dhcp. bootp and dhcp are treated the same.

    The DHCP method uses a DHCP server system to obtain its networking
    configuration. As you might guess, the BOOTP method is similar,
    requiring a BOOTP server to supply the networking configuration.

    The static method requires that you enter all the required
    networking information in the kickstart file. As the name implies,
    this information is static and will be used during and after the
    installation. The line for static networking is more complex, as you
    must include all network configuration information **on one line**. You
    must specify the IP address, netmask, gateway, and nameserver. For
    example:

::

   network --device=link --bootproto=static --ip=10.0.2.15 --netmask=255.255.255.0 --gateway=10.0.2.254 --nameserver=10.0.2.1

   If you use the static method, be aware of the following restriction:

   All static networking configuration information must be specified
   on one line; you cannot wrap lines using a backslash, for example.

   ibft setting is for reading the configuration from iBFT table. It
   was added in F16.

``--device=``

    Specifies device to be configured and/or activated with the network
    command. The device can be specified in the same ways as
    `ksdevice <https://rhinstaller.github.io/anaconda/boot-options.html#ksdevice>`__ boot option. For
    example:

    ``network --bootproto=dhcp --device=eth0``

``--ip=``

    IP address for the interface.

``--ipv6=``

    IPv6 address for the interface. This can be the static address in
    form ``<IPv6 address>[/<prefix length>]``, e.g. 3ffe:ffff:0:1::1/128
    (if prefix is omitted 64 is assumed), "auto" for address assignment
    based on automatic neighbor discovery, or "dhcp" to use the DHCPv6
    protocol.

``--gateway=``

    Default gateway, as an IPv4 or IPv6 address.

``--nodefroute``

    Prevents grabbing of the default route by the device. It can be
    useful when activating additional devices in installer using
    ``--activate`` option. Since F16.

``--nameserver=``

    Primary nameserver, as an IP address. Multiple nameservers must be
    comma separated.

``--nodns``

    Do not configure any DNS server.

``--netmask=``

    Netmask for the installed system.

``--hostname=``

    Hostname for the installed system.

``--ethtool=``

    Specifies additional low-level settings for the network device which
    will be passed to the ethtool program.

``--essid=``

    The network ID for wireless networks.

``--wepkey=``

    The WEP encryption key for wireless networks.

``--wpakey=``

    The WPA encryption key for wireless networks (since F16).

``--onboot=``

    Whether or not to enable the device a boot time.

``--dhcpclass=``

    The DHCP class.

``--mtu=``

    The MTU of the device.

``--noipv4``

    Disable IPv4 on this device.

``--noipv6``

    Disable IPv6 on this device.

``--bondslaves``

    Bonded device with name specified by ``--device`` option will be
    created using slaves specified in this option. Example:
    ``--bondslaves=eth0,eth1``. Since Fedora 19.

``--bondopts``

    A comma-separated list of optional parameters for bonded interface
    specified by ``--bondslaves`` and ``--device`` options. Example:
    ``--bondopts=mode=active-backup,primary=eth1``. If an option itself
    contains comma as separator use semicolon to separate the options.
    Since Fedora 19.

``--vlanid``

    Id (802.1q tag) of vlan device to be created using parent device
    specified by ``--device`` option. For example
    ``network --device=eth0 --vlanid=171`` will create vlan device
    ``eth0.171``. Since Fedora 19.

``--teamslaves``

    Team device with name specified by ``--device`` option will be
    created using slaves specified in this option. Slaves are separated
    by comma. A slave can be followed by its configuration which is a
    single-quoted json format string with double qoutes escaped by
    ``'\'`` character. Example:
    ``--teamslaves="p3p1'{\"prio\": -10, \"sticky\": true}',p3p2'{\"prio\": 100}'"``.
    See also ``--teamconfig`` option. Since Fedora 20.

``--teamconfig``

    Double-quoted team device configuration which is a json format
    string with double quotes escaped with ``'\'`` character. The device
    name is specified by ``--device`` option and its slaves and their
    configuration by ``--teamslaves`` option. Since Fedora 20. Example:

::

    network --device team0 --activate --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2  \
    --teamslaves="p3p1'{\"prio\": -10, \"sticky\": true}',p3p2'{\"prio\": 100}'" \
    --teamconfig="{\"runner\": {\"name\": \"activebackup\"}}"


part or partition
-----------------

Creates a partition on the system. This command is required.

**All partitions created will be formatted as part of the installation process unless ``--noformat`` and ``--onpart`` are used.**

``part <mntpoint>``

The ``<mntpoint>`` is where the partition will be mounted and must be of
one of the following forms:

    ``/<path>``

        For example, /, /usr, /home

    ``swap``

        The partition will be used as swap space.

        To determine the size of the swap partition automatically, use
        the ``--recommended`` option. Starting with Fedora 18 the
        ``--hibernation`` option can be used to automatically determine
        the size of the swap partition big enough for hibernation.

    ``raid.<id>``

        The partition will be used for software RAID (refer to raid).

    ``pv.<id>``

        The partition will be used for LVM (refer to logvol).

    ``btrfs.<id>``

        The partition will be used for BTRFS volume (refer to btrfs).

    ``biosboot``

        The partition will be used for a BIOS Boot Partition. As of
        Fedora 16 there must be a biosboot partition for the bootloader
        to be successfully installed onto a disk that contains a
        GPT/GUID partition table (refer to bootloader).

``--size=``

    The minimum partition size in megabytes. Specify an integer value
    here such as 500. Do not append the number with MB.

``--grow``

    Tells the partition to grow to fill available space (if any), or up
    to the maximum size setting. Note that --grow is not supported for
    partitions containing a RAID volume on top of them.

``--maxsize=``

    The maximum partition size in megabytes when the partition is set to
    grow. Specify an integer value here, and do not append the number
    with MB.

``--noformat``

    Tells the installation program not to format the partition, for use
    with the ``--onpart`` command.

``--onpart=`` or ``--usepart=``

    Put the partition on an already existing device. Use
    "--onpart=LABEL=name" or "--onpart=UUID=name" to specify a partition
    by label or uuid respectively.

    **Anaconda may create partitions in any particular order, so it is safer to use labels than absolute partition names.**

``--ondisk=`` or ``--ondrive=``

    Forces the partition to be created on a particular disk.

``--asprimary``

    Forces automatic allocation of the partition as a primary partition
    or the partitioning will fail.

   **TIP:** *The ``--asprimary`` option only makes sense with the MBR partitioning scheme and is ignored when the GPT partitioning scheme is used.*

``--fsprofile=``

    Specifies a usage type to be passed to the program that makes a
    filesystem on this partition. A usage type defines a variety of
    tuning parameters to be used when making a filesystem. For this
    option to work, the filesystem must support the concept of usage
    types and there must be a configuration file that lists valid types.
    For ext2/3/4, this configuration file is ``/etc/mke2fs.conf``.

``--mkfsoptions=``

    Specifies additional parameters to be passed to the program that makes
    a filesystem on this partition. This is similar to ``--fsprofile`` but
    works for all filesystems, not just the ones that support the profile
    concept. No processing is done on the list of arguments, so they must
    be supplied in a format that can be passed directly to the mkfs program.
    This means multiple options should be comma-separated or surrounded by
    double quotes, depending on the filesystem.

``--fstype=``

    Sets the file system type for the partition. Valid values include
    ext4, ext3, ext2, xfs, btrfs, swap, and vfat. Other filesystems may
    be valid depending on command line arguments passed to anaconda to
    enable other filesystems.

``--fsoptions=``

    Specifies a free form string of options to be used when mounting the
    filesystem. This string will be copied into the /etc/fstab file of
    the installed system and should be enclosed in quotes.

``--label=``

    Specify the label to give to the filesystem to be made on the
    partition. If the given label is already in use by another
    filesystem, a new label will be created for this partition.

``--recommended``

    Determine the size of the partition automatically.

``--onbiosdisk=``

    Forces the partition to be created on a particular disk as
    discovered by the BIOS.

``--encrypted``

    Specify that this partition should be encrypted.

``--passphrase=``

    Specify the passphrase to use when encrypting this partition.
    Without the above --encrypted option, this option does nothing. If
    no passphrase is specified, the default system-wide one is used, or
    the installer will stop and prompt if there is no default.

``--escrowcert=<url>``

    Load an X.509 certificate from ``<url>``. Store the data encryption
    key of this partition, encrypted using the certificate, as a file in
    ``/root``. Only relevant if ``--encrypted`` is specified as well.

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well. In addition
    to storing the data encryption key, generate a random passphrase and
    add it to this partition. Then store the passphrase, encrypted using
    the certificate specified by ``--escrowcert``, as a file in
    ``/root``. If more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

``--resize``

    Attempt to resize this partition to the size given by ``--size=``.
    This option must be used with ``--onpart --size=``, or an error will
    be raised.

   **If partitioning fails for any reason, diagnostic messages will appear on virtual console 3.**


poweroff
--------

Turn off the machine after the installation is complete. Normally,
kickstart displays a message and waits for the user to press a key
before rebooting.


raid
----

Assembles a software RAID device. This command is of the form:

``raid <mntpoint> --level=<level> --device=<mddevice> <partitions*>``

``<mntpoint>``

    Location where the RAID file system is mounted. If it is /, the RAID
    level must be 1 unless a boot partition (/boot) is present. If a
    boot partition is present, the /boot partition must be level 1 and
    the root (/) partition can be any of the available types. The
    ``<partitions*>`` (which denotes that multiple partitions can be
    listed) lists the RAID identifiers to add to the RAID array.

``--level=``

    RAID level to use (0, 1, 4, 5, 6, or 10).

``--device=``

    Name of the RAID device to use (such as 'fedora-root' or 'home'). As
    of Fedora 19, RAID devices are no longer referred to by names like
    'md0'. If you have an old (v0.90 metadata) array that you cannot
    assign a name to, you can specify the array by a filesystem label or
    UUID (eg: --device=LABEL=fedora-root).

``--spares=``

    Specifies the number of spare drives allocated for the RAID array.
    Spare drives are used to rebuild the array in case of drive failure.

``--fstype=``

    Sets the file system type for the RAID array. Valid values include
    ext4, ext3, ext2, btrfs, swap, and vfat. Other filesystems may be
    valid depending on command line arguments passed to anaconda to
    enable other filesystems.

``--fsoptions=``

    Specifies a free form string of options to be used when mounting the
    filesystem. This string will be copied into the /etc/fstab file of
    the installed system and should be enclosed in quotes.

``--mkfsoptions=``

    Specifies additional parameters to be passed to the program that makes
    a filesystem on this partition. No processing is done on the list of arguments,
    so they must be supplied in a format that can be passed directly to the mkfs
    program.  This means multiple options should be comma-separated or surrounded
    by double quotes, depending on the filesystem.

``--label=``

    Specify the label to give to the filesystem to be made. If the given
    label is already in use by another filesystem, a new label will be
    created.

``--noformat``

    Use an existing RAID device and do not format the RAID array.

``--useexisting``

    Use an existing RAID device and reformat it.

``--encrypted``

    Specify that this RAID device should be encrypted.

``--passphrase=``

    Specify the passphrase to use when encrypting this RAID device.
    Without the above --encrypted option, this option does nothing. If
    no passphrase is specified, the default system-wide one is used, or
    the installer will stop and prompt if there is no default.

``--escrowcert=<url>``

    Load an X.509 certificate from ``<url>``. Store the data encryption
    key of this RAID device, encrypted using the certificate, as a file
    in ``/root``. Only relevant if ``--encrypted`` is specified as well.

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well. In addition
    to storing the data encryption key, generate a random passphrase and
    add it to this RAID device. Then store the passphrase, encrypted
    using the certificate specified by ``--escrowcert``, as a file in
    ``/root``. If more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

The following example shows how to create a RAID level 1 partition for
/, and a RAID level 5 for /usr, assuming there are three disks on the
system. It also creates three swap partitions, one on each drive.

::

    part raid.01 --size=6000 --ondisk=sda
    part raid.02 --size=6000 --ondisk=sdb
    part raid.03 --size=6000 --ondisk=sdc

    part swap1 --size=512 --ondisk=sda
    part swap2 --size=512 --ondisk=sdb
    part swap3 --size=512 --ondisk=sdc

    part raid.11 --size=6000 --ondisk=sda
    part raid.12 --size=6000 --ondisk=sdb
    part raid.13 --size=6000 --ondisk=sdc

    raid / --level=1 --device=md0 raid.01 raid.02 raid.03
    raid /usr --level=5 --device=md1 raid.11 raid.12 raid.13


realm
-----

Join an Active Directory or FreeIPA domain.

``realm join <domain.example.com>``

``--computer-ou=``

    The distinguished name of an organizational unit to create the
    computer account. The exact format of the distinguished name depends
    on the client software and membership software. You can usually omit
    the root DSE portion of distinguished name.

``--no-password``

    Perform the join automatically without a password.

``--one-time-password=``

    Perform the join using a one time password specified on the command
    line. This is not possible with all types of realms.

``--client-software=``

    Only join realms for which we can use the given client software.
    Possible values include *sssd* or *winbind*. Not all values are
    supported for all realms. By default the client software is
    automatically selected.

``--server-software=``

    Only join realms which run the given server software. Possible
    values include *active-directory* or *freeipa*.

``--membership-software=``

    The software to use when joining to the realm. Possible values
    include *samba* or *adcli*. Not all values are supported for all
    realms. By default the membership software is automatically
    selected.

::

    realm join --one-time-password=12345 DC.EXAMPLE.COM


reboot
------

Reboot after the installation is complete. Normally, kickstart displays
a message and waits for the user to press a key before rebooting.

``--eject``

    Attempt to eject CD or DVD media before rebooting.

``--kexec``

    Use kexec to reboot into the new system, bypassing BIOS/Firmware and bootloader.


repo
----

Configures additional yum repositories that may be used as sources for
package installation. Multiple repo lines may be specified. By default,
anaconda has a configured set of repos taken from /etc/anaconda.repos.d
plus a special Installation Repo in the case of a media install. The
exact set of repos in this directory changes from release to release and
cannot be listed here. There will likely always be a repo named
"updates".

Note: If you want to enable one of the repos in /etc/anaconda.repos.d
that is disabled by default (like "updates"), you should use --name= but
none of the other options. anaconda will look for a repo by this name
automatically. Providing a baseurl or mirrorlist URL will result in
anaconda attempting to add another repo by the same name, which will
cause a conflicting repo error.

``repo --name=<name> [--baseurl=<url>|--mirrorlist=<url>]  [options]``

``--name=``

    The repo id. This option is required. If a repo has a name that
    conflicts with a previously added one, the new repo will be ignored.
    Because anaconda has a populated list of repos when it starts, this
    means that users cannot create new repos that override these names.
    Please check /etc/anaconda.repos.d from the operating system you
    wish to install to see what names are not available.

``--baseurl=``

    The URL for the repository. The variables that may be used in yum
    repo config files are not supported here. You may use one of either
    this option or ``--mirrorlist``, not both. If an NFS repository is
    specified, it should be of the form ``nfs://host:/path/to/repo``.
    Note that there is a colon after the host--Anaconda passes
    everything after "nfs://\ " directly to the mount command instead of
    parsing URLs according to RFC 2224. Variable substitution is done
    for $releasever and $basearch in the url (added in F19).

``--mirrorlist=``

    The URL pointing at a list of mirrors for the repository. The
    variables that may be used in yum repo config files are not
    supported here. You may use one of either this option or
    ``--baseurl``, not both. Variable substitution is done for
    $releasever and $basearch in the url (added in F19).

``--cost=``

    An integer value to assign a cost to this repository. If multiple
    repositories provide the same packages, this number will be used to
    prioritize which repository will be used before another.
    Repositories with a lower cost take priority over repositories with
    higher cost.

``--excludepkgs=``

    A comma-separated list of package names and globs that must not be
    pulled from this repository. This is useful if multiple repositories
    provide the same package and you want to make sure it comes from a
    particular repository.

``--includepkgs=``

    A comma-separated list of package names and globs that must be
    pulled from this repository. This is useful if multiple repositories
    provide the same package and you want to make sure it comes from
    this repository.

``--proxy=[protocol://][username[:password]@]host[:port]``

    Specify an HTTP/HTTPS/FTP proxy to use just for this repository.
    This setting does not affect any other repositories, nor how the
    install.img is fetched on HTTP installs. The various parts of the
    argument act like you would expect.

``--ignoregroups=true``

    This option is used when composing installation trees and has no
    effect on the installation process itself. It tells the compose
    tools to not look at the package group information when mirroring
    trees so as to avoid mirroring large amounts of unnecessary data.

``--noverifyssl``

    For a https repo do not check the server's certificate with what
    well-known CA validate and do not check the server's hostname
    matches the certificate's domain name.

``--install``

    Install this repository to the target system so that it can be used
    after reboot. Added in anaconda-22.3-1


reqpart
-------

Automatically create partitions required by your hardware platform. These include a ``/boot/efi`` for x86_64 and Aarch64 systems with UEFI firmware, ``biosboot`` for x86_64 systems with BIOS firmware and GPT, and ``PRePBoot`` for IBM Power Systems.

Note: This command can not be used together with ``autopart``, because ``autopart`` does the same and creates other partitions or logical volumes such as ``/`` and ``swap`` on top. In contrast with ``autopart``, this command only creates platform-specific partitions and leaves the rest of the drive empty, allowing you to create a custom layout.

``reqpart [--add-boot]``

``--add-boot``

   Create a separate ``/boot`` partition in addition to the platform-specific partition created by the base command.

rescue
------

Automatically enter the installer's rescue mode. This gives you a chance
to repair the system should something catastrophic happen.

``rescue [--nomount|--romount]``

``--nomount|--romount]``

    Controls how the installed system is mounted in the rescue
    environment. By default, the installer will find your system and
    mount it in read-write mode, telling you where it has performed this
    mount. You may optionally choose to not mount anything or mount in
    read-only mode. Only one of these two options may be given at any
    one time.


rootpw
------

This required command sets the system's root password to the
``<password>`` argument.

``rootpw [options] <password>``

``--iscrypted|--plaintext``

    If this is present, the password argument is assumed to already be
    encrypted. ``--plaintext`` has the opposite effect - the password
    argument is assumed to not be encrypted. To create an encrypted
    password you can use python:
    ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Salt"))'``
    This will generate sha512 crypt of your password using your provided
    salt.

``--lock``

    If this is present, the root account is locked by default. That is,
    the root user will not be able to login from the console.


selinux
-------

Sets the state of SELinux on the installed system. SELinux defaults to
enforcing in anaconda.

``selinux [--disabled|--enforcing|--permissive]``

``--disabled``

    If this is present, SELinux is disabled.

``--enforcing``

    If this is present, SELinux is set to enforcing mode.

``--permissive``

    If this is present, SELinux is enabled, but only logs things that
    would be denied in enforcing mode.


services
--------

Modifies the default set of services that will run under the default
runlevel. The services listed in the disabled list will be disabled
before the services listed in the enabled list are enabled.

``services [--disabled=<list>]  [--enabled=<list>]``

``--disabled=``

    Disable the services given in the comma separated list.

``--enabled=``

    Enable the services given in the comma separated list.


shutdown
--------

At the end of installation, shut down the machine. This is the same as
the poweroff command. Normally, kickstart displays a message and waits
for the user to press a key before rebooting.


sshkey
------

This installs a ssh key to the authorized\_keys file of the specified
user on the installed system.

``sshkey --username=<user> "ssh key"``

Note that the key should be quoted, it contains spaces. And the user
should exist (or be root) either via creation by a package install or
the kickstart user command. Added in anaconda-22.13-1


sshpw
-----

The installer can start up ssh to provide for interactivity and
inspection, just like it can with telnet. The "inst.sshd" option must be
specified on the kernel command-line for Anaconda to start an ssh
daemon. The sshpw command is used to control the accounts created in the
installation environment that may be remotely logged into. For each
instance of this command given, a user will be created. These users will
not be created on the final system - they only exist for use while the
installer is running.

Note that by default, root has a blank password. If you don't want any
user to be able to ssh in and have full access to your hardware, you
must specify sshpw for username root. Also note that if Anaconda fails
to parse the kickstart file, it will allow anyone to login as root and
have full access to your hardware.

``sshpw --username=<name> [--iscrypted|--plaintext] [--lock] [--sshkey] <password>``

``--username=``

    Provides the name of the user. This option is required.

``--iscrypted|--plaintext``

    If this is present, the password argument is assumed to already be
    encrypted. --plaintext has the opposite effect - the password
    argument is assumed to not be encrypted. The default is plaintext.

``--lock``

    If this is present, the new user account is locked by default. That
    is, the user will not be able to login from the console.

``--sshkey``

    This is used to set a ssh key for the user during the installation.
    password is copied into the account's .ssh/authorized_keys file.


skipx
-----

If present, X is not configured on the installed system.


text
----

Perform the kickstart installation in text mode. Kickstart installations
are performed in graphical mode by default.


timezone
--------

This required command sets the system time zone to which may be any of
the time zones listed by timeconfig.

``timezone [--utc]  <timezone>``

``--utc``

    If present, the system assumes the hardware clock is set to UTC
    (Greenwich Mean) time.

   *To get the list of supported timezones, you can either run this script: http://vpodzime.fedorapeople.org/timezones_list.py or look at this list: http://vpodzime.fedorapeople.org/timezones_list.txt*

Starting with Fedora 18 the ``timezone`` command has two new options:

``timezone [--utc] [--nontp] [--ntpservers=<server1>,<server2>,...,<serverN>] <timezone>``

``--nontp``

    Disable automatic starting of NTP service.

    ``--nontp`` and ``--ntpservers`` are mutually exclusive.

``--ntpservers=<server1>,<server2>,...,<serverN>``

    Specify a list of NTP servers to be used (comma-separated list with
    no spaces). The chrony package is automatically installed when this
    option is used. If you don't want the package to be automatically
    installed then use ``-chrony`` in package selection.

    For example:
    ``timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz Europe/Prague``


updates
-------

Specify the location of an updates.img for use in installation. See
anaconda-release-notes.txt for a description of how to make an
updates.img.

``updates [URL]``

    If present, the URL for an updates image.

    If not present, anaconda will attempt to load from a floppy disk.


upgrade
-------

**Note that from F18 onward, upgrades are no longer supported in anaconda and should be done with FedUp, the Fedora update tool.**

**If using F21 or later, the DNF system upgrade plugin is recommended instead.**

Tells the system to upgrade an existing system rather than install a
fresh system. You must specify one of cdrom, harddrive, nfs, or url (for
ftp and http) as the location of the installation tree. Refer to install
for details.

``--root-device=<root>`` (optional)

    On a system with multiple installs, this option specifies which
    filesystem holds the installation to be upgraded. This can be
    specified by device name, UUID=, or LABEL= just like the harddrive
    command may be.


user
----

Creates a new user on the system.

``user --name=<username> [--gecos=<string>] [--groups=<list>]  [--homedir=<homedir>] [--password=<password>]  [--iscrypted|--plaintext] [--lock]  [--shell=<shell>] [--uid=<uid>] [--gid=<gid>]``

   **The Anaconda version used in F19 and F20 will create unlocked user accounts with \*NO\* password unless --password or --lock is passed. This was a bug, which is fixed in newer releases.**

``--name=``

    Provides the name of the user. This option is required.

``--gecos=``

    Provides the GECOS information for the user. This is a string of
    various system-specific fields separated by a comma. It is
    frequently used to specify the user's full name, office number, and
    the like. See ``man 5 passwd`` for more details.

``--groups=``

    In addition to the default group, a comma separated list of group
    names the user should belong to. Any groups that do not already
    exist will be created.
    As of Fedora 24, the group name can optionally be followed by a GID in
    parenthesis, for example, ``newgroup(5002)``. If the group already exists
    with a different GID, an error will be raised.

``--homedir=``

    The home directory for the user. If not provided, this defaults to
    /home/.

``--lock``

    If this is present, the new user account is locked by default. That
    is, the user will not be able to login from the console.

``--password=``

    The new user's password. If not provided, the account will be locked
    by default.
    If this is present, the password argument is assumed to already be
    encrypted. ``--plaintext`` has the opposite effect - the password
    argument is assumed to not be encrypted. To create an encrypted
    password you can use python:
    ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Sault"))'``
    This will generate sha512 crypt of your password using your provided
    salt.

``--iscrypted|--plaintext``

    Is the password provided by ``--password`` already encrypted or not?
    ``--plaintext`` has the opposite effect - the password argument is
    assumed to not be encrypted.

``--shell=``

    The user's login shell. If not provided, this defaults to the system
    default.

``--uid=``

    The user's UID. If not provided, this defaults to the next available
    non-system UID.

``--gid=``

    The GID of the user's primary group. If not provided, this defaults
    to the next available non-system GID.


vnc
---

Allows the graphical installation to be viewed remotely via VNC. This
method is usually preferred over text mode, as there are some size and
language limitations in text installs. With no options, this command
will start a VNC server on the machine with no password and will print
out the command that needs to be run to connect a remote machine.

``vnc [--host=<hostname>]  [--port=<port>]  [--password=<password>]``

``--host=``

    Instead of starting a VNC server on the install machine, connect to
    the VNC viewer process listening on the given hostname.

``--port=``

    Provide a port that the remote VNC viewer process is listening on.
    If not provided, anaconda will use the VNC default.

``--password=``

    Set a password which must be provided to connect to the VNC session.
    This is optional, but recommended.


volgroup
--------

Use to create a Logical Volume Management (LVM) group.

``volgroup <name> <partitions*> <options>``

``<name>``

    Name given to the volume group. The (which denotes that multiple
    partitions can be listed) lists the identifiers to add to the volume
    group.

``--noformat``

    Use an existing volume group. Do not specify partitions when using
    this option.

``--useexisting``

    Use an existing volume group. Do not specify partitions when using
    this option.

``--pesize=``

    Set the size of the physical extents in KiB.

``--reserved-space=``

    Specify an amount of space to leave unused in a volume group, in
    megabytes. (new volume groups only)

``--reserved-percent=``

    Specify a percentage of total volume group space to leave unused.
    (new volume groups only)

Create the partition first, create the logical volume group, and then
create the logical volume. For example:

::

    part pv.01 --size 3000
    volgroup myvg pv.01
    logvol / --vgname=myvg --size=2000 --name=rootvol


xconfig
-------

Configures the X Window System. If this option is not given, anaconda
will use X to attempt to automatically configure. Please try this before
manually configuring your system.

``--defaultdesktop=``

    Specify either GNOME or KDE to set the default desktop (assumes that
    GNOME Desktop Environment and/or KDE Desktop Environment has been
    installed through %packages).

``--startxonboot``

    Use a graphical login on the installed system.


zerombr
-------

If zerombr is specified, any disks whose formatting is unrecognized are
initialized. This will destroy all of the contents of disks with invalid
partition tables or other formatting unrecognizable to the installer. It
is useful so that the installation program does not ask if it should
initialize the disk label if installing to a brand new hard drive.


zfcp
----

``--devnum=``

``--fcplun=``

``--wwpn=``


%include
--------

Use the ``%include /path/to/file`` or ``%include <url>`` command
to include the contents of another file in the kickstart file as though
the contents were at the location of the %include command in the
kickstart file.


%ksappend
---------

The ``%ksappend url`` directive is very similar to ``%include`` in that
it is used to include the contents of additional files as though they
were at the location of the ``%ksappend`` directive. The difference is
in when the two directives are processed. ``%ksappend`` is processed in
an initial pass, before any other part of the kickstart file. Then, this
expanded kickstart file is passed to the rest of anaconda where all
``%pre`` scripts are handled, and then finally the rest of the kickstart
file is processed in order, which includes ``%include`` directives.

Thus, ``%ksappend`` provides a way to include a file containing ``%pre``
scripts, while ``%include`` does not.


Chapter 3. Package Selection
============================

Use the %packages command to begin a kickstart file section that lists
the packages you would like to install.

Packages can be specified by group or by individual package name. The
installation program defines several groups that contain related
packages. Refer to the repodata/\*comps.xml file on the first CD-ROM for
a list of groups. Each group has an id, user visibility value, name,
description, and package list. In the package list, the packages marked
as mandatory are always installed if the group is selected, the packages
marked default are selected by default if the group is selected, and the
packages marked optional must be specifically selected even if the group
is selected to be installed.

In most cases, it is only necessary to list the desired groups and not
individual packages. Note that the Core group is always selected by
default, so it is not necessary to specify it in the %packages section.

The %packages section is required to be closed with %end. Also, multiple
%packages sections may be given. This may be handy if the kickstart file
is used as a template and pulls in various other files with the %include
mechanism.

Here is an example %packages selection:

::

    %packages
    @X Window System
    @GNOME Desktop Environment
    @Graphical Internet
    @Sound and Video
    dhcp
    %end

As you can see, groups are specified, one to a line, starting with an ``@``
symbol followed by the full group name as given in the comps.xml file.
Groups can also be specified using the id for the group, such as
gnome-desktop. Specify individual packages with no additional characters
(the dhcp line in the example above is an individual package).

**Since Fedora 21** you can also specify environments using the ``@^``
prefix followed by full environment name as given in the comps.xml file.
If multiple environments are specified, only the last one specified will
be used. Environments can be mixed with both group specifications (even
if the given group is not part of the specified environment) and package
specifications.

Here is an example of requesting the GNOME Desktop environment to be
selected for installation:

::

    %packages
    @^gnome-desktop-environment
    %end

Additionally, individual packages may be specified using globs. For
instance:

::

    %packages
    vim*
    kde-i18n-*
    %end

This would install all packages whose names start with "vim" or
"kde-i18n-".

You can also specify which packages or groups not to install from the
default package list:

::

    %packages
    -autofs
    -@Sound and Video
    %end


Global %packages options
------------------------

The following options are available for use in the %packages section
header:

    ``--default``

        Install the default package set. This corresponds to the package
        set that would be installed if no other selections were made on
        the package customization screen during an interactive install.

    ``--excludedocs``

        Do not install any of the documentation from any packages. For
        the most part, this means files in /usr/share/doc\* will not get
        installed though it could mean other files as well, depending on
        how the package was built.

    ``--ignoremissing``

        Ignore any packages or groups specified in the packages section
        that are not found in any configured repository. The default
        behavior is to halt the installation and ask the user if the
        installation should be aborted or continued. This option allows
        fully automated installation even in the error case. It is used
        as follows:

        ``%packages --ignoremissing``

    ``--instLangs=``

        Specify the list of languages that should be installed. This is
        different from the package group level selections, though. This
        option does not specify what package groups should be installed.
        Instead, it controls which translation files from individual
        packages should be installed by setting RPM macros.

    ``--multilib``

        Enable yum's "all" multilib\_policy as opposed to the default of
        "best".

    ``--nocore``

        Do not install the @core group (installed by default,
        otherwise).

   **Omitting the core group can produce a system that is not bootable or that cannot finish the install. Use with caution.**


Group-level options
-------------------

In addition, group lines in the %packages section can take the following
options:

    ``--nodefaults``

        Only install the group's mandatory packages, not the default
        selections.

    ``--optional``

        In addition to the mandatory and default packages, also install
        the optional packages. This means all packages in the group will
        be installed.


Chapter 4. Pre-installation Script
==================================

You can add commands to run on the system immediately after the ks.cfg
has been parsed and the lang, keyboard, and url options have been
processed. This section must be at the end of the kickstart file (after
the commands) and must start with the %pre command. You can access the
network in the %pre section; however, name service has not been
configured at this point, so only IP addresses will work.

Preinstallation scripts are required to be closed with %end.

**If your script spawns a daemon process, you must make sure to close stdout
and stderr.  Doing so is standard procedure for creating daemons.  If you do
not close these file descriptors, the installation will appear hung as
anaconda waits for an EOF from the script.**


**Note that the pre-install script is not run in the chroot environment.**

    ``--interpreter /usr/bin/python``

        Allows you to specify a different scripting language, such as
        Python. Replace /usr/bin/python with the scripting language of
        your choice.

    ``--erroronfail``

        If the pre-installation script fails, this option will cause an
        error dialog to be displayed and will halt installation. The
        error message will direct you to where the cause of the failure
        is logged.

    ``--log=``

        Log all messages from the script to the given log file.


Example
-------

Here is an example %pre section:

::

    %pre
    #!/bin/bash
    hds=""
    mymedia=""

    for file in /sys/block/sd*; do
    hds="$hds $(basename $file)"
    done

    set $hds
    numhd=$(echo $#)

    drive1=$(echo $hds | cut -d' ' -f1)
    drive2=$(echo $hds | cut -d' ' -f2)


    if [ $numhd == "2" ]  ; then
    echo "#partitioning scheme generated in %pre for 2 drives" > /tmp/part-include
    echo "clearpart --all" >> /tmp/part-include
    echo "part /boot --fstype ext4 --size 512 --ondisk sda" >> /tmp/part-include
    echo "part / --fstype ext4 --size 10000 --grow --ondisk sda" >> /tmp/part-include
    echo "part swap --recommended --ondisk $drive1" >> /tmp/part-include
    echo "part /home --fstype ext4 --size 10000 --grow --ondisk sdb" >> /tmp/part-include
    else
    echo "#partitioning scheme generated in %pre for 1 drive" > /tmp/part-include
    echo "clearpart --all" >> /tmp/part-include
    echo "part /boot --fstype ext4 --size 521" >> /tmp/part-include
    echo "part swap --recommended" >> /tmp/part-include
    echo "part / --fstype ext4 --size 2048" >> /tmp/part-include
    echo "part /home --fstype ext4 --size 2048 --grow" >> /tmp/part-include
    fi
    %end

This script determines the number of hard drives in the system and
writes a text file with a different partitioning scheme depending on
whether it has one or two drives. Instead of having a set of
partitioning commands in the kickstart file, include the line:

``%include /tmp/part-include``

The partitioning commands selected in the script will be used.


%pre-install script
-------------------

You can use the %pre-install section to run commands after the system has been
partitioned, filesystems created, and everything is mounted under /mnt/sysimage
Like %pre these scripts do not run in the chrooted environment.

Each %pre-install section is required to be closed with a corresponding %end.


Chapter 5. Post-installation Script
===================================

You have the option of adding commands to run on the system once the
installation is complete. This section must be at the end of the
kickstart file and must start with the %post command. This section is
useful for functions such as installing additional software and
configuring an additional nameserver.

You may have more than one %post section, which can be useful for cases
where some post-installation scripts need to be run in the chroot and
others that need access outside the chroot.

Each %post section is required to be closed with a corresponding %end.

**If you configured the network with static IP information, including a
nameserver, you can access the network and resolve IP addresses in the %post
section.  If you configured the network for DHCP, the /etc/resolv.conf file
has not been completed when the installation executes the %post section. You
can access the network, but you can not resolve IP addresses. Thus, if you
are using DHCP, you must specify IP addresses in the %post section.**

**If your script spawns a daemon process, you must make sure to close stdout
and stderr.  Doing so is standard procedure for creating daemons.  If you do
not close these file descriptors, the installation will appear hung as
anaconda waits for an EOF from the script.**

**The post-install script is run in a chroot environment; therefore, performing
tasks such as copying scripts or RPMs from the installation media will not
work.**

    ``--nochroot``

        Allows you to specify commands that you would like to run
        outside of the chroot environment.

    ``--interpreter /usr/bin/python``

        Allows you to specify a different scripting language, such as
        Python. Replace /usr/bin/python with the scripting language of
        your choice.

    ``--erroronfail``

        If the post-installation script fails, this option will cause an
        error dialog to be displayed and will halt installation. The
        error message will direct you to where the cause of the failure
        is logged.

    ``--log=``

        Log all messages from the script to the given log file.


Examples
--------

Run a script named runme from an NFS share:

::

    %post
    mkdir /mnt/temp
    mount 10.10.0.2:/usr/new-machines /mnt/temp
    open -s -w -- /mnt/temp/runme
    umount /mnt/temp
    %end

Copy the file /etc/resolv.conf to the file system that was just
installed:

::

    %post --nochroot
    cp /etc/resolv.conf /mnt/sysimage/etc/resolv.conf
    %end

**If your kickstart is being interpreted by the livecd-creator tool, you should
replace /mnt/sysimage above with $INSTALL_ROOT.**


Chapter 6. Making the Kickstart File Available
==============================================

A kickstart file must be placed in one of the following locations:

-  On a boot diskette

-  On a boot CD-ROM

-  On a network

Normally a kickstart file is copied to the boot diskette, or made
available on the network. The network-based approach is most commonly
used, as most kickstart installations tend to be performed on networked
computers.

Let us take a more in-depth look at where the kickstart file may be
placed.


Creating a Kickstart Boot Diskette
----------------------------------

To perform a diskette-based kickstart installation, the kickstart file
must be named ks.cfg and must be located in the boot diskette's
top-level directory. Refer to the section Making an Installation Boot
Diskette in the Red Hat Enterprise Linux Installation Guide for
instruction on creating a boot diskette. Because the boot diskettes are
in MS-DOS format, it is easy to copy the kickstart file under Linux
using the mcopy command:

``mcopy ks.cfg a:``

Alternatively, you can use Windows to copy the file. You can also mount
the MS-DOS boot diskette in Linux with the file system type vfat and use
the cp command to copy the file on the diskette.


Creating a Kickstart Boot CD-ROM
--------------------------------

To perform a CD-ROM-based kickstart installation, the kickstart file
must be named ks.cfg and must be located in the boot CD-ROM's top-level
directory. Since a CD-ROM is read-only, the file must be added to the
directory used to create the image that is written to the CD-ROM. Refer
to the Making an Installation Boot CD-ROM section in the Red Hat
Enterprise Linux Installation Guide for instruction on creating a boot
CD-ROM; however, before making the file.iso image file, copy the ks.cfg
kickstart file to the isolinux/ directory.


Making the Kickstart File Available on the Network
--------------------------------------------------

Network installations using kickstart are quite common, because system
administrators can easily automate the installation on many networked
computers quickly and painlessly. In general, the approach most commonly
used is for the administrator to have both a BOOTP/DHCP server and an
NFS server on the local network. The BOOTP/DHCP server is used to give
the client system its networking information, while the actual files
used during the installation are served by the NFS server. Often, these
two servers run on the same physical machine, but they are not required
to.

To perform a network-based kickstart installation, you must have a
BOOTP/DHCP server on your network, and it must include configuration
information for the machine on which you are attempting to install
Fedora or Red Hat Enterprise Linux. The BOOTP/DHCP server will provide
the client with its networking information as well as the location of
the kickstart file.

If a kickstart file is specified by the BOOTP/DHCP server, the client
system will attempt an NFS mount of the file's path, and will copy the
specified file to the client, using it as the kickstart file. The exact
settings required vary depending on the BOOTP/DHCP server you use.

Here is an example of a line from the dhcpd.conf file for the DHCP
server:

::

    filename "/usr/new-machine/kickstart/";
    server-name "blarg.redhat.com";

Note that you should replace the value after filename with the name of
the kickstart file (or the directory in which the kickstart file
resides) and the value after server-name with the NFS server name.

If the filename returned by the BOOTP/DHCP server ends with a slash
("/"), then it is interpreted as a path only. In this case, the client
system mounts that path using NFS, and searches for a particular file.
The filename the client searches for is:

::
   <ip-addr>-kickstart

The section of the filename should be replaced with the client's IP
address in dotted decimal notation. For example, the filename for a
computer with an IP address of 10.10.0.1 would be 10.10.0.1-kickstart.

Note that if you do not specify a server name, then the client system
will attempt to use the server that answered the BOOTP/DHCP request as
its NFS server. If you do not specify a path or filename, the client
system will try to mount /kickstart from the BOOTP/DHCP server and will
try to find the kickstart file using the same -kickstart filename as
described above.


HTTP Headers
~~~~~~~~~~~~

When Anaconda requests the kickstart over the network it includes
several custom HTTP headers:

``X-Anaconda-Architecture: x86_64`` indicates the architecture of the
system being installed to.

``X-Anaconda-System-Release: Fedora`` indicates the product name being
installed.

There are also 2 optional headers, controlled by the kernel command line
options
`kssendmac <https://rhinstaller.github.io/anaconda/boot-options.html#inst-ks-sendmac>`__
and
`kssendsn <https://rhinstaller.github.io/anaconda/boot-options.html#inst-ks-sendsn>`__


Chapter 7. Making the Installation Tree Available
=================================================

The kickstart installation needs to access an installation tree. An
installation tree is a copy of the binary Fedora or Red Hat Enterprise
Linux CD-ROMs with the same directory structure.

If you are performing a CD-based installation, insert the Fedora or Red
Hat Enterprise Linux CD-ROM #1 into the computer before starting the
kickstart installation.

If you are performing a hard-drive installation, make sure the ISO
images of the binary Fedora or Red Hat Enterprise Linux CD-ROMs are on a
hard drive in the computer.

If you are performing a network-based (NFS, FTP, or HTTP) installation,
you must make the installation tree available over the network. Refer to
the Preparing for a Network Installation section of the Red Hat
Enterprise Linux Installation Guide for details.


Chapter 8. Starting a Kickstart Installation
============================================

To begin a kickstart installation, you must boot the system from a
Fedora or Red Hat Enterprise Linux boot diskette, Fedora or Red Hat
Enterprise Linux boot CD-ROM, or the Fedora or Red Hat Enterprise Linux
CD-ROM #1 and enter a special boot command at the boot prompt. In order
to get to the boot prompt you must hit escape at the CD or DVD boot
menu. In case you don't know what I'm talking about I took a screenshot.
The installation program looks for a kickstart file if the ks command
line argument is passed to the kernel.

https://fedoraproject.org/wiki/File:Fedora_boot_screen.png


Boot Diskette
-------------

If the kickstart file is located on a boot diskette as described in the
Section called Creating a Kickstart Boot Diskette in Chapter 6, boot the
system with the diskette in the drive, and enter the following command
at the boot: prompt:

``linux ks=floppy``


CD-ROM #1 and Diskette
----------------------

The linux ks=floppy command also works if the ks.cfg file is located on
a vfat or ext2 file system on a diskette and you boot from the Fedora or
Red Hat Enterprise Linux CD-ROM #1.

An alternate boot command is to boot off the Fedora or Red Hat
Enterprise Linux CD-ROM #1 and have the kickstart file on a vfat or ext2
file system on a diskette. To do so, enter the following command at the
boot: prompt:

``linux ks=hd:fd0:/ks.cfg``


With Driver Disk
----------------

If you need to use a driver disk with kickstart, specify the dd option
as well. For example, to boot off a boot diskette and use a driver disk,
enter the following command at the boot: prompt:

``linux ks=floppy dd``


Boot CD-ROM
-----------

If the kickstart file is on a boot CD-ROM as described in the Section
called Creating a Kickstart Boot CD-ROM in Chapter 6, insert the CD-ROM
into the system, boot the system, and enter the following command at the
boot: prompt (where ks.cfg is the name of the kickstart file):

``linux ks=cdrom:<device>:/ks.cfg``


Other kickstart options
------------------------

``ks=nfs:<server>:/<path>``

    The installation program will look for the kickstart file on the NFS
    server , as file . The installation program will use DHCP to
    configure the Ethernet card. For example, if your NFS server is
    server.example.com and the kickstart file is in the NFS share
    /mydir/ks.cfg, the correct boot command would be
    ks=\ nfs:server.example.com:/mydir/ks.cfg.

``ks=http://<server>/<path>``

    The installation program will look for the kickstart file on the
    HTTP server , as file . The installation program will use DHCP to
    configure the Ethernet card. For example, if your HTTP server is
    server.example.com and the kickstart file is in the HTTP directory
    /mydir/ks.cfg, the correct boot command would be
    ks=\ http://server.example.com/mydir/ks.cfg.

``ks=floppy``

    The installation program looks for the file ks.cfg on a vfat or ext2
    file system on the diskette in /dev/fd0.

``ks=floppy:/<path>``

    The installation program will look for the kickstart file on the
    diskette in /dev/fd0, as file .

``ks=hd:<device>:/<file>``

    The installation program will mount the file system on (which must
    be vfat or ext2), and look for the kickstart configuration file as
    in that file system (for example, ks=hd:sda3:/mydir/ks.cfg).

``ks=bd:<biosdev>:/<path>``

    The installation program will mount the file system on the specified
    partition on the specified BIOS device (for example,
    ks=bd:80p3:/mydir/ks.cfg). Note this does not work for BIOS RAID
    sets.

``ks=file:/<file>``

    The installation program will try to read the file from the file
    system; no mounts will be done. This is normally used if the
    kickstart file is already on the initrd image.

``ks=cdrom:/<path>`` or in newer versions
``ks=cdrom:<cdrom device>:/<path>``

    The installation program will look for the kickstart file on CD-ROM,
    as file .

``ks``

    If ks is used alone, the installation program will configure the
    Ethernet card to use DHCP. The kickstart file is read from the
    "bootServer" from the DHCP response as if it is an NFS server
    sharing the kickstart file. By default, the bootServer is the same
    as the DHCP server. The name of the kickstart file is one of the
    following:

    -  If DHCP is specified and the bootfile begins with a /, the
       bootfile provided by DHCP is looked for on the NFS server.

    -  If DHCP is specified and the bootfile begins with something other
       then a /, the bootfile provided by DHCP is looked for in the
       /kickstart directory on the NFS server.

    -  If DHCP did not specify a bootfile, then the installation program
       tries to read the file /kickstart/1.2.3.4-kickstart, where
       1.2.3.4 is the numeric IP address of the machine being installed.

``ksdevice=<device>``

    The installation program will use this network device to connect to
    the network. For example, to start a kickstart installation with the
    kickstart file on an NFS server that is connected to the system
    through the eth1 device, use the command
    ``ks=nfs:<server>:/<path> ksdevice=eth1`` at the boot: prompt. For
    more information, see
    `anaconda boot options <https://rhinstaller.github.io/anaconda/boot-options.html>`__.


Example Kickstart Script
------------------------

Since I got tons of errors I thought I would share an example of a
kickstart script that works. This also has an example of an lvm setup. I
couldn't find a good example of an lvm anywhere else. I also added
comments where I thought would help. Please modify if you think you have
some other good examples.

::

    # Kickstart file automatically generated by anaconda.

    #version=DEVEL
    #url --url http://mirrors.kernel.org/fedora/releases/7/Fedora/i386/os
    #ks=http://127.0.0.1/ks.cfg
    #ks=http://localhost/ks.cfg
    url --url http://ftp.usf.edu/pub/fedora/linux/releases/14/Fedora/i386/os
    install
    cdrom
    lang en_US.UTF-8
    keyboard us
    network --onboot yes --device eth0 --bootproto dhcp --noipv6
    timezone --utc America/New_York
    rootpw  --iscrypted $6$s9i1bQbmW4oSWMJc$0oHfSz0b/d90EvHx7cy70RJGIHrP1awzAgL9A3x2tbkyh72P3kN41vssaI3/SJf4Y4qSo6zxc2gZ3srzc4ACX1
    selinux --permissive
    authconfig --enableshadow --passalgo=sha512 --enablefingerprint
    firewall --service=ssh
    # The following is the partition information you requested
    # Note that any partitions you deleted are not expressed
    # here so unless you clear all partitions first, this is
    # not guaranteed to work

    #I am deleting the old partitions with this
    clearpart --all --drives=sda

    #I am creating partitions here
    #I will create the lvm stuff farther down
    part /boot --fstype=ext4 --size=500 --ondisk=sda --asprimary
    part pv.5xwrsR-ldgG-FEmM-2Zu5-Jn3O-sx9T-unQUOe --grow --size=500 --ondisk=sda --asprimary

    #Very important to have the two part lines before the lvm stuff
    volgroup VG --pesize=32768 pv.5xwrsR-ldgG-FEmM-2Zu5-Jn3O-sx9T-unQUOe
    logvol / --fstype=ext4 --name=lv_root --vgname=VG --size=40960
    logvol /home --fstype=ext4 --name=lv_home --vgname=VG --size=25600
    logvol swap --fstype swap --name=lv_swap --vgname=VG --size=4096

    bootloader --location=mbr --driveorder=sda --append="rhgb quiet"

    %packages
    @admin-tools
    #@editors
    #@fonts
    @gnome-desktop
    #@games
    #@graphical-internet
    #@graphics
    @hardware-support
    @input-methods
    #@java
    #@office
    #@online-docs
    @printing
    @sound-and-video
    @text-internet
    @base-x
    xfsprogs
    mtools
    #gpgme
    #openoffice.org-opensymbol-fonts
    #gvfs-obexftp
    hdparm
    #gok
    #iok
    #vorbis-tools
    jack-audio-connection-kit
    #ncftp
    gdm
    %end

    # Reboot after installation
    reboot


More Kickstart usage examples
-----------------------------

Various Kickstart usage examples based on real use cases:

`Reinstalling Fedora with Kickstart on
BTRFS <http://fedoraproject.org/wiki/Anaconda/Kickstart/ReinstallingFedoraWithKickstartOnBTRFS>`__

`Kickstarting a Fedora Live
installation <http://fedoraproject.org/wiki/Anaconda/Kickstart/KickstartingFedoraLiveInstallation>`__
