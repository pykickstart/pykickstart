#!/usr/bin/python3

import sys

from pocketlint import FalsePositive, PocketLintConfig, PocketLinter

class PykickstartLintConfig(PocketLintConfig):
    def __init__(self):
        PocketLintConfig.__init__(self)

        self.falsePositives = [
            FalsePositive(r"^E1102.*: .*_TestCase.runTest: self.handler is not callable$"),
        ]

    @property
    def ignoreNames(self):
        return {"translation-canary"}

if __name__ == "__main__":
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    sys.exit(rc)
