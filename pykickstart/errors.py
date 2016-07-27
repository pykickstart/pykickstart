#
# errors.py:  Kickstart error handling.
#
# Chris Lumens <clumens@redhat.com>
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
"""
Error handling classes and functions.

This module exports a single function:

    formatErrorMsg - Properly formats an error message.

It also exports several exception classes:

    KickstartError - A generic exception class.

    KickstartParseError - An exception for errors occurring during parsing.

    KickstartValueError - No longer raised by pykickstart, but kept around for
                          backwards compatibility.

    KickstartVersionError - An exception for errors relating to unsupported
                            syntax versions.
"""
from pykickstart.i18n import _

def formatErrorMsg(lineno, msg=""):
    """Properly format the error message msg for inclusion in an exception."""
    if msg:
        mapping = {"lineno": lineno, "msg": msg}
        return _("The following problem occurred on line %(lineno)s of the kickstart file:\n\n%(msg)s\n") % mapping
    else:
        return _("There was a problem reading from line %s of the kickstart file") % lineno

class KickstartError(Exception):
    """A generic exception class for unspecific error conditions."""
    def __init__(self, val=""):
        """Create a new KickstartError exception instance with the descriptive
           message val.  val should be the return value of formatErrorMsg.
        """
        Exception.__init__(self)
        self.value = val

    def __str__(self):
        return self.value

class KickstartParseError(KickstartError):
    """An exception class for errors when processing the input file, such as
       unknown options, commands, or sections.
    """
    def __init__(self, msg):
        """Create a new KickstartParseError exception instance with the
           descriptive message msg.  msg should be the return value of
           formatErrorMsg.
        """
        KickstartError.__init__(self, msg)

    def __str__(self):
        return self.value

class KickstartValueError(KickstartError):
    """This exception class is no longer raised by pykickstart but is kept
       for backwards compatibility.
    """
    def __init__(self, msg):
        KickstartError.__init__(self, msg)

    def __str__(self):
        return self.value

class KickstartVersionError(KickstartError):
    """An exception class for errors related to using an incorrect version of
       kickstart syntax.
    """
    def __init__(self, msg):
        """Create a new KickstartVersionError exception instance with the
           descriptive message msg.  msg should be the return value of
           formatErrorMsg.
        """
        KickstartError.__init__(self, msg)

    def __str__(self):
        return self.value
