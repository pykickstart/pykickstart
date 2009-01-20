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
    def runTest(self):
        # --name and --vgname
        self.assert_parse("logvol / --name=NAME --vgname=VGNAME",
                          "logvol /  --name=NAME --vgname=VGNAME\n")
        # --fstype
        self.assert_parse("logvol / --fstype=\"BLAFS\" --name=NAME --vgname=VGNAME",
                          "logvol /  --fstype=\"BLAFS\" --name=NAME --vgname=VGNAME\n")
        # --grow
        self.assert_parse("logvol / --grow --name=NAME --vgname=VGNAME",
                          "logvol /  --grow --name=NAME --vgname=VGNAME\n")
        # --size
        self.assert_parse("logvol / --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --size=1024 --name=NAME --vgname=VGNAME\n")
        # --maxsize
        self.assert_parse("logvol / --maxsize=2048 --size=1024 --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --size=1024 --name=NAME --vgname=VGNAME\n")
        # --recommended
        self.assert_parse("logvol / --maxsize=2048 --recommended --name=NAME --vgname=VGNAME",
                          "logvol /  --maxsize=2048 --recommended --name=NAME --vgname=VGNAME\n")
        # --percent
        self.assert_parse("logvol / --percent=10 --name=NAME --vgname=VGNAME",
                          "logvol /  --percent=10 --name=NAME --vgname=VGNAME\n")
        # --noformat
        self.assert_parse("logvol / --noformat --name=NAME --vgname=VGNAME",
                          "logvol /  --noformat --name=NAME --vgname=VGNAME\n")
        # --useexisting
        self.assert_parse("logvol / --useexisting --name=NAME --vgname=VGNAME",
                          "logvol /  --useexisting --name=NAME --vgname=VGNAME\n")

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

if __name__ == "__main__":
    unittest.main()
