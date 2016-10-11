
auth or authconfig
------------------

::

    auth|authconfig [options]

.. versionadded:: Fedora3

This required command sets up the authentication
options for the system. This is just a wrapper
around the authconfig program, so all options
recognized by that program are valid for this
command. See the manual page for authconfig for a
complete list.

By default, passwords are normally encrypted and
are not shadowed.

positional arguments:

``[options]``

    See ``man authconfig``.

    .. versionadded:: Fedora3

autopart
--------

::

    autopart [--encrypted] [--passphrase PASSPHRASE] [--escrowcert <url>]
         [--backuppassphrase] [--nolvm] [--type TYPE] [--cipher CIPHER]
         [--fstype FSTYPE]

.. versionadded:: Fedora3

Automatically create partitions -- a root (/) partition,
a swap partition, and an appropriate boot partition
for the architecture. On large enough drives, this
will also create a /home partition.

The ``autopart`` command can't be used with the logvol,
part/partition, raid, reqpart, or volgroup in the same
kickstart file.

optional arguments:

``--encrypted``

    Should all devices with support be encrypted by default?
    This is equivalent to checking the "Encrypt" checkbox on
    the initial partitioning screen.

    .. versionadded:: Fedora9

``--passphrase PASSPHRASE``

    Only relevant if ``--encrypted`` is specified. Provide
    a default system-wide passphrase for all encrypted
    devices.

    .. versionadded:: Fedora9

``--escrowcert <url>``

    Only relevant if ``--encrypted`` is specified. Load an
    X.509 certificate from ``<url>``. Store the data
    encryption keys of all encrypted volumes created during
    installation, encrypted using the certificate, as files
    in ``/root``.

    .. versionadded:: Fedora12

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified. In
    addition to storing the data encryption keys, generate
    a random passphrase and add it to all encrypted volumes
    created during installation. Then store the passphrase,
    encrypted using the certificate specified by
    ``--escrowcert``, as files in ``/root`` (one file for
    each encrypted volume).

    .. versionadded:: Fedora12

``--nolvm``

    Don't use LVM when partitioning.

    .. versionadded:: Fedora16

    .. versionchanged:: Fedora17

    The same as ``--type=plain``

``--type TYPE``

    Select automatic partitioning scheme. Must be one of the
    following: ['lvm', 'btrfs', 'partition', 'thinp', 'plain']. Plain means regular
    partitions with no btrfs or lvm.

    .. versionadded:: Fedora17

    .. versionchanged:: Fedora20

    Partitioning scheme 'thinp' was added.

``--cipher CIPHER``

    Only relevant if ``--encrypted`` is specified. Specifies
    which encryption algorithm should be used to encrypt the
    filesystem.

    .. versionadded:: Fedora18

``--fstype FSTYPE``

    Use the specified filesystem type on the partitions.
    Note that it cannot be used with --type=btrfs since
    btrfs is both a partition scheme and a filesystem. eg.
    --fstype=ext4.

    .. versionadded:: Fedora21

autostep
--------

::

    autostep [--autoscreenshot]

.. versionadded:: Fedora3

Kickstart installs normally skip unnecessary screens.
This makes the installer step through every screen,
displaying each briefly.

This is mostly used for debugging.

optional arguments:

``--autoscreenshot``

    Take a screenshot at every step during installation and
    copy the images over to /root/anaconda-screenshots after
    installation is complete. This is most useful for
    documentation.

    .. versionadded:: Fedora3

bootloader
----------

::

    bootloader [--append APPENDLINE] [--location {mbr,partition,none,boot}]
           [--password PASSWORD] [--upgrade] [--driveorder DRIVEORDER]
           [--timeout TIMEOUT] [--default DEFAULT] [--iscrypted]
           [--md5pass _MD5PASS] [--boot-drive BOOTDRIVE] [--leavebootorder]
           [--extlinux] [--disabled] [--nombr]

.. versionadded:: Fedora3

This required command specifies how the boot loader
should be installed.

There must be a biosboot partition for the bootloader
to be installed successfully onto a disk that contains
a GPT/GUID partition table, which includes disks
initialized by anaconda. This partition may be created
with the kickstart command
``part biosboot --fstype=biosboot --size=1``. However,
in the case that a disk has an existing biosboot
partition, adding a ``part biosboot`` option is
unnecessary.

optional arguments:

``--append APPENDLINE``

    Specifies kernel parameters. The default set of bootloader
    arguments is "rhgb quiet". You will get this set of
    arguments regardless of what parameters you pass to
    --append, or if you leave out --append entirely.
    For example::

    ``bootloader --location=mbr --append="hdd=ide-scsi ide=nodma"``

    .. versionadded:: Fedora3

``--linear``

    .. versionadded:: Fedora3

    .. versionremoved:: Fedora4

``--nolinear``

    .. versionadded:: Fedora3

    .. versionremoved:: Fedora4

``--location {mbr,partition,none,boot}``

    Specifies where the boot record is written. Valid values
    are the following: mbr (the default), partition
    (installs the boot loader on the first sector of the
    partition containing the kernel), or none
    (do not install the boot loader).

    .. versionadded:: Fedora3

``--password PASSWORD``

    If using GRUB, sets the GRUB boot loader password. This
    should be used to restrict access to the GRUB shell,
    where arbitrary kernel options can be passed.

    .. versionadded:: Fedora3

``--upgrade``

    .. versionadded:: Fedora3

``--useLilo``

    .. versionadded:: Fedora3

    .. versionremoved:: Fedora4

``--driveorder DRIVEORDER``

    .. versionadded:: Fedora3

``--timeout TIMEOUT``

    Specify the number of seconds before the bootloader
    times out and boots the default option.

    .. versionadded:: Fedora8

``--default DEFAULT``

    Sets the default boot image in the bootloader
    configuration.

    .. versionadded:: Fedora8

``--lba32``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora12

    .. versionremoved:: Fedora14

``--iscrypted``

    If given, the password specified by ``--password=`` is
    already encrypted and should be passed to the bootloader
    configuration without additional modification.

    .. versionadded:: Fedora15

``--md5pass _MD5PASS``

    If using GRUB, similar to ``--password=`` except the
    password should already be encrypted.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora15

    If using GRUB, similar to ``--password=`` except the password
    should already be encrypted.

``--boot-drive BOOTDRIVE``

    Specifies which drive the bootloader should be written
    to and thus, which drive the computer will boot from.

    .. versionadded:: Fedora17

``--leavebootorder``

    On EFI or ISeries/PSeries machines, this option prevents
    the installer from making changes to the existing list
    of bootable images.

    .. versionadded:: Fedora18

``--extlinux``

    Use the extlinux bootloader instead of GRUB. This option
    only works on machines that are supported by extlinux.

    .. versionadded:: Fedora19

``--disabled``

    Do not install the boot loader.

    .. versionadded:: Fedora21

``--nombr``

    .. versionadded:: Fedora21

btrfs
-----

::

    btrfs [--noformat] [--useexisting] [--label LABEL] [--data DATALEVEL]
      [--metadata METADATALEVEL] [--subvol] [--parent PARENT] [--name NAME]
      [--mkfsoptions MKFSOPTS]

.. versionadded:: Fedora17

Defines a BTRFS volume or subvolume. This command
is of the form:

``btrfs <mntpoint> --data=<level> --metadata=<level> --label=<label> <partitions*>``

for volumes and of the form:

``btrfs <mntpoint> --subvol --name=<path> <parent>``

for subvolumes.

The ``<partitions*>`` (which denotes that multiple
partitions can be listed) lists the BTRFS identifiers
to add to the BTRFS volume. For subvolumes, should be
the identifier of the subvolume's parent volume.

``<mntpoint>``

Location where the file system is mounted.

optional arguments:

``--noformat``

    Use an existing BTRFS volume (or subvolume) and do not
    reformat the filesystem.

    .. versionadded:: Fedora17

``--useexisting``

    Same as ``--noformat``.

    .. versionadded:: Fedora17

``--label LABEL``

    Specify the label to give to the filesystem to be made.
    If the given label is already in use by another
    filesystem, a new label will be created. This option
    has no meaning for subvolumes.

    .. versionadded:: Fedora17

``--data DATALEVEL``

    RAID level to use (0, 1, 10) for filesystem data. Optional.
    This option has no meaning for subvolumes.

    .. versionadded:: Fedora17

``--metadata METADATALEVEL``

    RAID level to use (0, 1, 10) for filesystem/volume
    metadata. Optional. This option has no meaning for
    subvolumes.

    .. versionadded:: Fedora17

``--subvol``

    Create BTRFS subvolume.

    .. versionadded:: Fedora17

``--parent PARENT``

    .. versionadded:: Fedora17

``--name NAME``

    Subvolume name.

    .. versionadded:: Fedora17

``--mkfsoptions MKFSOPTS``

    Specifies additional parameters to be passed to the
    program that makes a filesystem on this partition. No
    processing is done on the list of arguments, so they
    must be supplied in a format that can be passed directly
    to the mkfs program. This means multiple options should
    be comma-separated or surrounded by double quotes,
    depending on the filesystem.

    .. versionadded:: Fedora23

The following example shows how to create a BTRFS
volume from member partitions on three disks with
subvolumes for root and home. The main volume is not
mounted or used directly in this example -- only
the root and home subvolumes::

    part btrfs.01 --size=6000 --ondisk=sda
    part btrfs.02 --size=6000 --ondisk=sdb
    part btrfs.03 --size=6000 --ondisk=sdc

    btrfs none --data=0 --metadata=1 --label=f17 btrfs.01 btrfs.02 btrfs.03
    btrfs / --subvol --name=root LABEL=f17
    btrfs /home --subvol --name=home f17

cdrom
-----

::

    cdrom

.. versionadded:: Fedora3

Install from the first CD-ROM/DVD drive on the
system.

clearpart
---------

::

    clearpart [--all] [--drives DRIVES] [--initlabel] [--linux] [--none]
          [--list DEVICES] [--disklabel DISKLABEL]

.. versionadded:: Fedora3

