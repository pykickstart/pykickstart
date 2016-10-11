
Chapter 4. Handling Tracebacks
==============================

::

    %traceback [--erroronfail] [--interpreter /usr/bin/python] [--log LOG]

These scripts run when the installer hits an internal error (a traceback, as
they are called in Python) and cannot continue.  When this situation happens,
the installer will display an error dialog to the screen that prompts the user
to file a bug or reboot.  At the same time, it will run all %traceback scripts
in the order they are provided in the kickstart file.

Each %traceback script is required to be closed with a corresponding %end.

.. note::

    These scripts could potentially run at
    any stage in installation - early on, between making filesystems and installing
    packages, before the bootloader is installed, when attempting to reboot, and
    so on.  For this reason, these scripts cannot be run in the chroot environment
    and you should not trust anything in the installed system.  These scripts are
    primarily for testing and error reporting purposes.

optional arguments:

``--erroronfail``

    If the error script fails, this option will cause an
    error dialog to be displayed and will halt installation.
    The error message will direct you to where the cause of
    the failure is logged.

    .. versionadded:: Fedora4

``--interpreter /usr/bin/python``

    Allows you to specify a different scripting language,
    such as Python. Replace /usr/bin/python with the
    scripting language of your choice.

    .. versionadded:: Fedora4

``--log LOG, --logfile LOG``

    Log all messages from the script to the given log file.

    .. versionadded:: Fedora4

Chapter 5. Handling Errors
==========================

::

    %onerror [--erroronfail] [--interpreter /usr/bin/python] [--log LOG]

These scripts run when the installer hits a fatal error, but not necessarily
a bug in the installer.  Some examples of these situations include errors in
packages that have been requested to be installed, failures when starting VNC
when requested, and error when scanning storage.  When these situations happen,
installaton cannot continue.  The installer will run all %onerror scripts in
the order they are provided in the kickstart file.

In addition, %onerror scripts will be run on a traceback as well.  To be exact,
all %onerror scripts will be run and then all %traceback scripts will be run
afterwards.

Each %onerror script is required to be closed with a corresponding %end.

.. note::

    These scripts could potentially run at
    any stage in installation - early on, between making filesystems and installing
    packages, before the bootloader is installed, when attempting to reboot, and
    so on.  For this reason, these scripts cannot be run in the chroot environment
    and you should not trust anything in the installed system.  These scripts are
    primarily for testing and error reporting purposes.

optional arguments:

``--erroronfail``

    If the error script fails, this option will cause an
    error dialog to be displayed and will halt installation.
    The error message will direct you to where the cause of
    the failure is logged.

    .. versionadded:: Fedora4

``--interpreter /usr/bin/python``

    Allows you to specify a different scripting language,
    such as Python. Replace /usr/bin/python with the
    scripting language of your choice.

    .. versionadded:: Fedora4

``--log LOG, --logfile LOG``

    Log all messages from the script to the given log file.

    .. versionadded:: Fedora4

Chapter 6. Post-installation Script
===================================

::

    %post [--erroronfail] [--interpreter /usr/bin/python] [--log LOG] [--nochroot]

You have the option of adding commands to run on the system once the
installation is complete. This section must be at the end of the
kickstart file and must start with the %post command. This section is
useful for functions such as installing additional software and
configuring an additional nameserver.

You may have more than one %post section, which can be useful for cases
where some post-installation scripts need to be run in the chroot and
others that need access outside the chroot.

Each %post section is required to be closed with a corresponding %end.

If you configured the network with static IP information, including a
nameserver, you can access the network and resolve IP addresses in the %post
section.  If you configured the network for DHCP, the /etc/resolv.conf file
has not been completed when the installation executes the %post section. You
can access the network, but you can not resolve IP addresses. Thus, if you
are using DHCP, you must specify IP addresses in the %post section.

If your script spawns a daemon process, you must make sure to close stdout
and stderr.  Doing so is standard procedure for creating daemons.  If you do
not close these file descriptors, the installation will appear hung as
anaconda waits for an EOF from the script.

