import unittest
from tests.baseclass import CommandTest
from pykickstart.constants import SELINUX_DISABLED, SELINUX_ENFORCING, SELINUX_PERMISSIVE

class FC3_TestCase(CommandTest):
    command = "selinux"

    def runTest(self):
        # pass
        self.assert_parse("selinux")
        self.assert_parse("selinux --permissive", "selinux --permissive\n")
        self.assert_parse("selinux --enforcing", "selinux --enforcing\n")
        self.assert_parse("selinux --disabled", "selinux --disabled\n")

        # fail
        self.assert_parse_error("selinux --cheese")
        self.assert_parse_error("selinux --crackers=CRUNCHY")

        # extra test coverage
        cmd = self.handler().commands[self.command]
        for mode in [-1, 99999]:
            cmd.selinux = mode
            self.assertEqual(cmd.__str__(), "# SELinux configuration\n")

        cmd.selinux = SELINUX_DISABLED
        self.assertEqual(cmd.__str__(), "# SELinux configuration\nselinux --disabled\n")

        cmd.selinux = SELINUX_ENFORCING
        self.assertEqual(cmd.__str__(), "# SELinux configuration\nselinux --enforcing\n")

        cmd.selinux = SELINUX_PERMISSIVE
        self.assertEqual(cmd.__str__(), "# SELinux configuration\nselinux --permissive\n")

if __name__ == "__main__":
    unittest.main()
