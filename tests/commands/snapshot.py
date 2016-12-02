import unittest
from tests.baseclass import CommandTest
from pykickstart.errors import KickstartValueError


class RHEL7_TestCase(CommandTest):
    command = "snapshot"

    def runTest(self):
        # pass
        self.assert_parse("snapshot vg00/lv --name test --when post-install",
                          "snapshot vg00/lv --name=test --when=post-install\n")
        self.assert_parse("snapshot vg00/lv --name=test --when=post-install",
                          "snapshot vg00/lv --name=test --when=post-install\n")
        self.assert_parse("snapshot vg00/lv --name=test --when pre-install",
                          "snapshot vg00/lv --name=test --when=pre-install\n")
        self.assert_parse("snapshot vg00/lv --name=test --when=pre-install",
                          "snapshot vg00/lv --name=test --when=pre-install\n")

        # missing required field
        self.assert_parse_error("snapshot", exception=KickstartValueError)
        self.assert_parse_error("snapshot vg00/lv", exception=KickstartValueError)
        self.assert_parse_error("snapshot --name=test", exception=KickstartValueError)
        self.assert_parse_error("snapshot vg00/lv --name=test", exception=KickstartValueError)
        self.assert_parse_error("snapshot vg00/lv --when=post-install", exception=KickstartValueError)
        self.assert_parse_error("snapshot --name")
        self.assert_parse_error("snapshot --when")
        self.assert_parse_error("snapshot --name=test --when")

        # bad lv name
        self.assert_parse_error("snapshot lv --name test --when post-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot vg_lv --name test --when post-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot vg//lv --name test --when post-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot vg\lv --name test --when post-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot vg=lv --name test --when post-install",
                                exception=KickstartValueError)

        # bad when option
        self.assert_parse_error("snapshot lv --name test --when error",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot lv --name test --when=error",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot lv --name test --when post-install --when pre-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot lv --name test --when=post-install --when pre-install",
                                exception=KickstartValueError)
        self.assert_parse_error("snapshot lv --name test --when=post-install --when=pre-install",
                                exception=KickstartValueError)

        # nonsensical parameter test
        self.assert_parse_error("snapshot --nonsense")
        self.assert_parse_error("snapshot nonsense", exception=KickstartValueError)


if __name__ == "__main__":
    unittest.main()
