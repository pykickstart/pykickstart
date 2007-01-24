#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
"""
Methods for working with kickstart versions.

This module defines several symbolic constants that specify kickstart syntax
versions.  Each version corresponds roughly to one release of Red Hat Linux,
Red Hat Enterprise Linux, or Fedora Core as these are where most syntax
changes take place.

This module also exports several functions:

    makeVersion - Given a version number, return an instance of the
                  matching handler class.

    returnClassForVersion - Given a version number, return the matching
                            handler class.  This does not return an
                            instance of that class, however.

    stringToVersion - Convert a string representation of a version number
                      into the symbolic constant.
"""
from rhpl.translate import _
from pykickstart.errors import KickstartVersionError

# Symbolic names for internal version numbers.
FC3 = 1000
FC4 = 2000
FC5 = 3000
FC6 = 4000
RHEL5 = 4100
F7  = 5000

# This always points at the latest version and is the default.
DEVEL = F7

def stringToVersion(string):
    """Convert string into one of the provided version constants.  Raises
       KickstartVersionError if string does not match anything.
    """
    if string.lower() in ["fc3", "fedora core 3"]:
        return FC3
    elif string.lower() in ["fc4", "fedora core 4"]:
        return FC4
    elif string.lower() in ["fc5", "fedora core 5"]:
        return FC5
    elif string.lower() in ["fc6", "fedora core 6"]:
        return FC6
    elif string.lower() in ["f7", "fedora 7"]:
        return F7
    elif string.lower() in ["rhel5", "red hat enterprise linux 5"]:
        return RHEL5
    elif string.lower() == "devel":
        return DEVEL
    else:
        raise KickstartVersionError(_("Unsupported version specified: %s") % string)

def returnClassForVersion(version=DEVEL):
    """Return the class of the syntax handler for version.  version can be
       either a string or the matching constant.  Raises KickstartValueError
       if version does not match anything.
    """
    try:
        version = int(version)
    except ValueError:
        version = stringToVersion(version)

    if version == FC3:
        from pykickstart.commands.fc3 import FC3Handler
        return FC3Handler
    elif version == FC4:
        from pykickstart.commands.fc4 import FC4Handler
        return FC4Handler
    elif version == FC5:
        from pykickstart.commands.fc5 import FC5Handler
        return FC5Handler
    elif version == FC6:
        from pykickstart.commands.fc6 import FC6Handler
        return FC6Handler
    elif version == F7:
        from pykickstart.commands.f7 import F7Handler
        return F7Handler
    elif version == RHEL5:
        from pykickstart.commands.rhel5 import RHEL5Handler
        return RHEL5Handler
    else:
        raise KickstartVersionError(_("Unsupported version specified: %s") % version)

def makeVersion(version=DEVEL):
    """Return a new instance of the syntax handler for version.  version can be
       either a string or the matching constant.  This function is useful for
       standalone programs which just need to handle a specific version of
       kickstart syntax (as provided by a command line argument, for example)
       and need to instantiate the correct object.
    """
    cl = returnClassForVersion(version)
    return cl()
