#
# errors.py:  Kickstart error handling.
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
"""
Error handling classes and functions.

This module exports a single function:

    formatErrorMsg - Properly formats an error message.

It also exports several exception classes:

    KickstartError - A generic exception class.

    KickstartParseError - An exception for errors relating to parsing.

    KickstartValueError - An exception for errors relating to option
                          processing.

    KickstartVersionError - An exception for errors relating to unsupported
                            syntax versions.
"""
from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

def formatErrorMsg(lineno, msg=""):
    """Properly format the error message msg for inclusion in an exception."""
    if msg != "":
        mapping = {"lineno": lineno, "msg": msg}
        return _("The following problem occurred on line %(lineno)s of the kickstart file:\n\n%(msg)s\n") % mapping
    else:
        return _("There was a problem reading from line %s of the kickstart file") % lineno

class KickstartError(Exception):
    """A generic exception class for unspecific error conditions."""
    def __init__(self, val = ""):
        """Create a new KickstartError exception instance with the descriptive
           message val.  val should be the return value of formatErrorMsg.
        """
        Exception.__init__(self)
        self.value = val

    def __str__ (self):
        return self.value

class KickstartParseError(KickstartError):
    """An exception class for errors when processing the input file, such as
       unknown options, commands, or sections.
    """
    def __init__(self, msg):
        """Create a new KickstartParseError exception instance with the
           descriptive message val.  val should be the return value of
           formatErrorMsg.
        """
        KickstartError.__init__(self, msg)

    def __str__(self):
        return self.value

class KickstartValueError(KickstartError):
    """An exception class for errors when processing arguments to commands,
       such as too many arguments, too few arguments, or missing required
       arguments.
    """
    def __init__(self, msg):
        """Create a new KickstartValueError exception instance with the
           descriptive message val.  val should be the return value of
           formatErrorMsg.
        """
        KickstartError.__init__(self, msg)

    def __str__ (self):
        return self.value

class KickstartVersionError(KickstartError):
    """An exception class for errors related to using an incorrect version of
       kickstart syntax.
    """
    def __init__(self, version):
        """Create a new KickstartVersionError exception instance with the
           descriptive message val.  val should be the return value of
           formatErrorMsg.
        """
        KickstartError.__init__(self, "Unsupported version specified; see version.py for now.")

    def __str__ (self):
        return self.value
