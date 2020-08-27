import six
import sys
import unittest
import tempfile
import os

from tests.baseclass import CommandTest, loadModules

from pykickstart.version import *           # pylint: disable=wildcard-import
from pykickstart.errors import KickstartVersionError

def getClassName(cls):
    return cls().__class__.__name__

class StringToVersion_TestCase(CommandTest):
    def runTest(self):

        # fail - no version specified
        self.assertRaises(KickstartVersionError, stringToVersion, "RHEL")
        self.assertRaises(KickstartVersionError, stringToVersion, "Red Hat Enterprise Linux")
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora")
        self.assertRaises(KickstartVersionError, stringToVersion, "F")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC")

        # fail - too old
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora Core 1")
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora Core 2")

        # fail - incorrect syntax
        self.assertRaises(KickstartVersionError, stringToVersion, "FC7")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC8")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC9")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC10")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC11")
        self.assertRaises(KickstartVersionError, stringToVersion, "F1111")
        self.assertRaises(KickstartVersionError, stringToVersion, "F 11")

        # fail - doesn't exist
        self.assertRaises(KickstartVersionError, stringToVersion, "Red hat Enterprise Linux 1")

        # pass - FC3
        self.assertEqual(stringToVersion("Fedora Core 3"), FC3)
        self.assertEqual(stringToVersion("FC3"), FC3)
        # pass - FC4
        self.assertEqual(stringToVersion("Fedora Core 4"), FC4)
        self.assertEqual(stringToVersion("FC4"), FC4)
        # pass - FC5
        self.assertEqual(stringToVersion("Fedora Core 5"), FC5)
        self.assertEqual(stringToVersion("FC5"), FC5)
        # pass - FC6
        self.assertEqual(stringToVersion("Fedora Core 6"), FC6)
        self.assertEqual(stringToVersion("FC6"), FC6)
        # pass - F7
        self.assertEqual(stringToVersion("Fedora Core 7"), F7)
        self.assertEqual(stringToVersion("Fedora 7"), F7)
        self.assertEqual(stringToVersion("F7"), F7)
        # pass - F8
        self.assertEqual(stringToVersion("Fedora Core 8"), F8)
        self.assertEqual(stringToVersion("Fedora 8"), F8)
        self.assertEqual(stringToVersion("F8"), F8)
        # pass - F9
        self.assertEqual(stringToVersion("Fedora Core 9"), F9)
        self.assertEqual(stringToVersion("Fedora 9"), F9)
        self.assertEqual(stringToVersion("F9"), F9)
        # pass - F10
        self.assertEqual(stringToVersion("Fedora Core 10"), F10)
        self.assertEqual(stringToVersion("Fedora 10"), F10)
        self.assertEqual(stringToVersion("F10"), F10)
        # pass - F11
        self.assertEqual(stringToVersion("Fedora 11"), F11)
        self.assertEqual(stringToVersion("F11"), F11)
        # pass - F12
        self.assertEqual(stringToVersion("Fedora 12"), F12)
        self.assertEqual(stringToVersion("F12"), F12)
        # pass - F13
        self.assertEqual(stringToVersion("Fedora 13"), F13)
        self.assertEqual(stringToVersion("F13"), F13)
        # pass - F14
        self.assertEqual(stringToVersion("Fedora 14"), F14)
        self.assertEqual(stringToVersion("F14"), F14)
        # pass - F15
        self.assertEqual(stringToVersion("Fedora 15"), F15)
        self.assertEqual(stringToVersion("F15"), F15)
        # pass - F16
        self.assertEqual(stringToVersion("Fedora 16"), F16)
        self.assertEqual(stringToVersion("F16"), F16)
        # pass - F17
        self.assertEqual(stringToVersion("Fedora 17"), F17)
        self.assertEqual(stringToVersion("F17"), F17)
        # pass - F18
        self.assertEqual(stringToVersion("Fedora 18"), F18)
        self.assertEqual(stringToVersion("F18"), F18)
        # pass - F19
        self.assertEqual(stringToVersion("Fedora 19"), F19)
        self.assertEqual(stringToVersion("F19"), F19)
        # pass - F20
        self.assertEqual(stringToVersion("Fedora 20"), F20)
        self.assertEqual(stringToVersion("F20"), F20)
        # pass - F21
        self.assertEqual(stringToVersion("Fedora 21"), F21)
        self.assertEqual(stringToVersion("F21"), F21)
        # pass - F22
        self.assertEqual(stringToVersion("Fedora 22"), F22)
        self.assertEqual(stringToVersion("F22"), F22)
        # pass - F23
        self.assertEqual(stringToVersion("Fedora 23"), F23)
        self.assertEqual(stringToVersion("F23"), F23)
        # pass - F24
        self.assertEqual(stringToVersion("Fedora 24"), F24)
        self.assertEqual(stringToVersion("F24"), F24)
        # pass - F25
        self.assertEqual(stringToVersion("Fedora 25"), F25)
        self.assertEqual(stringToVersion("F25"), F25)
        # pass - F26
        self.assertEqual(stringToVersion("Fedora 26"), F26)
        self.assertEqual(stringToVersion("F26"), F26)
        # pass - F27
        self.assertEqual(stringToVersion("Fedora 27"), F27)
        self.assertEqual(stringToVersion("F27"), F27)
        # pass - F28
        self.assertEqual(stringToVersion("Fedora 28"), F28)
        self.assertEqual(stringToVersion("F28"), F28)
        # pass - F29
        self.assertEqual(stringToVersion("Fedora 29"), F29)
        self.assertEqual(stringToVersion("F29"), F29)
        # pass - F30
        self.assertEqual(stringToVersion("Fedora 30"), F30)
        self.assertEqual(stringToVersion("F30"), F30)
        # pass - F31
        self.assertEqual(stringToVersion("Fedora 31"), F31)
        self.assertEqual(stringToVersion("F31"), F31)
        # pass - F32
        self.assertEqual(stringToVersion("Fedora 32"), F32)
        self.assertEqual(stringToVersion("F32"), F32)
        # pass - F33
        self.assertEqual(stringToVersion("Fedora 33"), F33)
        self.assertEqual(stringToVersion("F33"), F33)
        # pass - F34
        self.assertEqual(stringToVersion("Fedora 34"), F34)
        self.assertEqual(stringToVersion("F34"), F34)

        # pass - RHEL3
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux AS 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux ES 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux WS 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Desktop 3"), RHEL3)
        self.assertEqual(stringToVersion("RHEL3"), RHEL3)

        # pass - RHEL4
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux AS 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux ES 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux WS 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Desktop 4"), RHEL4)
        self.assertEqual(stringToVersion("RHEL4"), RHEL4)

        # pass - RHEL5
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 5"), RHEL5)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 5"), RHEL5)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 5"), RHEL5)
        for MINOR in range(1, 10):
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux 5.%s" % MINOR), RHEL5)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 5.%s" % MINOR), RHEL5)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 5.%s" % MINOR), RHEL5)
        self.assertEqual(stringToVersion("RHEL5"), RHEL5)

        # pass - RHEL6
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 6"), RHEL6)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 6"), RHEL6)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 6"), RHEL6)
        for MINOR in range(1, 10):
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux 6.%s" % MINOR), RHEL6)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 6.%s" % MINOR), RHEL6)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 6.%s" % MINOR), RHEL6)
        self.assertEqual(stringToVersion("RHEL6"), RHEL6)

        # pass - RHEL7
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 7"), RHEL7)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 7"), RHEL7)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 7"), RHEL7)
        for MINOR in range(1, 10):
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux 7.%s" % MINOR), RHEL7)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 7.%s" % MINOR), RHEL7)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 7.%s" % MINOR), RHEL7)
        self.assertEqual(stringToVersion("RHEL7"), RHEL7)

        # pass - RHEL8
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 8"), RHEL8)
        for MINOR in range(1,10):
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux 8.%s" % MINOR), RHEL8)
        self.assertEqual(stringToVersion("RHEL8"), RHEL8)

