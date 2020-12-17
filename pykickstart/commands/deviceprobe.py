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
from pykickstart.version import FC3, F29, F34, versionToLongString
from pykickstart.base import KickstartCommand, DeprecatedCommand, RemovedCommand
from pykickstart.options import KSOptionParser


class FC3_DeviceProbe(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.deviceprobe = kwargs.get("deviceprobe", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.deviceprobe:
            retval += "deviceprobe %s\n" % self.deviceprobe

        return retval

    def parse(self, args):
        self.deviceprobe = " ".join(args)
        return self

    def _getParser(self):
        return KSOptionParser(prog="deviceprobe", version=FC3, description="probe for devices")


class F29_DeviceProbe(DeprecatedCommand, FC3_DeviceProbe):

    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = FC3_DeviceProbe._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F29)
        return op

class F34_DeviceProbe(RemovedCommand, F29_DeviceProbe):
    def _getParser(self):
        op = F29_DeviceProbe._getParser(self)
        op.description += "\n\n.. versionremoved:: %s" % versionToLongString(F34)
        return op