The post-install script is run in a chroot environment; therefore, performing
tasks such as copying scripts or RPMs from the installation media will not
work.

optional arguments:

``--erroronfail``

    If the error script fails, this option will cause an
    error dialog to be displayed and will halt installation.
    The error message will direct you to where the cause of
    the failure is logged.

    .. versionadded:: Fedora4

``--interpreter /usr/bin/python``

    Allows you to specify a different scripting language,
    such as Python. Replace /usr/bin/python with the
    scripting language of your choice.

    .. versionadded:: Fedora4

``--log LOG, --logfile LOG``

    Log all messages from the script to the given log file.

    .. versionadded:: Fedora4

``--nochroot``

    Allows you to specify commands that you would like to
    run outside of the chroot environment.

    .. versionadded:: Fedora4

Examples
--------

Run a script named ``runme`` from an NFS share::

    %post
    mkdir /mnt/temp
    mount 10.10.0.2:/usr/new-machines /mnt/temp
    open -s -w -- /mnt/temp/runme
    umount /mnt/temp
    %end

Copy the file /etc/resolv.conf to the file system that was just
installed::

    %post --nochroot
    cp /etc/resolv.conf /mnt/sysimage/etc/resolv.conf
    %end

**If your kickstart is being interpreted by the livecd-creator tool, you should
replace /mnt/sysimage above with $INSTALL_ROOT.**

Chapter 7. Package Selection
============================

::

    %packages [--excludedocs] [--ignoremissing] [--nobase] [--nocore]
          [--ignoredeps] [--resolvedeps] [--default] [--instLangs INSTLANGS]
          [--multilib] [--excludeWeakdeps]

Use the %packages command to begin a kickstart file
section that lists the packages you would like to
install.

Packages can be specified by group or by individual
package name. The installation program defines
several groups that contain related packages. Refer
to the repodata/\*comps.xml file on the first CD-ROM
for a list of groups. Each group has an id, user
visibility value, name, description, and package
list. In the package list, the packages marked as
mandatory are always installed if the group is
selected, the packages marked default are selected
by default if the group is selected, and the packages
marked optional must be specifically selected even
if the group is selected to be installed.

In most cases, it is only necessary to list the
desired groups and not individual packages. Note
that the Core group is always selected by default,
so it is not necessary to specify it in the
%packages section.

The %packages section is required to be closed with
%end. Also, multiple %packages sections may be given.
This may be handy if the kickstart file is used as a
template and pulls in various other files with the
%include mechanism.

Here is an example %packages selection::

    %packages
    @X Window System
    @GNOME Desktop Environment
    @Graphical Internet
    @Sound and Video
    dhcp
    %end

As you can see, groups are specified, one to a line,
starting with an ``@`` symbol followed by the full
group name as given in the comps.xml file. Groups
can also be specified using the id for the group,
such as gnome-desktop. Specify individual packages
with no additional characters (the dhcp line in the
example above is an individual package).

You can also specify environments using the ``@^``
prefix followed by full environment name as given in
the comps.xml file.  If multiple environments are
specified, only the last one specified will be used.
Environments can be mixed with both group
specifications (even if the given group is not part
of the specified environment) and package
specifications.

Here is an example of requesting the GNOME Desktop
environment to be selected for installation::

    %packages
    @^gnome-desktop-environment
    %end

Additionally, individual packages may be specified
using globs. For instance::

    %packages
    vim*
    kde-i18n-*
    %end

This would install all packages whose names start
with "vim" or "kde-i18n-".

You can also specify which packages or groups not to
install from the default package list::

    %packages
    -autofs
    -@Sound and Video
    %end

optional arguments:

``--excludedocs``

    Do not install any of the documentation from any packages.
    For the most part, this means files in /usr/share/doc*
    will not get installed though it could mean other files
    as well, depending on how the package was built.

    .. versionadded:: Fedora4

``--ignoremissing``

    Ignore any packages or groups specified in the packages
    section that are not found in any configured repository.
    The default behavior is to halt the installation and ask
    the user if the installation should be aborted or
    continued. This option allows fully automated
    installation even in the error case.

    .. versionadded:: Fedora4