Removes partitions from the system, prior to creation
of new partitions. By default, no partitions are
removed.

If the clearpart command is used, then the ``--onpart``
command cannot be used on a logical partition.

optional arguments:

``--all``

    Erases all partitions from the system.

    .. versionadded:: Fedora3

``--drives DRIVES``

    Specifies which drives to clear partitions from. For
    example, the following clears the partitions on the
    first two drives on the primary IDE controller::

    ``clearpart --all --drives=sda,sdb``

    .. versionadded:: Fedora3

``--initlabel``

    Initializes the disk label to the default for your
    architecture (for example msdos for x86 and gpt for
    Itanium). This is only meaningful in combination with
    the '--all' option.

    .. versionadded:: Fedora3

``--linux``

    Erases all Linux partitions.

    .. versionadded:: Fedora3

``--none``

    Do not remove any partitions. This is the default

    .. versionadded:: Fedora3

``--list DEVICES``

    Specifies which partitions to clear. If given, this
    supersedes any of the ``--all`` and ``--linux``
    options. This can be across different drives::

    ``clearpart --list=sda2,sda3,sdb1``

    .. versionadded:: Fedora17

``--disklabel DISKLABEL``

    Set the default disklabel to use. Only disklabels
    supported for the platform will be accepted. eg. msdos
    and gpt for x86_64 but not dasd.

    .. versionadded:: Fedora21

graphical or text or cmdline
----------------------------

::

    graphical|text|cmdline

.. versionadded:: Fedora3

Controls which display mode will be used during
installation. If ``cmdline`` is chosen all required
installation options must be configured via kickstart
otherwise the installation will fail.

device
------

::

    device [--opts MODULEOPTS]

.. versionadded:: Fedora3

optional arguments:

``--opts MODULEOPTS``

    .. versionadded:: Fedora3

deviceprobe
-----------

::

    deviceprobe

.. versionadded:: Fedora3

dmraid
------

::

    dmraid --name NAME --dev DEVICES

.. versionadded:: Fedora6

optional arguments:

``--name NAME``

    .. versionadded:: Fedora6

``--dev DEVICES``

    .. versionadded:: Fedora6

driverdisk
----------

::

    driverdisk [--source SOURCE] [--biospart BIOSPART] [partition [partition ...]]

.. versionadded:: Fedora3

Driver diskettes can be used during kickstart
installations. You need to copy the driver disk's
contents to the root directory of a partition on
the system's hard drive. Then you need to use the
driverdisk command to tell the installation program
where to look for the driver disk.

positional arguments:

``partition``

    Partition containing the driver disk.

    .. versionadded:: Fedora3

optional arguments:

``--source SOURCE``

    Specify a URL for the driver disk. NFS locations can be
    given with ``nfs:host:/path/to/img``.

    .. versionadded:: Fedora3

``--biospart BIOSPART``

    BIOS partition containing the driver disk (such as 82p2).

    .. versionadded:: Fedora4

``--type TYPE``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora12

    .. versionremoved:: Fedora14

eula
----

::

    eula [--agreed]

.. versionadded:: Fedora20

Automatically accept Red Hat's EULA

optional arguments:

``--agreed, --agree, --accepted, --accept``

    Accept the EULA. This is mandatory option!

    .. versionadded:: Fedora20

fcoe
----

::

    fcoe --nic NIC [--dcb] [--autovlan]

.. versionadded:: Fedora12

optional arguments:

``--nic NIC``

    .. versionadded:: Fedora12

``--dcb``

    .. versionadded:: Fedora13

``--autovlan``

    .. versionadded:: RedHatEnterpriseLinux7

firewall
--------

::

    firewall [--disable] [--enable] [--port PORTS] [--trust TRUSTS]
         [--service SERVICES] [--ftp] [--http] [--smtp] [--ssh]
         [--remove-service REMOVE_SERVICES]

.. versionadded:: Fedora3

This option corresponds to the Firewall Configuration
screen in the installation program

optional arguments:

``--disable, --disabled``

    Do not configure any iptables rules.

    .. versionadded:: Fedora3

``--enable, --enabled``

    Reject incoming connections that are not in response
    to outbound requests, such as DNS replies or DHCP
    requests. If access to services running on this machine
    is needed, you can choose to allow specific services
    through the firewall.

    .. versionadded:: Fedora3

``--high HIGH``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora3

    .. versionremoved:: Fedora9

``--medium MEDIUM``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora3

    .. versionremoved:: Fedora9

``--port PORTS``

    You can specify that ports be allowed through the firewall
    using the port:protocol format. You can also specify ports
    numerically. Multiple ports can be combined into one option
    as long as they are separated by commas. For example::

    ``firewall --port=imap:tcp,1234:ucp,47``

    .. versionadded:: Fedora3

``--trust TRUSTS``

    Listing a device here, such as eth0, allows all traffic
    coming from that device to go through the firewall. To
    list more than one device, use --trust eth0 --trust eth1.
    Do NOT use a comma-separated format such as
    --trust eth0, eth1.

    .. versionadded:: Fedora3

``--service SERVICES``

    This option provides a higher-level way to allow services
    through the firewall. Some services (like cups, avahi, etc.)
    require multiple ports to be open or other special
    configuration in order for the service to work. You could
    specify each individual service with the ``--port`` option,
    or specify ``--service=`` and open them all at once.

    Valid options are anything recognized by the
    firewall-cmd program in the firewalld package.
    If firewalld is running::

    ``firewall-cmd --get-services``

    will provide a list of known service names.

    .. versionadded:: Fedora10

``--ftp``

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora10

``--http``

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora10

``--smtp``

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora10

``--ssh``

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora10

``--telnet TELNET``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora10

    .. versionremoved:: Fedora14

``--remove-service REMOVE_SERVICES``

    .. versionadded:: Fedora20

firstboot
---------

::

    firstboot [--disable] [--enable] [--reconfig]

.. versionadded:: Fedora3

Determine whether the Setup Agent starts the first
time the system is booted. If enabled, the
``initial-setup`` package must be installed. If not
specified, the setup agent (initial-setup) is disabled
by default.

optional arguments:

``--disable, --disabled``

    The Setup Agent is not started the first time the
    system boots.

    .. versionadded:: Fedora3

``--enable, --enabled``

    The Setup Agent is started the first time the
    system boots.

    .. versionadded:: Fedora3

``--reconfig``

    Enable the Setup Agent to start at boot time in
    reconfiguration mode. This mode enables the language,
    mouse, keyboard, root password, security level,
    time zone, and networking configuration options in
    addition to the default ones.

    .. versionadded:: Fedora3

group
-----

::

    group --name NAME [--gid GID]

.. versionadded:: Fedora12

Creates a new user group on the system. If a group with the given
name or GID already exists, this command will fail. In addition,
the ``user`` command can be used to create a new group for the
newly created user.

optional arguments:

``--name NAME``

    Provides the name of the new group.

    .. versionadded:: Fedora12

``--gid GID``

    The group's GID. If not provided, this defaults to the
    next available non-system GID.

    .. versionadded:: Fedora12

reboot or poweroff or shutdown or halt
--------------------------------------

::

    reboot|poweroff|shutdown|halt [--eject]

.. versionadded:: Fedora3

``reboot``

Reboot after the installation is complete. Normally,
kickstart displays a message and waits for the user
to press a key before rebooting.

``poweroff``

Turn off the machine after the installation is complete.
Normally, kickstart displays a message and waits for
the user to press a key before rebooting.

``shutdown``

At the end of installation, shut down the machine.
This is the same as the poweroff command. Normally,
kickstart displays a message and waits for the user
to press a key before rebooting.

``halt``

At the end of installation, display a message and wait for the user to
press a key before rebooting. This is the default action.

.. versionchanged:: Fedora18

The 'halt' command was added!

optional arguments:

``--eject``

    Attempt to eject CD or DVD media before rebooting.

    .. versionadded:: Fedora6

harddrive
---------

::

    harddrive [--biospart BIOSPART] [--partition PARTITION] --dir DIR

.. versionadded:: Fedora3

Install from a directory of ISO images on a local drive, which must
be either vfat or ext2. In addition to this directory, you must also
provide the install.img in some way. You can either do this by
booting off the boot.iso or by creating an images/ directory in the
same directory as the ISO images and placing install.img in there.

optional arguments:

``--biospart BIOSPART``

    BIOS partition to install from (such as 82p2).

    .. versionadded:: Fedora3

``--partition PARTITION``

    Partition to install from (such as, sdb2).

    .. versionadded:: Fedora3

``--dir DIR``

    Directory containing both the ISO images and the
    images/install.img. For example::

    ``harddrive --partition=hdb2 --dir=/tmp/install-tree``

    .. versionadded:: Fedora3

ignoredisk
----------

::

    ignoredisk [--drives IGNOREDISK] [--only-use ONLYUSE] [--interactive]

.. versionadded:: Fedora3

Controls anaconda's access to disks attached to the system. By
default, all disks will be available for partitioning. Only one of
the following three options may be used.

optional arguments:

``--drives IGNOREDISK``

    Specifies those disks that anaconda should not touch
    when partitioning, formatting, and clearing.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora8

    This argument is no longer required!

``--only-use ONLYUSE``

    Specifies the opposite - only disks listed here will be
    used during installation.

    .. versionadded:: Fedora8

``--interactive``

    Allow the user manually navigate the advanced storage
    screen.

    .. versionadded:: RedHatEnterpriseLinux6

install
-------

::

    install [--root-device ROOT_DEVICE]

            Install a fresh system. You must specify the type of
            installation from one of cdrom, harddrive, nfs, or url
            (for ftp or http installations).
            The install command and the installation method command
            must be on separate lines.

            Important: before Fedora 20 this command was known as
            install or upgrade but the upgrade part was deprecated!
        

optional arguments:

``--root-device ROOT_DEVICE``

    .. versionadded:: Fedora11

interactive
-----------

::

    interactive

.. versionadded:: Fedora3

.. deprecated:: Fedora14

iscsi
-----

