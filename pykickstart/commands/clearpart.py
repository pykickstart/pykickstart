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
import string

from pykickstart.base import *
from pykickstart.constants import *
from pykickstart.errors import *
from pykickstart.options import *

class FC3_ClearPart(KickstartCommand):
    def __init__(self, writePriority=120, drives=None, initAll=False,
                 type=None):
        KickstartCommand.__init__(self, writePriority)

        if drives == None:
            drives = []

        self.drives = drives
        self.initAll = initAll
        self.type = type

    def __str__(self):
        if self.type is None:
            return ""

        if self.type == CLEARPART_TYPE_NONE:
            clearstr = "--none"
        elif self.type == CLEARPART_TYPE_LINUX:
            clearstr = "--linux"
        elif self.type == CLEARPART_TYPE_ALL:
            clearstr = "--all"
        else:
            clearstr = ""

        if self.initAll:
            initstr = "--initlabel"
        else:
            initstr = ""

        if len(self.drives) > 0:
            drivestr = "--drives=" + string.join (self.drives, ",")
        else:
            drivestr = ""

        return "# Partition clearing information\nclearpart %s %s %s\n" % (clearstr, initstr, drivestr)

    def parse(self, args):
        def drive_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--all", dest="type", action="store_const",
                      const=CLEARPART_TYPE_ALL)
        op.add_option("--drives", dest="drives", action="callback",
                      callback=drive_cb, nargs=1, type="string")
        op.add_option("--initlabel", dest="initAll", action="store_true",
                      default=False)
        op.add_option("--linux", dest="type", action="store_const",
                      const=CLEARPART_TYPE_LINUX)
        op.add_option("--none", dest="type", action="store_const",
                      const=CLEARPART_TYPE_NONE)

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
