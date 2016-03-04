# -*- coding: utf-8 -*-
import os
import six
import unittest
import tempfile
import locale

from tests.baseclass import ParserTest

class HandleUnicode_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
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

        # pylint: disable=environment-modify
        # Make sure the locale is reset so that the traceback could happen
        del os.environ["LANG"]
        locale.resetlocale()

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

        (fd, name) = tempfile.mkstemp(prefix="ks-", suffix=".cfg", dir="/tmp", text=True)
        if six.PY3:
            buf = self.ks.encode("utf-8")
        else:
            buf = self.ks
        os.write(fd, buf)
        os.close(fd)

        # This should not traceback with a UnicodeError
        try:
            self.parser.readKickstart(name)

            # str(handler) should not cause traceback and should contain the
            # original non-ascii strings as utf-8 encoded byte strings and
            # str(self.handler) should not fail -- i.e. self.handler.__str__()
            # should return byte string not unicode string
            self.assertIn(self.get_encoded_str(unicode_str1), str(self.handler))
            self.assertIn(self.get_encoded_str(unicode_str2), str(self.handler))
        finally:
            os.unlink(name)

if __name__ == "__main__":
    if not six.PY3:
        unittest.main()
