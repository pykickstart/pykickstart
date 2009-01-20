import unittest, shlex
from tests.baseclass import *

from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.version import *
from pykickstart.commands.logvol import *

#class FC3_LogVolData(BaseData):
#class FC4_LogVolData(FC3_LogVolData):
#class RHEL5_LogVolData(FC4_LogVolData):
#class F9_LogVolData(FC3_LogVolData):

#class FC3_LogVol(KickstartCommand):
#class FC4_LogVol(FC3_LogVol):
#class RHEL5_LogVol(FC4_LogVol):
#class F9_LogVol(FC4_LogVol):

class FC3_TestCase(CommandTest):
    def setUp(self):
        CommandTest.setUp(self)
        # Disable checks for --bytes-per-inode -- not supported in FC3
        self.bytesPerInode = ""

    def runTest(self):

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
    def setUp(self):
        FC3_TestCase.setUp(self)
        # Enable checks for --bytes-per-inode -- supported in FC4
        self.bytesPerInode = "--bytes-per-inode=4096 "

    def fsoptions_tests(self):
        # --fsoptions
        self.assert_parse("logvol / --fstype=\"BLAFS\" --fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME",
                          "logvol /  --fstype=\"BLAFS\" %s--fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

    def parse_bytesPerInode(self):
        # --bytes-per-inode implicit
        self.assert_parse("logvol / --name=NAME --vgname=VGNAME",
                          "logvol /  --bytes-per-inode=4096 --name=NAME --vgname=VGNAME\n")

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

    def runTest(self):

        # run our baseclass tests first ... but add --bytes-per-inode to each
        # expected result
        FC3_TestCase.runTest(self)

        # --fsoptions
        self.fsoptions_tests()

        if self.bytesPerInode.count("--bytes-per-inode") > 0:
            # --bytes-per-inode
            self.parse_bytesPerInode()

    def encrypted_tests(self):

        # this method is only for derived classes
        self.assertNotEqual(self.__class__, FC4_TestCase)

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


class RHEL5_TestCase(FC4_TestCase):
    def runTest(self):
        # run our baseclass tests first
        FC4_TestCase.runTest(self)
        self.encrypted_tests()

class F9_TestCase(FC4_TestCase):
    def setUp(self):
        FC4_TestCase.setUp(self)
        # Disable checks for --bytes-per-inode
        self.bytesPerInode = ""

    def fsprofile_tests(self):

        # assert data types
        self.assert_type("logvol", "fsprofile", "string")

        # fail - missing value
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --fsprofile", KickstartParseError)

        # Using --fsprofile
        self.assert_parse("logvol / --fsprofile \"FS_PROFILE\" --name=NAME --vgname=VGNAME",
                          "logvol /  --fsprofile=\"FS_PROFILE\" --name=NAME --vgname=VGNAME\n")

    def runTest(self):
        # Run our baseclass tests first
        FC4_TestCase.runTest(self)

        # --encrypted and --passphrase tests
        self.encrypted_tests()

        # --fsoptions
        self.fsoptions_tests()

        # --fsprofile
        self.fsprofile_tests()

        # Ensure --bytes-per-inode has been deprecated
        self.assert_deprecated("logvol", "bytes-per-inode")

if __name__ == "__main__":
    unittest.main()
