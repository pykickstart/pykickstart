#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from pykickstart.errors import KickstartVersionError

# Symbolic names for internal version numbers.
FC4 = 100
FC5 = 150
FC6 = 200

# This always points at the latest version and is the default.
DEVEL = FC6

def stringToVersion(string):
    """Convert string into one of the provided version constants.  Raises
       KickstartVersionError if string does not match anything.
    """
    if string == "FC4":
        return FC4
    elif string == "FC5":
        return FC5
    elif string == "FC6":
        return FC6
    elif string == "DEVEL":
        return DEVEL
    else:
        raise KickstartVersionError(string)

def returnClassForVersion(version):
    """Return the class of the syntax handler for version.  version can be
       either a string or the matching constant.  Raises KickstartValueError
       if version does not match anything.
    """
    try:
        version = int(version)
    except ValueError:
        version = stringToVersion(version)

    if version == FC4:
        from pykickstart.commands.fc4 import FC4Handler
        return FC4Handler
    elif version == FC5:
        from pykickstart.commands.fc5 import FC5Handler
        return FC5Handler
    elif version == FC6:
        from pykickstart.commands.fc6 import FC6Handler
        return FC6Handler
    else:
        raise KickstartVersionError(version)

# Given a version of the kickstart syntax, this function imports the correct
# handler for that version and returns an instance of it.
def makeHandler(version):
    """Return a new instance of the syntax handler for version.  version can be
       either a string or the matching constant.  This function is useful for
       standalone programs which just need to handle a specific version of
       kickstart syntax (as provided by a command line argument, for example)
       and need to instantiate the correct object.
    """
    super = returnClassForVersion(version)
    return super()
