import unittest
from tests.baseclass import CommandTest


class F26_TestCase(CommandTest):
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
        self.assert_parse_error("snapshot")
        self.assert_parse_error("snapshot vg00/lv")
        self.assert_parse_error("snapshot --name=test")
        self.assert_parse_error("snapshot vg00/lv --name=test")
        self.assert_parse_error("snapshot vg00/lv --when=post-install")
        self.assert_parse_error("snapshot --name")
        self.assert_parse_error("snapshot --when")
        self.assert_parse_error("snapshot --name=test --when")

        # bad lv name
        self.assert_parse_error("snapshot lv --name test --when post-install")
        self.assert_parse_error("snapshot vg_lv --name test --when post-install")
        self.assert_parse_error("snapshot vg//lv --name test --when post-install")
        self.assert_parse_error("snapshot vg\\lv --name test --when post-install")
        self.assert_parse_error("snapshot vg=lv --name test --when post-install")

        # bad when option
        self.assert_parse_error("snapshot lv --name test --when error")
        self.assert_parse_error("snapshot lv --name test --when=error")
        self.assert_parse_error("snapshot lv --name test --when post-install --when pre-install")
        self.assert_parse_error("snapshot lv --name test --when=post-install --when pre-install")
        self.assert_parse_error("snapshot lv --name test --when=post-install --when=pre-install")

        # nonsensical parameter test
        self.assert_parse_error("snapshot --nonsense")
        self.assert_parse_error("snapshot nonsense")


if __name__ == "__main__":
    unittest.main()
