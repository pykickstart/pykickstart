import unittest
from tests.baseclass import CommandTest, CommandSequenceTest
from pykickstart.commands.realm import F19_Realm
from pykickstart.version import F19

class Realm_TestCase(unittest.TestCase):
    def runTest(self):
        cmd = F19_Realm()
        # additional code coverage
        self.assertEqual(cmd.__str__(), "")

class F19_TestCase(CommandTest):
    command = "realm"

    def runTest(self):

        # No realm command arguments
        self.assert_parse_error("realm")

        # Unsupported realmcommand
        self.assert_parse_error("realm unknown --args")

        # pass for join
        realm = self.assert_parse("realm join blah")
        self.assertEqual(realm.join_realm, "blah")
        self.assertEqual(realm.join_args, ["blah"])
        self.assertEqual(realm.discover_options, [])
        self.assertEqual(str(realm), "# Realm or domain membership\nrealm join blah\n")

        # pass for join with client-software
        realm = self.assert_parse("realm join --client-software=sssd --computer-ou=OU=blah domain.example.com")
        self.assertEqual(realm.join_realm, "domain.example.com")
        self.assertEqual(realm.join_args, ["--client-software=sssd", "--computer-ou=OU=blah", "domain.example.com"])
        self.assertEqual(realm.discover_options, ["--client-software=sssd"])
        self.assertEqual(str(realm), "# Realm or domain membership\nrealm join --client-software=sssd --computer-ou=OU=blah domain.example.com\n")

        # pass for join with one-time password
        realm = self.assert_parse("realm join --one-time-password=12345 domain.example.com")

        # pass for join with no password
        realm = self.assert_parse("realm join --no-password domain.example.com")

        # Bad arguments, the --no-password does not support an argument
        self.assert_parse_error("realm join --no-password=blah one.example.com")

        # Bad arguments, only one domain for join
        self.assert_parse_error("realm join one two")

        # Bad arguments, unsupported argument
        self.assert_parse_error("realm join --user=blah one.example.com")

        # Domain must be the last argument
        self.assert_parse_error("realm join test_domain --no-password")

class F19_MultipleJoin_TestCase(CommandSequenceTest):
    def __init__(self, *args, **kwargs):
        CommandSequenceTest.__init__(self, *args, **kwargs)
        self.version = F19

    def runTest(self):
        # fail - can't use join more than once
        self.assert_parse_error("""
realm join blah1
realm join blah2""")

if __name__ == "__main__":
    unittest.main()
