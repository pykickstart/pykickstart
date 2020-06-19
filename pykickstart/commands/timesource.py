#
# Copyright 2020 Red Hat, Inc.
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
from pykickstart.errors import KickstartParseError
from pykickstart.version import F33
from pykickstart.base import BaseData, KickstartCommand
from pykickstart.options import KSOptionParser

from pykickstart.i18n import _

class F33_TimesourceData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.ntp_server = kwargs.get("ntp_server", "")
        self.ntp_pool = kwargs.get("ntp_pool", "")
        self.ntp_disable = kwargs.get("ntp_disable", False)
        self.nts = kwargs.get("nts", False)

    def __eq__(self, y):
        if not y:
            return False

        if self.ntp_server:
            return self.ntp_server == y.ntp_server and self.nts == y.nts
        elif self.ntp_pool:
            return self.ntp_pool == y.ntp_pool and self.nts == y.nts
        else:
            # given that one of ntp_server/ntp_pool/ntp_disable is required
            # this will be --ntp_disable & such timesource invocations will
            # always be the same by definition
            return True

    def __ne__(self, y):
        return not self == y

    def __str__(self):
        retval = BaseData.__str__(self)

        args = self._getArgsAsStr()
        if args:
            retval += "timesource%s\n" % args

        return retval

    def _getArgsAsStr(self):
        retval = ""

        if self.ntp_server:
            retval += " --ntp-server=%s" % self.ntp_server
        if self.ntp_pool:
            retval += " --ntp-pool=%s" % self.ntp_pool
        if self.nts:
            retval += " --nts"
        if self.ntp_disable:
            retval += " --ntp-disable"

        return retval


class F33_Timesource(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()
        self.timesource_list = kwargs.get("timesource_list", [])
        self.exclusive_required_options = [("ntp_server", "--ntp-server"),
                                           ("ntp_pool", "--ntp-pool"),
                                           ("ntp_disable", "--ntp-disable")]

    def __str__(self):
        retval = ""
        for timesource_command in self.timesource_list:
            retval += timesource_command.__str__()

        return retval

    def _getParser(self):
        op = KSOptionParser(prog="timesource", description="""
                            Configures a timesource.""",
                            version=F33)
        op.add_argument("--ntp-server", version=F33, help="""
                        A single NTP server.

                        ``--ntp-server``, ``--ntp-pool`` and ``--ntp-disable`` are mutually exclusive.
                        """)
        op.add_argument("--ntp-pool", version=F33, help="""
                        A single NTP pool.

                        ``--ntp-pool``, ``--ntp-server`` and ``--ntp-disable`` are mutually exclusive.
                        """)
        op.add_argument("--ntp-disable", action="store_true",
                        default=False, version=F33, help="""
                        If specified, disable any NTP based time sync,
                        both on target system as well as in installation
                        environment.
                        """)
        op.add_argument("--nts", dest="nts", action="store_true",
                        default=False, version=F33, help="""
                        If specified, consider the provided hostname to be
                        a NTS compatible time source. Without the ``--nts``
                        option it will be considered to be a plain NTP time
                        source without NTS support.
                        """)
        return op

    def parse(self, args):
        td = self.dataClass()   # pylint: disable=not-callable
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_obj(ns, td)
        td.lineno = self.lineno

        # Check that just one of exclusive required options is specified
        used_options = [opt for attr, opt in self.exclusive_required_options
                        if getattr(ns, attr, None)]
        if len(used_options) == 0:
            mapping = {"options_list": ", ".join((opt for attr, opt in self.exclusive_required_options))}
            raise KickstartParseError(_("One of -%(options_list)s options must be specified for timesource command.") % mapping, lineno=self.lineno)
        if len(used_options) > 1:
            mapping = {"options_list": ", ".join((opt for opt in used_options))}
            raise KickstartParseError(_("Only one of %(options_list)s options may be specified for timesource command.") % mapping, lineno=self.lineno)

        return td

    def dataList(self):
        return self.timesource_list

    @property
    def dataClass(self):
        return self.handler.TimesourceData
