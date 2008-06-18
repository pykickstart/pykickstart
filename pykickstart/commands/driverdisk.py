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
from pykickstart.base import *
from pykickstart.options import *

import gettext
_ = lambda x: gettext.ldgettext("pykickstart", x)

class FC3_DriverDiskData(BaseData):
    def __init__(self, writePriority=0, partition="", source="", type=""):
        BaseData.__init__(self)

        self.partition = partition
        self.source = source
        self.type = type

    def __str__(self):
        retval = "driverdisk"

        if self.partition:
            retval += " %s" % self.partition

            if self.type:
                retval += " --type=%s" % self.type
        elif self.source:
            retval += " --source=%s" % self.source

        return retval + "\n"

class FC3_DriverDisk(KickstartCommand):
    def __init__(self, writePriority=0, driverdiskList=None):
        KickstartCommand.__init__(self, writePriority)
        self.op = self._getParser()

        if driverdiskList is None:
            driverdiskList = []

        self.driverdiskList = driverdiskList

    def __str__(self):
        retval = ""
        for dd in self.driverdiskList:
            retval += dd.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--source")
        op.add_option("--type")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)

        if len(extra) == 1 and opts.source:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Only one of --source and partition may be specified for driverdisk command."))

        if not extra and not opts.source:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("One of --source or partition must be specified for driverdisk command."))

        ddd = self.handler.DriverDiskData()
        self._setToObj(self.op, opts, ddd)
        if len(extra) == 1:
            ddd.partition = extra[0]

        self.add(ddd)

    def add(self, newObj):
        self.driverdiskList.append(newObj)
