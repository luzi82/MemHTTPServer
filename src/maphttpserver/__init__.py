import BaseHTTPServer

class MapHTTPServer(BaseHTTPServer.HTTPServer):
    
    def __init__(self,server_address):
        BaseHTTPServer.HTTPServer.__init__(self,server_address,MapHTTPRequestHandler)
        self.GET_map = {}

    def set_GET(self,path,content_type,content):
        self.GET_map[path]={
            'content_type':content_type,
            'content':content
        }

class MapHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if not self.path in self.server.GET_map:
            self.send_error(404)
            return
        entry = self.server.GET_map[self.path]
        self.send_response(200)
        self.send_header("Content-type", entry['content_type'])
        self.end_headers()
        self.wfile.write(entry['content'])
        self.wfile.close()
