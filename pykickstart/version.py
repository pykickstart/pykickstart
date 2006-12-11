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

# Given a version of the kickstart syntax, this function imports the correct
# handler for that version and returns an instance of it.
def makeHandler(version):
    try:
        version = int(version)
    except ValueError:
        version = stringToVersion(version)

    if version == FC4:
        from pykickstart.commands.fc4 import FC4Handler
        return FC4Handler()
    elif version == FC5:
        from pykickstart.commands.fc5 import FC5Handler
        return FC5Handler()
    elif version == FC6:
        from pykickstart.commands.fc6 import FC6Handler
        return FC6Handler()
    else:
        raise KickstartVersionError(version)
