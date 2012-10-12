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
        # Rely on any error handling from baseclass
        FC3_AutoPart.parse(self, extra)

        self._setToSelf(self.op, opts)
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

class F16_AutoPart(F12_AutoPart):
    removedKeywords = F12_AutoPart.removedKeywords
    removedAttrs = F12_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F12_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.lvm = kwargs.get("lvm", True)

    def __str__(self):
        retval = F12_AutoPart.__str__(self)

        # If requested, disable LVM autopart
        if not self.lvm:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --nolvm"
            retval += "\n"

        return retval

    def _getParser(self):
        op = F12_AutoPart._getParser(self)
        op.add_option("--nolvm", action="store_false", dest="lvm",
            default=True)
        return op

class F17_AutoPart(F16_AutoPart):
    def __init__(self, writePriority=100, *args, **kwargs):
        F16_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.type = kwargs.get("type", None)
        self.typeMap = { "lvm": AUTOPART_TYPE_LVM,
                         "btrfs": AUTOPART_TYPE_BTRFS,
                         "plain": AUTOPART_TYPE_PLAIN,
                         "partition": AUTOPART_TYPE_PLAIN }

    def __str__(self):
        retval = F16_AutoPart.__str__(self)
        if self.type is not None:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --type="
            if self.type == AUTOPART_TYPE_LVM:
                retval += "lvm"
            elif self.type == AUTOPART_TYPE_BTRFS:
                retval += "btrfs"
            else:
                retval += "plain"
            retval += "\n"

        return retval

    def _getParser(self):
        def type_cb(option, opt_str, value, parser):
            if self.typeMap.has_key(value.lower()):
                parser.values.ensure_value(option.dest,
                                           self.typeMap[value.lower()])

        def nolvm_cb(option, opt_str, value, parser):
            parser.values.ensure_value(option.dest, AUTOPART_TYPE_PLAIN)

        op = F16_AutoPart._getParser(self)
        op.add_option("--nolvm", action="callback", callback=nolvm_cb,
                      dest="type", nargs=0)

        op.add_option("--type", action="callback", callback=type_cb,
                      dest="type", nargs=1, type="string")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args, lineno=self.lineno)
        # Rely on any error handling from baseclass
        F16_AutoPart.parse(self, extra)

        self._setToSelf(self.op, opts)

        # make this always True to avoid writing --nolvm
        self.lvm = True

        return self

class F18_AutoPart(F17_AutoPart):
    removedKeywords = F17_AutoPart.removedKeywords
    removedAttrs = F17_AutoPart.removedAttrs

    def __init__(self, writePriority=100, *args, **kwargs):
        F17_AutoPart.__init__(self, writePriority=writePriority, *args, **kwargs)
        self.cipher = kwargs.get("cipher", "")

    def __str__(self):
        retval = F17_AutoPart.__str__(self)

        if self.encrypted and self.cipher:
            # remove any trailing newline
            retval = retval.strip()
            retval += " --cipher=\"%s\"" % self.cipher
            retval += "\n"

        return retval

    def _getParser(self):
        op = F17_AutoPart._getParser(self)
        op.add_option("--cipher")
        return op
