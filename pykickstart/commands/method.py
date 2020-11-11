#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2013 Red Hat, Inc.
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
from pykickstart.version import FC3, F34, versionToLongString
from pykickstart.base import KickstartCommand, DeprecatedCommand
from pykickstart.options import KSOptionParser

class FC3_Method(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    # These are all set up as part of the base KickstartCommand.  We want to
    # make sure looking them up gets redirected to the right place.
    internals = ["method",
                 "writePriority", "currentCmd", "currentLine", "handler", "lineno", "seen"]

    _methods = ["cdrom", "harddrive", "nfs", "url"]

    def _clear_seen(self):
        """ Reset all the method's seen attributes to False"""
        for method in self._methods:
            setattr(getattr(self.handler, method), "seen", False)

    def _get_command(self, method):
        """Get a command for the given method."""
        if method is None:
            # We use this to select the closest mirror option.
            # TODO: Raise an error instead.
            method = "url"

        if method not in self._methods:
            raise AttributeError("Unknown method: {}".format(method))

        return getattr(self.handler, method)

    @property
    def method(self):
        """Return the seen method or None."""
        for method in self._methods:
            if getattr(self.handler, method).seen:
                return method

        return None

    @method.setter
    def method(self, value):
        """Set which method is seen."""
        self._clear_seen()

        if value is None:
            return

        self._get_command(value).seen = True

    def __getattr__(self, name):
        """Get the attribute in the seen command.

        Called when an attribute lookup has not found
        the attribute in the usual places.
        """
        # Prevent recursion in copy and deepcopy.
        # See commit f5dbcfb for explanation.
        if name in ["handler", "method", "_methods"]:
            raise AttributeError()

        command = self._get_command(self.method)
        return getattr(command, name)

    def __setattr__(self, name, value):
        """Set the attribute in the seen command.

        Called when an attribute assignment is attempted.
        """
        if name in self.internals:
            super(FC3_Method, self).__setattr__(name, value)
            return

        command = self._get_command(self.method)
        # Check if the kickstart command has the attribute.
        # Instead of using hasattr, that calls getattr and catches the exception
        # that we would have to raise again, we call getattr directly.
        getattr(command, name)
        # Set the attribute of the kickstart command.
        command.__setattr__(name, value)

    def _getParser(self):
        """Return a parser."""

        description = "Proxy to the actual installation method. Valid installation methods are:\n\n"
        for method in self._methods:
            description += "* ``%s``\n" % method

        return KSOptionParser(prog="method", description=description, version=FC3)


# These are all just for compat.  Calling into the appropriate version-specific
# method command will deal with making sure the right options are used.
class FC6_Method(FC3_Method):
    pass

class F13_Method(FC6_Method):
    pass

class F14_Method(F13_Method):
    pass

class RHEL6_Method(F14_Method):
    pass

class F18_Method(F14_Method):
    pass

class F19_Method(FC3_Method):
    removedKeywords = FC3_Method.removedKeywords
    removedAttrs = FC3_Method.removedAttrs

    _methods = FC3_Method._methods + ["liveimg"]

class RHEL7_Method(F19_Method):
    removedKeywords = F19_Method.removedKeywords
    removedAttrs = F19_Method.removedAttrs

    _methods = F19_Method._methods + ["hmc"]

class F28_Method(RHEL7_Method):
    pass

class F34_Method(DeprecatedCommand, F19_Method):
    def __init__(self):  # pylint: disable=super-init-not-called
        DeprecatedCommand.__init__(self)

    def _getParser(self):
        op = F19_Method._getParser(self)
        op.description += "\n\n.. deprecated:: %s" % versionToLongString(F34)
        return op
