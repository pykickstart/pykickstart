#
# Copyright (C) 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from pykickstart.base import KickstartCommand
from pykickstart.options import KSOptionParser

class F21_OSTreeSetup(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, *args, **kwargs):
        KickstartCommand.__init__(self, *args, **kwargs)
        self.op = self._getParser()
        self.osname = kwargs.get('osname', None)
        self.remote = kwargs.get("remote", self.osname)
        self.url = kwargs.get('url', None)
        self.ref = kwargs.get('ref', None)
        self.nogpg = kwargs.get('nogpg', False)

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.osname:
            retval += "# OSTree setup\n"
            retval += "ostreesetup %s\n" % self._getArgsAsStr()

        return retval

    def _getArgsAsStr(self):
        retcmd = []
        if self.osname:
            retcmd.append('--osname="%s"' % self.osname)
        if self.remote:
            retcmd.append('--remote="%s"' % self.remote)
        if self.url:
            retcmd.append('--url="%s"' % self.url)
        if self.ref:
            retcmd.append('--ref="%s"' % self.ref)
        if self.nogpg:
            retcmd.append('--nogpg')
        return ' '.join(retcmd)

    def _getParser(self):
        op = KSOptionParser()
        op.add_option("--osname", dest="osname", required=1)
        op.add_option("--remote", dest="remote")
        op.add_option("--url", dest="url", required=1)
        op.add_option("--ref", dest="ref", required=1)
        op.add_option("--nogpg", action="store_true")
        return op

    def parse(self, args):
        (opts, _extra) = self.op.parse_args(args=args, lineno=self.lineno)
        self._setToSelf(self.op, opts)
        if self.remote is None:
            self.remote = self.osname
        return self

RHEL7_OSTreeSetup = F21_OSTreeSetup
