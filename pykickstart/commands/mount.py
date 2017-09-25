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
from pykickstart.errors import KickstartValueError, KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class RHEL7_MountData(BaseData):
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


class RHEL7_Mount(KickstartCommand):
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
        op = KSOptionParser()

        op.add_option("--reformat", dest="reformat", default=False)
        op.add_option("--mkfsoptions", dest="mkfs_opts", action="store")
        op.add_option("--mountoptions", dest="mount_opts", action="store")

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
            raise KickstartParseError(formatErrorMsg(self.lineno, msg=errorMsg))

        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)

        if len(extra) != 2:
            raise KickstartValueError(formatErrorMsg(self.lineno,
                                                     msg=_("Device and mount point required for %s") % "mount"))

        if extra[1].lower() != "none" and not extra[1].startswith("/"):  # the mount point
            raise KickstartValueError(formatErrorMsg(self.lineno,
                                                     msg=_("Invalid mount point '%s' given") % extra[1]))

        if opts.reformat is False and opts.mkfs_opts:
            raise KickstartValueError(formatErrorMsg(self.lineno,
                                                     msg=_("'--mkfsoptions' requires --reformat")))

        md = self.handler.MountData()
        md.lineno = self.lineno
        md.device = extra[0]
        md.mount_point = extra[1]
        md.mkfs_opts = opts.mkfs_opts
        md.mount_opts = opts.mount_opts

        if opts.reformat is False:
            # the default
            md.reformat = False
        elif len(opts.reformat) != 0:
            # a new format given
            md.reformat = True
            md.format = opts.reformat
        else:
            # XXX: OptionParser doesn't support this, but argparse does so
            #      better be ready
            # just '--reformat' specified
            md.reformat = True

        return md

    def dataList(self):
        return self.mount_points

