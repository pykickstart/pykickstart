from string import strip
import unittest
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.parser import Packages
from pykickstart.version import DEVEL, returnClassForVersion

class DevelPackagesBase(CommandTest):
    @property
    def handler(self):
        return returnClassForVersion(DEVEL)

class AddGlobs_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["vim-*"])
        pkgs.add(["kde*"])

        self.assertEqual("""%packages
kde*
vim-*

%end""", strip(str(pkgs)))

class AddGroups_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["@GroupA"])
        pkgs.add(["@group-b"])
        pkgs.add(["@GroupC"])

        # Groups are printed out in alphabetic order, so group-b comes after Group*
        self.assertEqual("""%packages
@GroupA
@GroupC
@group-b

%end""", strip(str(pkgs)))

        pkgs = Packages()
        pkgs.add(["@group-a --nodefaults"])
        self.assertEqual("""%packages
@group-a --nodefaults

%end""", strip(str(pkgs)))

        pkgs = Packages()
        pkgs.add(["@group-a --optional"])
        self.assertEqual("""%packages
@group-a --optional

%end""", strip(str(pkgs)))

        self.assertRaises(KickstartValueError, pkgs.add, ["@group-b --optional --nodefaults"])

class AddPackages_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["packageA"])
        pkgs.add(["packageB"])
        pkgs.add(["packageC"])

        self.assertEqual("""%packages
packageA
packageB
packageC

%end""", strip(str(pkgs)))

class ExcludeGlobs_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["-kde*"])
        pkgs.add(["-perl*"])
        pkgs.add(["-*spell"])

        self.assertEqual("""%packages
-*spell
-kde*
-perl*

%end""", strip(str(pkgs)))

class ExcludeGroups_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["-@Conflicts"])
        pkgs.add(["-@Clustering"])

        self.assertEqual("""%packages
-@Clustering
-@Conflicts

%end""", strip(str(pkgs)))

class ExcludePackage_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["-enlightenment"])
        pkgs.add(["-clanlib"])
        pkgs.add(["-libass"])

        self.assertEqual("""%packages
-clanlib
-enlightenment
-libass

%end""", strip(str(pkgs)))

class Mixed1_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["@group-a"])
        pkgs.add(["@group-b"])
        pkgs.add(["-@group-a"])

        self.assertEqual("""%packages
@group-b
-@group-a

%end""", strip(str(pkgs)))

class Mixed2_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["vim-enhanced"])
        pkgs.add(["package-b"])
        pkgs.add(["-vim-enhanced"])

        self.assertEqual("""%packages
package-b
-vim-enhanced

%end""", strip(str(pkgs)))

class Mixed3_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.add(["vim-enhanced"])
        pkgs.add(["package-b"])
        pkgs.add(["-vim*"])

        self.assertEqual("""%packages
package-b
vim-enhanced
-vim*

%end""", strip(str(pkgs)))

class MultiLib_TestCase(DevelPackagesBase):
    def runTest(self):
        pkgs = Packages()
        pkgs.default = True
        pkgs.multiLib = True
        self.assertEqual("""%packages --default --multilib

%end""", str(pkgs).strip())

if __name__ == "__main__":
    unittest.main()
