import unittest
import warnings

from tests.baseclass import ParserTest

from pykickstart.constants import KS_MISSING_IGNORE
from pykickstart.errors import KickstartParseError, KickstartDeprecationWarning
from pykickstart.parser import Group, Packages
from pykickstart.version import DEVEL, F7, F21, RHEL6, returnClassForVersion, RHEL7


class DevelPackagesBase(ParserTest):
    @property
    def handler(self):
        return returnClassForVersion(DEVEL)

    def runTest(self):
        self.get_parser()

class AddGlobs_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["vim-*"])
        pkgs.add(["kde*"])

        self.assertEqual("""%packages
kde*
vim-*

%end""", str(pkgs).strip())

class AddGroups_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["@GroupA"])
        pkgs.add(["@group-b"])
        pkgs.add(["@GroupC"])

        # Groups are printed out in alphabetic order, so group-b comes after Group*
        self.assertEqual("""%packages
@GroupA
@GroupC
@group-b

%end""", str(pkgs).strip())

        pkgs = Packages()
        pkgs.add(["@group-a --nodefaults"])
        self.assertEqual("""%packages
@group-a --nodefaults

%end""", str(pkgs).strip())

        pkgs = Packages()
        pkgs.add(["@group-a --optional"])
        self.assertEqual("""%packages
@group-a --optional

%end""", str(pkgs).strip())

        self.assertRaises(KickstartParseError, pkgs.add, ["@group-b --optional --nodefaults"])

class AddGroupsAndEnvironment_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["@^EnvironmentA"])
        pkgs.add(["@GroupB"])
        pkgs.add(["packageC"])

        self.assertEqual("""%packages
@^EnvironmentA
@GroupB
packageC

%end""", str(pkgs).strip())

class AddPackages_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["packageA"])
        pkgs.add(["packageB"])
        pkgs.add(["packageC"])

        self.assertEqual("""%packages
packageA
packageB
packageC

%end""", str(pkgs).strip())

class ExcludeGlobs_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["-kde*"])
        pkgs.add(["-perl*"])
        pkgs.add(["-*spell"])

        self.assertEqual("""%packages
-*spell
-kde*
-perl*

%end""", str(pkgs).strip())

class ExcludeGroups_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["-@Conflicts"])
        pkgs.add(["-@Clustering"])

        self.assertEqual("""%packages
-@Clustering
-@Conflicts

%end""", str(pkgs).strip())

class ExcludePackage_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["-enlightenment"])
        pkgs.add(["-clanlib"])
        pkgs.add(["-libass"])

        self.assertEqual("""%packages
-clanlib
-enlightenment
-libass

%end""", str(pkgs).strip())

class Mixed1_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["@group-a"])
        pkgs.add(["@group-b"])
        pkgs.add(["-@group-a"])

        self.assertEqual("""%packages
@group-b
-@group-a

%end""", str(pkgs).strip())

class Mixed2_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["vim-enhanced"])
        pkgs.add(["package-b"])
        pkgs.add(["-vim-enhanced"])

        self.assertEqual("""%packages
package-b
-vim-enhanced

%end""", str(pkgs).strip())

class Mixed3_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.add(["vim-enhanced"])
        pkgs.add(["package-b"])
        pkgs.add(["-vim*"])

        self.assertEqual("""%packages
package-b
vim-enhanced
-vim*

%end""", str(pkgs).strip())

class MultiLib_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.default = True
        pkgs.multiLib = True
        self.assertEqual("""%packages --default --multilib

%end""", str(pkgs).strip())

class WeakDeps_TestCase(DevelPackagesBase):
    def runTest(self):
        DevelPackagesBase.runTest(self)

        pkgs = Packages()
        pkgs.default = True
        pkgs.excludeWeakdeps = True
        self.assertEqual("""%packages --default --excludeWeakdeps

%end""", str(pkgs).strip())

class GroupObj_TestCase(DevelPackagesBase):
    def runTest(self):
        self.assertLess(Group("A"), Group("B"))
        self.assertLessEqual(Group("A"), Group("B"))
        self.assertLessEqual(Group("A"), Group("A"))
        self.assertEqual(Group("A"), Group("A"))
        self.assertNotEqual(Group("A"), Group("B"))
        self.assertGreater(Group("B"), Group("A"))
        self.assertGreaterEqual(Group("B"), Group("A"))
        self.assertGreaterEqual(Group("B"), Group("B"))

