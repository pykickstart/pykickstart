from pykickstart.errors import KickstartParseWarning
from tests.baseclass import CommandSequenceTest


class AutopartUsage_TestCase(CommandSequenceTest):
    """Test autopart command usage

    Autopart can't be used together with any of the part/partition, raid,
    logvol and volgroup command in the same kickstart file.
    This test case is used to check if parsing of such kickstarts correctly
    raises a parsing error.
    """

    def runTest(self):
        # first just parse some correct sequences to
        # check if the parsing itself works correctly
        correct_command_sequences = [
            "part / --size=2048",
            "partition / --size=2048",
            "autopart",
            "raid / --level=1 --device=md0 raid.01",
            "logvol / --vgname=foo --size=2000 --name=bar",
            "volgroup foo pv.01"
        ]
        for sequence in correct_command_sequences:
            self.assert_parse(sequence)

        # then check various incorrect sequences
        incorrect_command_sequences = [
            "part / --size=2048\nautopart",
            "autopart\npart / --size=2048",
            "partition / --size=2048\nautopart",
            "autopart\npartition / --size=2048",
            "raid / --level=1 --device=md0 raid.01\nautopart",
            "autopart\nraid / --level=1 --device=md0 raid.01",
            "logvol / --vgname=foo --size=2000 --name=bar\nautopart",
            "autopart\nlogvol / --vgname=foo --size=2000 --name=bar",
            "volgroup foo pv.01\nautopart",
            "autopart\nvolgroup foo pv.01"
        ]

        for sequence in incorrect_command_sequences:
            self.assert_parse_error(sequence)

        # also test all the commands being used at once

        long_incorrect_sequence = """
part / --size=2048
partition /opt --size=2048
autopart
raid / --level=1 --device=md0 raid.01
logvol / --vgname=foo --size=2000 --name=bar
volgroup foo pv.01
"""
        self.assert_parse_error(long_incorrect_sequence)


class TmpfsUsage_TestCase(CommandSequenceTest):
    """Test tmpfs usage with the partition command"""

    def runTest(self):
        # the tmpfs filesystem supports the size and fsopt options
        self.assert_parse('part /foo --size=100 --fstype=tmpfs --fsoptions="noexec"')
        self.assert_parse('part /ham --fstype=tmpfs --fsoptions="size=250%"')
        self.assert_parse('part /tmp --size=20000 --fstype=tmpfs')

        # the tmpfs filesystem dos not support the --grow and --maxsize
        # options
        self.assert_parse_error("part --fstype=tmpfs /tmp --grow")
        self.assert_parse_error("part --fstype=tmpfs /tmp --grow --maxsize=1000")
        self.assert_parse_error("part --fstype=tmpfs /tmp --maxsize=1000")

class PartitionDupes_TestCase(CommandSequenceTest):
    def runTest(self):
        # Two swap partitions is alright.
        self.assert_parse("""
part swap --size=1024 --fstype=swap
part swap --size=2048 --fstype=swap""")

        # Two root partitions is not.
        self.assert_parse_error("""
part / --size=1024 --fstype=ext4
part / --size=2048 --fstype=ext4""", exception=KickstartParseWarning)
