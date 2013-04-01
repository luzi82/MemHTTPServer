import unittest
from maphttpserver import MapHTTPServer
from httplib import HTTPConnection

class TestMapHTTPServer(unittest.TestCase):
    
    PORT = 10080

    def test_get(self):
        
        PORT = TestMapHTTPServer.PORT
        
        server = MapHTTPServer(('localhost',PORT))
        server.set_GET('asdf', 'text/html', 'ASDF')
        server.set_GET('qwer', 'text/plain', 'QWER')
        
        server.server_activate()

        client = HTTPConnection('localhost',PORT)
        client.connect()
        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()
        
        self.assertEqual(200, response.status)
        self.assertEqual('ASDF', response.read())
        self.assertEqual('text/html', response.getheader('Content-type'))
        
        client = HTTPConnection('localhost',PORT)
        client.connect()
        client.request('GET', 'qwer')
        server.handle_request()
        response = client.getresponse()
        
        self.assertEqual(200, response.status)
        self.assertEqual('QWER', response.read())
        self.assertEqual('text/plain', response.getheader('Content-type'))
        
    def test_404(self):

        PORT = TestMapHTTPServer.PORT
        
        server = MapHTTPServer(('localhost',PORT))

        server.server_activate()

        client = HTTPConnection('localhost',PORT)
        client.connect()
        client.request('GET', 'asdf')
        server.handle_request()
        response = client.getresponse()
        
        self.assertEqual(404, response.status)

if __name__ == '__main__':
    unittest.main()
