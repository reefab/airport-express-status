import plistlib
import json
from urllib.request import urlopen, Request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.path[1:]

        if host == 'health':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Status": "OK"}).encode())
        else:
            status = self.get_status(host)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Status": status}).encode())

    def get_status(self, host):
        httprequest = Request(f"http://{host}:7000/info")

        with urlopen(httprequest, timeout=60) as response:
            content = response.read()

        data = plistlib.loads(content)
        return data["statusFlags"] > 2000


httpd = ThreadingHTTPServer(("0.0.0.0", 8000), APIHandler)
httpd.serve_forever()
