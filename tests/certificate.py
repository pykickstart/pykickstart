import unittest
from tests.baseclass import ParserTest

from pykickstart.errors import KickstartParseError
from pykickstart import version         # pylint: disable=unused-import

CERT_CONTENT="""-----BEGIN CERTIFICATE-----
MIIBjTCCATOgAwIBAgIUWR5HO3v/0I80Ne0jQWVZFODuWLEwCgYIKoZIzj0EAwIw
FDESMBAGA1UEAwwJUlZURVNUIENBMB4XDTI0MTEyMDEzNTk1N1oXDTM0MTExODEz
NTk1N1owFDESMBAGA1UEAwwJUlZURVNUIENBMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAELghFKGEgS8+5/2nx50W0xOqTrKc2Jz/rD/jfL0m4z4fkeAslCOkIKv74
0wfBXMngxi+OF/b3Vh8FmokuNBQO5qNjMGEwHQYDVR0OBBYEFOJarl9Xkd13sLzI
mHqv6aESlvuCMB8GA1UdIwQYMBaAFOJarl9Xkd13sLzImHqv6aESlvuCMA8GA1Ud
EwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMAoGCCqGSM49BAMCA0gAMEUCIAet
7nyre42ReoRKoyHWLDsQmQDzoyU3FQdC0cViqOtrAiEAxYIL+XTTp7Xy9RNE4Xg7
yNWXfdraC/AfMM8fqsxlVJM=
-----END CERTIFICATE-----"""

CERT_CONTENT_2="""-----BEGIN CERTIFICATE-----
MIIBkTCCATegAwIBAgIUN6r4TjFJqP/TS6U25iOGL2Wt/6kwCgYIKoZIzj0EAwIw
FjEUMBIGA1UEAwwLUlZURVNUIDIgQ0EwHhcNMjQxMTIwMTQwMzIxWhcNMzQxMTE4
MTQwMzIxWjAWMRQwEgYDVQQDDAtSVlRFU1QgMiBDQTBZMBMGByqGSM49AgEGCCqG
SM49AwEHA0IABOtXBMEhtcH43dIDHkelODXrSWQQ8PW7oo8lQUEYTNAL1rpWJJDD
1u+bpLe62Z0kzYK0CpeKuXFfwGrzx7eA6vajYzBhMB0GA1UdDgQWBBStV+z7SZSi
YXlamkx+xjm/W1sMSTAfBgNVHSMEGDAWgBStV+z7SZSiYXlamkx+xjm/W1sMSTAP
BgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjAKBggqhkjOPQQDAgNIADBF
AiEAkQjETC3Yx2xOkA+R0/YR+R+QqpR8p1fd/cGKWFUYxSoCIEuDJcfvPJfFYdzn
CFOCLuymezWz+1rdIXLU1+XStLuB
-----END CERTIFICATE-----"""

CERT_CONTENT_WITH_EMPTY_LINE="""-----BEGIN CERTIFICATE-----
MIIBjTCCATOgAwIBAgIUWR5HO3v/0I80Ne0jQWVZFODuWLEwCgYIKoZIzj0EAwIw
FDESMBAGA1UEAwwJUlZURVNUIENBMB4XDTI0MTEyMDEzNTk1N1oXDTM0MTExODEz
NTk1N1owFDESMBAGA1UEAwwJUlZURVNUIENBMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAELghFKGEgS8+5/2nx50W0xOqTrKc2Jz/rD/jfL0m4z4fkeAslCOkIKv74
0wfBXMngxi+OF/b3Vh8FmokuNBQO5qNjMGEwHQYDVR0OBBYEFOJarl9Xkd13sLzI
mHqv6aESlvuCMB8GA1UdIwQYMBaAFOJarl9Xkd13sLzImHqv6aESlvuCMA8GA1Ud
EwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMAoGCCqGSM49BAMCA0gAMEUCIAet
7nyre42ReoRKoyHWLDsQmQDzoyU3FQdC0cViqOtrAiEAxYIL+XTTp7Xy9RNE4Xg7
yNWXfdraC/AfMM8fqsxlVJM=
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIBkTCCATegAwIBAgIUN6r4TjFJqP/TS6U25iOGL2Wt/6kwCgYIKoZIzj0EAwIw
FjEUMBIGA1UEAwwLUlZURVNUIDIgQ0EwHhcNMjQxMTIwMTQwMzIxWhcNMzQxMTE4
MTQwMzIxWjAWMRQwEgYDVQQDDAtSVlRFU1QgMiBDQTBZMBMGByqGSM49AgEGCCqG
SM49AwEHA0IABOtXBMEhtcH43dIDHkelODXrSWQQ8PW7oo8lQUEYTNAL1rpWJJDD
1u+bpLe62Z0kzYK0CpeKuXFfwGrzx7eA6vajYzBhMB0GA1UdDgQWBBStV+z7SZSi
YXlamkx+xjm/W1sMSTAfBgNVHSMEGDAWgBStV+z7SZSiYXlamkx+xjm/W1sMSTAP
BgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjAKBggqhkjOPQQDAgNIADBF
AiEAkQjETC3Yx2xOkA+R0/YR+R+QqpR8p1fd/cGKWFUYxSoCIEuDJcfvPJfFYdzn
CFOCLuymezWz+1rdIXLU1+XStLuB
-----END CERTIFICATE-----"""