::

    iscsi [--target TARGET] --ipaddr IPADDR [--port PORT] [--user USER]
      [--password PASSWORD] [--reverse-user USER_IN]
      [--reverse-password PASSWORD_IN] [--iface IFACE]

.. versionadded:: Fedora6

Specifies additional iSCSI storage to be attached
during installation. If you use the iscsi parameter,
you must also assign a name to the iSCSI node, using
the iscsiname parameter. The iscsiname parameter
must appear before the iscsi parameter in the
kickstart file.

We recommend that wherever possible you configure
iSCSI storage in the system BIOS or firmware (iBFT
for Intel systems) rather than use the iscsi
parameter. Anaconda automatically detects and uses
disks configured in BIOS or firmware and no special
configuration is necessary in the kickstart file.

If you must use the iscsi parameter, ensure that
networking is activated at the beginning of the
installation, and that the iscsi parameter appears
in the kickstart file before you refer to iSCSI
disks with parameters such as clearpart or
ignoredisk.

optional arguments:

``--target TARGET``

    The target iqn.

    .. versionadded:: Fedora6

``--ipaddr IPADDR``

    The IP address of the target to connect to.

    .. versionadded:: Fedora6

``--port PORT``

    The port number to connect to (default, --port=3260).

    .. versionadded:: Fedora6

``--user USER``

    The username required to authenticate with the target.

    .. versionadded:: Fedora6

``--password PASSWORD``

    The password that corresponds with the username specified
    for the target.

    .. versionadded:: Fedora6

``--reverse-user USER_IN``

    The username required to authenticate with the initiator
    from a target that uses reverse CHAP authentication.

    .. versionadded:: Fedora10

``--reverse-password PASSWORD_IN``

    The password that corresponds with the username
    specified for the initiator.

    .. versionadded:: Fedora10

``--iface IFACE``

    Bind connection to specific network interface instead
    of using the default one determined by network layer.
    Once used, it must be specified for all iscsi commands.

    .. versionadded:: Fedora17

iscsiname
---------

::

    iscsiname <iqn>

.. versionadded:: Fedora6

Assigns an initiator name to the computer. If you use the iscsi
parameter in your kickstart file, this parameter is mandatory, and
you must specify iscsiname in the kickstart file before you specify
iscsi.

positional arguments:

``<iqn>``

    IQN name

    .. versionadded:: Fedora6

key
---

::

    key [--skip]

.. versionadded:: RedHatEnterpriseLinux5

optional arguments:

``--skip``

    .. versionadded:: RedHatEnterpriseLinux5

keyboard
--------

::

    keyboard [--vckeymap VC_KEYMAP] [--xlayouts X_LAYOUTS]
         [--switch SWITCH_OPTIONS]
         [kbd [kbd ...]]

.. versionadded:: Fedora3

This required command sets system keyboard type.

.. versionchanged:: Fedora18

See the documentation of ``--vckeymap`` option and the tip at the end
of this section for a guide how to get values accepted by this command.

Either ``--vckeymap`` or ``--xlayouts`` must be used.

Alternatively, use the older format, ``arg``, which is still supported.
``arg`` can be an X layout or VConsole keymap name.

Missing values will be automatically converted from the given one(s).

positional arguments:

``kbd``

    Keyboard type

    .. versionadded:: Fedora3

optional arguments:

``--vckeymap VC_KEYMAP``

    Specify VConsole keymap that should be used. is a keymap
    name which is the same as the filename under
    /usr/lib/kbd/keymaps/ without the ".map.gz" extension.

    .. versionadded:: Fedora18

