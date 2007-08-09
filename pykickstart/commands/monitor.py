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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Monitor(KickstartCommand):
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

class FC6_Monitor(FC3_Monitor):
    def __init__(self, writePriority=0, hsync="", monitor="", probe=True,
                 vsync=""):
        FC3_Monitor.__init__(self, writePriority, hsync=hsync,
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
