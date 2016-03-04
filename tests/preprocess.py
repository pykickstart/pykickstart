import os
import six
import tempfile
from tests.baseclass import ParserTest

from pykickstart.errors import KickstartError, KickstartParseError
from pykickstart.parser import preprocessKickstart, preprocessFromString, preprocessKickstartToString, preprocessFromStringToString

###
### TESTING preprocessKickstart
###

class PK_No_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

    def setUp(self):
        ParserTest.setUp(self)
        self._processedPath = None

        (handle, self._path) = tempfile.mkstemp(prefix="ks-", text=True)
        s = self.ks
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._path)
        if self._processedPath:
            os.unlink(self._processedPath)

    def runTest(self):
        self._processedPath = preprocessKickstart(self._path)
        with open(self._processedPath) as f:
            self.assertEqual(f.read(), self.ks)

class PK_Ksappend_Missing(PK_No_Ksappend):
    def __init__(self, *args, **kwargs):
        PK_No_Ksappend.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
%ksappend /tmp/MISSING_FILE
"""

    def runTest(self):
        self.assertRaises(KickstartError, preprocessKickstart, self._path)

class PK_With_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

        self.ksappend = """
timezone America/New_York
"""

    def setUp(self):
        ParserTest.setUp(self)
        self._processedPath = None

        (handle, self._ksappendPath) = tempfile.mkstemp(prefix="ksappend-", text=True)
        s = self.ksappend
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

        # Write the ksappend file first so we know its filename for making the
        # %ksappend line.
        (handle, self._path) = tempfile.mkstemp(prefix="ks-", text=True)
        s = self.ks + "%ksappend " + self._ksappendPath
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._path)
        os.unlink(self._ksappendPath)
        if self._processedPath:
            os.unlink(self._processedPath)

    def runTest(self):
        self._processedPath = preprocessKickstart(self._path)
        with open(self._processedPath) as f:
            self.assertEqual(f.read(), self.ks + self.ksappend)

###
### TESTING preprocessFromString
###

class PFS_No_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

    def setUp(self):
        ParserTest.setUp(self)
        self._path = None

    def runTest(self):
        self._path = preprocessFromString(self.ks)
        with open(self._path) as f:
            self.assertEqual(f.read(), self.ks)

    def tearDown(self):
        ParserTest.tearDown(self)
        if self._path:
            os.unlink(self._path)

class PFS_Ksappend_Missing(PFS_No_Ksappend):
    def __init__(self, *args, **kwargs):
        PFS_No_Ksappend.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
%ksappend /tmp/MISSING_FILE
"""

    def runTest(self):
        self.assertRaises(KickstartError, preprocessFromString, self.ks)

class PFS_Ksappend_Invalid(PFS_No_Ksappend):
    def __init__(self, *args, **kwargs):
        PFS_No_Ksappend.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
%ksappend
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, preprocessFromString, self.ks)

class PFS_With_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

        self.ksappend = """
timezone America/New_York
"""

    def setUp(self):
        ParserTest.setUp(self)
        self._path = None

        (handle, self._ksappendPath) = tempfile.mkstemp(prefix="ksappend-", text=True)
        s = self.ksappend
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._ksappendPath)
        if self._path:
            os.unlink(self._path)

    def runTest(self):
        self._path = preprocessFromString(self.ks + "%ksappend " + self._ksappendPath)
        with open(self._path) as f:
            self.assertEqual(f.read(), self.ks + self.ksappend)

###
### TESTING preprocessKickstartToString
###

class PKTS_No_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

    def setUp(self):
        ParserTest.setUp(self)

        (handle, self._path) = tempfile.mkstemp(prefix="ks-", text=True)
        s = self.ks
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._path)

    def runTest(self):
        processed = preprocessKickstartToString(self._path)
        self.assertEqual(processed.decode(), self.ks)

class PKTS_Ksappend_Missing(PKTS_No_Ksappend):
    def __init__(self, *args, **kwargs):
        PKTS_No_Ksappend.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
%ksappend /tmp/MISSING_FILE
"""

    def runTest(self):
        self.assertRaises(KickstartError, preprocessKickstartToString, self._path)

class PKTS_Kickstart_Missing(ParserTest):
    def runTest(self):
        self.assertRaises(KickstartError, preprocessKickstartToString, "/tmp/MISSING_FILE")

class PKTS_With_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

        self.ksappend = """
timezone America/New_York
"""

    def setUp(self):
        ParserTest.setUp(self)

        (handle, self._ksappendPath) = tempfile.mkstemp(prefix="ksappend-", text=True)
        s = self.ksappend
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

        # Write the ksappend file first so we know its filename for making the
        # %ksappend line.
        (handle, self._path) = tempfile.mkstemp(prefix="ks-", text=True)
        s = self.ks + "%ksappend " + self._ksappendPath
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._path)
        os.unlink(self._ksappendPath)

    def runTest(self):
        processed = preprocessKickstartToString(self._path)
        self.assertEqual(processed.decode(), self.ks + self.ksappend)

###
### TESTING preprocessFromStringToString
###

class PFSTS_No_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

    def runTest(self):
        processed = preprocessFromStringToString(self.ks)
        self.assertEqual(processed.decode(), self.ks)

class PFSTS_Ksappend_Missing(PFSTS_No_Ksappend):
    def __init__(self, *args, **kwargs):
        PFSTS_No_Ksappend.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
%ksappend /tmp/MISSING_FILE
"""

    def runTest(self):
        self.assertRaises(KickstartError, preprocessFromStringToString, self.ks)

class PFSTS_With_Ksappend(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
lang en_US
keyboard us
autopart
"""

        self.ksappend = """
timezone America/New_York
"""

    def setUp(self):
        ParserTest.setUp(self)

        (handle, self._ksappendPath) = tempfile.mkstemp(prefix="ksappend-", text=True)
        s = self.ksappend
        if six.PY3:
            s = s.encode('utf-8')

        os.write(handle, s)
        os.close(handle)

    def tearDown(self):
        ParserTest.tearDown(self)
        os.unlink(self._ksappendPath)

    def runTest(self):
        processed = preprocessFromStringToString(self.ks + "%ksappend " + self._ksappendPath)
        self.assertEqual(processed.decode(), self.ks + self.ksappend)
