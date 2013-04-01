import BaseHTTPServer


class MapHTTPServer(BaseHTTPServer.HTTPServer):

    def __init__(self, server_address):
        BaseHTTPServer.HTTPServer.__init__(self, server_address,
                                           MapHTTPRequestHandler)
        self.path_to_output = {}

    def set_get_output(self, path, content_type, content):
        self.path_to_output[path] = {
            'content_type': content_type,
            'content': content
        }


class MapHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """HTTPRequestHandler for MapHTTPServer"""

    def do_GET(self): # pylint: disable-msg=C0103
        if not self.path in self.server.path_to_output:
            self.send_error(404)
            return
        entry = self.server.path_to_output[self.path]
        self.send_response(200)
        self.send_header("Content-type", entry['content_type'])
        self.end_headers()
        self.wfile.write(entry['content'])
        self.wfile.close()