class VersionToString_TestCase(CommandTest):
    def runTest(self):

        # Make sure DEVEL is the highest version, but RHEL versions aren't
        # counted as devel.
        highest = 0
        for (ver_str, ver_num) in list(versionMap.items()):
            if ver_str.startswith("RHEL"):
                continue

            highest = max(ver_num, highest)
        self.assertEqual(highest, DEVEL)

        # FC series
        self.assertEqual(versionToString(FC3), "FC3")
        self.assertEqual(versionToString(FC4), "FC4")
        self.assertEqual(versionToString(FC5), "FC5")
        self.assertEqual(versionToString(FC6), "FC6")
        # F series
        self.assertEqual(versionToString(F7), "F7")
        self.assertEqual(versionToString(F8), "F8")
        self.assertEqual(versionToString(F9), "F9")
        self.assertEqual(versionToString(F10), "F10")
        self.assertEqual(versionToString(F10, skipDevel=True), "F10")
        self.assertEqual(versionToString(F10, skipDevel=False), "F10")
        self.assertEqual(versionToString(F11, skipDevel=True), "F11")
        self.assertEqual(versionToString(F11, skipDevel=False), "F11")
        self.assertEqual(versionToString(F12, skipDevel=True), "F12")
        self.assertEqual(versionToString(F13, skipDevel=True), "F13")
        self.assertEqual(versionToString(F14, skipDevel=True), "F14")
        self.assertEqual(versionToString(F15, skipDevel=True), "F15")
        self.assertEqual(versionToString(F16, skipDevel=True), "F16")
        self.assertEqual(versionToString(F17, skipDevel=True), "F17")
        self.assertEqual(versionToString(F18, skipDevel=True), "F18")
        self.assertEqual(versionToString(F19, skipDevel=True), "F19")
        self.assertEqual(versionToString(F20, skipDevel=True), "F20")
        self.assertEqual(versionToString(F21, skipDevel=True), "F21")
        self.assertEqual(versionToString(F22, skipDevel=True), "F22")
        self.assertEqual(versionToString(F23, skipDevel=True), "F23")
        self.assertEqual(versionToString(F24, skipDevel=True), "F24")
        self.assertEqual(versionToString(F25, skipDevel=True), "F25")
        self.assertEqual(versionToString(F26, skipDevel=True), "F26")
        self.assertEqual(versionToString(F27, skipDevel=True), "F27")
        self.assertEqual(versionToString(F28, skipDevel=True), "F28")
        self.assertEqual(versionToString(F29, skipDevel=True), "F29")
        self.assertEqual(versionToString(F30, skipDevel=True), "F30")
        self.assertEqual(versionToString(F31, skipDevel=True), "F31")
        self.assertEqual(versionToString(F32, skipDevel=True), "F32")
        self.assertEqual(versionToString(F33, skipDevel=True), "F33")
        self.assertEqual(versionToString(F34, skipDevel=True), "F34")
        self.assertEqual(versionToString(F34, skipDevel=False), "DEVEL")
        # RHEL series
        self.assertEqual(versionToString(RHEL3), "RHEL3")
        self.assertEqual(versionToString(RHEL4), "RHEL4")
        self.assertEqual(versionToString(RHEL5), "RHEL5")
        self.assertEqual(versionToString(RHEL6), "RHEL6")
        self.assertEqual(versionToString(RHEL7), "RHEL7")
        self.assertEqual(versionToString(RHEL8), "RHEL8")

        # fail
        self.assertRaises(KickstartVersionError, versionToString, 47)

