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
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3_Vnc(KickstartCommand):
    def __init__(self, writePriority=0, enabled=False, password="", connect=""):
        KickstartCommand.__init__(self, writePriority)
        self.enabled = enabled
        self.password = password
        self.connect = connect

    def __str__(self):
        if not self.enabled:
            return ""

        retval = "vnc --enabled"

        if self.connect != "":
            retval += " --connect=%s" % self.connect
        if self.password != "":
            retval += " --password=%s" % self.password

        return retval + "\n"

    def _getParser(self):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--connect")
        op.add_option("--password", dest="password")
        return op

    def parse(self, args):
        op = self._getParser()
        self.enabled = True
        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class FC6_Vnc(FC3_Vnc):
    def __init__(self, writePriority=0, enabled=False, password="", host="",
                 port=""):
        FC3_Vnc.__init__(self, writePriority)
        self.enabled = enabled
        self.password = password
        self.host = host
        self.port = port

    def __str__(self):
        if not self.enabled:
            return ""

        retval = "vnc --enabled %s" % self.host

        if self.port != "":
            retval += " --port=%s" % self.port
        if self.password != "":
            retval += " --password=%s" % self.password

        return retval + "\n"

    def _getParser(self):
        def connect_cb (option, opt_str, value, parser):
            cargs = value.split(":")
            parser.values.ensure_value("host", cargs[0])

            if len(cargs) > 1:
                parser.values.ensure_value("port", cargs[1])

        op = FC3_Vnc._getParser(self)
        op.add_option("--connect", action="callback", callback=connect_cb,
                      nargs=1, type="string", deprecated=1)
        op.add_option("--host", dest="host")
        op.add_option("--port", dest="port")
        return op

    def parse(self, args):
        op = self._getParser()
        self.enabled = True
        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class F9_Vnc(FC6_Vnc):
    def _getParser(self):
        op = FC6_Vnc._getParser(self)
        op.remove_option("--connect")
        return op
