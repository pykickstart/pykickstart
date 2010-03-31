#
# James Laska <jlaska@redhat.com>
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

class FC3_TestCase(CommandTest):

    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.validLevels = ["RAID0", "RAID1", "RAID5", "RAID6"]

    def runTest(self, bytesPerInode=False):
        bpi = ""
        if bytesPerInode:
            bpi = "--bytes-per-inode=4096 "

        # pass
        # valid levels
        for level in self.validLevels:
            self.assert_parse("raid / --device=md0 --level=%s %sraid.01" % (level, bpi), \
                              "raid / --device=0 --level=%s %sraid.01\n" % (level, bpi))

        # device=md0, level=0
        self.assert_parse("raid / --device=md0 --level=0 %sraid.01" % (bpi), \
                          "raid / --device=0 --level=RAID0 %sraid.01\n" % (bpi))
        # device=0, level=1
        self.assert_parse("raid / --device=0 --level=1 %sraid.01 raid.02 raid.03" % (bpi), \
                          "raid / --device=0 --level=RAID1 %sraid.01 raid.02 raid.03\n" % (bpi))
        # device=2, level=RAID1
        self.assert_parse("raid / --device=md0 --level=RAID1 %sraid.01 raid.02 raid.03" % (bpi), \
                          "raid / --device=0 --level=RAID1 %sraid.01 raid.02 raid.03\n" % (bpi))
        # spares=0
        self.assert_parse("raid / --device=md2 --level=5 --spares=0 %sraid.01 raid.02 raid.03" % (bpi), \
                          "raid / --device=2 --level=RAID5 %sraid.01 raid.02 raid.03\n" % (bpi))
        # spares != 0
        self.assert_parse("raid / --device=md2 --level=5 --spares=2 %sraid.01 raid.02 raid.03" % (bpi), \
                          "raid / --device=2 --level=RAID5 --spares=2 %sraid.01 raid.02 raid.03\n" % (bpi))

        # fstype
        self.assert_parse("raid / --device=md0 --fstype=ASDF --level=6 %sraid.01 raid.02" % (bpi), \
                          "raid / --device=0 --fstype=\"ASDF\" --level=RAID6 %sraid.01 raid.02\n" % (bpi))
        # useexisting
        self.assert_parse("raid / --device=md0 --level=6 --useexisting %sraid.01 raid.02" % (bpi), \
                          "raid / --device=0 --level=RAID6 --useexisting %sraid.01 raid.02\n" % (bpi))

        # noformat
        self.assert_parse("raid / --device=md0 --level=6 --noformat --useexisting %sraid.01 raid.02" % (bpi), \
                          "raid / --device=0 --level=RAID6 --noformat --useexisting %sraid.01 raid.02\n" % (bpi))

        # fail
        # no mountpoint or options
        self.assert_parse_error("raid", KickstartValueError)
        # no mountpoint or options ... just partitions
        self.assert_parse_error("raid part.01 part.01", KickstartValueError)
        # no mountpoint
        self.assert_parse_error("raid --level=0 --device=md0", KickstartValueError)
        # no options
        self.assert_parse_error("raid /", KickstartValueError)
        # no device
        self.assert_parse_error("raid / --level=0", KickstartValueError)
        # no level -- FIXME -- I would think should should fail, but it doesn't
        # self.assert_parse_error("raid / --device=md0", KickstartValueError)
        # No raid members defined
        self.assert_parse_error("raid / --level=0 --device=md0", KickstartValueError)

        # Invalid device string - device=asdf0
        self.assert_parse_error("raid / --device=asdf0 --level=RAID1 raid.01 raid.02 raid.03", ValueError)

class FC4_TestCase(FC3_TestCase):
    def runTest(self, bytesPerInode=False):
        # run FC3 test case
        FC3_TestCase.runTest(self, bytesPerInode=bytesPerInode)

        bpi = ""
        if bytesPerInode:
            bpi = "--bytes-per-inode=4096 "

        # pass
        # fsoptions
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=6 --fsoptions \"these=are,options\" %sraid.01 raid.02" % (bpi), \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID6 --fsoptions=\"these=are,options\" %sraid.01 raid.02\n" % (bpi))