``--xlayouts X_LAYOUTS``

    Specify a list of X layouts that should be used
    (comma-separated list without spaces). Accepts the same
    values as setxkbmap(1), but uses either the layout format
    (such as cz) or the 'layout (variant)' format (such as
    'cz (qwerty)'). For example::

    ``keyboard --xlayouts=cz,'cz (qwerty)'`

    .. versionadded:: Fedora18

``--switch SWITCH_OPTIONS``

    Specify a list of layout switching options that should
    be used (comma-separated list without spaces). Accepts
    the same values as setxkbmap(1) for layout switching.
    For example::

    ``keyboard --xlayouts=cz,'cz (qwerty)' --switch=grp:alt_shift_toggle``

    .. versionadded:: Fedora18

*If you know only the description of the layout (e.g. Czech (qwerty)),
you can use http://vpodzime.fedorapeople.org/layouts_list.py to list
all available layouts and find the one you want to use. The string in
square brackets is the valid layout specification as Anaconda accepts
it. The same goes for switching options and
http://vpodzime.fedorapeople.org/switching_list.py*

lang
----

::

    lang [--addsupport LOCALE] <lang>

.. versionadded:: Fedora3

This required command sets the language to use during installation
and the default language to use on the installed system to ``<id>``.
This can be the same as any recognized setting for the $LANG
environment variable, though not all languages are supported during
installation.

Certain languages (mainly Chinese, Japanese, Korean, and Indic
languages) are not supported during text mode installation. If one
of these languages is specified using the lang command, installation
will continue in English though the running system will have the
specified langauge by default.

The file /usr/share/system-config-language/locale-list provides a
list the valid language codes in the first column of each line and
is part of the system-config-languages package.

positional arguments:

``<lang>``

    Language ID.

    .. versionadded:: Fedora3

optional arguments:

``--addsupport LOCALE``

    Install the support packages for the given locales,
    specified as a comma-separated list. Each locale may be
    specified in the same ways as the primary language may
    be, as described above.

    .. versionadded:: Fedora19

langsupport
-----------

::

    langsupport [--default DEFLANG]

.. versionadded:: Fedora3

.. deprecated:: Fedora5

optional arguments:

``--default DEFLANG``

    .. versionadded:: Fedora3

lilo
----

::

    lilo [--append APPENDLINE] [--linear] [--nolinear]
     [--location {mbr,partition,none,boot}] [--lba32] [--password PASSWORD]
     [--md5pass MD5PASS] [--upgrade] [--useLilo] [--driveorder DRIVEORDER]

.. versionadded:: Fedora3

This required command specifies how the boot loader
should be installed.

There must be a biosboot partition for the bootloader
to be installed successfully onto a disk that contains
a GPT/GUID partition table, which includes disks
initialized by anaconda. This partition may be created
with the kickstart command
``part biosboot --fstype=biosboot --size=1``. However,
in the case that a disk has an existing biosboot
partition, adding a ``part biosboot`` option is
unnecessary.

optional arguments:

``--append APPENDLINE``

    Specifies kernel parameters. The default set of bootloader
    arguments is "rhgb quiet". You will get this set of
    arguments regardless of what parameters you pass to
    --append, or if you leave out --append entirely.
    For example::

    ``bootloader --location=mbr --append="hdd=ide-scsi ide=nodma"``

    .. versionadded:: Fedora3

``--linear``

    .. versionadded:: Fedora3

``--nolinear``

    .. versionadded:: Fedora3

``--location {mbr,partition,none,boot}``

    Specifies where the boot record is written. Valid values
    are the following: mbr (the default), partition
    (installs the boot loader on the first sector of the
    partition containing the kernel), or none
    (do not install the boot loader).

    .. versionadded:: Fedora3

``--lba32``

    .. versionadded:: Fedora3

``--password PASSWORD``

    If using GRUB, sets the GRUB boot loader password. This
    should be used to restrict access to the GRUB shell,
    where arbitrary kernel options can be passed.

    .. versionadded:: Fedora3

``--md5pass MD5PASS``

    If using GRUB, similar to ``--password=`` except the
    password should already be encrypted.

    .. versionadded:: Fedora3

``--upgrade``

    .. versionadded:: Fedora3

``--useLilo``

    .. versionadded:: Fedora3

``--driveorder DRIVEORDER``

    .. versionadded:: Fedora3

lilocheck
---------

::

    lilocheck

.. versionadded:: Fedora3

liveimg
-------

::

    liveimg --url <url> [--proxy <proxyurl>] [--noverifyssl] [--checksum <sha256>]

.. versionadded:: Fedora19

Install a disk image instead of packages. The image can be the
squashfs.img from a Live iso, or any filesystem mountable by the
install media (eg. ext4). Anaconda expects the image to contain
utilities it needs to complete the system install so the best way to
create one is to use livemedia-creator to make the disk image. If
the image contains /LiveOS/\*.img (this is how squashfs.img is
structured) the first \*.img file inside LiveOS will be mounted and
used to install the target system. The URL may also point to a
tarfile of the root filesystem. The file must end in .tar, .tbz,
.tgz, .txz, .tar.bz2, tar.gz, tar.xz

optional arguments:

``--url <url>``

    The URL to install from. http, https, ftp and file are
    supported.

    .. versionadded:: Fedora19

``--proxy <proxyurl>``

    Specify an HTTP/HTTPS/FTP proxy to use while performing
    the install. The various parts of the argument act like
    you would expect. Syntax is::

    ``--proxy=[protocol://][username[:password]@]host[:port]``

    .. versionadded:: Fedora19

``--noverifyssl``

    For a tree on a HTTPS server do not check the server's
    certificate with what well-known CA validate and do not
    check the server's hostname matches the certificate's
    domain name.

    .. versionadded:: Fedora19

``--checksum <sha256>``

    Optional sha256 checksum of the image file

    .. versionadded:: Fedora19

logging
-------

::

    logging [--host HOST] [--port PORT]
        [--level {debug,info,warning,error,critical}]

.. versionadded:: Fedora6

This command controls the error logging of anaconda during
installation. It has no effect on the installed system.

optional arguments:

``--host HOST``

    Send logging information to the given remote host, which must be
    running a syslogd process configured to accept remote logging.

    .. versionadded:: Fedora6

``--port PORT``

    If the remote syslogd process uses a port other than the default, it
    may be specified with this option.

    .. versionadded:: Fedora6

``--level {debug,info,warning,error,critical}``

    Specify the minimum level of messages that appear on tty3.
    All messages will still be sent to the log file regardless
    of this level, however.

    .. versionadded:: Fedora6

logvol
------

::

    logvol [--fstype FSTYPE] [--grow] [--maxsize MAXSIZEMB] --name NAME
       [--noformat] [--percent PERCENT] [--recommended] [--size SIZE]
       [--useexisting] --vgname VGNAME [--fsoptions FSOPTS]
       [--fsprofile FSPROFILE] [--encrypted] [--passphrase PASSPHRASE]
       [--escrowcert <url>] [--backuppassphrase] [--label LABEL] [--resize]
       [--hibernation] [--cipher CIPHER] [--thinpool] [--thin]
       [--poolname POOL_NAME] [--chunksize CHUNK_SIZE]
       [--metadatasize METADATA_SIZE] [--profile PROFILE]
       [--mkfsoptions MKFSOPTS]
       <mntpoint>

.. versionadded:: Fedora3

Create a logical volume for Logical Volume Management
(LVM).

positional arguments:

``<mntpoint>``

    Mountpoint for this logical volume or 'none'.

    .. versionadded:: Fedora3

optional arguments:

``--fstype FSTYPE``

    Sets the file system type for the logical volume. Valid
    values include ext4, ext3, ext2, btrfs, swap, and vfat.
    Other filesystems may be valid depending on command line
    arguments passed to Anaconda to enable other filesystems.

    .. versionadded:: Fedora3

``--grow``

    Tells the logical volume to grow to fill available space
    (if any), or up to the maximum size setting. Note that
    --grow is not supported for logical volumes containing
    a RAID volume on top of them.

    .. versionadded:: Fedora3

``--maxsize MAXSIZEMB``

    The maximum size in MiB the logical volume may grow to.
    Specify an integer value here, and do not append any
    units.  This option is only relevant if ``--grow`` is
    specified as well.

    .. versionadded:: Fedora3

``--name NAME``

    The name of this logical volume.

    .. versionadded:: Fedora3

``--noformat``

    Use an existing logical volume and do not format it.

    .. versionadded:: Fedora3

``--percent PERCENT``

    Specify the size of the logical volume as a percentage
    of available space in the volume group. Without the above
    --grow option, this may not work.

    .. versionadded:: Fedora3

``--recommended``

    Determine the size of the logical volume automatically.

    .. versionadded:: Fedora3

``--size SIZE``

    Size of this logical volume.

    .. versionadded:: Fedora3

``--useexisting``

    Use an existing logical volume and reformat it.

    .. versionadded:: Fedora3

``--vgname VGNAME``

    Name of the Volume Group this logical volume belongs to.

    .. versionadded:: Fedora3

``--fsoptions FSOPTS``

    Specifies a free form string of options to be used when
    mounting the filesystem. This string will be copied into
    the /etc/fstab file of the installed system and should
    be enclosed in quotes.

    .. versionadded:: Fedora4

``--bytes-per-inode BYTES_PER_INODE``

    Specify the bytes/inode ratio.

    .. versionadded:: Fedora4

    .. deprecated:: Fedora9

    .. versionremoved:: Fedora14

``--fsprofile FSPROFILE``

    Specifies a usage type to be passed to the program that
    makes a filesystem on this partition. A usage type
    defines a variety of tuning parameters to be used when
    making a filesystem. For this option to work, the
    filesystem must support the concept of usage types and
    there must be a configuration file that lists valid
    types. For ext2/3/4, this configuration file is
    ``/etc/mke2fs.conf``.

    .. versionadded:: Fedora9

``--encrypted``

    Specify that this logical volume should be encrypted.

    .. versionadded:: Fedora9

``--passphrase PASSPHRASE``

    Specify the passphrase to use when encrypting this
    logical volume. Without the above ``--encrypted``
    option, this option does nothing. If no passphrase is
    specified, the default system-wide one is used, or the
    installer will stop and prompt if there is no default.

    .. versionadded:: Fedora9

``--escrowcert <url>``

    Load an X.509 certificate from ``<url>``. Store the data
    encryption key of this logical volume, encrypted using
    the certificate, as a file in ``/root``. Only relevant
    if ``--encrypted`` is specified as well.

    .. versionadded:: Fedora12

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well.
    In addition to storing the data encryption key, generate
    a random passphrase and add it to this logical volume.
    Then store the passphrase, encrypted using the certificate
    specified by ``--escrowcert``, as a file in ``/root``. If
    more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

    .. versionadded:: Fedora12

``--label LABEL``

    Specify the label to give to the filesystem to be made.
    If the given label is already in use by another
    filesystem, a new label will be created.

    .. versionadded:: Fedora15

``--resize``

    Attempt to resize this logical volume to the size given
    by ``--size=``. This option must be used with
    ``--useexisting --size=``, or an error will be raised.

    .. versionadded:: Fedora17

``--hibernation``

    This option can be used to automatically determine the
    size of the swap partition big enough for hibernation.

    .. versionadded:: Fedora18

``--cipher CIPHER``

    Only relevant if ``--encrypted`` is specified. Specifies
    which encryption algorithm should be used to encrypt the
    filesystem.

    .. versionadded:: Fedora18

``--thinpool``

    Create a thin pool logical volume. Use a mountpoint
    of 'none'.

    .. versionadded:: Fedora20

``--thin``

    Create a thin logical volume. Requires ``--poolname``.

    .. versionadded:: Fedora20

``--poolname POOL_NAME``

    Specify the name of the thin pool in which to create a
    thin logical volume. Requires ``--thin``.

    .. versionadded:: Fedora20

``--chunksize CHUNK_SIZE``

    Specify the chunk size (in KiB) for a new thin pool
    device.

    .. versionadded:: Fedora20

``--metadatasize METADATA_SIZE``

    Specify the metadata area size (in MiB) for a new thin
    pool device.

    .. versionadded:: Fedora20

``--profile PROFILE``

    Specify an LVM profile for the thin pool (see lvm(8),
    standard profiles are 'default' and 'thin-performance'
    defined in the /etc/lvm/profile/ directory).

    .. versionadded:: Fedora21

``--mkfsoptions MKFSOPTS``

    Specifies additional parameters to be passed to the
    program that makes a filesystem on this partition. No
    processing is done on the list of arguments, so they
    must be supplied in a format that can be passed directly
    to the mkfs program.  This means multiple options should
    be comma-separated or surrounded by double quotes,
    depending on the filesystem.

    .. versionadded:: RedHatEnterpriseLinux7

Create the partition first, create the logical volume
group, and then create the logical volume. For example::

    part pv.01 --size 3000
    volgroup myvg pv.01
    logvol / --vgname=myvg --size=2000 --name=rootvol

mediacheck
----------

::

    mediacheck

.. versionadded:: Fedora4

If given, this will force anaconda to run mediacheck
on the installation media. This command requires that
installs be attended, so it is disabled by default.

method
------

::

    method

.. versionadded:: Fedora3

monitor
-------

::

    monitor [--hsync HSYNC] [--monitor MONITOR] [--vsync VSYNC] [--noprobe]

.. versionadded:: Fedora3

If the monitor command is not given, anaconda will
use X to automatically detect your monitor settings.
Please try this before manually configuring your
monitor.

.. deprecated:: Fedora10

optional arguments:

``--hsync HSYNC``

    Specifies the horizontal sync frequency of the monitor.

    .. versionadded:: Fedora3

``--monitor MONITOR``

    Use specified monitor; monitor name should be from the
    list of monitors in /usr/share/hwdata/MonitorsDB from
    the hwdata package. The list of monitors can also be
    found on the X Configuration screen of the
    Kickstart Configurator. This is ignored if --hsync or
    --vsync is provided. If no monitor information is
    provided, the installation program tries to probe for
    it automatically.

    .. versionadded:: Fedora3

``--vsync VSYNC``

    Specifies the vertical sync frequency of the monitor.

    .. versionadded:: Fedora3

``--noprobe``

    Do not probe the monitor.

    .. versionadded:: Fedora6

mouse
-----

::

    mouse [--device DEVICE] [--emulthree]

.. versionadded:: RedHatEnterpriseLinux3

.. deprecated: Fedora3

optional arguments:

``--device DEVICE``

    .. versionadded:: RedHatEnterpriseLinux3

``--emulthree``

    .. versionadded:: RedHatEnterpriseLinux3

multipath
---------

::

    multipath --name NAME --device DEVICE --rule RULE

.. versionadded:: Fedora6

optional arguments:

``--name NAME``

    .. versionadded:: Fedora6

``--device DEVICE``

    .. versionadded:: Fedora6

``--rule RULE``

    .. versionadded:: Fedora6

network
-------

::

    network [--bootproto {dhcp,bootp,static,query,ibft}] [--dhcpclass DHCPCLASS]
        [--device DEVICE] [--essid ESSID] [--ethtool ETHTOOL]
        [--gateway GATEWAY] [--hostname HOSTNAME] [--ip IP] [--mtu MTU]
        [--nameserver NAMESERVER] [--netmask NETMASK] [--nodns]
        [--onboot ONBOOT] [--wepkey WEPKEY] [--notksdevice] [--noipv4]
        [--noipv6] [--ipv6 IPV6] [--activate] [--nodefroute] [--wpakey WPAKEY]
        [--bondslaves BONDSLAVES] [--bondopts BONDOPTS] [--vlanid VLANID]
        [--ipv6gateway IPV6GATEWAY] [--teamslaves TEAMSLAVES]
        [--teamconfig TEAMCONFIG] [--interfacename INTERFACENAME]
        [--bridgeslaves BRIDGESLAVES] [--bridgeopts BRIDGEOPTS]
        [--no-activate]

.. versionadded:: Fedora3

Configures network information for target system
and activates network devices in installer
environment. Device of the first network command is
activated if network is required, e.g. in case of
network installation or using vnc. Activation of the
device can be also explicitly required by
``--activate`` option. If the device has already
been activated to get kickstart file (e.g. using
configuration provided with boot options or entered
in loader UI) it is re-activated with configuration
from kickstart file.

The device given by the first network command is
activated also in case of non-network installs, and
this device is not re-activated using kickstart
configuration.

optional arguments:

``--bootproto {dhcp,bootp,static,query,ibft}``

    The default setting is dhcp. bootp and dhcp are treated
    the same. The DHCP method uses a DHCP server system to
    obtain its networking configuration. As you might guess,
    the BOOTP method is similar, requiring a BOOTP server to
    supply the networking configuration.

    The static method requires that you enter all the
    required networking information in the kickstart file.
    As the name implies, this information is static and will
    be used during and after the installation. The line for
    static networking is more complex, as you must include
    all network configuration information **on one line**.
    You must specify the IP address, netmask, gateway, and
    nameserver. For example::

    ``network --device=link --bootproto=static --ip=10.0.2.15 --netmask=255.255.255.0 --gateway=10.0.2.254 --nameserver=10.0.2.1``

    If you use the static method, be aware of the following
    restriction:

    All static networking configuration information must be
    specified on one line; you cannot wrap lines using a
    backslash, for example.

    ``ibft`` setting is for reading the configuration from
    iBFT table.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora9

    The 'query' value was added.

    .. versionchanged:: Fedora16

    The 'ibft' value was added.

``--dhcpclass DHCPCLASS``

    The DHCP class.

    .. versionadded:: Fedora3

``--device DEVICE``

    Specifies device to be configured and/or activated with
    the network command. The device can be specified in the
    same ways as
    `ksdevice <https://rhinstaller.github.io/anaconda/boot-options.html#ksdevice>`__
    boot option. For example::

    ``network --bootproto=dhcp --device=eth0``

    .. versionadded:: Fedora3

