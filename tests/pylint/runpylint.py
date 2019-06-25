#!/usr/bin/env python3

import sys
import yaml

from pocketlint import FalsePositive, PocketLintConfig, PocketLinter

class PykickstartLintConfig(PocketLintConfig):
    def __init__(self):
        PocketLintConfig.__init__(self)

        self.falsePositives = [
            FalsePositive(r"^W1113.*: Keyword argument before variable positional arguments list in the definition of __init__ function$"),
        ]

    @property
    def ignoreNames(self):
        ignores = {"translation-canary"}

        if os.path.isfile(".travis.yml"):
            with open(".travis.yml", "r") as input:
                data = yaml.safe_load(input)

            if data.has_key("before_install"):
                for line in data["before_install"]:
                    if line.startswith("virtualenv "):
                        ignores.add(line.split()[-1]
                        break

        return ignores

if __name__ == "__main__":
    conf = PykickstartLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    if rc in [0, 4]:
        sys.exit(0)
    else:
        sys.exit(rc)
