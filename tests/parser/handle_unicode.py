# -*- coding: utf-8 -*-
import six
import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart import version

class HandleUnicode_TestCase(ParserTest):
    ks = """
rootpw ááááááááá

%post
echo áááááá
%end
"""
    def get_encoded_str(self, string, force_encode=False):
        if force_encode or not six.PY3:
            return string.encode("utf-8")
        else:
            return string


    def runTest(self):
        unicode_str1 = u"ááááááááá"
        unicode_str2 = u"áááááá"

        # parser should parse string including non-ascii characters
        self.parser.readKickstartFromString(self.ks)

        # str(handler) should not cause traceback and should contain the
        # original non-ascii strings as utf-8 encoded byte strings and
        # str(self.handler) should not fail -- i.e. self.handler.__str__()
        # should return byte string not unicode string
        self.assertIn(self.get_encoded_str(unicode_str1), str(self.handler))
        self.assertIn(self.get_encoded_str(unicode_str2), str(self.handler))

        # set root password to unicode string
        self.handler.rootpw.password = unicode_str1

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(self.get_encoded_str(unicode_str1), str(self.handler))

        # set root password to encoded string
        self.handler.rootpw.password = self.get_encoded_str(unicode_str1, force_encode=True)

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(str(self.get_encoded_str(unicode_str1, force_encode=True)), str(self.handler))

if __name__ == "__main__":
    if not six.PY3:
        unittest.main()