``--essid ESSID``

    The network ID for wireless networks.

    .. versionadded:: Fedora3

``--ethtool ETHTOOL``

    Specifies additional low-level settings for the network
    device which will be passed to the ethtool program.

    .. versionadded:: Fedora3

``--gateway GATEWAY``

    Default gateway, as an IPv4 or IPv6 address.

    .. versionadded:: Fedora3

``--hostname HOSTNAME``

    Hostname for the installed system.

    .. versionadded:: Fedora3

``--ip IP``

    IP address for the interface.

    .. versionadded:: Fedora3

``--mtu MTU``

    The MTU of the device.

    .. versionadded:: Fedora3

``--nameserver NAMESERVER``

    Primary nameserver, as an IP address. Multiple
    nameservers must be comma separated.

    .. versionadded:: Fedora3

``--netmask NETMASK``

    Netmask for the installed system.

    .. versionadded:: Fedora3

``--nodns``

    Do not configure any DNS server.

    .. versionadded:: Fedora3

``--onboot ONBOOT``

    Whether or not to enable the device a boot time.

    .. versionadded:: Fedora3

``--wepkey WEPKEY``

    The WEP encryption key for wireless networks.

    .. versionadded:: Fedora3

``--notksdevice``

    This network device is not used for kickstart.

    .. versionadded:: Fedora4

``--noipv4``

    Disable IPv4 on this device.

    .. versionadded:: Fedora6

``--noipv6``

    Disable IPv6 on this device.

    .. versionadded:: Fedora6

``--ipv6 IPV6``

    IPv6 address for the interface. This can be the static
    address in form ``<IPv6 address>[/<prefix length>]``,
    e.g. 3ffe:ffff:0:1::1/128 (if prefix is omitted 64 is
    assumed), "auto" for address assignment based on automatic
    neighbor discovery, or "dhcp" to use the DHCPv6 protocol.

    .. versionadded:: Fedora8

``--activate``

    As noted above, using this option ensures any matching
    devices beyond the first will also be activated.

    .. versionadded:: Fedora16

``--nodefroute``

    Prevents grabbing of the default route by the device.
    It can be useful when activating additional devices in
    installer using ``--activate`` option.

    .. versionadded:: Fedora16

``--wpakey WPAKEY``

    The WPA encryption key for wireless networks.

    .. versionadded:: Fedora16

``--bondslaves BONDSLAVES``

    Bonded device with name specified by ``--device`` option
    will be created using slaves specified in this option.
    Example::

    ``--bondslaves=eth0,eth1``.

    .. versionadded:: Fedora19

``--bondopts BONDOPTS``

    A comma-separated list of optional parameters for bonded
    interface specified by ``--bondslaves`` and ``--device``
    options. Example::

    ``--bondopts=mode=active-backup,primary=eth1``

    If an option itself contains comma as separator use
    semicolon to separate the options.

    .. versionadded:: Fedora19

``--vlanid VLANID``

    Id (802.1q tag) of vlan device to be created using parent
    device specified by ``--device`` option. For example::

    ``network --device=eth0 --vlanid=171``

    will create vlan device ``eth0.171``.

    .. versionadded:: Fedora19

``--ipv6gateway IPV6GATEWAY``

    Address of IPv6 gateway.

    .. versionadded:: Fedora19

``--teamslaves TEAMSLAVES``

    Team device with name specified by ``--device`` option
    will be created using slaves specified in this option.
    Slaves are separated by comma. A slave can be followed
    by its configuration which is a single-quoted json format
    string with double qoutes escaped by ``''`` character.
    Example::

    ``--teamslaves="p3p1'{"prio": -10, "sticky": true}',p3p2'{"prio": 100}'"``.

    See also ``--teamconfig`` option.

    .. versionadded:: Fedora20

``--teamconfig TEAMCONFIG``

    Double-quoted team device configuration which is a json
    format string with double quotes escaped with ``''``
    character. The device name is specified by ``--device``
    option and its slaves and their configuration by
    ``--teamslaves`` option. Example::

    ``network --device team0 --activate --bootproto static --ip=10.34.102.222 --netmask=255.255.255.0 --gateway=10.34.102.254 --nameserver=10.34.39.2 --teamslaves="p3p1'{"prio": -10, "sticky": true}',p3p2'{"prio": 100}'" --teamconfig="{"runner": {"name": "activebackup"}}"``

    .. versionadded:: Fedora20

``--interfacename INTERFACENAME``

    .. versionadded:: Fedora21

``--bridgeslaves BRIDGESLAVES``

    .. versionadded:: RedHatEnterpriseLinux7

``--bridgeopts BRIDGEOPTS``

    .. versionadded:: RedHatEnterpriseLinux7

``--no-activate``

    Use this option with first network command to prevent
    activation of the device in istaller environment

    .. versionadded:: RedHatEnterpriseLinux7

nfs
---

::

    nfs --server <hostname> --dir <directory> [--opts <options>]

.. versionadded:: Fedora3

Install from the NFS server specified. This can
either be an exploded installation tree or a
directory of ISO images. In the latter case, the
install.img must also be provided subject to the
same rules as with the harddrive installation
method described above.

optional arguments:

``--server <hostname>``

    Server from which to install (hostname or IP).

    .. versionadded:: Fedora3

``--dir <directory>``

    Directory containing the Packages/ directory of the
    installation tree. If doing an ISO install, this
    directory must also contain images/install.img.

    .. versionadded:: Fedora3

``--opts <options>``

    Mount options to use for mounting the NFS export. Any
    options that can be specified in /etc/fstab for an NFS
    mount are allowed. The options are listed in the nfs(5)
    man page. Multiple options are separated with a comma.

    .. versionadded:: Fedora6

ostreesetup
-----------

::

    ostreesetup --osname OSNAME [--remote REMOTE] --url URL --ref REF [--nogpg]

.. versionadded:: Fedora21

Used for OSTree installations. See
https://wiki.gnome.org/action/show/Projects/OSTree
for more information about OSTree.

optional arguments:

``--osname OSNAME``

    Management root for OS installation.

    .. versionadded:: Fedora21

``--remote REMOTE``

    Management root for OS installation.

    .. versionadded:: Fedora21

``--url URL``

    Repository URL.

    .. versionadded:: Fedora21

``--ref REF``

    Name of branch inside the repository.

    .. versionadded:: Fedora21

``--nogpg``

    Disable GPG key verification.

    .. versionadded:: Fedora21

part or partition
-----------------

::

    part|partition [--active] [--asprimary] [--fstype FSTYPE] [--grow]
               [--maxsize MAXSIZEMB] [--noformat] [--onbiosdisk ONBIOSDISK]
               [--ondisk DISK] [--onpart ONPART] [--recommended] [--size SIZE]
               [--fsoptions FSOPTS] [--label LABEL] [--fsprofile FSPROFILE]
               [--encrypted] [--passphrase PASSPHRASE] [--escrowcert <url>]
               [--backuppassphrase] [--resize] [--hibernation]
               [--cipher CIPHER] [--mkfsoptions MKFSOPTS]
               <mntpoint>

.. versionadded:: Fedora3

Creates a partition on the system. This command is
required. All partitions created will be formatted
as part of the installation process unless
``--noformat`` and ``--onpart`` are used.

positional arguments:

``<mntpoint>``

    The ``<mntpoint>`` is where the partition will be mounted
    and must be of one of the following forms:

    ``/<path>``

    For example, /, /usr, /home

    ``swap``

    The partition will be used as swap space.

    ``raid.<id>``

    The partition will be used for software RAID.
    Refer to the ``raid`` command.

    ``pv.<id>``

    The partition will be used for LVM. Refer to the
    ``logvol`` command.

    ``btrfs.<id>``

    The partition will be used for BTRFS volume. Rerefer to
    the ``btrfs`` command.

    ``biosboot``

    The partition will be used for a BIOS Boot Partition. As
    of Fedora 16 there must be a biosboot partition for the
    bootloader to be successfully installed onto a disk that
    contains a GPT/GUID partition table. Rerefer to the
    ``bootloader`` command.

    .. versionadded:: Fedora3

optional arguments:

``--active``

    .. versionadded:: Fedora3

``--asprimary``

    Forces automatic allocation of the partition as a primary
    partition or the partitioning will fail.

    **TIP:** *The ``--asprimary`` option only makes sense
    with the MBR partitioning scheme and is ignored when the
    GPT partitioning scheme is used.*

    .. versionadded:: Fedora3

``--fstype FSTYPE, --type FSTYPE``

    Sets the file system type for the partition. Valid
    values include ext4, ext3, ext2, xfs, btrfs, swap, and
    vfat. Other filesystems may be valid depending on
    command line arguments passed to anaconda to enable
    other filesystems.

    .. versionadded:: Fedora3

