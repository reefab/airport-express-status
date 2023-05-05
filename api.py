import plistlib
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.path[1:]
        
        print(f"Trying host: {host}")

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

    def get_status(self, host) -> bool:
        try:
            with urlopen(f"http://{host}:7000/info", timeout=60) as response:
                content = response.read()
        except HTTPError as error:
            print(error.status, error.reason)
            return False
        except URLError as error:
            print(error.reason)
            return False
        except TimeoutError:
            print("Request timed out")
            return False


        data = plistlib.loads(content)
        return data["statusFlags"] > 2000


httpd = ThreadingHTTPServer(("0.0.0.0", 8000), APIHandler)
httpd.serve_forever()
