import unittest
from memhttpserver import MemHTTPServer
from httplib import HTTPConnection


class TestMemHTTPServer(unittest.TestCase):

    PORT = 10080

    def test_get(self):

        PORT = TestMemHTTPServer.PORT

        server = MemHTTPServer(('localhost', PORT))
        server.set_get_output('asdf', 'text/html', 'ASDF')
        server.set_get_output('qwer', 'text/plain', 'QWER')

        server.server_activate()

        client = HTTPConnection('localhost', PORT)
        client.connect()
        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()

        self.assertEqual(200, response.status)
        self.assertEqual('ASDF', response.read())
        self.assertEqual('text/html', response.getheader('Content-type'))

        client = HTTPConnection('localhost', PORT)
        client.connect()
        client.request('GET', 'qwer')
        server.handle_request()
        response = client.getresponse()

        self.assertEqual(200, response.status)
        self.assertEqual('QWER', response.read())
        self.assertEqual('text/plain', response.getheader('Content-type'))

    def test_404(self):

        PORT = TestMemHTTPServer.PORT

        server = MemHTTPServer(('localhost', PORT))

        server.server_activate()

        client = HTTPConnection('localhost', PORT)
        client.connect()
        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()

        self.assertEqual(404, response.status)

    def test_change(self):

        PORT = TestMemHTTPServer.PORT

        server = MemHTTPServer(('localhost', PORT))
        server.set_get_output('asdf', 'text/html', 'ASDF')

        server.server_activate()

        client = HTTPConnection('localhost', PORT)
        client.connect()
        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()

        self.assertEqual(200, response.status)
        self.assertEqual('ASDF', response.read())
        self.assertEqual('text/html', response.getheader('Content-type'))

        server.set_get_output('asdf', 'text/plain', 'QWER')

        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()

        self.assertEqual(200, response.status)
        self.assertEqual('QWER', response.read())
        self.assertEqual('text/plain', response.getheader('Content-type'))
        
    def test_timeout(self):
        
        PORT = TestMemHTTPServer.PORT

        server = MemHTTPServer(('localhost', PORT))
        server.timeout = 1

        server.server_activate()
        server.handle_request()

if __name__ == '__main__':
    unittest.main()