``--grow``

    Tells the partition to grow to fill available space
    (if any), or up to the maximum size setting. Note that
    ``--grow`` is not supported for partitions containing a
    RAID volume on top of them.

    .. versionadded:: Fedora3

``--maxsize MAXSIZEMB``

    The maximum size in MiB the partition may grow to.
    Specify an integer value here, and do not append any
    units. This option is only relevant if ``--grow`` is
    specified as well.

    .. versionadded:: Fedora3

``--noformat``

    Tells the installation program not to format the
    partition, for use with the ``--onpart`` command.

    .. versionadded:: Fedora3

``--onbiosdisk ONBIOSDISK``

    Forces the partition to be created on a particular disk
    as discovered by the BIOS.

    .. versionadded:: Fedora3

``--ondisk DISK, --ondrive DISK``

    Forces the partition to be created on a particular disk.

    .. versionadded:: Fedora3

``--onpart ONPART, --usepart ONPART``

    Put the partition on an already existing device. Use
    "--onpart=LABEL=name" or "--onpart=UUID=name" to specify
    a partition by label or uuid respectively.

    Anaconda may create partitions in any particular order,
    so it is safer to use labels than absolute partition
    names.

    .. versionadded:: Fedora3

``--recommended``

    Determine the size of the partition automatically.

    .. versionadded:: Fedora3

``--size SIZE``

    The minimum partition size in MiB. Specify an integer
    value here and do not append any units.

    .. versionadded:: Fedora3

``--fsoptions FSOPTS``

    Specifies a free form string of options to be used when
    mounting the filesystem. This string will be copied into
    the /etc/fstab file of the installed system and should
    be enclosed in quotes.

    .. versionadded:: Fedora4

``--label LABEL``

    Specify the label to give to the filesystem to be made
    on the partition. If the given label is already in use
    by another filesystem, a new label will be created for
    this partition.

    .. versionadded:: Fedora4

``--bytes-per-inode BYTES_PER_INODE``

    Specify the bytes/inode ratio.

    .. versionadded:: Fedora4

    .. deprecated:: Fedora9

    .. versionremoved:: Fedora14

``--fsprofile FSPROFILE``

    Specifies a usage type to be passed to the program that
    makes a filesystem on this partition. A usage type
    defines a variety of tuning parameters to be used when
    making a filesystem. For this option to work, the
    filesystem must support the concept of usage types and
    there must be a configuration file that lists valid
    types. For ext2/3/4, this configuration file is
    ``/etc/mke2fs.conf``.

    .. versionadded:: Fedora9

``--encrypted``

    Specify that this partition should be encrypted.

    .. versionadded:: Fedora9

``--passphrase PASSPHRASE``

    Specify the passphrase to use when encrypting this
    partition. Without the above --encrypted option, this
    option does nothing. If no passphrase is specified, the
    default system-wide one is used, or the installer will
    stop and prompt if there is no default.

    .. versionadded:: Fedora9

``--start START``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora11

    .. versionremoved:: Fedora14

``--end END``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora11

    .. versionremoved:: Fedora14

``--escrowcert <url>``

    Load an X.509 certificate from ``<url>``. Store the
    data encryption key of this partition, encrypted using
    the certificate, as a file in ``/root``. Only relevant
    if ``--encrypted`` is specified as well.

    .. versionadded:: Fedora12

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well.
    In addition to storing the data encryption key, generate
    a random passphrase and add it to this partition. Then
    store the passphrase, encrypted using the certificate
    specified by ``--escrowcert``, as a file in ``/root``.
    If more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

    .. versionadded:: Fedora12

``--resize``

    Attempt to resize this partition to the size given by
    ``--size=``. This option must be used with
    ``--onpart --size=``, or an error will be raised.

    .. versionadded:: Fedora17

``--hibernation``

    This option can be used to automatically determine the
    size of the swap partition big enough for hibernation.

    .. versionadded:: Fedora18

``--cipher CIPHER``

    Only relevant if ``--encrypted`` is specified. Specifies
    which encryption algorithm should be used to encrypt the
    filesystem.

    .. versionadded:: Fedora18

``--mkfsoptions MKFSOPTS``

    Specifies additional parameters to be passed to the
    program that makes a filesystem on this partition. This
    is similar to ``--fsprofile`` but works for all
    filesystems, not just the ones that support the profile
    concept. No processing is done on the list of arguments,
    so they must be supplied in a format that can be passed
    directly to the mkfs program. This means multiple
    options should be comma-separated or surrounded by
    double quotes, depending on the filesystem.

    .. versionadded:: Fedora23

If partitioning fails for any reason, diagnostic
messages will appear on virtual console 3.

raid
----

::

    raid --device DEVICE [--fstype FSTYPE] [--level LEVEL] [--noformat]
     [--spares SPARES] [--useexisting] [--fsoptions FSOPTS]
     [--fsprofile FSPROFILE] [--encrypted] [--passphrase PASSPHRASE]
     [--escrowcert <url>] [--backuppassphrase] [--label LABEL]
     [--cipher CIPHER] [--mkfsoptions MKFSOPTS]
     <mntpoint> [<partitions*> [<partitions*> ...]]

.. versionadded:: Fedora3

Assembles a software RAID device.

positional arguments:

``<mntpoint>``

    Location where the RAID file system is mounted. If it
    is /, the RAID level must be 1 unless a boot partition
    (/boot) is present. If a boot partition is present, the
    /boot partition must be level 1 and the root (/)
    partition can be any of the available types.

    .. versionadded:: Fedora3

``<partitions*>``

    The software raid partitions lists the RAID identifiers
    to add to the RAID array.

    .. versionadded:: Fedora3

optional arguments:

``--device DEVICE``

    Name of the RAID device to use (such as 'fedora-root'
    or 'home'). As of Fedora 19, RAID devices are no longer
    referred to by names like 'md0'. If you have an old
    (v0.90 metadata) array that you cannot assign a name to,
    you can specify the array by a filesystem label or UUID
    (eg: --device=LABEL=fedora-root).

    .. versionadded:: Fedora3

``--fstype FSTYPE``

    Sets the file system type for the RAID array. Valid
    values include ext4, ext3, ext2, btrfs, swap, and vfat.
    Other filesystems may be valid depending on command
    line arguments passed to anaconda to enable other
    filesystems.

    .. versionadded:: Fedora3

``--level LEVEL``

    RAID level to use set(['RAID10', 'RAID5', 'RAID4', 'RAID6', 'RAID1', 'RAID0']).

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora7

    The "RAID10" level was added.

    .. versionchanged:: Fedora13

    The "RAID4" level was added.

``--noformat``

    Use an existing RAID device and do not format the RAID
    array.

    .. versionadded:: Fedora3

``--spares SPARES``

    Specifies the number of spare drives allocated for the
    RAID array. Spare drives are used to rebuild the array
    in case of drive failure.

    .. versionadded:: Fedora3

``--useexisting``

    Use an existing RAID device and reformat it.

    .. versionadded:: Fedora3

``--fsoptions FSOPTS``

    Specifies a free form string of options to be used when
    mounting the filesystem. This string will be copied into
    the /etc/fstab file of the installed system and should
    be enclosed in quotes.

    .. versionadded:: Fedora4

``--bytes-per-inode BYTES_PER_INODE``

    Specify the bytes/inode ratio.

    .. versionadded:: Fedora5

    .. deprecated:: Fedora9

    .. versionremoved:: Fedora14

``--fsprofile FSPROFILE``

    Specifies a usage type to be passed to the program that
    makes a filesystem on this partition. A usage type
    defines a variety of tuning parameters to be used when
    making a filesystem. For this option to work, the
    filesystem must support the concept of usage types and
    there must be a configuration file that lists valid
    types. For ext2/3/4, this configuration file is
    ``/etc/mke2fs.conf``.

    .. versionadded:: Fedora9

``--encrypted``

    Specify that this RAID device should be encrypted.

    .. versionadded:: Fedora9

``--passphrase PASSPHRASE``

    Specify the passphrase to use when encrypting this RAID
    device. Without the above --encrypted option, this option
    does nothing. If no passphrase is specified, the default
    system-wide one is used, or the installer will stop and
    prompt if there is no default.

    .. versionadded:: Fedora9

``--escrowcert <url>``

    Load an X.509 certificate from ``<url>``. Store the
    data encryption key of this partition, encrypted using
    the certificate, as a file in ``/root``. Only relevant
    if ``--encrypted`` is specified as well.

    .. versionadded:: Fedora12

``--backuppassphrase``

    Only relevant if ``--escrowcert`` is specified as well.
    In addition to storing the data encryption key, generate
    a random passphrase and add it to this partition. Then
    store the passphrase, encrypted using the certificate
    specified by ``--escrowcert``, as a file in ``/root``.
    If more than one LUKS volume uses ``--backuppassphrase``,
    the same passphrase will be used for all such volumes.

    .. versionadded:: Fedora12

``--label LABEL``

    Specify the label to give to the filesystem to be made.
    If the given label is already in use by another
    filesystem, a new label will be created.

    .. versionadded:: Fedora15

``--cipher CIPHER``

    Only relevant if ``--encrypted`` is specified. Specifies
    which encryption algorithm should be used to encrypt the
    filesystem.

    .. versionadded:: Fedora18

``--mkfsoptions MKFSOPTS``

    Specifies additional parameters to be passed to the
    program that makes a filesystem on this partition. No
    processing is done on the list of arguments, so they
    must be supplied in a format that can be passed directly
    to the mkfs program. This means multiple options should
    be comma-separated or surrounded by double quotes,
    depending on the filesystem.

    .. versionadded:: Fedora23

The following example shows how to create a RAID
level 1 partition for /, and a RAID level 5 for
/usr, assuming there are three disks on the
system. It also creates three swap partitions, one
on each drive::

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

::

    realm

.. versionadded:: Fedora19

repo
----