class FC5_TestCase(FC4_TestCase):
    def runTest(self, bytesPerInode=True):
        # run FC4 test case
        FC4_TestCase.runTest(self, bytesPerInode=bytesPerInode)

        bpi = ""
        if bytesPerInode:
            bpi = "--bytes-per-inode=4096 "

        # pass
        # fsoptions
        self.assert_parse("raid / --device=md0 --fstype=\"ext2\" --level=RAID0 %sraid.01 raid.02" % (bpi,), \
                          "raid / --device=0 --fstype=\"ext2\" --level=RAID0 %sraid.01 raid.02\n" % (bpi,))

    def passphrase_tests(self, bytesPerInode=True):

        bpi = ""
        if bytesPerInode:
            bpi = "--bytes-per-inode=4096 "
        # pass
        # encrypted
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1 %s--encrypted raid.01 raid.02" % (bpi), \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID1 %s--encrypted raid.01 raid.02\n" % (bpi))
        # passphrase
        # FIXME - should this fail since no --encrypted?
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1 %s--passphrase=asdf raid.01 raid.02" % (bpi), \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID1 %sraid.01 raid.02\n" % (bpi))

        # encrypted w/ passphrase
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1 %s--encrypted --passphrase=asdf raid.01 raid.02" % (bpi), \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID1 %s--encrypted --passphrase=\"asdf\" raid.01 raid.02\n" % (bpi))

        # fail
        # --encrypted=<value>
        self.assert_parse_error("raid / --device=md0 --level=1 --encrypted=1", KickstartParseError)

class RHEL5_TestCase(FC5_TestCase):
    def __init__(self, *kargs, **kwargs):
        FC5_TestCase.__init__(self, *kargs, **kwargs)
        self.validLevels.append("RAID10")

    def runTest(self, bytesPerInode=True):
        # run FC4 test case
        FC5_TestCase.runTest(self, bytesPerInode=bytesPerInode)

        self.passphrase_tests(bytesPerInode)

class F7_TestCase(FC5_TestCase):
    def __init__(self, *kargs, **kwargs):
        FC5_TestCase.__init__(self, *kargs, **kwargs)
        self.validLevels.append("RAID10")

class F9_TestCase(F7_TestCase):
    '''F9_TestCase'''
    def runTest(self):
        # run F7 test case
        F7_TestCase.runTest(self, bytesPerInode=False)

        # fsprofile
        self.assert_parse("raid / --device=md0 --fstype=\"ext3\" --level=1 --fsprofile=ASDF raid.01 raid.02", \
                          "raid / --device=0 --fstype=\"ext3\" --level=RAID1 --fsprofile=\"ASDF\" raid.01 raid.02\n")

        # deprecated
        self.assert_deprecated("raid", "--bytes-per-inode")

class F12_TestCase(F9_TestCase):
    '''F12_TestCase'''
    def runTest(self):
        # run F9 test case
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("raid / --device=md0 --escrowcert=\"http://x/y\" "
                          "raid.01 raid.02",
                          "raid / --device=0 raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted --backuppassphrase "
                          "raid.01 raid.02",
                          "raid / --device=0 --encrypted raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted "
                          "--escrowcert=\"http://x/y\" raid.01 raid.02",
                          "raid / --device=0 --encrypted "
                          "--escrowcert=\"http://x/y\" raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted "
                          "--escrowcert=\"http://x/y\" --backuppassphrase "
                          "raid.01 raid.02",
                          "raid / --device=0 --encrypted "
                          "--escrowcert=\"http://x/y\" --backuppassphrase "
                          "raid.01 raid.02\n")
        self.assert_parse("raid / --device=md0 --encrypted "
                          "--escrowcert=http://x/y raid.01 raid.02",
                          "raid / --device=0 --encrypted "
                          "--escrowcert=\"http://x/y\" raid.01 raid.02\n")

        # fail
        self.assert_parse_error("raid / --device=md0 raid.01 raid.02 "
                                "--escrowcert")
        self.assert_parse_error("raid / --device=md0 --escrowcert "
                                "--backuppassphrase raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --encrypted --escrowcert "
                                "--backuppassphrase raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --backuppassphrase=False "
                                "raid.01 raid.02")
        self.assert_parse_error("raid / --device=md0 --backuppassphrase=True "
                                "raid.01 raid.02")

class F13_TestCase(F12_TestCase):
    def __init__(self, *kargs, **kwargs):
        F12_TestCase.__init__(self, *kargs, **kwargs)
        self.validLevels.append("RAID4")

if __name__ == "__main__":
    unittest.main()
