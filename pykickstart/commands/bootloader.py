#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import string

from pykickstart.base import *
from pykickstart.options import *

class FC3_Bootloader(KickstartCommand):
    def __init__(self, writePriority=0, appendLine="", driveorder=None,
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

    def __str__(self):
        if self.location != "":
            retval = "# System bootloader configuration\nbootloader"

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

            return retval + "\n"
        else:
            return ""

    def parse(self, args):
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

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

        if self.currentCmd == "lilo":
            self.useLilo = True

class FC4_Bootloader(FC3_Bootloader):
    def __init__(self, writePriority=0, appendLine="", driveorder=None,
                 forceLBA=False, location="", md5pass="", password="",
                 upgrade=False):
        KickstartCommand.__init__(self, writePriority)
        self.appendLine = appendLine

        if driveorder == None:
            driveorder = []

        self.driveorder = driveorder

        self.forceLBA = forceLBA
        self.location = location
        self.md5pass = md5pass
        self.password = password
        self.upgrade = upgrade

    def __str__(self):
        if self.location != "":
            retval = "# System bootloader configuration\nbootloader"

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

            return retval + "\n"
        else:
            return ""

    def parse(self, args):
        def driveorder_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--append", dest="appendLine")
        op.add_option("--location", dest="location", type="choice",
                      default="mbr",
                      choices=["mbr", "partition", "none", "boot"])
        op.add_option("--lba32", dest="forceLBA", action="store_true",
                      default=False)
        op.add_option("--password", dest="password", default="")
        op.add_option("--md5pass", dest="md5pass", default="")
        op.add_option("--upgrade", dest="upgrade", action="store_true",
                      default=False)
        op.add_option("--driveorder", dest="driveorder", action="callback",
                      callback=driveorder_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
