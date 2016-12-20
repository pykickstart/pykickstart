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
from pykickstart.version import versionToLongString, FC3, F24
from pykickstart.base import BaseData, DeprecatedCommand, KickstartCommand
from pykickstart.errors import KickstartParseError, KickstartParseWarning
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class F8_DeviceData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.moduleName = kwargs.get("moduleName", "")
        self.moduleOpts = kwargs.get("moduleOpts", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.moduleName == y.moduleName

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)

        if self.moduleName:
            retval += "device %s" % self.moduleName

            if self.moduleOpts:
                retval += " --opts=\"%s\"" % self.moduleOpts

        return retval + "\n"

class FC3_Device(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.type = kwargs.get("type", "")
        self.moduleName = kwargs.get("moduleName", "")
        self.moduleOpts = kwargs.get("moduleOpts", "")

    def __eq__(self, y):
        if not y:
            return False

        return self.moduleName == y.moduleName

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.moduleName:
            retval += "device %s %s" % (self.type, self.moduleName)

            if self.moduleOpts:
                retval += " --opts=\"%s\"" % self.moduleOpts

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(prog="device", description="""
            On most PCI systems, the installation program will autoprobe for
            Ethernet and SCSI cards properly. On older systems and some PCI
            systems, however, kickstart needs a hint to find the proper
            devices. The device command, which tells the installation program
            to install extra modules, is in this format:

            ``device <moduleName> --opts=<options>``

            ``<moduleName>``

            Replace with the name of the kernel module which should be
            installed.""", version=FC3)
        op.add_argument("--opts", dest="moduleOpts", default="", version=FC3,
                        help="""
                        Options to pass to the kernel module. For example:

                        ``--opts="aic152x=0x340 io=11"``
                        """)
        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) != 2:
            raise KickstartParseError(_("device command requires two arguments: module type and name"), lineno=self.lineno)
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "device", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.moduleOpts = ns.moduleOpts
        self.type = extra[0]
        self.moduleName = extra[1]
        return self

class F8_Device(FC3_Device):
    removedKeywords = FC3_Device.removedKeywords
    removedAttrs = FC3_Device.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_Device.__init__(self, writePriority, *args, **kwargs)
        self.deviceList = kwargs.get("deviceList", [])

    def __str__(self):
        retval = ""
        for device in self.deviceList:
            retval += device.__str__()

        return retval

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) != 1:
            raise KickstartParseError(_("%(command)s command requires a single argument: %(argument)s") % {"command": "device", "argument": "module name"}, lineno=self.lineno)
        elif any(arg for arg in extra if arg.startswith("-")):
            mapping = {"command": "device", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        dd = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, dd)
        dd.lineno = self.lineno
        dd.moduleName = extra[0]

        # Check for duplicates in the data list.
        if dd in self.dataList():
            warnings.warn(_("A module with the name %s has already been defined.") % dd.moduleName, KickstartParseWarning)

        return dd

    def dataList(self):
        return self.deviceList

    @property
    def dataClass(self):
        return self.handler.DeviceData

class F24_Device(DeprecatedCommand, F8_Device):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = F8_Device._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F24)
        return op
