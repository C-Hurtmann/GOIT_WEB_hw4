from http.server import SimpleHTTPRequestHandler
import socketserver
import urllib


DIRECTORY = 'front-init'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(directory=DIRECTORY, *args, **kwargs)
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [i.split('=') for i in data_parse.split('&')]}
        print(data_dict)
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run_server(port, handler=Handler):
    with socketserver.UDPServer(("", port), handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    run_server(3000)