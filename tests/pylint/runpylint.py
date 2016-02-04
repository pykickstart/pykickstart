#!/usr/bin/python3

import sys

from pocketlint import PocketLintConfig, PocketLinter

class PykickstartLintConfig(PocketLintConfig):
    @property
    def ignoreNames(self):
        return {"translation-canary"}

if __name__ == "__main__":
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    sys.exit(rc)
