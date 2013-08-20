#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2013 Red Hat, Inc.
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

class FC3_Method(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    # These are all set up as part of the base KickstartCommand.  We want to
    # make sure looking them up gets redirected to the right place.
    internals = ["method",
                 "writePriority", "currentCmd", "currentLine", "handler", "lineno", "seen"]

    def __getattr__(self, name):
        if self.handler.cdrom.seen:
            if name == "method":
                return "cdrom"
            else:
                return getattr(self.handler.cdrom, name)
        elif self.handler.harddrive.seen:
            if name == "method":
                return "harddrive"
            else:
                return getattr(self.handler.harddrive, name)
        elif self.handler.nfs.seen:
            if name == "method":
                return "nfs"
            else:
                return getattr(self.handler.nfs, name)
        else:
            if name == "method":
                return "url"
            else:
                return getattr(self.handler.url, name)

    def __setattr__(self, name, value):
        if name in self.internals:
            if name == "method" and value == "cdrom":
                setattr(self.handler.cdrom, "seen", True)
            elif name == "method" and value == "harddrive":
                setattr(self.handler.harddrive, "seen", True)
            elif name == "method" and value == "nfs":
                setattr(self.handler.nfs, "seen", True)
            elif name == "method" and value == "url":
                setattr(self.handler.url, "seen", True)
            KickstartCommand.__setattr__(self, name, value)
        elif self.handler.cdrom.seen:
            setattr(self.handler.cdrom, name, value)
        elif self.handler.harddrive.seen:
            setattr(self.handler.harddrive, name, value)
        elif self.handler.nfs.seen:
            setattr(self.handler.nfs, name, value)
        else:
            setattr(self.handler.url, name, value)

# These are all just for compat.  Calling into the appropriate version-specific
# method command will deal with making sure the right options are used.
FC6_Method = FC3_Method

F13_Method = FC6_Method

F14_Method = F13_Method

RHEL6_Method = F14_Method

F18_Method = F14_Method

class F19_Method(FC3_Method):
    removedKeywords = FC3_Method.removedKeywords
    removedAttrs = FC3_Method.removedAttrs

    def __getattr__(self, name):
        if self.handler.liveimg.seen:
            if name == "method":
                return "liveimg"
            else:
                return getattr(self.handler.liveimg, name)
        else:
            return FC3_Method.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name in self.internals:
            if name == "method" and value == "liveimg":
                setattr(self.handler.liveimg, "seen", True)
            else:
                FC3_Method.__setattr__(self, name, value)
        elif self.handler.liveimg.seen:
            setattr(self.handler.liveimg, name, value)
        else:
            FC3_Method.__setattr__(self, name, value)
