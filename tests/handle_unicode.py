# -*- coding: utf-8 -*-
import os
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
        self.assertIn(unicode_str1, str(self.handler))
        self.assertIn(unicode_str2, str(self.handler))

        # set root password to unicode string
        self.handler.rootpw.password = unicode_str1

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(unicode_str1, str(self.handler))

        # set root password to encoded string
        self.handler.rootpw.password = unicode_str1

        # str(handler) should not cause traceback and should contain the
        # original unicode string as utf-8 encoded byte string
        self.assertIn(str(unicode_str1), str(self.handler))

        (fd, name) = tempfile.mkstemp(prefix="ks-", suffix=".cfg", dir="/tmp", text=True)
        buf = self.ks.encode("utf-8")
        os.write(fd, buf)
        os.close(fd)

        # This should not traceback with a UnicodeError
        try:
            self.parser.readKickstart(name)

            # str(handler) should not cause traceback and should contain the
            # original non-ascii strings as utf-8 encoded byte strings and
            # str(self.handler) should not fail -- i.e. self.handler.__str__()
            # should return byte string not unicode string
            self.assertIn(unicode_str1, str(self.handler))
            self.assertIn(unicode_str2, str(self.handler))
        finally:
            os.unlink(name)
