from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
import urllib
import json

from variable import FILE_PATH, SERVER_ADDRESS
from services.socket_client import run_socket_client
from jinja2 import Environment, FileSystemLoader

class OwnHTTPRequestHandler(BaseHTTPRequestHandler):
    def send_html(self, namefile, status = 200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join(FILE_PATH['html'], namefile), 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filepath, status):
        self.send_response(status)
        mt, _ = mimetypes.guess_type(filepath)
        if mt:
            self.send_header('Content-type', mt)
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(filepath, 'rb') as f:
            self.wfile.write(f.read())

    def do_GET(self):
        if self.path == '/':
            self.send_html('index.html', 200)
        elif self.path == '/message':
            self.send_html('message.html', 200)
        elif self.path == '/messages':
            print(os.getcwd())
            env = Environment(loader=FileSystemLoader( FILE_PATH['html']))
            template = env.get_template('templallmess.html')
            with open(os.path.join(*FILE_PATH['storage']), 'rb') as f:
                messages = json.loads(f.read())
                print(messages)
            result = template.render(messages=messages, )
            with open(os.path.join(FILE_PATH['html'], "allmessage.html"), "w", encoding='utf-8') as f:
                f.write(result)
            self.send_html('allmessage.html', 200)
        else:
            if os.path.exists(os.path.join(FILE_PATH['static'], self.path[1:])):
                self.send_static(os.path.join(FILE_PATH['static'], self.path[1:]), 200)
            else:
                self.send_html('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data = urllib.parse.unquote_plus(data.decode())
        data = {key: value for key, value in [el.split('=') for el in data.split('&')]}
        res = run_socket_client(SERVER_ADDRESS['host'], SERVER_ADDRESS['port'], data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        


def run_server(host = SERVER_ADDRESS['host'], port = SERVER_ADDRESS['port']):
    server = HTTPServer((SERVER_ADDRESS['host'], SERVER_ADDRESS['port']), OwnHTTPRequestHandler)
    try:
        print('Server is running.......')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server closed.')
        server.server_close()