``--nobase``

    Do not install the @base group (installed by default,
    otherwise).

    .. versionadded:: Fedora18

    .. deprecated:: Fedora18

``--nocore``

    Do not install the @core group (installed by default,
    otherwise).

    **Omitting the core group can produce a system that is
    not bootable or that cannot finish the install. Use
    with caution.**

    .. versionadded:: Fedora21

``--ignoredeps``

    .. versionadded:: Fedora4

    .. deprecated:: Fedora4

``--resolvedeps``

    .. versionadded:: Fedora4

    .. deprecated:: Fedora4

``--default``

    Install the default package set. This corresponds to the
    package set that would be installed if no other
    selections were made on the package customization screen
    during an interactive install.

    .. versionadded:: Fedora7

``--instLangs INSTLANGS``

    Specify the list of languages that should be installed.
    This is different from the package group level
    selections, though. This option does not specify what
    package groups should be installed. Instead, it controls
    which translation files from individual packages should
    be installed by setting RPM macros.

    .. versionadded:: Fedora9

``--multilib``

    Enable yum's "all" multilib_policy as opposed to the
    default of "best".

    .. versionadded:: Fedora18

``--excludeWeakdeps``

    Do not install packages from weak dependencies. These
    are packages linked to the selected package set by
    Recommends and Supplements flags. By default weak
    dependencies will be installed.

    .. versionadded:: Fedora24

Group-level options
-------------------

In addition, group lines in the %packages section
can take the following options:

``--nodefaults``

    Only install the group's mandatory packages, not
    the default selections.

``--optional``

    In addition to the mandatory and default packages,
    also install the optional packages. This means all
    packages in the group will be installed.

Chapter 8. Pre-install Script
=============================

::

    %pre-install [--erroronfail] [--interpreter /usr/bin/python] [--log LOG]

You can use the %pre-install section to run commands after the system has been
partitioned, filesystems created, and everything is mounted under /mnt/sysimage
Like %pre these scripts do not run in the chrooted environment.

Each %pre-install section is required to be closed with a corresponding %end.

optional arguments:

``--erroronfail``

    If the error script fails, this option will cause an
    error dialog to be displayed and will halt installation.
    The error message will direct you to where the cause of
    the failure is logged.

    .. versionadded:: Fedora4

``--interpreter /usr/bin/python``

    Allows you to specify a different scripting language,
    such as Python. Replace /usr/bin/python with the
    scripting language of your choice.

    .. versionadded:: Fedora4

``--log LOG, --logfile LOG``

    Log all messages from the script to the given log file.

    .. versionadded:: Fedora4

Chapter 9. Pre-installation script
==================================

::

    %pre [--erroronfail] [--interpreter /usr/bin/python] [--log LOG]

You can add commands to run on the system immediately after the ks.cfg
has been parsed and the lang, keyboard, and url options have been
processed. This section must be at the end of the kickstart file (after
the commands) and must start with the %pre command. You can access the
network in the %pre section; however, name service has not been
configured at this point, so only IP addresses will work.

Preinstallation scripts are required to be closed with %end.

If your script spawns a daemon process, you must make sure to close
``stdout`` and ``stderr``. Doing so is standard procedure for creating
daemons. If you do not close these file descriptors, the installation
will appear hung as anaconda waits for an EOF from the script.

.. note::

    The pre-install script is not run in the chroot environment.

optional arguments:

``--erroronfail``

    If the error script fails, this option will cause an
    error dialog to be displayed and will halt installation.
    The error message will direct you to where the cause of
    the failure is logged.

    .. versionadded:: Fedora4

``--interpreter /usr/bin/python``

    Allows you to specify a different scripting language,
    such as Python. Replace /usr/bin/python with the
    scripting language of your choice.

    .. versionadded:: Fedora4

``--log LOG, --logfile LOG``

    Log all messages from the script to the given log file.

    .. versionadded:: Fedora4

Example
-------

Here is an example %pre section::

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
