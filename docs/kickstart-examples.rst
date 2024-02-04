
.. _kickstart-examples:

Kickstart Examples
************************

Selecting disks by size
==========================

An example ``%pre`` section which selects disks by size.

::

    # Partition information is created during install using the %pre section
    %pre --interpreter /bin/bash --log /tmp/ks_pre.log

        # Dump whole SCSI/IDE disks out sorted from smallest to largest
        # ouputting just the name
        disks=(`lsblk -n -o NAME -l -b -x SIZE -d -I 8,3`) || exit 1

        # We are assuming we have 3 disks which will be used
        # and we will create some variables to represent
        d0=${disks[0]}
        d1=${disks[1]}
        d2=${disks[2]}

        echo "part /home --fstype="xfs" --ondisk=$d2 --grow" >> /tmp/disks
        echo "part swap --fstype="swap" --ondisk=$d0 --size=4096" >> /tmp/disks
        echo "part / --fstype="xfs" --ondisk=$d1 --grow" >> /tmp/disks
        echo "part /boot --fstype="xfs" --ondisk=$d1 --size=1024" >> /tmp/disks
    %end


Leverage ``%include /tmp/disks`` in the kickstart file to utilize.