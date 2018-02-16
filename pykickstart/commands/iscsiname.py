#
# Chris Lumens <clumens@redhat.com>
# Peter Jones <pjones@redhat.com>
#
# Copyright 2006, 2007 Red Hat, Inc.
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
from pykickstart.version import FC6
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class FC6_IscsiName(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=70, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.iscsiname = kwargs.get("iscsiname", "")

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if self.iscsiname:
            retval += "iscsiname %s\n" % self.iscsiname

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="iscsiname", description="""
            Assigns an initiator name to the computer. If you use the iscsi
            parameter in your kickstart file, this parameter is mandatory, and
            you must specify iscsiname in the kickstart file before you specify
            iscsi.""", version=FC6)
        op.add_argument("iqn", metavar="<iqn>", nargs=1, version=FC6, help="""
                        IQN name""")
        return op

    def parse(self, args):
        (_ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)
        assert len(_ns.iqn) == 1

        if extra:
            mapping = {"command": "iscsiname", "options": extra}
            raise KickstartParseError(_("Unexpected arguments to %(command)s command: %(options)s") % mapping, lineno=self.lineno)

        self.iscsiname = _ns.iqn[0]
        return self
