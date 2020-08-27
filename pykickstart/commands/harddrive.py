#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007, 2009, 2013 Red Hat, Inc.
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
from pykickstart.version import FC3, F33
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_HardDrive(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.biospart = kwargs.get("biospart", None)
        self.partition = kwargs.get("partition", None)
        self.dir = kwargs.get("dir", None)

        self.op = self._getParser()

        self.deleteRemovedAttrs()

    def __eq__(self, other):
        if not other:
            return False

        return self.biospart == other.biospart and self.partition == other.partition and self.dir == other.dir

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use hard drive installation media\n"

        if self.biospart is not None:
            retval += "harddrive --dir=%s --biospart=%s\n" % (self.dir, self.biospart)
        else:
            retval += "harddrive --dir=%s --partition=%s\n" % (self.dir, self.partition)

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="harddrive", description="""
            Install from a directory of ISO images on a local drive, which must
            be either vfat or ext2. In addition to this directory, you must also
            provide the install.img in some way. You can either do this by
            booting off the boot.iso or by creating an images/ directory in the
            same directory as the ISO images and placing install.img in there.
            """, version=FC3)
        op.add_argument("--biospart", version=FC3,
                        help="BIOS partition to install from (such as 82p2).")
        op.add_argument("--partition", version=FC3,
                        help="Partition to install from (such as, sdb2).")
        op.add_argument("--dir", required=True, version=FC3, help="""
                        Directory containing both the ISO images and the
                        images/install.img. For example::

                        ``harddrive --partition=hdb2 --dir=/tmp/install-tree``
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        if self.biospart is None and self.partition is None or \
           self.biospart is not None and self.partition is not None:
            raise KickstartParseError(_("One of biospart or partition options must be specified."), lineno=self.lineno)

        return self


class F33_HardDrive(FC3_HardDrive):
    removedKeywords = KickstartCommand.removedKeywords + ["biospart"]
    removedAttrs = KickstartCommand.removedAttrs + ["biospart"]

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_HardDrive.__init__(self, writePriority, *args, **kwargs)

    def __eq__(self, other):
        if not other:
            return False

        return self.partition == other.partition and self.dir == other.dir

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if not self.seen:
            return retval

        retval += "# Use hard drive installation media\n"
        retval += "harddrive --dir=%s --partition=%s\n" % (self.dir, self.partition)

        return retval

    def _getParser(self):
        op = FC3_HardDrive._getParser(self)
        op.remove_argument("--biospart", version=F33)
        op.add_argument("--partition", required=True, version=F33,
                        help="Partition to install from (such as, sdb2).")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        return self
