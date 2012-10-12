import unittest, shlex
from tests.baseclass import *

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.version import *
from pykickstart.commands.logvol import *

class FC3_TestCase(CommandTest):
    command = "logvol"

    def runTest(self):
        if "--bytes-per-inode" in self.optionList:
            self.bytesPerInode = "--bytes-per-inode=4096 "
        else:
            self.bytesPerInode = ""

        # --name and --vgname
        self.assert_parse("logvol / --name=NAME --vgname=VGNAME",
                          "logvol /  %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --fstype
        self.assert_parse("logvol / --fstype=\"BLAFS\" --name=NAME --vgname=VGNAME",
                          "logvol /  --fstype=\"BLAFS\" %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --grow
        self.assert_parse("logvol / --grow --name=NAME --vgname=VGNAME",
                          "logvol /  --grow %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --size
        self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --maxsize
        self.assert_parse("logvol / --maxsize=2048 --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --recommended
        self.assert_parse("logvol / --maxsize=2048 --recommended --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --recommended %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --percent
        self.assert_parse("logvol / --percent=10 --name=NAME --vgname=VGNAME",
                          "logvol /  --percent=10 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --noformat
        # FIXME - should --noformat also be adding --useexisting (seems counter
        # to posted documentation 
        # http://fedoraproject.org/wiki/Anaconda/Kickstart)
        self.assert_parse("logvol / --noformat --name=NAME --vgname=VGNAME",
                          "logvol /  --noformat --useexisting %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --useexisting
        self.assert_parse("logvol / --useexisting --name=NAME --vgname=VGNAME",
                          "logvol /  --useexisting %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

        # assert data types
        self.assert_type("logvol", "size", "int")
        self.assert_type("logvol", "maxsize", "int")
        self.assert_type("logvol", "percent", "int")

        # fail - incorrect type
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --size=SIZE", KickstartParseError)
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --maxsize=MAXSIZE", KickstartParseError)
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --percent=PCT", KickstartParseError)

        # assert required options
        self.assert_required("logvol", "name")
        self.assert_required("logvol", "vgname")

        # fail - missing required
        self.assert_parse_error("logvol / --name=NAME", KickstartValueError)
        self.assert_parse_error("logvol / --vgname=NAME", KickstartValueError)

        # fail - missing a mountpoint
        self.assert_parse_error("logvol", KickstartValueError)
        self.assert_parse_error("logvol --name=NAME", KickstartValueError)
        self.assert_parse_error("logvol --vgname=NAME", KickstartValueError)

class FC4_TestCase(FC3_TestCase):
    def runTest(self):

        # run our baseclass tests first ... but add --bytes-per-inode to each
        # expected result
        FC3_TestCase.runTest(self)

        # --fsoptions
        if "--fsoptions" in self.optionList:
            self.assert_parse("logvol / --fstype=\"BLAFS\" --fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME",
                              "logvol /  --fstype=\"BLAFS\" %s--fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

        if "--bytes-per-inode" in self.optionList:
            # --bytes-per-inode explicit
            self.assert_parse("logvol / --bytes-per-inode=123 --name=NAME --vgname=VGNAME",
                              "logvol /  --bytes-per-inode=123 --name=NAME --vgname=VGNAME\n")

            # assert data types
            self.assert_type("logvol", "bytes-per-inode", "int")

            # fail - incorrect type
            self.assert_parse_error("logvol / --bytes-per-inode B --name=NAME --vgname=VGNAME", KickstartParseError)

            # fail - missing value
            self.assert_parse_error("logvol / --bytes-per-inode --name=NAME --vgname=VGNAME", KickstartParseError)
            self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --bytes-per-inode", KickstartParseError)

        if "--encrypted" in self.optionList:
            # Just --encrypted
            self.assert_parse("logvol / --encrypted --name=NAME --vgname=VGNAME",
                              "logvol /  %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Both --encrypted and --passphrase
            self.assert_parse("logvol / --encrypted --passphrase PASSPHRASE --name=NAME --vgname=VGNAME",
                              "logvol /  %s--encrypted --passphrase=\"PASSPHRASE\" --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Using --encrypted with --passphrase=<empty>
            self.assert_parse("logvol / --encrypted --passphrase= --name=NAME --vgname=VGNAME",
                              "logvol /  %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
            self.assert_parse("logvol / --encrypted --passphrase=\"\" --name=NAME --vgname=VGNAME",
                              "logvol /  %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
            self.assert_parse("logvol / --encrypted --passphrase \"\" --name=NAME --vgname=VGNAME",
                              "logvol /  %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Just --passphrase without --encrypted
            self.assert_parse("logvol / --passphrase=\"PASSPHRASE\" --name=NAME --vgname=VGNAME",
                              "logvol /  %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # fail - missing value
            self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --encrypted --passphrase", KickstartParseError)

            # fail - --encrypted does not take a value
            self.assert_parse_error("logvol / --encrypted=1 --name=NAME --vgname=VGNAME", KickstartParseError)

RHEL5_TestCase = FC4_TestCase

class F9_TestCase(FC4_TestCase):
    def runTest(self):
        # Run our baseclass tests first
        FC4_TestCase.runTest(self)

        # assert data types
        self.assert_type("logvol", "fsprofile", "string")

        # fail - missing value
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --fsprofile", KickstartParseError)

        # Using --fsprofile
        self.assert_parse("logvol / --fsprofile \"FS_PROFILE\" --name=NAME --vgname=VGNAME",
                          "logvol /  --fsprofile=\"FS_PROFILE\" --name=NAME --vgname=VGNAME\n")

        # Ensure --bytes-per-inode has been deprecated
        self.assert_deprecated("logvol", "bytes-per-inode")

class F12_TestCase(F9_TestCase):
    def runTest(self):
        # Run our baseclass tests first
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("logvol / --name=NAME --vgname=VGNAME "
                          "--escrowcert=\"http://x/y\"",
                          "logvol /  --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --encrypted --backuppassphrase --name=NAME "
                          "--vgname=VGNAME",
                          "logvol /  --encrypted --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase --name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --encrypted --escrowcert=http://x/y "
                          "--name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME\n")

        # fail
        self.assert_parse_error("logvol / --escrowcert --name=NAME "
                                "--vgname=VGNAME")
        self.assert_parse_error("logvol / --escrowcert --backuppassphrase "
                                "--name=NAME --vgname=VGNAME")
        self.assert_parse_error("logvol / --encrypted --escrowcert "
                                "--backuppassphrase --name=NAME "
                                "--vgname=VGNAME")
        self.assert_parse_error("logvol / --backuppassphrase=False --name=NAME "
                                "--vgname=VGNAME")
        self.assert_parse_error("logvol / --backuppassphrase=True --name=NAME "
                                "--vgname=VGNAME")

class RHEL6_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        self.assert_parse("logvol / --encrypted --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --cipher=\"3-rot13\" --name=NAME --vgname=VGNAME\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("logvol / --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --name=NAME --vgname=VGNAME\n")

        self.assert_parse_error("logvol / --cipher --name=NAME --vgname=VGNAME")

        self.assert_parse("logvol swap --hibernation "
                            "--name=NAME --vgname=VGNAME")
        self.assert_parse("logvol swap --recommended --hibernation "
                            "--name=NAME --vgname=VGNAME")

class F14_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)
        self.assert_removed("logvol", "--bytes-per-inode")

class F15_TestCase(F14_TestCase):
    def runTest(self):
        F14_TestCase.runTest(self)
        self.assert_parse("logvol / --name=NAME --vgname=VGNAME --label=ROOT",
                          "logvol /  --label=\"ROOT\" --name=NAME --vgname=VGNAME\n")

class F17_TestCase(F15_TestCase):
    def runTest(self):
        F15_TestCase.runTest(self)
        self.assert_parse("logvol /x --name=NAME --size 1000 --vgname=VGNAME "
                          "--useexisting --resize",
                          "logvol /x  --size=1000 --useexisting --resize "
                          "--name=NAME --vgname=VGNAME\n")
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize")

        # no useexisting
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize --size=500")

        # no size
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize --useexisting")

class F18_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)

        self.assert_parse("logvol swap --name=NAME --vgname=VGNAME "\
                          "--hibernation")
        self.assert_parse("logvol swap --name=NAME --vgname=VGNAME "\
                          "--recommended --hibernation")

        self.assert_parse("logvol / --encrypted --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --cipher=\"3-rot13\" --name=NAME --vgname=VGNAME\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("logvol / --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --name=NAME --vgname=VGNAME\n")

        self.assert_parse_error("logvol / --cipher --name=NAME --vgname=VGNAME")

if __name__ == "__main__":
    unittest.main()
