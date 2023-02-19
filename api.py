import plistlib
import json
from urllib.request import urlopen, Request
from http.server import HTTPServer, BaseHTTPRequestHandler

class APIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        host = self.path[1:]

        status = self.get_status(host)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'Status': status}).encode())

    def get_status(self, host):
        url = f'http://{host}:7000/info'
        httprequest = Request(url)

        with urlopen(httprequest) as response:
            content = response.read()

        data = plistlib.loads(content)
        return data['statusFlags']> 2000

httpd = HTTPServer(('localhost', 8000), APIHandler)
httpd.serve_forever()