::

    repo --name NAME [--baseurl BASEURL] [--mirrorlist MIRRORLIST] [--cost COST]
     [--excludepkgs EXCLUDEPKGS] [--includepkgs INCLUDEPKGS]
     [--ignoregroups IGNOREGROUPS] [--proxy PROXY] [--noverifyssl] [--install]

.. versionadded:: Fedora6

Configures additional yum repositories that may be
used as sources for package installation. Multiple
repo lines may be specified. By default, anaconda
has a configured set of repos taken from
/etc/anaconda.repos.d plus a special Installation
Repo in the case of a media install. The exact set
of repos in this directory changes from release to
release and cannot be listed here. There will
likely always be a repo named "updates".

Note: If you want to enable one of the repos in
/etc/anaconda.repos.d that is disabled by default
(like "updates"), you should use --name= but none
of the other options. anaconda will look for a repo
by this name automatically. Providing a baseurl or
mirrorlist URL will result in anaconda attempting
to add another repo by the same name, which will
cause a conflicting repo error.

optional arguments:

``--name NAME``

    The repo id. This option is required. If a repo has a
    name that conflicts with a previously added one, the
    new repo will be ignored. Because anaconda has a
    populated list of repos when it starts, this means that
    users cannot create new repos that override these names.
    Please check /etc/anaconda.repos.d from the operating
    system you wish to install to see what names are not
    available.

    .. versionadded:: Fedora6

``--baseurl BASEURL``

    The URL for the repository. The variables that may be
    used in yum repo config files are not supported here.
    You may use one of either this option or
    ``--mirrorlist``, not both. If an NFS repository is
    specified, it should be of the form
    ``nfs://host:/path/to/repo``. Note that there is a
    colon after the host. Anaconda passes everything after
    "nfs:// " directly to the mount command instead of
    parsing URLs according to RFC 2224. Variable
    substitution is done for $releasever and $basearch in
    the url.

    .. versionadded:: Fedora6

    .. versionchanged:: Fedora15

    ``--mirrorlist`` and ``--baseurl`` are not required anymore!

``--mirrorlist MIRRORLIST``

    The URL pointing at a list of mirrors for the
    repository. The variables that may be used in yum repo
    config files are not supported here. You may use one of
    either this option or ``--baseurl``, not both. Variable
    substitution is done for $releasever and $basearch in
    the url.

    .. versionadded:: Fedora6

    .. versionchanged:: Fedora15

    ``--mirrorlist`` and ``--baseurl`` are not required anymore!

``--cost COST``

    An integer value to assign a cost to this repository.
    If multiple repositories provide the same packages,
    this number will be used to prioritize which repository
    will be used before another. Repositories with a lower
    cost take priority over repositories with higher cost.

    .. versionadded:: Fedora8

``--excludepkgs EXCLUDEPKGS``

    A comma-separated list of package names and globs that
    must not be pulled from this repository. This is useful
    if multiple repositories provide the same package and
    you want to make sure it comes from a particular
    repository.

    .. versionadded:: Fedora8

``--includepkgs INCLUDEPKGS``

    A comma-separated list of package names and globs that
    must be pulled from this repository. This is useful if
    multiple repositories provide the same package and you
    want to make sure it comes from this repository.

    .. versionadded:: Fedora8

``--ignoregroups IGNOREGROUPS``

    This option is used when composing installation trees
    and has no effect on the installation process itself.
    It tells the compose tools to not look at the package
    group information when mirroring trees so as to avoid
    mirroring large amounts of unnecessary data.

    .. versionadded:: Fedora11

