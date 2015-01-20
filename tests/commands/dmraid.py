# Andy Lindeberg <alindebe@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
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

import unittest
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.dmraid import *

class FC6_TestCase(CommandTest):
    command = "dmraid"

    def runTest(self):
        # pass
        self.assert_parse("dmraid --name=onamai --dev=debaisi", "dmraid --name=onamai --dev=\"debaisi\"\n")
        self.assert_parse("dmraid --name onamai --dev debaisi", "dmraid --name=onamai --dev=\"debaisi\"\n")
        self.assert_parse("dmraid --dev=deb1,deb2 --name onamai", "dmraid --name=onamai --dev=\"deb1,deb2\"\n")
        self.assert_parse("dmraid --dev \"deb1,deb2\" --name=onamai", "dmraid --name=onamai --dev=\"deb1,deb2\"\n")

        # fail
        self.assert_parse_error("dmraid", KickstartValueError)
        self.assert_parse_error("dmraid --name", KickstartParseError)
        self.assert_parse_error("dmraid --dev", KickstartParseError)
        self.assert_parse_error("dmraid --name=onamai", KickstartValueError)
        self.assert_parse_error("dmraid --name onamai", KickstartValueError)
        self.assert_parse_error("dmraid --dev debaisi", KickstartValueError)
        self.assert_parse_error("dmraid --dev=deb1,deb2", KickstartValueError)
        self.assert_parse_error("dmraid --magic", KickstartParseError)

if __name__ == "__main__":
    unittest.main()
