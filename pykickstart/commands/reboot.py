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
from pykickstart.version import versionToLongString, FC3, FC6, F18, F23
from pykickstart.base import KickstartCommand
from pykickstart.constants import KS_REBOOT, KS_SHUTDOWN, KS_WAIT
from pykickstart.options import KSOptionParser

class FC3_Reboot(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.action = kwargs.get("action", None)

    def _getArgsAsStr(self):
        return ""

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.action == KS_REBOOT:
            retval += "# Reboot after installation\nreboot"
            retval += self._getArgsAsStr() + "\n"
        elif self.action == KS_SHUTDOWN:
            retval += "# Shutdown after installation\nshutdown"
            retval += self._getArgsAsStr() + "\n"

        return retval

    def parse(self, args):
        if self.currentCmd == "reboot":
            self.action = KS_REBOOT
        else:
            self.action = KS_SHUTDOWN

        return self

    def _getParser(self):
        op = KSOptionParser(prog="reboot|poweroff|shutdown", description="""

                            ``reboot``

                            Reboot after the installation is complete. Normally,
                            kickstart displays a message and waits for the user
                            to press a key before rebooting.

                            ``poweroff``

                            Turn off the machine after the installation is complete.
                            Normally, kickstart displays a message and waits for
                            the user to press a key before rebooting.

                            ``shutdown``

                            At the end of installation, shut down the machine.
                            This is the same as the poweroff command. Normally,
                            kickstart displays a message and waits for the user
                            to press a key before rebooting.""", version=FC3)
        return op


class FC6_Reboot(FC3_Reboot):
    removedKeywords = FC3_Reboot.removedKeywords
    removedAttrs = FC3_Reboot.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Reboot.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.eject = kwargs.get("eject", False)

    def _getArgsAsStr(self):
        retval = FC3_Reboot._getArgsAsStr(self)

        if self.eject:
            retval += " --eject"

        return retval

    def _getParser(self):
        op = FC3_Reboot._getParser(self)
        op.add_argument("--eject", action="store_true", version=FC6,
                        default=False, help="""
                        Attempt to eject CD or DVD media before rebooting.
                        """)
        return op

    def parse(self, args):
        FC3_Reboot.parse(self, args)
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class F18_Reboot(FC6_Reboot):
    removedKeywords = FC6_Reboot.removedKeywords
    removedAttrs = FC6_Reboot.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC6_Reboot.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

    def __str__(self):
        retval = FC6_Reboot.__str__(self)

        if self.action == KS_WAIT:
            retval = "# Halt after installation\nhalt"
            retval += self._getArgsAsStr() + "\n"

        return retval

    def parse(self, args):
        FC6_Reboot.parse(self, args)
        if self.currentCmd == "halt":
            self.action = KS_WAIT
        return self

    def _getParser(self):
        op = FC6_Reboot._getParser(self)
        op.prog += "|halt"
        op.description += dedent("""

        ``halt``

        At the end of installation, display a message and wait for the user to
        press a key before rebooting. This is the default action.

        .. versionchanged:: %s

        The 'halt' command was added!

        """ % versionToLongString(F18))
        return op

class F23_Reboot(F18_Reboot):
    removedKeywords = F18_Reboot.removedKeywords
    removedAttrs = F18_Reboot.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        F18_Reboot.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.kexec = kwargs.get("kexec", False)

    def _getArgsAsStr(self):
        retval = F18_Reboot._getArgsAsStr(self)

        if self.kexec:
            retval += " --kexec"

        return retval

    def _getParser(self):
        op = F18_Reboot._getParser(self)
        op.add_argument("--kexec", action="store_true", version=F23,
                        default=False, help="""
                        Use kexec to reboot into the new system, bypassing
                        BIOS/Firmware and bootloader.""")
        return op
