#!/usr/bin/env python3

import sys

from pocketlint import FalsePositive, PocketLintConfig, PocketLinter

class PykickstartLintConfig(PocketLintConfig):
    def __init__(self):
        PocketLintConfig.__init__(self)

        self.falsePositives = [
            FalsePositive(r"^W1113.*: Keyword argument before variable positional arguments list in the definition of __init__ function$"),
            FalsePositive("W0707.*raise-missing-from"),
        ]

    @property
    def ignoreNames(self):
        return {"translation-canary", ".tox"}

if __name__ == "__main__":
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    if rc in [0, 4]:
        sys.exit(0)
    else:
        sys.exit(rc)
