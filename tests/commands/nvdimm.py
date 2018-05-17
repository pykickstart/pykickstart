#
# Radek Vykydal <rvykydal@redhat.com>
#
# Copyright 2018 Red Hat, Inc.
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
from tests.baseclass import CommandTest

from pykickstart.errors import *

class RHEL7_TestCase(CommandTest):
    command = "nvdimm"

    def runTest(self):
        # pass
        self.assert_parse("nvdimm reconfigure --namespace=namespace0.0 --mode=sector --sectorsize=512",
                          "nvdimm reconfigure --namespace=namespace0.0 --mode=sector --sectorsize=512\n")
        self.assert_parse("nvdimm reconfigure --namespace=whatever --mode=sector --sectorsize=512",
                          "nvdimm reconfigure --namespace=whatever --mode=sector --sectorsize=512\n")

        # fail
        # --sectorsize is required when recofiguring to sector --mode
        self.assert_parse_error("nvdimm reconfigure --namespace=namespace0.0 --mode=sector",
                                KickstartValueError)
        self.assert_parse_error("nvdimm reconfigure --namespace=namespace0.0 --mode=invalid --sectorsize=512")
        self.assert_parse_error("nvdimm reconfigure --mode=sector --sectorsize=512",
                                KickstartValueError)
        self.assert_parse_error("nvdimm reconfigure extra --namespace=namespace0.0 --mode=sector --sectorsize=512",
                                KickstartValueError)
        self.assert_parse_error("nvdimm --namespace=namespace0.0 --mode=sector --sectorsize=512",
                                KickstartValueError)
        self.assert_parse_error("nvdimm invalid_action --namespace=namespace0.0 --mode=sector --sectorsize=512",
                                KickstartValueError)

if __name__ == "__main__":
    unittest.main()
