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

if __name__ == "__main__":
    unittest.main()
