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
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class F8_DeviceData(BaseData):
    def __init__(self, moduleName="", moduleOpts=""):
        BaseData.__init__(self)
        self.moduleName = moduleName
        self.moduleOpts = moduleOpts

    def __str__(self):
        if self.moduleName != "":
            if self.moduleOpts != "":
                retval = "--opts=%s" % self.moduleOpts
            else:
                retval = ""

            return "device %s %s\n" % (self.moduleName, retval)
        else:
            return ""

class FC3_Device(KickstartCommand):
    def __init__(self, writePriority=0, type="", moduleName="", moduleOpts=""):
        KickstartCommand.__init__(self, writePriority)
        self.type = type
        self.moduleName = moduleName
        self.moduleOpts = moduleOpts

    def __str__(self):
        if self.moduleName != "":
            if self.moduleOpts != "":
                retval = "--opts=%s" % self.moduleOpts
            else:
                retval = ""

            return "device %s %s %s\n" % (self.type, self.moduleName, retval)
        else:
            return ""

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--opts", dest="moduleOpts", default="")
        return op

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 2:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("device command requires two arguments: module type and name"))

        self.opts = opts.moduleOpts
        self.type = extra[0]
        self.moduleName = extra[1]

class F8_Device(FC3_Device):
    def __init__(self, writePriority=0, deviceList=None):
        FC3_Device.__init__(self, writePriority)

        if deviceList == None:
            deviceList = []

        self.deviceList = deviceList

    def __str__(self):
        retval = ""
        for device in self.deviceList:
            retval += device.__str__()

        return retval

    def parse(self, args):
        op = self._getParser()
        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 1:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("%s command requires a single argument: %s") % ("device", "module name"))

        dd = F8_DeviceData()
        self._setToObj(op, opts, dd)
        dd.moduleName = extra[0]
        self.add(dd)

    def add(self, newObj):
        self.deviceList.append(newObj)