``--proxy PROXY``

    Specify an HTTP/HTTPS/FTP proxy to use just for this
    repository. This setting does not affect any other
    repositories, nor how the install.img is fetched on
    HTTP installs. The various parts of the argument act
    like you would expect. The syntax is::

    ``--proxy=[protocol://][username[:password]@]host[:port]``

    .. versionadded:: Fedora13

``--noverifyssl``

    For a https repo do not check the server's certificate
    with what well-known CA validate and do not check the
    server's hostname matches the certificate's domain name.

    .. versionadded:: Fedora14

``--install``

    Install this repository to the target system so that it
    can be used after reboot.

    .. versionadded:: Fedora21

reqpart
-------

::

    reqpart [--add-boot]

.. versionadded:: Fedora23

Automatically create partitions required by your
hardware platform. These include a ``/boot/efi``
for x86_64 and Aarch64 systems with UEFI firmware,
``biosboot`` for x86_64 systems with BIOS firmware
and GPT, and ``PRePBoot`` for IBM Power Systems.

Note: This command can not be used together with
``autopart``, because ``autopart`` does the same
and creates other partitions or logical volumes
such as ``/`` and ``swap`` on top. In contrast with
``autopart``, this command only creates
platform-specific partitions and leaves the rest of
the drive empty, allowing you to create a custom
layout.

optional arguments:

``--add-boot``

    Create a separate ``/boot`` partition in addition to the
    platform-specific partition created by the base command.

    .. versionadded:: Fedora23

rescue
------

::

    rescue [--nomount] [--romount]

.. versionadded:: Fedora10

Automatically enter the installer's rescue mode.
This gives you a chance to repair the system should
something catastrophic happen.

optional arguments:

``--nomount``

    Don't mount the installed system.

    .. versionadded:: Fedora10

``--romount``

    Mount the installed system in read-only mode.

    .. versionadded:: Fedora10

By default, the installer will find your system and
mount it in read-write mode, telling you where it has
performed this mount. You may optionally choose to
not mount anything or mount in read-only mode. Only
one of these two options may be given at any one
time.

rootpw
------

::

    rootpw [--iscrypted] [--lock] [--plaintext] [<password> [<password> ...]]

.. versionadded:: Fedora3

This required command sets the system's root
password.

positional arguments:

``<password>``

    The desired root password.

    .. versionadded:: Fedora3

optional arguments:

``--iscrypted``

    If this is present, the password argument is assumed to
    already be encrypted. To create an encrypted password
    you can use python::

    ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Salt"))'``

    This will generate sha512 crypt of your password using
    your provided salt.

    .. versionadded:: Fedora3

``--lock``

    If this is present, the root account is locked by
    default. That is, the root user will not be able to
    login from the console.

    .. versionadded:: Fedora8

``--plaintext``

    The password argument is assumed to not be encrypted.
    This is the default!

    .. versionadded:: Fedora8

selinux
-------

::

    selinux [--disabled] [--enforcing] [--permissive]

.. versionadded:: Fedora3

Sets the state of SELinux on the installed system.
SELinux defaults to enforcing in anaconda.

optional arguments:

``--disabled``

    If this is present, SELinux is disabled.

    .. versionadded:: Fedora3

``--enforcing``

    If this is present, SELinux is set to enforcing mode.

    .. versionadded:: Fedora3

``--permissive``

    If this is present, SELinux is enabled, but only logs
    things that would be denied in enforcing mode.

    .. versionadded:: Fedora3

Only one of ``--disabled``, ``--enabled`` or
``--permissive`` must be specified!

services
--------

::

    services [--disabled <list>] [--enabled <list>]

.. versionadded:: Fedora6

Modifies the default set of services that will run
under the default runlevel. The services listed in
the disabled list will be disabled before the
services listed in the enabled list are enabled.

optional arguments:

``--disabled <list>``

    Disable the services given in the comma separated list.

    .. versionadded:: Fedora6

``--enabled <list>``

    Enable the services given in the comma separated list.

    .. versionadded:: Fedora6

One of --disabled or --enabled must be provided.

skipx
-----

::

    skipx

.. versionadded:: Fedora3

If present, X is not configured on the installed
system.

sshpw
-----

::

    sshpw --username <name> [--iscrypted] [--plaintext] [--lock]
      [<password> [<password> ...]]

.. versionadded:: Fedora13

The installer can start up ssh to provide for
interactivity and inspection, just like it can with
telnet. The "inst.sshd" option must be specified on
the kernel command-line for Anaconda to start an ssh
daemon. The sshpw command is used to control the
accounts created in the installation environment that
may be remotely logged into. For each instance of
this command given, a user will be created. These
users will not be created on the final system -
they only exist for use while the installer is
running.

Note that by default, root has a blank password. If
you don't want any user to be able to ssh in and
have full access to your hardware, you must specify
sshpw for username root. Also note that if Anaconda
fails to parse the kickstart file, it will allow
anyone to login as root and have full access to
your hardware.

positional arguments:

``<password>``

    The password string to use.

    .. versionadded:: Fedora13

optional arguments:

``--username <name>``

    Provides the name of the user. This option is required.

    .. versionadded:: Fedora13

``--iscrypted``

    If this is present, the password argument is assumed to
    already be encrypted.

    .. versionadded:: Fedora13

``--plaintext``

    If this is present, the password argument is assumed to
    not be encrypted. This is the default.

    .. versionadded:: Fedora13

``--lock``

    If this is present, the new user account is locked by
    default. That is, the user will not be able to login
    from the console.

    .. versionadded:: Fedora13

timezone
--------

::

    timezone [--utc] [--nontp] [--ntpservers <server1>,<server2>,...,<serverN>]
         [<timezone>]

.. versionadded:: Fedora3

This required command sets the system time zone to
which may be any of the time zones listed by
timeconfig.

positional arguments:

``<timezone>``

    Timezone name, e.g. Europe/Sofia.
    This is optional but at least one of the options needs
    to be used if no timezone is specified.

    .. versionadded:: Fedora3

optional arguments:

``--utc, --isUtc``

    If present, the system assumes the hardware clock is set
    to UTC (Greenwich Mean) time.

    *To get the list of supported timezones, you can either
    run this script:
    http://vpodzime.fedorapeople.org/timezones_list.py or
    look at this list:
    http://vpodzime.fedorapeople.org/timezones_list.txt*

    .. versionadded:: Fedora6

``--nontp``

    Disable automatic starting of NTP service.

    ``--nontp`` and ``--ntpservers`` are mutually exclusive.

    .. versionadded:: Fedora18

``--ntpservers <server1>,<server2>,...,<serverN>``

    Specify a list of NTP servers to be used (comma-separated
    list with no spaces). The chrony package is automatically
    installed when this option is used. If you don't want the
    package to be automatically installed then use ``-chrony``
    in package selection. For example::

    ``timezone --ntpservers=ntp.cesnet.cz,tik.nic.cz Europe/Prague``

    .. versionadded:: Fedora18

unsupported_hardware
--------------------

::

    unsupported_hardware

.. versionadded:: RedHatEnterpriseLinux6

updates
-------

::

    updates [[URL] [[URL] ...]]

.. versionadded:: Fedora7

Specify the location of an updates.img for use in
installation. See anaconda-release-notes.txt for a
description of how to make an updates.img.

positional arguments:

``[URL]``

    If present, the URL for an updates image.

    If not present, anaconda will attempt to load from a
    floppy disk.

    .. versionadded:: Fedora7

install or upgrade
------------------

::

    install|upgrade [--root-device ROOT_DEVICE]

.. versionadded:: Fedora3

Install a fresh system or upgrade an existing system.
Install is the default mode. For installation, you must
specify the type of installation from one of
cdrom, harddrive, nfs, or url (for ftp or http installations).
The install command and the installation method command
must be on separate lines.

.. deprecated:: Fedora20

Starting with F18, upgrades are no longer supported in
anaconda and should be done with FedUp, the Fedora update
tool. Starting with F21, the DNF system-upgrade plugin is
recommended instead.  Therefore, the upgrade command
essentially does nothing.

optional arguments:

``--root-device ROOT_DEVICE``

    .. versionadded:: Fedora11

url
---

::

    url [--proxy URL] [--noverifyssl] [--url URL] [--mirrorlist URL]

.. versionadded:: Fedora3

Install from an installation tree on a remote server
via FTP or HTTP.

optional arguments:

``--proxy URL``

    Specify an HTTP/HTTPS/FTP proxy to use while performing
    the install. The various parts of the argument act like
    you would expect. The syntax is::

    [protocol://][username[:password]@]host[:port]

    .. versionadded:: Fedora13

``--noverifyssl``

    For a tree on a HTTPS server do not check the server's
    certificate with what well-known CA validate and do not
    check the server's hostname matches the certificate's
    domain name.

    .. versionadded:: Fedora14

``--url URL``

    The URL to install from. Variable substitution is done
    for $releasever and $basearch in the url.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora18

    This parameter is no longer required because you could
    use ``--mirrorlist`` instead.

``--mirrorlist URL``

    The mirror URL to install from. Variable substitution
    is done for $releasever and $basearch in the url.

    .. versionadded:: Fedora18

user
----

::

    user [--groups <group1>,<group2>,...,<groupN>] [--homedir HOMEDIR]
     [--iscrypted] --name NAME [--password PASSWORD] [--shell SHELL]
     [--uid INT] [--lock] [--plaintext] [--gecos GECOS] [--gid INT]

.. versionadded:: Fedora6

Creates a new user on the system.

optional arguments:

``--groups <group1>,<group2>,...,<groupN>``

    In addition to the default group, a comma separated
    list of group names the user should belong to. Any groups
    that do not already exist will be created. If the group
    already exists with a different GID, an error will
    be raised.

    .. versionadded:: Fedora6

``--homedir HOMEDIR``

    The home directory for the user. If not provided, this
    defaults to /home/.

    .. versionadded:: Fedora6

``--iscrypted``

    If specified, consider the password provided by
    ``--password`` already encrypted. This is the default.

    .. versionadded:: Fedora6

``--name NAME``

    Provides the name of the user. This option is required.

    .. versionadded:: Fedora6

``--password PASSWORD``

    The new user's password. If not provided, the account
    will be locked by default. If this is present, the
    password argument is assumed to already be encrypted.
    ``--plaintext`` has the opposite effect - the password
    argument is assumed to not be encrypted. To create an
    encrypted password you can use python::

    ``python -c 'import crypt; print(crypt.crypt("My Password", "$6$My Sault"))'``

    This will generate sha512 crypt of your password using
    your provided salt.

    .. versionadded:: Fedora6

``--shell SHELL``

    The user's login shell. If not provided, this defaults
    to the system default.

    .. versionadded:: Fedora6

``--uid INT``

    The user's UID. If not provided, this defaults to the
    next available non-system UID.

    .. versionadded:: Fedora6

``--lock``

    If this is present, the new user account is locked by
    default. That is, the user will not be able to login
    from the console.

    .. versionadded:: Fedora8

``--plaintext``

    If specified, consider the password provided by
    ``--password`` to be plain text.

    .. versionadded:: Fedora8

``--gecos GECOS``

    Provides the GECOS information for the user. This is a
    string of various system-specific fields separated by a
    comma. It is frequently used to specify the user's full
    name, office number, and the like. See ``man 5 passwd``
    for more details.

    .. versionadded:: Fedora12

``--gid INT``

    The GID of the user's primary group. If not provided,
    this defaults to the next available non-system GID.

    .. versionadded:: Fedora19

vnc
---

::

    vnc [--password PASSWORD] [--host HOST] [--port PORT]

.. versionadded:: Fedora3

Allows the graphical installation to be viewed
remotely via VNC. This method is usually preferred
over text mode, as there are some size and language
limitations in text installs. With no options, this
command will start a VNC server on the machine with
no password and will print out the command that
needs to be run to connect a remote machine.

optional arguments:

``--password PASSWORD``

    Set a password which must be provided to connect to the
    VNC session. This is optional, but recommended.

    .. versionadded:: Fedora3

``--connect host[:port]``

    Connect to a remote host instead of starting VNC server
    locally.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora6

    Added support for host[:port] syntax.

    .. versionremoved:: Fedora9

``--host HOST``

    Instead of starting a VNC server on the install machine,
    connect to the VNC viewer process listening on the given
    hostname.

    .. versionadded:: Fedora6

``--port PORT``

    Provide a port that the remote VNC viewer process is
    listening on. If not provided, anaconda will use the
    VNC default.

    .. versionadded:: Fedora6

volgroup
--------

::

    volgroup [--noformat] [--useexisting] [--reserved-space RESERVED_SPACE]
         [--reserved-percent RESERVED_PERCENT] [--pesize PESIZE]
         [<name> [<name> ...]] [<partitions*> [<partitions*> ...]]

.. versionadded:: Fedora3

Creates a Logical Volume Management (LVM) group.

positional arguments:

``<name>``

    Name given to the volume group. The (which denotes that
    multiple partitions can be listed) lists the identifiers
    to add to the volume group.

    .. versionadded:: Fedora3

``<partitions*>``

    Physical Volume partitions to be included in this
    Volume Group

    .. versionadded:: Fedora3

optional arguments:

``--noformat``

    Use an existing volume group. Do not specify partitions
    when using this option.

    .. versionadded:: Fedora3

``--useexisting``

    Use an existing volume group. Do not specify partitions
    when using this option.

    .. versionadded:: Fedora3

``--reserved-space RESERVED_SPACE``

    Specify an amount of space to leave unused in a volume
    group, in MiB. Do not append any units. This option is
    only used for new volume groups.

    .. versionadded:: Fedora16

``--reserved-percent RESERVED_PERCENT``

    Specify a percentage of total volume group space to
    leave unused (new volume groups only).

    .. versionadded:: Fedora16

``--pesize PESIZE``

    Set the size of the physical extents in KiB.

    .. versionadded:: Fedora3

    .. versionchanged:: Fedora21

    Set the size of the physical extents in KiB.

Create the partition first, create the logical
volume group, and then create the logical volume.
For example::

    part pv.01 --size 3000
    volgroup myvg pv.01
    logvol / --vgname=myvg --size=2000 --name=rootvol

xconfig
-------

::

    xconfig [--defaultdesktop GNOME|KDE] [--startxonboot]

.. versionadded:: Fedora3

Configures the X Window System. If this option is
not given, Anaconda will use X and attempt to
automatically configure. Please try this before
manually configuring your system.

optional arguments:

``--defaultdesktop GNOME|KDE``

    Specify either GNOME or KDE to set the default desktop
    (assumes that GNOME Desktop Environment and/or KDE
    Desktop Environment has been installed through
    %packages).

    .. versionadded:: Fedora3

``--server SERVER``

    .. versionadded:: Fedora3

    .. versionremoved:: Fedora6

``--startxonboot``

    Use a graphical login on the installed system.

    .. versionadded:: Fedora3

``--card CARD``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora6

    .. versionremoved:: Fedora9

``--hsync HSYNC``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora6

    .. versionremoved:: Fedora9

``--monitor MONITOR``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora6

    .. versionremoved:: Fedora9

``--noprobe NOPROBE``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora6

    .. versionremoved:: Fedora9

``--vsync VSYNC``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora6

    .. versionremoved:: Fedora9

``--driver DRIVER``

    .. versionadded:: Fedora6

    .. deprecated:: Fedora10

    .. versionremoved:: Fedora14

``--depth DEPTH``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora10

    .. versionremoved:: Fedora14

``--resolution RESOLUTION``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora10

    .. versionremoved:: Fedora14

``--videoram VIDEORAM``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora10

    .. versionremoved:: Fedora14

zerombr
-------

::

    zerombr

.. versionadded:: Fedora3

If zerombr is specified, any disks whose formatting
is unrecognized are initialized. This will destroy
all of the contents of disks with invalid partition
tables or other formatting unrecognizable to the
installer. It is useful so that the installation
program does not ask if it should initialize the
disk label if installing to a brand new hard drive.

zfcp
----

::

    zfcp --devnum DEVNUM --fcplun FCPLUN --wwpn WWPN

.. versionadded:: Fedora3

optional arguments:

``--devnum DEVNUM``

    .. versionadded:: Fedora3

``--fcplun FCPLUN``

    .. versionadded:: Fedora3

``--wwpn WWPN``

    .. versionadded:: Fedora3

``--scsiid SCSIID``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora12

    .. versionremoved:: Fedora14

``--scsilun SCSILUN``

    .. versionadded:: Fedora3

    .. deprecated:: Fedora12

    .. versionremoved:: Fedora14
