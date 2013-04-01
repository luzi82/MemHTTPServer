import BaseHTTPServer


class MemHTTPServer(BaseHTTPServer.HTTPServer):
    """
    Simple HTTPServer

    >>> import httplib
    >>> server = MemHTTPServer(('', 10080))
    >>> server.set_get_output('path', 'text/html', 'content')
    >>> server.server_activate()
    >>> client = httplib.HTTPConnection('localhost', 10080)
    >>> client.connect()
    >>> client.request('GET', 'path')
    >>> server.handle_request()
    >>> response = client.getresponse()
    >>> print response.getheader('Content-type')
    text/html
    >>> print response.read()
    content
    """

    def __init__(self, server_address):
        BaseHTTPServer.HTTPServer.__init__(self, server_address,
                                           MemHTTPRequestHandler)
        self.path_to_output = {}

    def set_get_output(self, path, content_type, content):
        self.path_to_output[path] = {
            'content_type': content_type,
            'content': content
        }


class MemHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    HTTPRequestHandler for MemHTTPServer
    Don't use it in other HTTPServer
    """

    def do_GET(self): # pylint: disable-msg=C0103
        """Override BaseHTTPRequestHandler.do_GET"""
        
        if not self.path in self.server.path_to_output:
            self.send_error(404)
            return
        entry = self.server.path_to_output[self.path]
        self.send_response(200)
        self.send_header("Content-type", entry['content_type'])
        self.end_headers()
        self.wfile.write(entry['content'])
        self.wfile.close()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
