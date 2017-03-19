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
   #. The %pre, %pre-install, %post, %onerror, and %traceback sections --
      These sections can be in any order and are not required. Refer to
      Chapter 4, Chapter 5, and Chapter 6  for details.

-  The %packages, %pre, %pre-install, %post, %onerror, and %traceback sections
   are all required to be closed with %end
-  Items that are not required can be omitted.
-  Omitting any required item will result in the installation program
   prompting the user for an answer to the related item, just as the
   user would be prompted during a typical installation. Once the answer
   is given, the installation will continue unattended unless it finds
   another missing item.
-  One installation source command from the list of commands in the ``method``
   proxy command must be specified for the fully automated kickstart
   installation. This is required even for Fedora -- the closest mirror can't
   be chosen by the kickstart file.
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


Chapter 2. Kickstart Commands in Fedora
=======================================

The following commands can be placed in a kickstart file. If you prefer
to use a graphical interface for creating your kickstart file, you can
use the Kickstart Configurator application.

Most commands take arguments.  If an argument is followed equals mark (``=``),
a value must be specified after it.

In the example commands, options in '''[square brackets]''' are optional
arguments for the command.

pykickstart processes arguments to commands just like the shell does:

::

   If a list of arguments can be passed in, the arguments must be separated by
   commas and not include any extra spaces.  If extra spaces are required in the
   list of arguments, the entire argument must be surrounded by double quotes.
   If quotes, spaces, or other special characters need to be added to the
   arguments list, they must be escaped.

.. include:: commands.rst


%include
--------

Use the ``%include /path/to/file`` or ``%include <url>`` command
to include the contents of another file in the kickstart file as though
the contents were at the location of the ``%include`` command in the
kickstart file.

Note the semantics of most kickstart commands default to "last keyword
wins", which means that for example if you have a
``services --enable=foo,bar`` in one file, and `%include` that file
and use ``services --enable=baz``, only the ``baz`` service will be
enabled.

The Kickstart documentation usually notes which commands support
multiple instances - this is mostly multi-line commands such as
``%packages`` and ``%post``.  Other exceptions include the ``user`` and
``group`` commands.  Consult individual command documentation for
semantics.


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


Chapter 3. Kickstart Commands in Red Hat Enterprise Linux
=========================================================

The following commands can be placed in a kickstart file. If you prefer
to use a graphical interface for creating your kickstart file, you can
use the Kickstart Configurator application.

Most commands take arguments.  If an argument is followed equals mark (``=``),
a value must be specified after it.

In the example commands, options in '''[square brackets]''' are optional
arguments for the command.

pykickstart processes arguments to commands just like the shell does:

::

   If a list of arguments can be passed in, the arguments must be separated by
   commas and not include any extra spaces.  If extra spaces are required in the
   list of arguments, the entire argument must be surrounded by double quotes.
   If quotes, spaces, or other special characters need to be added to the
   arguments list, they must be escaped.

.. include:: commands_rhel.rst


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

.. include:: sections.rst


Chapter 10. Making the Kickstart File Available
===============================================

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
`inst.ks.sendmac <https://rhinstaller.github.io/anaconda/boot-options.html#inst-ks-sendmac>`__
and
`inst.ks.sendsn <https://rhinstaller.github.io/anaconda/boot-options.html#inst-ks-sendsn>`__

Prior to Fedora 17 and Red Hat Enterprise Linux 7, these options were
named ``kssendmac`` and ``kssendsn``.

Chapter 11. Making the Installation Tree Available
==================================================

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


Chapter 12. Starting a Kickstart Installation
=============================================

To begin a kickstart installation, you must boot the system from a
Fedora or Red Hat Enterprise Linux boot diskette, Fedora or Red Hat
Enterprise Linux boot CD-ROM, or the Fedora or Red Hat Enterprise Linux
CD-ROM #1 and enter a special boot command at the boot prompt. In order
to get to the boot prompt you must hit escape at the CD or DVD boot
menu. In case you don't know what I'm talking about I took a screenshot.
The installation program looks for a kickstart file if the ks command
line argument is passed to the kernel.

https://fedoraproject.org/wiki/File:Fedora_boot_screen.png

Prior to Fedora 17 and Red Hat Enterprise Linux 7, all the various forms
of the ``inst.ks=`` parameter were simply named ``ks=``.


Boot Diskette
-------------

