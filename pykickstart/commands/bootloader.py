#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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
import string

from pykickstart.base import *
from pykickstart.options import *

class FC3_Bootloader(KickstartCommand):
    def __init__(self, writePriority=10, appendLine="", driveorder=None,
                 forceLBA=False, linear=True, location="", md5pass="",
                 password="", upgrade=False, useLilo=False):
        KickstartCommand.__init__(self, writePriority)
        self.appendLine = appendLine

        if driveorder == None:
            driveorder = []

        self.driveorder = driveorder

        self.forceLBA = forceLBA
        self.linear = linear
        self.location = location
        self.md5pass = md5pass
        self.password = password
        self.upgrade = upgrade
        self.useLilo = useLilo

    def _getArgsAsStr(self):
        retval = ""

        if self.appendLine != "":
            retval += " --append=\"%s\"" % self.appendLine
        if self.linear:
            retval += " --linear"
        if self.location:
            retval += " --location=%s" % self.location
        if self.forceLBA:
            retval += " --lba32"
        if self.password != "":
            retval += " --password=%s" % self.password
        if self.md5pass != "":
            retval += " --md5pass=%s" % self.md5pass
        if self.upgrade:
            retval += " --upgrade"
        if self.useLilo:
            retval += " --useLilo"
        if len(self.driveorder) > 0:
            retval += " --driveorder=%s" % string.join(self.driveorder, ",")

        return retval

    def __str__(self):
        if self.location != "":
            retval = "# System bootloader configuration\nbootloader"
            retval += self._getArgsAsStr()
            return retval + "\n"
        else:
            return ""

    def _getParser(self):
        def driveorder_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--append", dest="appendLine")
        op.add_option("--linear", dest="linear", action="store_true",
                      default=True)
        op.add_option("--nolinear", dest="linear", action="store_false")
        op.add_option("--location", dest="location", type="choice",
                      default="mbr",
                      choices=["mbr", "partition", "none", "boot"])
        op.add_option("--lba32", dest="forceLBA", action="store_true",
                      default=False)
        op.add_option("--password", dest="password", default="")
        op.add_option("--md5pass", dest="md5pass", default="")
        op.add_option("--upgrade", dest="upgrade", action="store_true",
                      default=False)
        op.add_option("--useLilo", dest="useLilo", action="store_true",
                      default=False)
        op.add_option("--driveorder", dest="driveorder", action="callback",
                      callback=driveorder_cb, nargs=1, type="string")
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if self.currentCmd == "lilo":
            self.useLilo = True

class FC4_Bootloader(FC3_Bootloader):
    def __init__(self, writePriority=10, appendLine="", driveorder=None,
                 forceLBA=False, location="", md5pass="", password="",
                 upgrade=False):
        FC3_Bootloader.__init__(self, writePriority)
        self.appendLine = appendLine

        if driveorder == None:
            driveorder = []

        self.driveorder = driveorder

        self.forceLBA = forceLBA
        self.location = location
        self.md5pass = md5pass
        self.password = password
        self.upgrade = upgrade

    def _getArgsAsStr(self):
        retval = ""
        if self.appendLine != "":
            retval += " --append=\"%s\"" % self.appendLine
        if self.location:
            retval += " --location=%s" % self.location
        if self.forceLBA:
            retval += " --lba32"
        if self.password != "":
            retval += " --password=%s" % self.password
        if self.md5pass != "":
            retval += " --md5pass=%s" % self.md5pass
        if self.upgrade:
            retval += " --upgrade"
        if len(self.driveorder) > 0:
            retval += " --driveorder=%s" % string.join(self.driveorder, ",")
        return retval

    def __str__(self):
        if self.location != "":
            retval = "# System bootloader configuration\nbootloader"
            retval += self._getArgsAsStr()
            return retval + "\n"
        else:
            return ""

    def _getParser(self):
        op = FC3_Bootloader._getParser(self)
        op.remove_option("--linear")
        op.remove_option("--nolinear")
        op.remove_option("--useLilo")
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class F8_Bootloader(FC4_Bootloader):
    def __init__(self, writePriority=10, appendLine="", driveorder=None,
                 forceLBA=False, location="", md5pass="", password="",
                 upgrade=False):
        FC4_Bootloader.__init__(self, writePriority, appendLine, driveorder,
                                forceLBA, location, md5pass, password, upgrade)

        self.timeout = None

    def _getArgsAsStr(self):
        ret = FC4_Bootloader._getArgsAsStr(self)

        if self.timeout is not None:
            ret += "--timeout=%d" %(self.timeout,)

        return ret

    def _getParser(self):
        op = FC4_Bootloader._getParser(self)
        op.add_option("--timeout", dest="timeout")
        return op
