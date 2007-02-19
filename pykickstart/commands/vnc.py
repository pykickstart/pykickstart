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
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC3Vnc(KickstartCommand):
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

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--connect")
        op.add_option("--password", dest="password")

        self.enabled = True

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)

class FC6Vnc(FC3Vnc):
    def __init__(self, writePriority=0, enabled=False, password="", host="",
                 port=""):
        FC3Vnc.__init__(self, writePriority)
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

    def parse(self, args):
        def connect_cb (option, opt_str, value, parser):
            cargs = value.split(":")
            parser.values.ensure_value("host", cargs[0])

            if len(cargs) > 1:
                parser.values.ensure_value("port", cargs[1])

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--connect", action="callback", callback=connect_cb,
                      nargs=1, type="string", deprecated=1)
        op.add_option("--password", dest="password")
        op.add_option("--host", dest="host")
        op.add_option("--port", dest="port")

        self.enabled = True

        (opts, extra) = op.parse_args(args=args)
        self._setToSelf(op, opts)
