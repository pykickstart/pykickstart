#!/usr/bin/python3

import os

from pocketlint import PocketLintConfig, PocketLinter

class PykickstartLintConfig(PocketLintConfig):
    @property
    def pylintPlugins(self):
        retval = super(PykickstartLintConfig, self).pylintPlugins
        retval.remove("pocketlint.checkers.eintr")
        return retval

if __name__ == "__main__":
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    os._exit(rc)
