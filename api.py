from plistlib import loads, InvalidFileException
from json import dumps
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.path[1:]
        
        print(f"Trying host: {host}")

        if host == 'health':
            self.set_response("OK", 200)
        else:
            
            self.get_status(host)

    def get_status(self, host: str) -> None:
        try:
            with urlopen(f"http://{host}:7000/info", timeout=60) as response:
                content = response.read()
                data = loads(content)
                self.set_response(data["statusFlags"] > 2000, response.status)
        except InvalidFileException as error: 
            self.set_response("Invalid file", 200)
        except HTTPError as error:
            self.set_response(False, error.status)
        except URLError as error:
            self.set_response(False, 500)
        except TimeoutError:
            print("Request timed out")
            self.set_response(False, 408)
           
    def set_response(self, status: str = "Error", statusCode: int = 500) -> None:
            self.send_response(statusCode)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(dumps({"Status": status, "StatusCode": statusCode}).encode())


httpd = ThreadingHTTPServer(("0.0.0.0", 8000), APIHandler)
httpd.serve_forever()
