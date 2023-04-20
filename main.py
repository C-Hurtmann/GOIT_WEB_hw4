from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class HTTPHandler(BaseHTTPRequestHandler):
    project_map = {'#': 'front-init/index.html',
                   '/message.html': 'front-init/message.html'}
    
    def do_GET(self):
        location = urlparse(self.path)
        try:
            self.send_html_file(self.project_map[location.path])
        except KeyError:
            self.send_html_file('front-init/error.html')
        
    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

            
def run():
    server_address = ('', 3000)
    http = HTTPServer(server_address, HTTPHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
