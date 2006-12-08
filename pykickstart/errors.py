#
# parser.py:  Kickstart file parser.
#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

def formatErrorMsg(lineno, msg=""):
    if msg != "":
        mapping = {"lineno": lineno, "msg": msg}
        return _("The following problem occurred on line %(lineno)s of the kickstart file:\n\n%(msg)s\n") % mapping
    else:
        return _("There was a problem reading from line %s of the kickstart file") % lineno

class KickstartError(Exception):
    def __init__(self, val = ""):
        Exception.__init__(self)
        self.value = val

    def __str__ (self):
        return self.value

class KickstartParseError(KickstartError):
    def __init__(self, msg):
        KickstartError.__init__(self, msg)

    def __str__(self):
        return self.value

class KickstartValueError(KickstartError):
    def __init__(self, msg):
        KickstartError.__init__(self, msg)

    def __str__ (self):
        return self.value

class KickstartVersionError(KickstartError):
    def __init__(self, version):
        KickstartError.__init__(self, "Unsupported version specified; see version.py for now.")

    def __str__ (self):
        return self.value
