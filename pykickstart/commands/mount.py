#
# Copyright (C) 2017  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Vratislav Podzimek <vpodzime@redhat.com>
#

from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser, mountpoint
from pykickstart.version import F27

from pykickstart.i18n import _

class F27_MountData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.mount_point = kwargs.get("mount_point", "")
        self.device = kwargs.get("device", "")
        self.format = kwargs.get("format", "")
        self.reformat = kwargs.get("reformat", False)
        self.mkfs_opts = kwargs.get("mkfs_opts", "")
        self.mount_opts = kwargs.get("mount_opts", "")

    def __eq__(self, other):
        if not other:
            return False

        return self.mount_point == other.mount_point

    def __ne__(self, other):
        return not self == other

    def _getArgsAsStr(self):
        retval = "%s" % self.device

        retval += " %s" % self.mount_point or "none"

        if self.reformat:
            retval += " --reformat"
            if self.format:
                retval += "=%s" % self.format

        if self.mkfs_opts:
            retval += " --mkfsoptions=\"%s\"" % self.mkfs_opts

        if self.mount_opts:
            retval += " --mountoptions=\"%s\"" % self.mount_opts

        return retval

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "mount %s\n" % self._getArgsAsStr()
        return retval


class F27_Mount(KickstartCommand):
    """The 'mount' kickstart command"""

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.op = self._getParser()
        self.mount_points = kwargs.get("mount_points") or list()

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        for mpoint in self.mount_points:
            retval += str(mpoint)

        if retval != "":
            retval = "# Mount points configuration\n" + retval + "\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="mount", description="""
                            Assigns a mount point to a block device and
                            optionally reformats it to a given format. It at
                            least requires a device and a mount point where the
                            mount point can be ``none`` in case the format on
                            the device is not mountable or in case the device
                            should just be reformatted.

                            The difference between this command and the other
                            commands for storage configuration (``part``,
                            ``logvol``,...) is that it doesn't require the whole
                            storage stack to be described in the kickstart
                            file. The user just needs to make sure that the
                            specified block device exists in the system. The
                            installer doesn't necessarily have to know all the
                            details about of the given device. If, on the other
                            hand, the installer is supposed to **create** the
                            storage stack with all the devices mounted at
                            various places, the ``part``, ``logvol``, ``raid``,
                            etc. commands have to be used.
                            """, version=F27)

        op.add_argument("device", metavar="<device>", nargs=1, version=F27,
                        help="""The block device to mount""")
        op.add_argument("mntpoint", metavar="<mntpoint>", type=mountpoint, nargs=1,
                        version=F27, help="""
                        The ``<mntpoint>`` is where the <device> will be
                        mounted.  Must be a valid mount point, for example
                        ``/``, ``/usr``, ``/home``, or ``none`` if the device
                        cannot (e.g. swap) or should not be mounted.""")

        op.add_argument("--reformat", dest="reformat", nargs="?", version=F27, const=True, default=False,
                        help="Specifies the new format (e.g. a file system) for the device.")
        op.add_argument("--mkfsoptions", dest="mkfs_opts", action="store", version=F27,
                        help="""
                        Specifies additional parameters to be passed to the
                        program that makes a filesystem on this partition. No
                        processing is done on the list of arguments, so they
                        must be supplied in a format that can be passed directly
                        to the mkfs program.  This means multiple options should
                        be comma-separated or surrounded by double quotes,
                        depending on the filesystem.""")
        op.add_argument("--mountoptions", dest="mount_opts", action="store", version=F27,
                        help="""
                        Specifies a free form string of options to be used when
                        mounting the filesystem. This string will be copied into
                        the /etc/fstab file of the installed system and should
                        be enclosed in quotes.""")

        return op

    def parse(self, args):
        # the 'mount' command can't be used together with any other
        # partitioning-related command
        conflicting_command = None

        # seen indicates that the corresponding
        # command has been seen in kickstart
        if self.handler.autopart.seen:
            conflicting_command = "autopart"
        if self.handler.partition.seen:
            conflicting_command = "part/partition"
        elif self.handler.raid.seen:
            conflicting_command = "raid"
        elif self.handler.volgroup.seen:
            conflicting_command = "volgroup"
        elif self.handler.logvol.seen:
            conflicting_command = "logvol"
        elif hasattr(self.handler, "reqpart") and self.handler.reqpart.seen:
            conflicting_command = "reqpart"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The '%s' and 'mount' commands can't be used at the same time") % \
                         conflicting_command
            raise KickstartParseError(errorMsg, lineno=self.lineno)

        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if extra:
            mapping = {"command": "mount", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        md = self.dataClass()  # pylint: disable=not-callable
        self.set_to_obj(ns, md)
        md.lineno = self.lineno
        md.device = ns.device[0]
        md.mount_point = ns.mntpoint[0]

        if md.mount_point.lower() != "none" and not md.mount_point.startswith("/"):
            raise KickstartParseError(_("Invalid mount point '%s' given") % md.mount_point, lineno=self.lineno)

        if md.reformat is False and md.mkfs_opts:
            raise KickstartParseError(_("'--mkfsoptions' requires --reformat"), lineno=self.lineno)

        # The semantics is as follows:
        #   --reformat          -> just reformat with the same format as existing
        #   --reformat=SOME_FMT -> reformat to given format
        #   no '--reformat'     -> don't reformat
        #
        # md.reformat can either be 'False' (not specified), 'True' (just
        # '--reformat') or a non-empty string ('--reformat=FORMAT'). Only the
        # last case requires special treatment.
        if md.reformat and md.reformat is not True:
            # a new format given
            md.format = md.reformat
            md.reformat = True

        return md

    def dataList(self):
        return self.mount_points

    @property
    def dataClass(self):
        return self.handler.MountData