If the kickstart file is located on a boot diskette as described in the
Section called Creating a Kickstart Boot Diskette in Chapter 6, boot the
system with the diskette in the drive, and enter the following command
at the boot: prompt:

``linux inst.ks=floppy``


CD-ROM #1 and Diskette
----------------------

The linux inst.ks=floppy command also works if the ks.cfg file is located on
a vfat or ext2 file system on a diskette and you boot from the Fedora or
Red Hat Enterprise Linux CD-ROM #1.

An alternate boot command is to boot off the Fedora or Red Hat
Enterprise Linux CD-ROM #1 and have the kickstart file on a vfat or ext2
file system on a diskette. To do so, enter the following command at the
boot: prompt:

``linux inst.ks=hd:fd0:/ks.cfg``


With Driver Disk
----------------

If you need to use a driver disk with kickstart, specify the dd option
as well. For example, to boot off a boot diskette and use a driver disk,
enter the following command at the boot: prompt:

``linux inst.ks=floppy dd``


Boot CD-ROM
-----------

If the kickstart file is on a boot CD-ROM as described in the Section
called Creating a Kickstart Boot CD-ROM in Chapter 6, insert the CD-ROM
into the system, boot the system, and enter the following command at the
boot: prompt (where ks.cfg is the name of the kickstart file):

``linux inst.ks=cdrom:<device>:/ks.cfg``


Other kickstart options
------------------------

``inst.ks=nfs:<server>:/<path>``

    The installation program will look for the kickstart file on the NFS
    server , as file . The installation program will use DHCP to
    configure the Ethernet card. For example, if your NFS server is
    server.example.com and the kickstart file is in the NFS share
    /mydir/ks.cfg, the correct boot command would be
    inst.ks=\ nfs:server.example.com:/mydir/ks.cfg.

``inst.ks=http://<server>/<path>``

    The installation program will look for the kickstart file on the
    HTTP server , as file . The installation program will use DHCP to
    configure the Ethernet card. For example, if your HTTP server is
    server.example.com and the kickstart file is in the HTTP directory
    /mydir/ks.cfg, the correct boot command would be
    inst.ks=\ http://server.example.com/mydir/ks.cfg.

``inst.ks=floppy``

    The installation program looks for the file ks.cfg on a vfat or ext2
    file system on the diskette in /dev/fd0.

``inst.ks=floppy:/<path>``

    The installation program will look for the kickstart file on the
    diskette in /dev/fd0, as file .

``inst.ks=hd:<device>:/<file>``

    The installation program will mount the file system on (which must
    be vfat or ext2), and look for the kickstart configuration file as
    in that file system (for example, inst.ks=hd:sda3:/mydir/ks.cfg).

``inst.ks=bd:<biosdev>:/<path>``

    The installation program will mount the file system on the specified
    partition on the specified BIOS device (for example,
    inst.ks=bd:80p3:/mydir/ks.cfg). Note this does not work for BIOS RAID
    sets.

``inst.ks=file:/<file>``

    The installation program will try to read the file from the file
    system; no mounts will be done. This is normally used if the
    kickstart file is already on the initrd image.

``inst.ks=cdrom:/<path>`` or in newer versions
``inst.ks=cdrom:<cdrom device>:/<path>``

    The installation program will look for the kickstart file on CD-ROM,
    as file .

``inst.ks``

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

``inst.ks.device=<device>``

    The installation program will use this network device to connect to
    the network. For example, to start a kickstart installation with the
    kickstart file on an NFS server that is connected to the system
    through the eth1 device, use the command
    ``inst.ks=nfs:<server>:/<path> ksdevice=eth1`` at the boot: prompt. For
    more information, see
    `anaconda boot options <https://rhinstaller.github.io/anaconda/boot-options.html>`__.

    Prior to Fedora 17 and Red Hat Enterprise Linux 7, this option was named
    ``ksdevice=``.


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
    #inst.ks=http://127.0.0.1/ks.cfg
    #inst.ks=http://localhost/ks.cfg
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

`JAKS <https://github.com/jas-/jaks>`__ (Just Another Kickstart Script) - Generic kickstart script for all `anaconda` based installations.
Includes `jaks2iso` to assist with generating bootable ISO for UEFI/8086 boot rom good for DVD and/or USB installations.
Also includes `%post` installation hooks through use of `jaks-post-config` toolkit.
