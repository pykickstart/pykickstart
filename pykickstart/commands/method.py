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
from pykickstart.version import FC3
from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class FC3_Method(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    # These are all set up as part of the base KickstartCommand.  We want to
    # make sure looking them up gets redirected to the right place.
    internals = ["method",
                 "writePriority", "currentCmd", "currentLine", "handler", "lineno", "seen"]

    _methods = ["cdrom", "harddrive", "nfs", "url"]

    def _clear_seen(self):
        """ Reset all the method's seen attrs to False"""
        for method in self._methods:
            setattr(getattr(self.handler, method), "seen", False)

    def __getattr__(self, name):
        if name in self.internals:
            if name == "method":
                for method in self._methods:
                    if getattr(self.handler, method).seen:
                        return method
                return None
            else:
                return object.__getattribute__(self, name)

        # Return name from first seen handler, or url
        for method in self._methods:
            if getattr(self.handler, method).seen:
                return getattr(getattr(self.handler, method), name)

        return getattr(self.handler.url, name)

    def __setattr__(self, name, value):
        if name in self.internals:
            if name == "method":
                self._clear_seen()
                if value == "cdrom":
                    setattr(self.handler.cdrom, "seen", True)
                elif value == "harddrive":
                    setattr(self.handler.harddrive, "seen", True)
                elif value == "nfs":
                    setattr(self.handler.nfs, "seen", True)
                elif value == "url":
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

    def _getParser(self):
        # TODO:
        # this command appears to be duplicate of cdrom, nfs, url and liveimg
        # what is it's purpose ?
        return KSOptionParser(prog="method", description="", version=FC3)


# These are all just for compat.  Calling into the appropriate version-specific
# method command will deal with making sure the right options are used.
class FC6_Method(FC3_Method):
    pass

class F13_Method(FC6_Method):
    pass

class F14_Method(F13_Method):
    pass

class RHEL6_Method(F14_Method):
    pass

class F18_Method(F14_Method):
    pass

class F19_Method(FC3_Method):
    removedKeywords = FC3_Method.removedKeywords
    removedAttrs = FC3_Method.removedAttrs

    _methods = FC3_Method._methods + ["liveimg"]

    def __getattr__(self, name):
        if name == "handler":
            raise AttributeError()

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
                self._clear_seen()
                setattr(self.handler.liveimg, "seen", True)
            else:
                FC3_Method.__setattr__(self, name, value)
        elif self.handler.liveimg.seen:
            setattr(self.handler.liveimg, name, value)
        else:
            FC3_Method.__setattr__(self, name, value)
