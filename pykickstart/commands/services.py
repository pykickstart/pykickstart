#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
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
import string

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6_Services(KickstartCommand):
    def __init__(self, writePriority=0, disabled=None, enabled=None):
        KickstartCommand.__init__(self, writePriority)

        if disabled == None:
            disabled = []

        self.disabled = disabled

        if enabled == None:
            enabled = []

        self.enabled = enabled

    def __str__(self):
        retval = ""

        if len(self.disabled) > 0:
            retval += " --disabled=%s" % string.join(self.disabled, ",")
        if len(self.enabled) > 0:
            retval += " --enabled=%s" % string.join(self.enabled, ",")

        if retval != "":
            return "# System services\nservices %s\n" % retval
        else:
            return ""

    def parse(self, args):
        def services_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--disabled", dest="disabled", action="callback",
                      callback=services_cb, nargs=1, type="string")
        op.add_option("--enabled", dest="enabled", action="callback",
                      callback=services_cb, nargs=1, type="string")

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
