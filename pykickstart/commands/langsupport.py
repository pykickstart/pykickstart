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

class FC3LangSupport(KickstartCommand):
    def __init__(self, writePriority=0, deflang="en_US.UTF-8", supported=None):
        KickstartCommand.__init__(self, writePriority)
        self.deflang = deflang

        if supported == None:
            supported = []

        self.supported = supported

    def __str__(self):
        retval = "langsupport --default=%s" % self.deflang

        if self.supported:
            retval += " %s" % " ".join(self.supported)

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--default", dest="deflang", default="en_US.UTF-8")

        (opts, extra) = op.parse_args(args=args)
        self.deflang = opts.deflang
        self.supported = extra

class FC5LangSupport(DeprecatedCommand):
    def __init__(self):
        DeprecatedCommand.__init__(self)