class returnClassForVersion_TestCase(CommandTest):
    def runTest(self):

        # Test that everything in version.versionMap has a handler, except
        # for DEVEL.
        for (name, vers) in list(versionMap.items()):
            if name == "DEVEL":
                continue

            self.assertEqual(returnClassForVersion(vers).version, vers)

        # test that unknown version will raise an exception
        import pykickstart.version as ver
        orig_versionToString = ver.versionToString
        with self.assertRaises(KickstartVersionError):
            def fake_versionToString(version, skipDevel=False):
                return "-1"

            ver.versionToString = fake_versionToString
            ver.returnClassForVersion(-1)
        ver.versionToString = orig_versionToString

        # Load the handlers
        _path = os.path.join(os.path.dirname(__file__), "..", "pykickstart", "handlers")
        _path = os.path.abspath(_path)
        for module in loadModules(_path, cls_pattern="Handler", skip_list=["control"]):
            if module.__name__.endswith("Handler") and module.__name__ not in ["BaseHandler"]:
                # What is the version of the handler?
                vers = module.__name__.replace("Handler", "")
                self.assertTrue(vers in versionMap)
                # Ensure that returnClassForVersion returns what we expect
                self.assertEqual(getClassName(returnClassForVersion(versionMap[vers])), getClassName(module))

class versionFromFile_TestCase(CommandTest):
    def runTest(self):

        def write_ks_cfg(buf):
            (fd, name) = tempfile.mkstemp(prefix="ks-", suffix=".cfg", dir="/tmp", text=True)
            if six.PY3:
                buf = buf.encode(sys.getdefaultencoding())
            os.write(fd, buf)
            os.close(fd)
            return name

        # no version specified
        ks_cfg = '''
# This is a sample kickstart file
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # proper format ... DEVEL
        ks_cfg = '''
# This is a sample kickstart file
#version=DEVEL
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # proper format ... RHEL3
        ks_cfg = '''
# This is a sample kickstart file
#version=RHEL3
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), RHEL3)
        os.unlink(ks_cfg)

        # improper format ... fallback to DEVEL
        ks_cfg = '''
# This is a sample kickstart file
# version: FC3
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # unknown version specified ... raise exception
        ks_cfg = '''
# This is a sample kickstart file
#version=RHEL5000
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertRaises(KickstartVersionError, versionFromFile, ks_cfg)
        os.unlink(ks_cfg)

class FailedImpImport_TestCase(CommandTest):
    def runTest(self):
        try:
            # will force another import
            del sys.modules['pykickstart.version']
            del sys.modules['importlib']

            import pykickstart.version as ver
            from pykickstart.handlers.f23 import F23Handler

            cls = ver.returnClassForVersion(ver.F23)

            # assert the names; b/c of how the importlib.import_module() works
            # asserting both classes being equal fails
            self.assertEqual(cls.__name__, F23Handler.__name__)
        finally:
            # force import to reload these modules
            del sys.modules['pykickstart.version']
            del sys.modules['importlib']

if __name__ == "__main__":
    unittest.main()