class GroupsAreHashable_TestCase(ParserTest):
    def runTest(self):
        hash(Group(name="groupA"))

class Packages_Options_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages --ignoremissing --default --instLangs="bg_BG" --excludedocs
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that the options are parsed as expected
        self.assertTrue(self.handler.packages.default)
        self.assertTrue(self.handler.packages.excludeDocs)
        self.assertEqual(self.handler.packages.handleMissing, KS_MISSING_IGNORE)
        self.assertEqual(self.handler.packages.instLangs, "bg_BG")

        # And then test that all those options would be printed out
        # correctly.
        self.assertEqual(str(self.handler.packages), "\n%packages --default --excludedocs --ignoremissing --instLangs=bg_BG\n\n%end\n")

        # extra test coverage
        self.assertTrue(self.parser._sections['%packages'].seen)

class Packages_Options_Empty_InstLangs_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages --instLangs=
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that instLangs is an empty string
        self.assertEqual(self.handler.packages.instLangs, "")

        # Verify that the empty instLangs comes back out
        self.assertEqual(str(self.handler.packages).strip(), "%packages --instLangs=\n\n%end")

class Packages_Options_No_InstLangs_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that instLangs is None
        self.assertIsNone(self.handler.packages.instLangs)

        # Verify that --instLangs is not displayed
        self.assertEqual(str(self.handler.packages).strip(), "%packages\n\n%end")

class Packages_Contains_Comments_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
packageA    # this is an end-of-line comment
# this is a whole line comment
packageB
packageC
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)

        # Verify that the packages are what we think they are.
        self.assertEqual(len(self.handler.packages.packageList), 3)
        self.assertEqual(self.handler.packages.packageList[0], "packageA")
        self.assertEqual(self.handler.packages.packageList[1], "packageB")
        self.assertEqual(self.handler.packages.packageList[2], "packageC")

class Packages_Contains_Nobase_1_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = F21
        self.ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[-1].message, KickstartDeprecationWarning)

class Packages_Contains_Nobase_2_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = RHEL6
        self.ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 0)

            self.assertEqual(str(self.handler.packages), "\n%packages --nobase\nbash\n\n%end\n")

class Packages_Contains_Nobase_3_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages --nobase
bash
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Nocore_1_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages --nocore
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(str(self.handler.packages), "\n%packages --nocore\n\n%end\n")

class Packages_Contains_Nobase_Default_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = F21
        self.ks = """
%packages --nobase --default
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Nocore_Default_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages --nocore --default
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Packages_Contains_Environment_1_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
@^whatever-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "whatever-environment")

class Packages_Contains_Environment_2_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
@^whatever-environment
@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "another-environment")

class Packages_Contains_Environment_3_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
@^whatever-environment
-@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "whatever-environment")

class Packages_Contains_Environment_4_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
@^whatever-environment
-@^whatever-environment
@^another-environment
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(self.handler.packages.environment, "another-environment")

# An empty %packages section is allowed, and means something different from %packages --default.
# An empty section means to install the minimum amount of stuff, while --default means to install
# whatever would have been installed had this been a graphical installation and the user just
# accepted whatever was offered.
class Packages_Empty_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%packages
%end
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertTrue(self.handler.packages.seen)
            self.assertEqual(str(self.handler.packages).strip(), "%packages\n\n%end")

class Old_Packages_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = F7
        self.ks = """
%packages
bash
"""

    def runTest(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(str(self.handler.packages), "\n%packages\nbash\n\n")

class Packages_Timeout_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = RHEL7
        self.ks = """
    %packages --timeout=60
    bash
    %end
    """

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 0)
            self.assertEqual(str(self.handler.packages), "\n%packages --timeout=60\nbash\n\n%end\n")

class Packages_Retries_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.version = RHEL7
        self.ks = """
    %packages --retries=10
    bash
    %end
    """

    def runTest(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.parser.readKickstartFromString(self.ks)
            self.assertEqual(len(w), 0)
            self.assertEqual(str(self.handler.packages), "\n%packages --retries=10\nbash\n\n%end\n")

if __name__ == "__main__":
    unittest.main()
