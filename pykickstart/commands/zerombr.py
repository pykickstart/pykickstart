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
import warnings

from pykickstart.base import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_ZeroMbr(KickstartCommand):
    def __init__(self, writePriority=110, zerombr=False):
        KickstartCommand.__init__(self, writePriority)
        self.zerombr = zerombr

    def __str__(self):
        if self.zerombr:
            return "# Clear the Master Boot Record\nzerombr\n"
        else:
            return ""

    def parse(self, args):
        if len(args) > 0:
            warnings.warn(_("Ignoring deprecated option on line %s:  The zerombr command no longer takes any options.  In future releases, this will result in a fatal error from kickstart.  Please modify your kickstart file to remove any options.") % self.lineno, DeprecationWarning)

        self.zerombr = True

class F9_ZeroMbr(FC3_ZeroMbr):
    def parse(self, args):
        if len(args) > 0:
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Kickstart command %s does not take any arguments") % "zerombr")

        self.zerombr = True
