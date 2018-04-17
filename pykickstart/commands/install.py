#
# Alexander Todorov <atodorov@redhat.com>
#
# Copyright 2016 Red Hat, Inc.
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
from pykickstart.base import DeprecatedCommand
from pykickstart.version import F20, F29, versionToLongString
from pykickstart.commands.upgrade import F11_Upgrade


class F20_Install(F11_Upgrade):
    """
        The upgrade command has been deprecated in Fedora 20. This
        class should be used for any further updates to the install
        command. This separation is required because there's no
        clean way of deprecating only half of the behavior of some
        command class and still have the handlers map to the latest
        possible version of this class!
    """
    def _getParser(self):
        op = super(F20_Install, self)._getParser()
        op.prog = "install"
        op.description = """
            Install a fresh system. You must specify the type of
            installation from one of cdrom, harddrive, nfs, or url
            (for ftp or http installations).
            The install command and the installation method command
            must be on separate lines.

            Important: before Fedora 20 this command was known as
            install or upgrade but the upgrade part was deprecated!
        """
        op.version = F20

        return op

    def parse(self, args):
        super(F20_Install, self).parse(args)
        # since F20 we always return False for upgrades
        self.upgrade = False

        return self


class F29_Install(DeprecatedCommand, F20_Install):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = F20_Install._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F29)
        return op
