import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.realm import *

class F19_TestCase(CommandTest):
    command = "realm"

    def runTest(self):

        # No realm command arguments
        self.assert_parse_error("realm", KickstartValueError)

        # Unsupported realmcommand
        self.assert_parse_error("realm unknown --args", KickstartValueError)

        # pass for join
        realm = self.assert_parse("realm join blah")
        self.assertEquals(realm.join_realm, "blah")
        self.assertEquals(realm.join_args, ["blah"])
        self.assertEquals(realm.discover_options, [])
        self.assertEquals(str(realm), "# Realm or domain membership\nrealm join blah\n")

        # pass for join with client-software
        realm = self.assert_parse("realm join --client-software=sssd --computer-ou=OU=blah domain.example.com")
        self.assertEquals(realm.join_realm, "domain.example.com")
        self.assertEquals(realm.join_args, ["--client-software=sssd", "--computer-ou=OU=blah", "domain.example.com"])
        self.assertEquals(realm.discover_options, ["--client-software=sssd"])
        self.assertEquals(str(realm), "# Realm or domain membership\nrealm join --client-software=sssd --computer-ou=OU=blah domain.example.com\n")

        # Bad arguments, only one domain for join
        self.assert_parse_error("realm join one two", KickstartValueError)

        # Bad arguments, unsupported argument
        self.assert_parse_error("realm join --user=blah one.example.com", KickstartValueError)

        # Bad arguments, unsupported argument
        self.assert_parse_error("realm join --user=blah one.example.com", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
