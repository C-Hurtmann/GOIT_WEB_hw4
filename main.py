from datetime import datetime
from http.server import SimpleHTTPRequestHandler
import socket
import socketserver
import urllib
from threading import Thread
import json

DIRECTORY = "front-init"
HTTP_SERVER_PORT = 3000
SOCKET_SERVER_PORT = 5000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(directory=DIRECTORY, *args, **kwargs)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        run_socket_client(data_parse)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()


def run_http_server(port, handler=Handler):
    print("HTTP server activated")
    with socketserver.TCPServer(("localhost", port), handler) as httpd:
        httpd.serve_forever()


def run_socket_server(port):
    print("Socket server activated")
    host = socket.gethostname()
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    try:
        while True:
            data, address = server.recvfrom(1024)
            formated_data = format_data(data.decode())
            send_to_storage(formated_data)
    except KeyboardInterrupt:
        print("Socket server destroyed")
    finally:
        server.close()


def run_socket_client(message):
    print("Client activated")
    host = socket.gethostname()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = host, SOCKET_SERVER_PORT
    encoded_message = message.encode()
    client.sendto(encoded_message, server)
    client.close()


def format_data(data):
    data_dict = {key: value for key, value in [i.split("=") for i in data.split("&")]}
    now = datetime.now()
    return {str(now): data_dict}


def send_to_storage(data):
    with open("storage/data.json", "r+") as f:
        if not f.read():
            f.write('{}')

    with open("storage/data.json", "r+") as f:
        storage_data = json.load(f)
        storage_data.update(data)
        f.seek(0)
        json.dump(storage_data, f, indent=4)


def main():
    http = Thread(target=run_http_server, args=(HTTP_SERVER_PORT,))
    http.start()
    server = Thread(target=run_socket_server, args=(SOCKET_SERVER_PORT,))
    server.start()


if __name__ == "__main__":
    main()
