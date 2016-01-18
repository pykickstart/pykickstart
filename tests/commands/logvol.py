from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.errors import KickstartParseError

class FC3_TestCase(CommandTest):
    command = "logvol"

    def __init__(self, *kargs, **kwargs):
        CommandTest.__init__(self, *kargs, **kwargs)
        self.bytesPerInode = ""

    def runTest(self):
        if "--bytes-per-inode" in self.optionList:
            self.bytesPerInode = "--bytes-per-inode=4096 "

        self.assertFalse(self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME") == None)
        self.assertTrue(self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME") != \
                        self.assert_parse("logvol / --size=1024 --name=OTHER --vgname=VGNAME"))
        self.assertFalse(self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME") == \
                         self.assert_parse("logvol / --size=1024 --name=OTHER --vgname=VGNAME"))
        self.assertFalse(self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME") == \
                         self.assert_parse("logvol / --size=1024 --name=NAME --vgname=OTHERVG"))

        # --name and --vgname
        self.assert_parse("logvol / --size=10240 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=10240 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --fstype
        self.assert_parse("logvol / --fstype=\"BLAFS\" --size=10240 --name=NAME --vgname=VGNAME",
                          "logvol /  --fstype=\"BLAFS\" --size=10240 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --grow
        self.assert_parse("logvol / --grow --size=10240 --name=NAME --vgname=VGNAME",
                          "logvol /  --grow --size=10240 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --size
        self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --maxsize
        self.assert_parse("logvol / --maxsize=2048 --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
        # --recommended
        self.assert_parse("logvol / --maxsize=2048 --recommended --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --recommended --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
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
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --size=SIZE", KickstartParseError, "argument --size: invalid int value: 'SIZE'")
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --maxsize=MAXSIZE", KickstartParseError, "argument --maxsize: invalid int value: 'MAXSIZE'")
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --percent=PCT", KickstartParseError, "argument --percent: invalid int value: 'PCT'")

        # assert required options
        self.assert_required("logvol", "name")
        self.assert_required("logvol", "vgname")

        # fail - missing required
        self.assert_parse_error("logvol / --name=NAME", KickstartParseError, "arguments are required: --vgname")
        self.assert_parse_error("logvol / --vgname=NAME", KickstartParseError, "arguments are required: --name")

        # fail - missing a mountpoint
        self.assert_parse_error("logvol", KickstartParseError, "arguments are required: --name")
        self.assert_parse_error("logvol --name=NAME", KickstartParseError, "arguments are required: --vgname")
        self.assert_parse_error("logvol --vgname=NAME", KickstartParseError, "arguments are required: --name")
        self.assert_parse_error("logvol --name=NAME --vgname=NAME", KickstartParseError, "Mount point required for logvol")

class FC3_Duplicate_TestCase(CommandSequenceTest):
    def runTest(self):
        self.assert_parse("""
logvol / --size=1024 --name=nameA --vgname=vgA
logvol /home --size=1024 --name=nameB --vgname=vgA""")

        self.assert_parse("""
logvol / --size=1024 --name=nameA --vgname=vgA
logvol /home --size=1024 --name=nameA --vgname=vgB""")

        self.assert_parse_error("""
logvol / --size=1024 --name=nameA --vgname=vgA
logvol /home --size=1024 --name=nameA --vgname=vgA""", UserWarning)

class FC4_TestCase(FC3_TestCase):
    def runTest(self):

        # run our baseclass tests first ... but add --bytes-per-inode to each
        # expected result
        FC3_TestCase.runTest(self)

        # --fsoptions
        if "--fsoptions" in self.optionList:
            self.assert_parse("logvol / --fstype=\"BLAFS\" --size=1024 --fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME",
                              "logvol /  --fstype=\"BLAFS\" --size=1024 %s--fsoptions=\"ABC 123\" --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

        if "--bytes-per-inode" in self.optionList:
            # --bytes-per-inode explicit
            self.assert_parse("logvol / --bytes-per-inode=123 --name=NAME --vgname=VGNAME",
                              "logvol /  --bytes-per-inode=123 --name=NAME --vgname=VGNAME\n")

            # assert data types
            self.assert_type("logvol", "bytes-per-inode", "int")

            # fail - incorrect type
            self.assert_parse_error("logvol / --bytes-per-inode B --name=NAME --vgname=VGNAME", KickstartParseError, "argument --bytes-per-inode: invalid int value: 'B'")

            # fail - missing value
            self.assert_parse_error("logvol / --bytes-per-inode --name=NAME --vgname=VGNAME", KickstartParseError, "argument --bytes-per-inode: expected one argument")
            self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --bytes-per-inode", KickstartParseError, "argument --bytes-per-inode: expected one argument")

        if "--encrypted" in self.optionList:
            # Just --encrypted
            self.assert_parse("logvol / --size=1024 --encrypted --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Both --encrypted and --passphrase
            self.assert_parse("logvol / --size=1024 --encrypted --passphrase PASSPHRASE --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--encrypted --passphrase=\"PASSPHRASE\" --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Using --encrypted with --passphrase=<empty>
            self.assert_parse("logvol / --size=1024 --encrypted --passphrase= --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
            self.assert_parse("logvol / --size=1024 --encrypted --passphrase=\"\" --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)
            self.assert_parse("logvol / --size=1024 --encrypted --passphrase \"\" --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--encrypted --name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # Just --passphrase without --encrypted
            self.assert_parse("logvol / --size=1024 --passphrase=\"PASSPHRASE\" --name=NAME --vgname=VGNAME",
                              "logvol /  --size=1024 %s--name=NAME --vgname=VGNAME\n" % self.bytesPerInode)

            # fail - missing value
            self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --encrypted --passphrase", KickstartParseError, "argument --passphrase: expected one argument")

            # fail - --encrypted does not take a value
            self.assert_parse_error("logvol / --encrypted=1 --name=NAME --vgname=VGNAME", KickstartParseError, "argument --encrypted: ignored explicit argument")

RHEL5_TestCase = FC4_TestCase

class F9_TestCase(FC4_TestCase):
    def runTest(self):
        # Run our baseclass tests first
        FC4_TestCase.runTest(self)

        # assert data types
        self.assert_type("logvol", "fsprofile", "string")

        # fail - missing value
        self.assert_parse_error("logvol / --name=NAME --vgname=VGNAME --fsprofile", KickstartParseError, "argument --fsprofile: expected one argument")

        # Using --fsprofile
        self.assert_parse("logvol / --size=1024 --fsprofile \"FS_PROFILE\" --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --fsprofile=\"FS_PROFILE\" --name=NAME --vgname=VGNAME\n")

        # Ensure --bytes-per-inode has been deprecated
        self.assert_deprecated("logvol", "bytes-per-inode")

class F12_TestCase(F9_TestCase):
    def runTest(self):
        # Run our baseclass tests first
        F9_TestCase.runTest(self)

        # pass
        self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME "
                          "--escrowcert=\"http://x/y\"",
                          "logvol /  --size=1024 --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --size=1024 --encrypted --backuppassphrase --name=NAME "
                          "--vgname=VGNAME",
                          "logvol /  --size=1024 --encrypted --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --size=1024 --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --size=1024 --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --encrypted --escrowcert=\"http://x/y\" "
                          "--backuppassphrase --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol / --size=1024 --encrypted --escrowcert=http://x/y "
                          "--name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --encrypted --escrowcert=\"http://x/y\" "
                          "--name=NAME --vgname=VGNAME\n")

        # fail
        self.assert_parse_error("logvol / --escrowcert --name=NAME --vgname=VGNAME",
                                KickstartParseError,
                                "argument --escrowcert: expected one argument")
        self.assert_parse_error("logvol / --escrowcert --backuppassphrase --name=NAME --vgname=VGNAME",
                                KickstartParseError,
                                "argument --escrowcert: expected one argument")
        self.assert_parse_error("logvol / --encrypted --escrowcert --backuppassphrase --name=NAME --vgname=VGNAME",
                                KickstartParseError,
                                "argument --escrowcert: expected one argument")
        self.assert_parse_error("logvol / --backuppassphrase=False --name=NAME --vgname=VGNAME",
                                KickstartParseError,
                                "argument --backuppassphrase: ignored explicit argument")
        self.assert_parse_error("logvol / --backuppassphrase=True --name=NAME --vgname=VGNAME",
                                KickstartParseError,
                                "argument --backuppassphrase: ignored explicit argument")

class RHEL6_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)

        self.assert_parse("logvol / --size=1024 --fsprofile \"FS_PROFILE\" --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --fsprofile=\"FS_PROFILE\" --name=NAME --vgname=VGNAME\n")

        self.assert_parse("logvol / --encrypted --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --encrypted --cipher=\"3-rot13\" --name=NAME --vgname=VGNAME\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("logvol / --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --name=NAME --vgname=VGNAME\n")

        self.assert_parse_error("logvol / --cipher --name=NAME --vgname=VGNAME", regex="argument --cipher: expected one argument")

        self.assert_parse("logvol swap --hibernation --name=NAME --vgname=VGNAME",
                          "logvol swap  --hibernation --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol swap --recommended --hibernation --name=NAME --vgname=VGNAME",
                          "logvol swap  --recommended --hibernation --name=NAME --vgname=VGNAME\n")

        # thinp
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool",
                          "logvol none  --thinpool --name=pool1 --vgname=vg\n")
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool "
                          "--chunksize=512",
                          "logvol none  --thinpool --chunksize=512 "
                          "--name=pool1 --vgname=vg\n")
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool "
                          "--metadatasize=4 --chunksize=1024",
                          "logvol none  --thinpool --metadatasize=4 "
                          "--chunksize=1024 --name=pool1 --vgname=vg\n")
        self.assert_parse("logvol /home --name=home --vgname=vg "
                          "--thin --poolname=pool1",
                          "logvol /home  --thin --poolname=pool1 "
                          "--name=home --vgname=vg\n")
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool --profile=performance --size=500",
                          "logvol none  --size=500 --thinpool --profile=performance --name=pool1 --vgname=vg\n")

        # missing pool name
        self.assert_parse_error("logvol /home --name=home --vgname=vg --thin")

        # chunksize is an int
        self.assert_parse_error("logvol none --name=pool1 --vgname=vg "
                                "--thinpool --chunksize=foo")

        # both --thin and --thinpool
        self.assert_parse_error("logvol /home --name=home --thin --thinpool --vgname=vg --size=10000")

        # chunksize and/or metadata size and not thinpool
        self.assert_parse_error("logvol none --name=pool1 --vgname=vg "
                                "--chunksize=512")

class RHEL6_AutopartLogVol_TestCase(CommandSequenceTest):
    def runTest(self):
        # fail - can't use both autopart and logvol
        self.assert_parse_error("""
autopart
logvol / --size=1024 --name=lv --vgname=vg""", KickstartParseError)

class F14_TestCase(F12_TestCase):
    def runTest(self):
        F12_TestCase.runTest(self)
        self.assert_removed("logvol", "--bytes-per-inode")

class F15_TestCase(F14_TestCase):
    def runTest(self):
        F14_TestCase.runTest(self)
        self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME --label=ROOT",
                          "logvol /  --size=1024 --label=\"ROOT\" --name=NAME --vgname=VGNAME\n")

class F17_TestCase(F15_TestCase):
    def runTest(self):
        F15_TestCase.runTest(self)
        self.assert_parse("logvol /x --name=NAME --size 1000 --vgname=VGNAME "
                          "--useexisting --resize",
                          "logvol /x  --size=1000 --useexisting --resize "
                          "--name=NAME --vgname=VGNAME\n")
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize", regex="--resize can only be used in conjunction with --useexisting")

        # no useexisting
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize --size=500", regex="--resize can only be used in conjunction with --useexisting")

        # no size
        self.assert_parse_error("logvol /x --name=NAME --vgname=VGNAME --resize --useexisting", regex="--resize requires --size to indicate new size")

class F18_TestCase(F17_TestCase):
    def runTest(self):
        F17_TestCase.runTest(self)

        self.assert_parse("logvol swap --name=NAME --vgname=VGNAME --hibernation --size=1024",
                          "logvol swap  --size=1024 --hibernation --name=NAME --vgname=VGNAME\n")
        self.assert_parse("logvol swap --name=NAME --vgname=VGNAME --recommended --hibernation --size=1024",
                          "logvol swap  --recommended --size=1024 --hibernation --name=NAME --vgname=VGNAME\n")

        self.assert_parse("logvol / --size=1024 --encrypted --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --encrypted --cipher=\"3-rot13\" --name=NAME --vgname=VGNAME\n")
        # Allowed here, but anaconda should complain.  Note how we throw out
        # cipher from the output if there's no --encrypted.
        self.assert_parse("logvol / --size=1024 --cipher=3-rot13 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --name=NAME --vgname=VGNAME\n")

        self.assert_parse_error("logvol / --cipher --name=NAME --vgname=VGNAME", regex="argument --cipher: expected one argument")

class F20_TestCase(F18_TestCase):
    def runTest(self):
        F18_TestCase.runTest(self)

        self.assert_parse("logvol none --size=1024 --name=pool1 --vgname=vg --thinpool",
                          "logvol none  --size=1024 --thinpool --name=pool1 --vgname=vg\n")
        self.assert_parse("logvol none --size=1024 --name=pool1 --vgname=vg "
                          "--thinpool --chunksize=512",
                          "logvol none  --size=1024 --thinpool --chunksize=512 "
                          "--name=pool1 --vgname=vg\n")
        self.assert_parse("logvol none --size=1024 --name=pool1 --vgname=vg "
                          "--thinpool --metadatasize=4 --chunksize=1024",
                          "logvol none  --size=1024 --thinpool "
                          "--metadatasize=4 --chunksize=1024 --name=pool1 "
                          "--vgname=vg\n")
        self.assert_parse("logvol /home --size=1024 --name=home --vgname=vg "
                          "--thin --poolname=pool1",
                          "logvol /home  --size=1024 --thin --poolname=pool1 "
                          "--name=home --vgname=vg\n")

        # missing pool name
        self.assert_parse_error("logvol /home --name=home --vgname=vg --thin",
                                regex="--thin requires --poolname to specify pool name")

        # chunksize is an int
        self.assert_parse_error("logvol none --name=pool1 --vgname=vg "
                                "--thinpool --chunksize=foo",
                                regex="argument --chunksize: invalid int value: 'foo'")

        # both --thin and --thinpool
        self.assert_parse_error("logvol /home --name=home --thin --thinpool --vgname=vg --size=10000", regex="--thin and --thinpool cannot both be specified for the same logvol")

        # chunksize and/or metadata size and not thinpool
        self.assert_parse_error("logvol none --name=pool1 --vgname=vg "
                                "--chunksize=512",
                                regex="--chunksize and --metadatasize are for thin pools only")

        # logvol w/out specified size
        self.assert_parse_error("logvol none --name=pool1 --vgname=vg --thinpool",
                                regex="No size given for logical volume")

        # use existing logvol, which must have a size
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool --useexisting")

        # logvol with a disallowed percent value
        self.assert_parse_error("logvol / --percent=1000 --name=NAME --vgname=VGNAME",
                                regex="Percentage must be between 0 and 100.")

class F21_TestCase(F20_TestCase):
    def runTest(self):
        F20_TestCase.runTest(self)

        # --profile should work for all logvol commands even though it may be
        # implemented only for some types (thin pool,...)
        self.assert_parse("logvol none --name=pool1 --vgname=vg --thinpool --profile=performance --size=500",
                          "logvol none  --size=500 --thinpool --profile=performance --name=pool1 --vgname=vg\n")
        self.assert_parse("logvol /home --name=homelv --vgname=vg --profile=performance --size=500")

        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=2 --percent=30")

class RHEL7_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

        # pass
        self.assert_parse("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing",
                          "logvol /  --size=4096 --mkfsoptions=\"some,thing\" --name=LVNAME --vgname=VGNAME\n")

        # can't use --mkfsoptions if you're not formatting
        self.assert_parse_error("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing --noformat")

        # can't use --mkfsoptions with --fsprofile
        self.assert_parse_error("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing --fsprofile=PROFILE")

class F23_TestCase(F21_TestCase):
    def runTest(self):
        F21_TestCase.runTest(self)

        # can't use --mkfsoptions with --fsprofile
        self.assert_parse_error("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing --fsprofile=PROFILE")

        # accept cache specifications
        self.assert_parse("logvol /home --name=home --vgname=vg --size=500 --cachesize=250 --cachepvs=pv.01,pv.02 --cachemode=writeback",
                          "logvol /home  --size=500 --cachesize=250 --cachepvs=pv.01,pv.02 --cachemode=writeback --name=home --vgname=vg\n")
        # cache mode is not required
        self.assert_parse("logvol /home --name=home --vgname=vg --size=500 --cachesize=250 --cachepvs=pv.01,pv.02")

        # both cache size and cache PVs are required
        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=500 --cachesize=250")
        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=500 --cachepvs=pv.01,pv.02")
        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=500 --cachemode=writeback")
        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=500 --cachesize=250 --cachepvs=pv.01,pv.02 --cachemode=writeback --useexisting")
        self.assert_parse_error("logvol /home --name=home --vgname=vg --size=500 --cachesize=250 --cachepvs=pv.01,pv.02 --cachemode=writeback --noformat")

        # pass
        self.assert_parse("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing",
                          "logvol /  --size=4096 --mkfsoptions=\"some,thing\" --name=LVNAME --vgname=VGNAME\n")

        # can't use --mkfsoptions if you're not formatting
        self.assert_parse_error("logvol / --size=4096 --name=LVNAME --vgname=VGNAME --mkfsoptions=some,thing --noformat")

if __name__ == "__main__":
    unittest.main()
