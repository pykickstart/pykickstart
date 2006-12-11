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
FC5 = 100
FC6 = 150

# This always points at the latest version and is the default.
DEVEL = FC6

# Given a version of the kickstart syntax, this function imports the correct
# handler for that version and returns an instance of it.
def makeHandler(version):
    version = int(version)

    if version == FC5:
        from pykickstart.commands.fc5 import FC5Handler
        return FC5Handler()
    elif version == FC6:
        from pykickstart.commands.fc6 import FC6Handler
        return FC6Handler()
    else:
        raise KickstartVersionError(version)
