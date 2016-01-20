#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007, 2012 Red Hat, Inc.
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
from pykickstart.base import KickstartCommand
from pykickstart.constants import CLEARPART_TYPE_ALL, CLEARPART_TYPE_LINUX, CLEARPART_TYPE_LIST, CLEARPART_TYPE_NONE
from pykickstart.options import KSOptionParser, commaSplit

class FC3_ClearPart(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=120, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.drives = kwargs.get("drives", [])
        self.initAll = kwargs.get("initAll", False)
        self.type = kwargs.get("type", None)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.type is None:
            return retval

        if self.type == CLEARPART_TYPE_NONE:
            clearstr = " --none"
        elif self.type == CLEARPART_TYPE_LINUX:
            clearstr = " --linux"
        elif self.type == CLEARPART_TYPE_ALL:
            clearstr = " --all"
        else:
            clearstr = ""

        if self.initAll:
            initstr = " --initlabel"
        else:
            initstr = ""

        if len(self.drives) > 0:
            drivestr = " --drives=" + ",".join(self.drives)
        else:
            drivestr = ""

        retval += "# Partition clearing information\nclearpart%s%s%s\n" % (clearstr, initstr, drivestr)
        return retval

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--all", dest="type", action="store_const", const=CLEARPART_TYPE_ALL)
        op.add_argument("--drives", type=commaSplit)
        op.add_argument("--initlabel", dest="initAll", action="store_true", default=False)
        op.add_argument("--linux", dest="type", action="store_const", const=CLEARPART_TYPE_LINUX)
        op.add_argument("--none", dest="type", action="store_const", const=CLEARPART_TYPE_NONE)
        return op

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)
        return self

class F17_ClearPart(FC3_ClearPart):
    def __init__(self, *args, **kwargs):
        super(F17_ClearPart, self).__init__(*args, **kwargs)
        self.devices = kwargs.get("devices", [])

    def __str__(self):
        s = super(F17_ClearPart, self).__str__()
        if s and len(self.devices) > 0:
            s = s.rstrip()
            s += " --list=" + ",".join(self.devices)
            s += "\n"
        return s

    def _getParser(self):
        op = FC3_ClearPart._getParser(self)
        op.add_argument("--list", dest="devices", type=commaSplit)
        return op

    def parse(self, args):
        obj = FC3_ClearPart.parse(self, args)
        if getattr(obj, "devices", []):
            obj.type = CLEARPART_TYPE_LIST

        return obj

class F21_ClearPart(F17_ClearPart):
    def __init__(self, *args, **kwargs):
        super(F21_ClearPart, self).__init__(*args, **kwargs)
        self.disklabel = kwargs.get("disklabel", "")

    def __str__(self):
        s = super(F21_ClearPart, self).__str__()
        if s and self.disklabel:
            s = s.rstrip()
            s += " --disklabel=%s\n" % self.disklabel
        return s

    def _getParser(self):
        op = F17_ClearPart._getParser(self)
        op.add_argument("--disklabel", default="")
        return op
