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
Error and warning handling classes and functions.

This module exports several exception classes:

    KickstartError - A generic exception class.

    KickstartParseError - An exception for errors occurring during parsing.

    KickstartValueError - No longer raised by pykickstart, but kept around for
                          backwards compatibility.

    KickstartVersionError - An exception for errors relating to unsupported
                            syntax versions.

And some warning classes:

    KickstartWarning - A generic warning class.

    KickstartParseWarning - A class for warnings occurring during parsing.

    KickstartDeprecationWarning - A class for warnings occurring during parsing
                                  related to deprecated commands and options.

"""
import warnings
from pykickstart.i18n import _


def formatErrorMsg(lineno, msg=""):
    """This function is deprecated. KickstartError formats the error message now,
       so this function returns a tuple that can be formatted by KickstartError.

       You should call:
       KickstartError(message, lineno=lineno)

       But the deprecated way is still supported:
       KickstartError(formatErrorMsg(message, lineno=lineno))

    """
    warnings.warn("Function formatErrorMsg is deprecated. The error messages "
                  "are formatted by KickstartError now.", DeprecationWarning)

    return lineno, msg

def _format_error_message(lineno, msg=""):
    """Properly format the error message msg in an exception.
       This function should be called only in exceptions to format the error messages.
    """
    if msg:
        return _("The following problem occurred on line %(lineno)s of the kickstart file:"
                 "\n\n%(msg)s\n") % {"lineno": lineno, "msg": msg}

    return _("There was a problem reading from line %s of the kickstart file") % lineno

class KickstartError(Exception):
    """A generic exception class for unspecific error conditions."""

    def __init__(self, msg="", lineno=None, formatting=True):
        """Create a new KickstartError exception instance with the descriptive
           message msg. The msg will be formatted if formatting is allowed and
           the line number lineno is set.
        """
        Exception.__init__(self)
        self.message = msg
        self.lineno = lineno

        # Accept tuples from formatErrorMsg for backwards compatibility.
        if isinstance(msg, tuple) and len(msg) == 2:
            self.lineno, self.message = msg

        # Keep the value attribute for backwards compatibility.
        self.value = self.message

        # Format the error message if it is allowed.
        if formatting and self.lineno is not None:
            self.value = _format_error_message(self.lineno, self.message)

    def __str__(self):
        return self.value

class KickstartParseError(KickstartError):
    """An exception class for errors when processing the input file, such as
       unknown options, commands, or sections.
    """

class KickstartValueError(KickstartError):
    """This exception class is no longer raised by pykickstart but is kept
       for backwards compatibility.
    """

class KickstartVersionError(KickstartError):
    """An exception class for errors related to using an incorrect version of
       kickstart syntax.
    """

class KickstartWarning(Warning):
    """A generic warning class for unspecific conditions."""

class KickstartParseWarning(KickstartWarning, UserWarning):
    """A class for warnings occurring during parsing an input file, such as
       defining duplicate entries and setting removed keywords.
    """

class KickstartDeprecationWarning(KickstartParseWarning, DeprecationWarning):
    """A class for warnings occurring during parsing related to using deprecated
       commands and options.
    """
