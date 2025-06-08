#
# Copyright 2025 Red Hat, Inc.
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
from pykickstart.version import F43
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class F43_RDP(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.enabled = kwargs.get("enabled", False)
        self.password = kwargs.get("password", "")
        self.username = kwargs.get("username", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if not self.enabled:
            return retval

        retval += "rdp"

        if self.username:
            retval += " --username=%s" % self.username
        if self.password:
            retval += " --password=%s" % self.password

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(prog="rdp", description="""
                            Allows the graphical installation to be viewed
                            remotely via RDP (Remote Desktop Protocol). This
                            method is usually preferred over text mode, as
                            there are some size and language limitations in
                            text installs. With no options, this
                            command will enable RDP mode in Anaconda and wait
                            for user to locally set username and password.""",
                            version=F43)
        op.add_argument("--username", version=F43, help="""
                        Set a username which must be provided to connect by
                        the RDP client.""")
        op.add_argument("--password", version=F43, help="""
                        Set a password which must be provided to connect by
                        the RDP client.""")
        return op

    def parse(self, args):
        self.enabled = True
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self
