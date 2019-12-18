#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2008 Red Hat, Inc.
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
from pykickstart.version import FC3, FC6, F9, F10, F14
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class FC3_XConfig(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.card = kwargs.get("card", "")
        self.defaultdesktop = kwargs.get("defaultdesktop", "")
        self.depth = kwargs.get("depth", 0)
        self.hsync = kwargs.get("hsync", "")
        self.monitor = kwargs.get("monitor", "")
        self.noProbe = kwargs.get("noProbe", False)
        self.resolution = kwargs.get("resolution", "")
        self.server = kwargs.get("server", "")
        self.startX = kwargs.get("startX", False)
        self.videoRam = kwargs.get("videoRam", "")
        self.vsync = kwargs.get("vsync", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.card:
            retval += " --card=%s" % self.card
        if self.defaultdesktop:
            retval += " --defaultdesktop=%s" % self.defaultdesktop
        if self.depth != 0:
            retval += " --depth=%d" % self.depth
        if self.hsync:
            retval += " --hsync=%s" % self.hsync
        if self.monitor:
            retval += " --monitor=%s" % self.monitor
        if self.noProbe:
            retval += " --noprobe"
        if self.resolution:
            retval += " --resolution=%s" % self.resolution
        if self.server:
            retval += " --server=%s" % self.server
        if self.startX:
            retval += " --startxonboot"
        if self.videoRam:
            retval += " --videoram=%s" % self.videoRam
        if self.vsync:
            retval += " --vsync=%s" % self.vsync

        if retval:
            retval = "# X Window System configuration information\nxconfig %s\n" % retval

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="xconfig", description="""
                            Configures the X Window System. If this option is
                            not given, Anaconda will use X and attempt to
                            automatically configure. Please try this before
                            manually configuring your system.""", version=FC3)
        op.add_argument("--card", version=FC3, help="REMOVED")
        op.add_argument("--defaultdesktop", metavar="GNOME|KDE", help="""
                        Specify either GNOME or KDE to set the default desktop
                        (assumes that GNOME Desktop Environment and/or KDE
                        Desktop Environment has been installed through
                        %%packages).""", version=FC3)
        op.add_argument("--depth", type=int, version=FC3, help="REMOVED")
        op.add_argument("--hsync", version=FC3, help="REMOVED")
        op.add_argument("--monitor", version=FC3, help="REMOVED")
        op.add_argument("--noprobe", dest="noProbe", action="store_true",
                        default=False, version=FC3, help="REMOVED")
        op.add_argument("--resolution", version=FC3, help="REMOVED")
        op.add_argument("--server", version=FC3, help="REMOVED")
        op.add_argument("--startxonboot", dest="startX", action="store_true",
                        default=False, version=FC3, help="""
                        Use a graphical login on the installed system.""")
        op.add_argument("--videoram", dest="videoRam", version=FC3, help="REMOVED")
        op.add_argument("--vsync", version=FC3, help="REMOVED")
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class FC6_XConfig(FC3_XConfig):
    removedKeywords = FC3_XConfig.removedKeywords + ["card", "hsync", "monitor", "noProbe", "server", "vsync"]
    removedAttrs = FC3_XConfig.removedAttrs + ["card", "hsync", "monitor", "noProbe", "server", "vsync"]

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_XConfig.__init__(self, writePriority, *args, **kwargs)
        self.deleteRemovedAttrs()

        self.driver = kwargs.get("driver", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if hasattr(self, "driver") and self.driver:
            retval += " --driver=%s" % self.driver
        if self.defaultdesktop:
            retval += " --defaultdesktop=%s" % self.defaultdesktop
        if self.depth != 0:
            retval += " --depth=%d" % self.depth
        if hasattr(self, "resolution") and self.resolution:
            retval += " --resolution=%s" % self.resolution
        if self.startX:
            retval += " --startxonboot"
        if hasattr(self, "videoRam") and self.videoRam:
            retval += " --videoram=%s" % self.videoRam

        if retval:
            retval = "# X Window System configuration information\nxconfig %s\n" % retval

        return retval

    def _getParser(self):
        op = FC3_XConfig._getParser(self)
        op.add_argument("--card", deprecated=FC6)
        op.add_argument("--driver", version=FC6, help="REMOVED")
        op.add_argument("--hsync", deprecated=FC6)
        op.add_argument("--monitor", deprecated=FC6)
        op.add_argument("--noprobe", deprecated=FC6)
        op.add_argument("--vsync", deprecated=FC6)
        op.remove_argument("--server", version=FC6, help="")
        return op

class F9_XConfig(FC6_XConfig):
    removedKeywords = FC6_XConfig.removedKeywords
    removedAttrs = FC6_XConfig.removedAttrs

    def _getParser(self):
        op = FC6_XConfig._getParser(self)
        op.remove_argument("--card", version=F9)
        op.remove_argument("--hsync", version=F9)
        op.remove_argument("--monitor", version=F9)
        op.remove_argument("--noprobe", version=F9)
        op.remove_argument("--vsync", version=F9)
        return op

class F10_XConfig(F9_XConfig):
    removedKeywords = F9_XConfig.removedKeywords + ["driver", "resolution", "videoRam"]
    removedAttrs = F9_XConfig.removedAttrs + ["driver", "resolution", "videoRam"]

    def __init__(self, writePriority=0, *args, **kwargs):
        F9_XConfig.__init__(self, writePriority, *args, **kwargs)
        self.deleteRemovedAttrs()

    def _getParser(self):
        op = F9_XConfig._getParser(self)
        op.add_argument("--driver", deprecated=F10)
        op.add_argument("--depth", deprecated=F10)
        op.add_argument("--resolution", deprecated=F10)
        op.add_argument("--videoram", deprecated=F10)
        return op

class F14_XConfig(F10_XConfig):
    removedKeywords = F10_XConfig.removedKeywords
    removedAttrs = F10_XConfig.removedAttrs

    def _getParser(self):
        op = F10_XConfig._getParser(self)
        op.remove_argument("--driver", version=F14)
        op.remove_argument("--depth", version=F14)
        op.remove_argument("--resolution", version=F14)
        op.remove_argument("--videoram", version=F14)
        return op
