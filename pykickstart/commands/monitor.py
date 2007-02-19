#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3Monitor(KickstartCommand):
    def __init__(self, writePriority=0, hsync="", monitor="", vsync=""):
        KickstartCommand.__init__(self, writePriority)
        self.hsync = hsync
        self.monitor = monitor
        self.vsync = vsync

    def __str__(self):
        retval = "monitor"

        if self.hsync != "":
            retval += " --hsync=%s" % self.hsync
        if self.monitor != "":
            retval += " --monitor=\"%s\"" % self.monitor
        if self.vsync != "":
            retval += " --vsync=%s" % self.vsync

        if retval != "monitor":
            return retval + "\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--hsync")
        op.add_option("--monitor")
        op.add_option("--vsync")

        (opts, extra) = op.parse_args(args=args)

        if extra:
            mapping = {"cmd": "monitor", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(cmd)s command: %(options)s") % mapping)

        self._setToSelf(op, opts)

class FC6Monitor(FC3Monitor):
    def __init__(self, writePriority=0, hsync="", monitor="", probe=True,
                 vsync=""):
        FC3Monitor.__init__(self, writePriority, hsync=hsync,
                            monitor=monitor, vsync=vsync)
        self.probe = probe

    def __str__(self):
        retval = "monitor"

        if self.hsync != "":
            retval += " --hsync=%s" % self.hsync
        if self.monitor != "":
            retval += " --monitor=\"%s\"" % self.monitor
        if not self.probe:
            retval += " --noprobe"
        if self.vsync != "":
            retval += " --vsync=%s" % self.vsync

        if retval != "monitor":
            return retval + "\n"
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--hsync", dest="hsync")
        op.add_option("--monitor", dest="monitor")
        op.add_option("--noprobe", dest="probe", action="store_false",
                      default=True)
        op.add_option("--vsync", dest="vsync")

        (opts, extra) = op.parse_args(args=args)

        if extra:
            mapping = {"cmd": "monitor", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(cmd)s command: %(options)s") % mapping)

        self._setToSelf(op, opts)
