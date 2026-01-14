from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import unittest
import os
import tempfile
import threading

from pykickstart import load
from pykickstart.errors import KickstartError

class LoadTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._content = """
auth --enableshadow --passalgo=sha512
graphical
firstboot --enable
ignoredisk --only-use=vda
keyboard --vckeymap=cz --xlayouts='cz'
lang cs_CZ.UTF-8

network  --bootproto=dhcp --device=ens3 --ipv6=auto --activate
network  --hostname=test
rootpw password
timezone Europe/Prague --isUtc
user --groups=wheel --name=testuser --password=password --iscrypted --gecos="Test User"
xconfig  --startxonboot
bootloader --location=mbr --boot-drive=vda
autopart --type=lvm
clearpart --all --initlabel --drives=vda

%packages
@^xfce-desktop-environment
@xfce-apps
@xfce-media
%end

%addon com_redhat_kdump --disable --reserve-mb='128'
%end
"""

    def setUp(self):
        (handle, self._path) = tempfile.mkstemp(prefix="testfile-", text=True)
        os.write(handle, self._content.encode("utf-8"))
        os.close(handle)

    def tearDown(self):
        os.unlink(self._path)

class Load_To_String_TestCase(LoadTest):
    def runTest(self):
        self.assertEqual(self._content, load.load_to_str(self._path))

class Load_To_File_TestCase(LoadTest):
    def __init__(self, *args, **kwargs):
        LoadTest.__init__(self, *args, **kwargs)
        self._target_path = ""

    def runTest(self):
        (handle, self._target_path) = tempfile.mkstemp(prefix="testfile", text=True)
        os.close(handle)
        target_path = load.load_to_file(self._path, self._target_path)
        self.assertEqual(target_path, self._target_path)
        with open(self._target_path, 'r') as f:
            self.assertEqual(self._content, f.read())
        with self.assertRaises(KickstartError):
            load.load_to_file("/tmp/foo", "/tmp/bar")

    def tearDown(self):
        super(Load_To_File_TestCase, self).tearDown()
        os.unlink(self._target_path)

class DirServer(ThreadingHTTPServer):
    def __init__(self, address, directory):
        super().__init__(address, SimpleHTTPRequestHandler)
        self.directory = directory

    def finish_request(self, request, client_address):
        SimpleHTTPRequestHandler(request, client_address, self, directory=self.directory)

class Load_From_URL_Test(LoadTest):
    def setUp(self):
        super(Load_From_URL_Test, self).setUp()

        self._server = DirServer(('127.0.0.1', 0), os.path.dirname(self._path))
        httpd_port = self._server.server_port
        self._url = 'http://127.0.0.1:%d/%s' % (httpd_port, os.path.basename(self._path))
        # wrong URL (HTTPS request won't be handled correctly by the HTTP server)
        self._url_https = "https" + self._url.lstrip("http")
        threading.Thread(target=self._server.serve_forever).start()

    def tearDown(self):
        super(Load_From_URL_Test, self).tearDown()
        self._server.shutdown()

class Load_From_URL_To_Str_TestCase(Load_From_URL_Test):
    def runTest(self):
        self.assertEqual(self._content, load.load_to_str(self._url))
        self.assertRaises(KickstartError, load.load_to_str, self._url_https)

class Load_From_URL_To_File_TestCase(Load_From_URL_Test):
    def setUp(self):
        super(Load_From_URL_To_File_TestCase, self).setUp()
        (handle, self._target_path) = tempfile.mkstemp(prefix="testfile", text=True)
        os.close(handle)

    def runTest(self):
        target_path = load.load_to_file(self._url, self._target_path)
        self.assertEqual(target_path, self._target_path)
        with open(self._target_path, 'r') as f:
            self.assertEqual(self._content, f.read())
        self.assertEqual(self._content, load.load_to_str(self._url))

        # raises SSLError in _load_url()
        with self.assertRaises(KickstartError):
            load.load_to_file(self._url_https, self._target_path)

        # raises RequestException in _load_url()
        with self.assertRaises(KickstartError):
            load.load_to_file('http://test.local/ks.cfg', self._target_path)

        # raises IOError in load_file()
        with self.assertRaises(KickstartError):
            load.load_to_file(self._url, '/no/exist')

        # request.status_code == 404 in _load_url()
        with self.assertRaises(KickstartError):
            load.load_to_file(self._url+'.TEST', '/tmp/foo')

    def tearDown(self):
        super(Load_From_URL_To_File_TestCase, self).tearDown()
        os.unlink(self._target_path)

if __name__ == "__main__":
    unittest.main()