CERT_CONTENT_WITH_TRAILING_NEWLINE="""-----BEGIN CERTIFICATE-----
MIIBjTCCATOgAwIBAgIUWR5HO3v/0I80Ne0jQWVZFODuWLEwCgYIKoZIzj0EAwIw
FDESMBAGA1UEAwwJUlZURVNUIENBMB4XDTI0MTEyMDEzNTk1N1oXDTM0MTExODEz
NTk1N1owFDESMBAGA1UEAwwJUlZURVNUIENBMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAELghFKGEgS8+5/2nx50W0xOqTrKc2Jz/rD/jfL0m4z4fkeAslCOkIKv74
0wfBXMngxi+OF/b3Vh8FmokuNBQO5qNjMGEwHQYDVR0OBBYEFOJarl9Xkd13sLzI
mHqv6aESlvuCMB8GA1UdIwQYMBaAFOJarl9Xkd13sLzImHqv6aESlvuCMA8GA1Ud
EwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMAoGCCqGSM49BAMCA0gAMEUCIAet
7nyre42ReoRKoyHWLDsQmQDzoyU3FQdC0cViqOtrAiEAxYIL+XTTp7Xy9RNE4Xg7
yNWXfdraC/AfMM8fqsxlVJM=
-----END CERTIFICATE-----
"""

class Simple_Header_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --filename=custom_certificate.pem --dir /etc/pki/ca-trust/source/anchors/
{CERT_CONTENT}
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.certificates), 1)

        # Verify the certificate defaults.
        cert = self.handler.certificates[0]
        self.assertEqual(cert.filename, "custom_certificate.pem")
        self.assertEqual(cert.dir, "/etc/pki/ca-trust/source/anchors/")
        self.assertEqual(cert.cert, CERT_CONTENT)

class Missing_Dir_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --filename=custom_certificate.pem
{CERT_CONTENT}
%end
"""

    def runTest(self):
        with self.assertRaises(KickstartParseError) as cm:
            self.parser.readKickstartFromString(self.ks)

        expected = "the following arguments are required: --dir"
        self.assertIn(expected, str(cm.exception))

class Missing_Filename_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate
{CERT_CONTENT}
%end
"""

    def runTest(self):
        with self.assertRaises(KickstartParseError) as cm:
            self.parser.readKickstartFromString(self.ks)

        expected = "the following arguments are required: --filename"
        self.assertIn(expected, str(cm.exception))

class Multiple_Terminated_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --filename=custom_certificate_1.pem --dir /etc/pki/edns
{CERT_CONTENT}
%end

%certificate --filename=custom_certificate_2.pem --dir /etc/pki/edns
{CERT_CONTENT_2}
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.certificates), 2)

        # Verify the first certificate.
        cert = self.handler.certificates[0]
        self.assertEqual(cert.filename, "custom_certificate_1.pem")
        self.assertEqual(cert.cert, CERT_CONTENT)

        # Verify the second certificate.
        cert = self.handler.certificates[1]
        self.assertEqual(cert.filename, "custom_certificate_2.pem")
        self.assertEqual(cert.cert, CERT_CONTENT_2)

class Multiple_Unterminated_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --filename=custom_certificate_1.pem --dir /etc/pki/edns
{CERT_CONTENT}

%certificate --filename=custom_certificate_2.pem --dir /etc/pki/edns
{CERT_CONTENT_2}
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Missing_Certificate_Body_Fails_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%certificate --filename=custom_certificate.pem --dir /etc/pki/ca-trust/source/anchors/
%end
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Cert_Content_Empty_Line_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --filename=custom_certificate_1.pem --dir /etc/pki/edns
{CERT_CONTENT_WITH_EMPTY_LINE}
%end

%certificate --filename=custom_certificate_2.pem --dir /etc/pki/edns
{CERT_CONTENT_WITH_TRAILING_NEWLINE}
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.certificates), 2)

        # Verify the first certificate.
        cert = self.handler.certificates[0]
        self.assertEqual(cert.filename, "custom_certificate_1.pem")
        self.assertEqual(cert.cert, CERT_CONTENT_WITH_EMPTY_LINE)

        # Verify the second certificate.
        cert = self.handler.certificates[1]
        self.assertEqual(cert.filename, "custom_certificate_2.pem")
        self.assertEqual(cert.cert, CERT_CONTENT_WITH_TRAILING_NEWLINE)


if __name__ == "__main__":
    unittest.main()
