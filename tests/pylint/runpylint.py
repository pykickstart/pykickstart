#!/usr/bin/env python3

import sys

import astroid
from pocketlint import FalsePositive, PocketLintConfig, PocketLinter
import pylint

class PykickstartLintConfig(PocketLintConfig):
    def __init__(self):
        PocketLintConfig.__init__(self)

        self.falsePositives = [
            FalsePositive(r"^W1113.*: Keyword argument before variable positional arguments list in the definition of __init__ function$"),
            FalsePositive(r"W0707.*raise-missing-from"),
            FalsePositive(r"W1406.*redundant-u-string-prefix"),
            FalsePositive(r"W1514.*unspecified-encoding"),
        ]

    @property
    def ignoreNames(self):
        return {"translation-canary", ".tox"}

if __name__ == "__main__":
    print("INFO: Using pylint v%s, astroid v%s" % (pylint.version, astroid.version))
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    if rc in [0, 4]:
        sys.exit(0)
    else:
        sys.exit(rc)
