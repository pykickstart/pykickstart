# -*- coding: utf-8 -*-
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

    def runTest(self):
        unicode_str1 = u"ááááááááá"
        unicode_str2 = u"áááááá"
        encoded_str1 = unicode_str1.encode("utf-8")
        encoded_str2 = unicode_str2.encode("utf-8")

        # parser should parse string including non-ascii characters
        self.parser.readKickstartFromString(self.ks)

        # str(handler) should not cause traceback and should contain the
        # original non-ascii strings as utf-8 encoded byte strings and
        # str(self.handler) should not fail -- i.e. self.handler.__str__()
        # should return byte string not unicode string
        self.assertIn(encoded_str1, str(self.handler))
        self.assertIn(encoded_str2, str(self.handler))

        # set root password to unicode string
        self.handler.rootpw.password = unicode_str1

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(encoded_str1, str(self.handler))

        # set root password to encoded string
        self.handler.rootpw.password = encoded_str1

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(encoded_str1, str(self.handler))

if __name__ == "__main__":
    unittest.main()
