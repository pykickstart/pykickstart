from tools import ksverdiff
import unittest.mock as mock
from unittest.mock import call
from unittest import TestCase
from pykickstart.version import versionMap


class ListVersions_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main(['-l'])
        self.assertEqual(retval, 0)

        _print_calls = []
        for key in sorted(versionMap.keys()):
            _print_calls.append(call(key))
        _print.assert_has_calls(_print_calls)

class MissingFromToOptions_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main([])
        self.assertEqual(retval, 1)
        _print.assert_called_with('You must specify two syntax versions.')

class InvalidKSVersion_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main(['-f', 'F23', '-t', 'INVALID'])
        self.assertEqual(retval, 1)
        _print.assert_called_with('The version Unsupported version specified: INVALID is not supported by pykickstart')

class From23To25_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main(['-f', 'F23', '-t', 'F25'])
        self.assertEqual(retval, 0)
        _calls = []
        _calls.append(call('The following commands were removed in F25:'))
        _calls.append(call(''))
        _calls.append(call('The following commands were deprecated in F25:'))
        _calls.append(call('device dmraid multipath upgrade'))
        _calls.append(call())
        _calls.append(call('The following commands were added in F25:'))
        _calls.append(call(''))
        _calls.append(call('The following options were added to the network command in F25:'))
        _calls.append(call('--no-activate'))
        _calls.append(call())
        _calls.append(call('The following options were added to the raid command in F25:'))
        _calls.append(call('--chunksize'))
        _calls.append(call())
        _calls.append(call('The following options were added to the sshpw command in F25:'))
        _calls.append(call('--sshkey'))

        _print.assert_has_calls(_calls)

class From10To11_Deprecated_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main(['-f', 'F10', '-t', 'F11'])
        self.assertEqual(retval, 0)
        _calls = []
        # validate only deprecation calls
        _calls.append(call('The following options were deprecated from the xconfig command in F11:'))
        _calls.append(call('--depth --driver --resolution --videoram'))
        _print.assert_has_calls(_calls)

class From10To14_Removed_TestCase(TestCase):
    @mock.patch('tools.ksverdiff.print')
    def runTest(self, _print):
        retval = ksverdiff.main(['-f', 'F10', '-t', 'F14'])
        self.assertEqual(retval, 0)
        _calls = []
        # validate only removed calls
        _calls.append(call('The following options were removed from the xconfig command in F14:'))
        _calls.append(call('--depth --driver --resolution --videoram'))
        _print.assert_has_calls(_calls)
