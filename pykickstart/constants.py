#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005-2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
CLEARPART_TYPE_LINUX = 0
CLEARPART_TYPE_ALL = 1
CLEARPART_TYPE_NONE = 2

DISPLAY_MODE_CMDLINE = 0
DISPLAY_MODE_GRAPHICAL = 1
DISPLAY_MODE_TEXT = 2

FIRSTBOOT_DEFAULT = 0
FIRSTBOOT_SKIP = 1
FIRSTBOOT_RECONFIG = 2

KS_MISSING_PROMPT = 0
KS_MISSING_IGNORE = 1

SELINUX_DISABLED = 0
SELINUX_ENFORCING = 1
SELINUX_PERMISSIVE = 2

KS_SCRIPT_PRE = 0
KS_SCRIPT_POST = 1
KS_SCRIPT_TRACEBACK = 2

KS_WAIT = 0
KS_REBOOT = 1
KS_SHUTDOWN = 2

KS_INSTKEY_SKIP = -99

BOOTPROTO_DHCP = "dhcp"
BOOTPROTO_BOOTP = "bootp"
BOOTPROTO_STATIC = "static"
