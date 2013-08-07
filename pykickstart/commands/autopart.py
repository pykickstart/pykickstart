#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008, 2012 Red Hat, Inc.
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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC3_AutoPart(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.autopart = kwargs.get("autopart", False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.autopart:
            retval += "autopart\n"

        return retval

    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "autopart")

        self.autopart = True
        return self

class F9_AutoPart(FC3_AutoPart):
    removedKeywords = FC3_AutoPart.removedKeywords
    removedAttrs = FC3_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        FC3_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.encrypted = kwargs.get("encrypted", False)
        self.passphrase = kwargs.get("passphrase", "")

        self.op = self._getParser()

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.autopart:
            retval += "autopart"

        if self.encrypted:
            retval += " --encrypted"

            if self.passphrase != "":
                retval += " --passphrase=\"%s\""% self.passphrase

        if retval != "":
            retval += "\n"

        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--encrypted", action="store_true", default=False)
        op.add_option("--passphrase")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)
        self.autopart = True
        return self

class F12_AutoPart(F9_AutoPart):
    removedKeywords = F9_AutoPart.removedKeywords
    removedAttrs = F9_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F9_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)

        self.escrowcert = kwargs.get("escrowcert", "")
        self.backuppassphrase = kwargs.get("backuppassphrase", False)

    def __str__(self):
        retval = F9_AutoPart.__str__(self)

        if self.encrypted and self.escrowcert != "":
            retval = retval.strip()

            retval += " --escrowcert=\"%s\"" % self.escrowcert

            if self.backuppassphrase:
                retval += " --backuppassphrase"

            retval += "\n"

        return retval

    def _getParser(self):
        op = F9_AutoPart._getParser(self)
        op.add_option("--escrowcert")
        op.add_option("--backuppassphrase", action="store_true", default=False)
        return op

class RHEL6_AutoPart(F12_AutoPart):
    removedKeywords = F12_AutoPart.removedKeywords
    removedAttrs = F12_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F12_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.cipher = kwargs.get("cipher", "")

    def __str__(self):
        retval = F12_AutoPart.__str__(self)

        if self.encrypted and self.cipher:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --cipher=\"%s\"" % self.cipher
            retval += "\n"

        return retval

    def _getParser(self):
        op = F12_AutoPart._getParser(self)
        op.add_option("--cipher")
        return op

    def parse(self, args):
        # call the overriden command to do it's job first
        retval = F12_AutoPart.parse(self, args)

        # Using autopart together with other partitioning command such as
        # part/partition, raid, logvol or volgroup can lead to hard to debug
        # behavior that might among other result into an unbootable system.
        #
        # Therefore if any of those commands is detected in the same kickstart
        # together with autopart, an error is raised and installation is
        # aborted.
        conflicting_command = ""

        # currentCmd != "" indicates that the corresponding
        # command has been seen in kickstart
        if self.handler.partition.currentCmd:
            conflicting_command = "part/partition)"
        elif self.handler.raid.currentCmd:
            conflicting_command = "raid"
        elif self.handler.volgroup.currentCmd:
            conflicting_command = "volgroup"
        elif self.handler.logvol.currentCmd:
            conflicting_command = "logvol"

        if conflicting_command:
            # allow for translation of the error message
            errorMsg = _("The %s and autopart commands can't be used at the same time")
            # set the placeholder with the offending command
            errorMsg = errorMsg % conflicting_command
            raise KickstartParseError, formatErrorMsg(self.lineno, msg=errorMsg)
        return retval
