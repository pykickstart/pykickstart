#
# Martin Kolman <mkolman@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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

from pykickstart.base import BaseData, KickstartCommand
from pykickstart.errors import KickstartParseError
from pykickstart.options import KSOptionParser
from pykickstart.version import F29, RHEL8

from pykickstart.i18n import _


class F29_ModuleData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.name = kwargs.get("name", "")
        self.stream = kwargs.get("stream", "")

    def __eq__(self, y):
        if not y:
            return False
        return (self.name == y.name and self.stream == y.stream)

    def __ne__(self, y):
        return not self == y


    def __str__(self):
        retval = BaseData.__str__(self)

        args = self._getArgsAsStr()
        if args:
            retval += "module%s\n" % args

        return retval

    def _getArgsAsStr(self):
        retval = " --name=%s" % self.name
        # --stream is optional
        if self.stream:
            retval += " --stream=%s" % self.stream
        return retval

class RHEL8_ModuleData(F29_ModuleData):
    removedKeywords = F29_ModuleData.removedKeywords
    removedAttrs = F29_ModuleData.removedAttrs

    def __init__(self, *args, **kwargs):
        F29_ModuleData.__init__(self, *args, **kwargs)
        self.enable = kwargs.get("enable", True)

    def _getArgsAsStr(self):
        retval = F29_ModuleData._getArgsAsStr(self)

        # --disable is optional
        if not self.enable:
            retval += " --disable"

        return retval


class F29_Module(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)

        self.moduleList = kwargs.get("moduleList", [])
        self.op = self._getParser()

    def __str__(self):
        retval = ""

        for module in self.moduleList:
            retval += module.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="module", description="""
                            The module command makes it possible to manipulate
                            modules.

                            (In this case we mean modules as introduced by the
                            Fedora modularity initiative.)

                            A module is defined by a unique name and a stream id,
                            where single module can (and usually has) multiple
                            available streams.

                            Streams will in most cases corresponds to stable
                            releases of the given software components
                            (such as Node.js, Django, etc.) but there could be
                            also other use cases, such as a raw upstream master
                            branch stream or streams corresponding to an upcoming
                            stable release.

                            For more information see the Fedora modularity
                            initiative documentation:
                            https://docs.pagure.org/modularity/""", version=F29)
        op.add_argument("--name", metavar="<module_name>", version=F29, required=True,
                        help="""
                        Name of the module to enable.""")
        op.add_argument("--stream", metavar="<module_stream_name>", version=F29, required=False,
                        help="""
                        Name of the module stream to enable.""")

        return op

    def parse(self, args):
        (ns, extra) = self.op.parse_known_args(args=args, lineno=self.lineno)

        if len(extra) > 0:
            msg = _("The enable module command does not take position arguments!")
            raise KickstartParseError(msg, lineno=self.lineno)

        enable_module_data = self.dataClass()   # pylint: disable=not-callable
        self.set_to_obj(ns, enable_module_data)
        enable_module_data.lineno = self.lineno

        return enable_module_data

    def dataList(self):
        return self.moduleList

    @property
    def dataClass(self):
        return self.handler.ModuleData

class RHEL8_Module(F29_Module):
    removedKeywords = F29_Module.removedKeywords
    removedAttrs = F29_Module.removedAttrs

    def _getParser(self):
        op = F29_Module._getParser(self)
        op.add_argument("--disable", version=RHEL8,
                        action="store_false",
                        dest="enable",
                        help="Disable module.")
        return op
