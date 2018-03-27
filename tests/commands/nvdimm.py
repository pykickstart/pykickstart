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


class F28_TestCase(CommandTest):
    command = "nvdimm"

    def runTest(self):
        # pass
        self.assert_parse("nvdimm reconfigure --namespace=namespace0.0 --mode=sector --sectorsize=512",
                          "nvdimm reconfigure --namespace=namespace0.0 --mode=sector --sectorsize=512\n")
        self.assert_parse("nvdimm reconfigure --namespace=whatever --mode=sector --sectorsize=512",
                          "nvdimm reconfigure --namespace=whatever --mode=sector --sectorsize=512\n")

        self.assert_parse("nvdimm use --namespace=whatever",
                          "nvdimm use --namespace=whatever\n")
        self.assert_parse("nvdimm use --blockdevs=pmem0s1",
                          "nvdimm use --blockdevs=pmem0s1\n")
        self.assert_parse("nvdimm use --blockdevs=pmem0s1,pmem0s2",
                          "nvdimm use --blockdevs=pmem0s1,pmem0s2\n")

        # fail
        # --sectorsize is required when recofiguring to sector --mode
        self.assert_parse_error("nvdimm reconfigure --namespace=namespace0.0 --mode=sector")
        self.assert_parse_error("nvdimm reconfigure --namespace=namespace0.0 --mode=invalid --sectorsize=512")
        # --namespace is requried for reconfigure
        self.assert_parse_error("nvdimm reconfigure --mode=sector --sectorsize=512")
        self.assert_parse_error("nvdimm reconfigure extra --namespace=namespace0.0 --mode=sector --sectorsize=512")
        self.assert_parse_error("nvdimm --namespace=namespace0.0 --mode=sector --sectorsize=512")
        self.assert_parse_error("nvdimm invalid_action --namespace=namespace0.0 --mode=sector --sectorsize=512")

        # Only one of --namespace --blockdevs is allowed
        self.assert_parse_error("nvdimm reconfigure --namespace=namespace0.0 --blockdevs=pmem0s1 --mode=sector")
        self.assert_parse_error("nvdimm use --namespace=namespace0.0 --blockdevs=pmem0s1 --mode=sector")
        # Only --namespace is allowed for reconfigure action
        self.assert_parse_error("nvdimm reconfigure --blockdev=pmem0s1 --mode=sector")


if __name__ == "__main__":
    unittest.main()
