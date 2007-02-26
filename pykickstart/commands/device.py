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
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Device(KickstartCommand):
    def __init__(self, writePriority=0, type="", moduleName="", moduleOpts=""):
        KickstartCommand.__init__(self, writePriority)
        self.type = type
        self.moduleName = moduleName
        self.deviceOpts = moduleOpts

    def __str__(self):
        if self.moduleName != "":
            if self.moduleOpts != "":
                retval = "--opts=%s" % self.moduleOpts
            else:
                retval = ""

            return "device %s %s %s\n" % (self.type, self.moduleName, retval)
        else:
            return ""

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--opts", dest="moduleOpts", default="")

        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 2:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("device command requires two arguments: module type and name"))

        self.opts = opts.moduleOpts
        self.type = extra[0]
        self.moduleName = extra[1]
