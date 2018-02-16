#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2015 Red Hat, Inc.
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
from pykickstart.version import F23
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class F23_ReqPart(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.reqpart = kwargs.get("reqpart", False)
        self.addBoot = kwargs.get("addBoot", False)

        self.op = self._getParser()

    def _getArgsAsStr(self):
        retval = ""

        if self.addBoot:
            retval += " --add-boot"

        return retval

    def __str__(self):
        retval = KickstartCommand.__str__(self)
        if self.reqpart:
            retval += "reqpart%s\n" % self._getArgsAsStr()
        return retval

    def _getParser(self):
        op = KSOptionParser(prog="reqpart", description="""
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
                            layout.""", version=F23)
        op.add_argument("--add-boot", action="store_true", version=F23,
                        dest="addBoot", default=False, help="""
                        Create a separate ``/boot`` partition in addition to the
                        platform-specific partition created by the base command.
                        """)
        return op

    def parse(self, args):
        # Using reqpart and autopart at the same time is not allowed.
        if self.handler.autopart.seen:
            errorMsg = _("The %s and reqpart commands can't be used at the same time") % \
                         "autopart"
            raise KickstartParseError(errorMsg, lineno=self.lineno)
        # the same applies to the 'mount' command
        if hasattr(self.handler, "mount") and self.handler.mount.seen:
            errorMsg = _("The mount and reqpart commands can't be used at the same time")
            raise KickstartParseError(errorMsg, lineno=self.lineno)

        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        self.reqpart = True
        return self

class RHEL7_ReqPart(F23_ReqPart):
    pass
