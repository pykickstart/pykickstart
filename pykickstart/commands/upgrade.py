#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
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
from textwrap import dedent
from pykickstart.version import versionToLongString, FC3, F11, F20
from pykickstart.base import DeprecatedCommand, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC3_Upgrade(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.upgrade = kwargs.get("upgrade", None)
        self.op = self._getParser()

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.upgrade is None:
            return retval

        if self.upgrade:
            retval += "# Upgrade existing installation\nupgrade\n"
        else:
            retval += "# Install OS instead of upgrade\ninstall\n"

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="install|upgrade", description="""
                            Install a fresh system or upgrade an existing system.
                            Install is the default mode. For installation, you must
                            specify the type of installation from one of
                            cdrom, harddrive, nfs, or url (for ftp or http installations).
                            The install command and the installation method command
                            must be on separate lines.""",
                            version=FC3)
        return op

    def parse(self, args):
        self.op.parse_args(args=args, lineno=self.lineno)

        if self.currentCmd == "upgrade":
            self.upgrade = True
        else:
            self.upgrade = False

        return self

class F11_Upgrade(FC3_Upgrade):
    removedKeywords = FC3_Upgrade.removedKeywords
    removedAttrs = FC3_Upgrade.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Upgrade.__init__(self, writePriority, *args, **kwargs)

        self.op = self._getParser()
        self.root_device = kwargs.get("root_device", None)

    def __str__(self):
        if self.upgrade and (self.root_device is not None):
            retval = KickstartCommand.__str__(self)
            retval += "# Upgrade existing installation\nupgrade --root-device=%s\n" % self.root_device
        else:
            retval = FC3_Upgrade.__str__(self)

        return retval

    def _getParser(self):
        op = FC3_Upgrade._getParser(self)
        op.add_argument("--root-device", dest="root_device", version=F11,
                        help="""
                        On a system with multiple installs, this option specifies which
                        filesystem holds the installation to be upgraded. This can be
                        specified by device name, UUID=, or LABEL= just like the harddrive
                        command may be.""")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)

        if ns.root_device == "":
            raise KickstartParseError(_("Kickstart command %(command)s does not accept empty parameter %(parameter)s") % {"command": "upgrade", "parameter": "--root-device"}, lineno=self.lineno)
        else:
            self.root_device = ns.root_device

        if self.currentCmd == "upgrade":
            self.upgrade = True
        else:
            self.upgrade = False

        return self

class F20_Upgrade(DeprecatedCommand, F11_Upgrade):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = F11_Upgrade._getParser(self)
        op.description += dedent("""

                        .. deprecated:: %s

                        Starting with F18, upgrades are no longer supported in
                        anaconda and should be done with FedUp, the Fedora update
                        tool. Starting with F21, the DNF system-upgrade plugin is
                        recommended instead.  Therefore, the upgrade command
                        essentially does nothing.""" % versionToLongString(F20))
        return op
