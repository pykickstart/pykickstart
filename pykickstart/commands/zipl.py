#
# Copyright 2019 Red Hat, Inc.
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
from pykickstart.constants import SECURE_BOOT_AUTO, SECURE_BOOT_ENABLED, SECURE_BOOT_DISABLED, \
    SECURE_BOOT_DEFAULT
from pykickstart.version import F32
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser


class F32_Zipl(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=10, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.secure_boot = kwargs.get("secure_boot", SECURE_BOOT_DEFAULT)

    def _getParser(self):
        op = KSOptionParser(prog="zipl", version=F32, description="""
                            This command specifies the ZIPL configuration for s390x.
                            """)
        op.add_argument("--secure-boot", dest="secure_boot", version=F32,
                        action="store_const", const=SECURE_BOOT_AUTO,
                        help="""
                        Enable Secure Boot if supported by the installing machine.

                        **Note** When installed on a model newer than IBM z14, the
                        installed system cannot be booted from an IBM z14 and earlier
                        models.
                        """)
        op.add_argument("--force-secure-boot", dest="secure_boot", version=F32,
                        action="store_const", const=SECURE_BOOT_ENABLED,
                        help="""
                        Enable Secure Boot unconditionally.

                        **Note** Installation will fail on IBM z14 and earlier models.
                        """)
        op.add_argument("--no-secure-boot", dest="secure_boot", version=F32,
                        action="store_const", const=SECURE_BOOT_DISABLED,
                        help="""
                        Disable Secure Boot.

                        **Note** Secure Boot is not supported on IBM z14 and earlier
                        models, therefore choose '--no-secure-boot' if you intend to
                        boot the installed system on such models.
                        """)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.secure_boot is not SECURE_BOOT_DEFAULT:
            retval += "# ZIPL configuration\nzipl"
            retval += self._getArgsAsStr() + "\n"

        return retval

    def _getArgsAsStr(self):
        ret = ""

        if self.secure_boot == SECURE_BOOT_AUTO:
            ret += " --secure-boot"
        elif self.secure_boot == SECURE_BOOT_ENABLED:
            ret += " --force-secure-boot"
        elif self.secure_boot == SECURE_BOOT_DISABLED:
            ret += " --no-secure-boot"

        return ret


class RHEL8_Zipl(F32_Zipl):
    pass
