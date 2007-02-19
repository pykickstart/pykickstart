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
from pykickstart.options import *

class FC3_IgnoreDisk(KickstartCommand):
    def __init__(self, writePriority=0, ignoredisk=None):
        KickstartCommand.__init__(self, writePriority)

        if ignoredisk == None:
            ignoredisk = []

        self.ignoredisk = ignoredisk

    def __str__(self):
        if len(self.ignoredisk) > 0:
            return "ignoredisk --drives=%s\n" % string.join(self.ignoredisk, ",")
        else:
            return ""

    def parse(self, args):
        def drive_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)
            
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--drives", dest="drives", action="callback",
                      callback=drive_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)
        self.ignoredisk = opts.drives
