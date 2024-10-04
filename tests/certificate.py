import unittest
from tests.baseclass import ParserTest

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart import version         # pylint: disable=unused-import

CERT_CONTENT="""-----BEGIN CERTIFICATE-----
MIIDRzCCAi+gAwIBAgIJAJKb9X1rNl2YMA0GCSqGSIb3DQEBCwUAMIGFMQswCQYD
VQQGEwJVUzETMBEGA1UECAwKU29tZS1TdGF0ZTEUMBIGA1UEBwwLU29tZS1TdGF0
...
-----END CERTIFICATE-----"""

CERT_CONTENT_2="""-----BEGIN CERTIFICATE-----
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
...
-----END CERTIFICATE-----"""

class Simple_Header_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --name=custom_certificate.pem --path /etc/pki/ca-trust/source/anchors/
{CERT_CONTENT}
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.certificates), 1)

        # Verify the certificate defaults.
        cert = self.handler.certificates[0]
        self.assertEqual(cert.name, "custom_certificate.pem")
        self.assertEqual(cert.path, "/etc/pki/ca-trust/source/anchors/")
        self.assertEqual(cert.cert, CERT_CONTENT)

class Multiple_Terminated_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --name=custom_certificate_1.pem
{CERT_CONTENT}
%end

%certificate --name=custom_certificate_2.pem
{CERT_CONTENT_2}
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.certificates), 2)

        # Verify the first certificate.
        cert = self.handler.certificates[0]
        self.assertEqual(cert.name, "custom_certificate_1.pem")
        self.assertEqual(cert.cert, CERT_CONTENT)

        # Verify the second certificate.
        cert = self.handler.certificates[1]
        self.assertEqual(cert.name, "custom_certificate_2.pem")
        self.assertEqual(cert.cert, CERT_CONTENT_2)

class Multiple_Unterminated_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = f"""
%certificate --name=custom_certificate_1.pem
{CERT_CONTENT}

%certificate --name=custom_certificate_2.pem
{CERT_CONTENT_2}
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Missing_Certificate_Body_Fails_TestCase(ParserTest):
    def __init__(self, *args, **kwargs):
        ParserTest.__init__(self, *args, **kwargs)
        self.ks = """
%certificate --name=custom_certificate.pem --path /etc/pki/ca-trust/source/anchors/
%end
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

if __name__ == "__main__":
    unittest.main()
