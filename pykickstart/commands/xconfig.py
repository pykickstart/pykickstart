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

class FC3XConfig(KickstartCommand):
    def __init__(self, writePriority=0, card="", defaultdesktop="", depth=0,
                 hsync="", monitor="", noProbe=False, resolution="", server="",
                 startX=False, videoRam="", vsync=""):
        KickstartCommand.__init__(self, writePriority)
        self.card = card
        self.defaultdesktop = defaultdesktop
        self.depth = depth
        self.hsync = hsync
        self.monitor = monitor
        self.noProbe = noProbe
        self.resolution = resolution
        self.server = server
        self.startX = startX
        self.videoRam = videoRam
        self.vsync = vsync

    def __str__(self):
        retval = ""

        if self.card != "":
            retval += " --card=%s" % self.card
        if self.defaultdesktop != "":
            retval += " --defaultdesktop=%s" % self.defaultdesktop
        if self.depth != 0:
            retval += " --depth=%d" % self.depth
        if self.hsync != "":
            retval += " --hsync=%s" % self.hsync
        if self.monitor != "":
            retval += " --monitor=%s" % self.monitor
        if self.noProbe:
            retval += " --noprobe"
        if self.resolution != "":
            retval += " --resolution=%s" % self.resolution
        if self.server != "":
            retval += " --server=%s" % self.server
        if self.startX:
            retval += " --startxonboot"
        if self.videoRam != "":
            retval += " --videoram=%s" % self.videoRam
        if self.vsync != "":
            retval += " --vsync=%s" % self.vsync

        if retval != "":
            retval = "# X Window System configuration information\nxconfig %s\n" % retval

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--card")
        op.add_option("--defaultdesktop")
        op.add_option("--depth", action="store", type="int", nargs=1)
        op.add_option("--hsync")
        op.add_option("--monitor")
        op.add_option("--noprobe", dest="noProbe", action="store_true",
                      default=False)
        op.add_option("--resolution")
        op.add_option("--server")
        op.add_option("--startxonboot", dest="startX", action="store_true",
                      default=False)
        op.add_option("--videoram", dest="videoRam")
        op.add_option("--vsync")

        (opts, extra) = op.parse_args(args=args)
        if extra:
            mapping = {"command": "xconfig", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

        self._setToSelf(op, opts)

class FC6XConfig(FC3XConfig):
    def __init__(self, writePriority=0, driver="", defaultdesktop="", depth=0,
                 resolution="", startX=False, videoRam=""):
        FC3XConfig.__init__(self, writePriority)
        self.driver = driver
        self.defaultdesktop = defaultdesktop
        self.depth = depth
        self.resolution = resolution
        self.startX = startX
        self.videoRam = videoRam

    def __str__(self):
        retval = ""

        if self.driver != "":
            retval += " --driver=%s" % self.driver
        if self.defaultdesktop != "":
            retval += " --defaultdesktop=%s" % self.defaultdesktop
        if self.depth != 0:
            retval += " --depth=%d" % self.depth
        if self.resolution != "":
            retval += " --resolution=%s" % self.resolution
        if self.startX:
            retval += " --startxonboot"
        if self.videoRam != "":
            retval += " --videoram=%s" % self.videoRam

        if retval != "":
            retval = "# X Window System configuration information\nxconfig %s\n" % retval

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--card", deprecated=1)
        op.add_option("--driver", dest="driver")
        op.add_option("--defaultdesktop", dest="defaultdesktop")
        op.add_option("--depth", dest="depth", action="store", type="int",
                      nargs=1)
        op.add_option("--hsync", deprecated=1)
        op.add_option("--monitor", deprecated=1)
        op.add_option("--noprobe", deprecated=1)
        op.add_option("--resolution", dest="resolution")
        op.add_option("--startxonboot", dest="startX", action="store_true",
                      default=False)
        op.add_option("--videoram", dest="videoRam")
        op.add_option("--vsync", deprecated=1)

        (opts, extra) = op.parse_args(args=args)
        if extra:
            mapping = {"command": "xconfig", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

        self._setToSelf(op, opts)
