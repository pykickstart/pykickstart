#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005-2016 Red Hat, Inc.
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
CLEARPART_TYPE_LINUX = 0
CLEARPART_TYPE_ALL = 1
CLEARPART_TYPE_NONE = 2
CLEARPART_TYPE_LIST = 3

AUTOPART_TYPE_PLAIN = 0
AUTOPART_TYPE_BTRFS = 1
AUTOPART_TYPE_LVM = 2
AUTOPART_TYPE_LVM_THINP = 3

DISPLAY_MODE_CMDLINE = 0
DISPLAY_MODE_GRAPHICAL = 1
DISPLAY_MODE_TEXT = 2

FIRSTBOOT_DEFAULT = 0
FIRSTBOOT_SKIP = 1
FIRSTBOOT_RECONFIG = 2

KS_MISSING_PROMPT = 0
KS_MISSING_IGNORE = 1

KS_BROKEN_REPORT = 0
KS_BROKEN_IGNORE = 1

SELINUX_DISABLED = 0
SELINUX_ENFORCING = 1
SELINUX_PERMISSIVE = 2

SNAPSHOT_WHEN_POST_INSTALL = 0
SNAPSHOT_WHEN_PRE_INSTALL = 1

KS_SCRIPT_PRE = 0
KS_SCRIPT_POST = 1
KS_SCRIPT_TRACEBACK = 2
KS_SCRIPT_PREINSTALL = 3
KS_SCRIPT_ONERROR = 4

KS_WAIT = 0
KS_REBOOT = 1
KS_SHUTDOWN = 2

KS_INSTKEY_SKIP = -99

BOOTPROTO_DHCP = "dhcp"
BOOTPROTO_BOOTP = "bootp"
BOOTPROTO_STATIC = "static"
BOOTPROTO_QUERY = "query"
BOOTPROTO_IBFT = "ibft"

GROUP_REQUIRED = 0
GROUP_DEFAULT = 1
GROUP_ALL = 2

BIND_TO_MAC = "mac"

NVDIMM_MODE_SECTOR = "sector"

NVDIMM_ACTION_RECONFIGURE = "reconfigure"
NVDIMM_ACTION_USE = "use"

SECURE_BOOT_DEFAULT = -1
SECURE_BOOT_DISABLED = 0
SECURE_BOOT_ENABLED = 1
SECURE_BOOT_AUTO = 2
