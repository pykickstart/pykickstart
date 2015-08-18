import unittest
from tests.baseclass import CommandTest, CommandSequenceTest

from pykickstart.errors import KickstartValueError

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

        # pass for join with one-time password
        realm = self.assert_parse("realm join --one-time-password=12345 domain.example.com")

        # pass for join with no password
        realm = self.assert_parse("realm join --no-password domain.example.com")

        # Bad arguments, the --no-password does not support an argument
        self.assert_parse_error("realm join --no-password=blah one.example.com", KickstartValueError)

        # Bad arguments, only one domain for join
        self.assert_parse_error("realm join one two", KickstartValueError)

        # Bad arguments, unsupported argument
        self.assert_parse_error("realm join --user=blah one.example.com", KickstartValueError)

class F19_MultipleJoin_TestCase(CommandSequenceTest):
    def runTest(self):
        # fail - can't use join more than once
        self.assert_parse_error("""
realm join blah1
realm join blah2""")

if __name__ == "__main__":
    unittest.main()
