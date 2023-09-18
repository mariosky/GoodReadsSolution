from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

# Código basado en:
# https://realpython.com/python-http-server/
# https://docs.python.org/3/library/http.server.html
# https://docs.python.org/3/library/http.cookies.html


class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        # Este código no va aquí, es mejor
        # sacarlo a su propio método.
        # Es solo un ejemplo.
        c = self.cookies
        if not c:
            print("No cookie")
            c = SimpleCookie()
            c["session"] = 1
            c["session"]["max-age"] = 10
            print(c)
        else:
            print("Cookie found")
            session = c.get("session", 1)
            c["session"]["max-age"] = 10
            # Utiliza session como clave.
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header('Set-Cookie', c.output(header=''))
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def do_POST(self):
        self.do_GET()

    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p>  Path: {self.path}         </p>
    <p>  Headers: {self.headers}      </p>
    <p>  Cookies: {self.cookies}      </p>
    <p>  Query Data: {self.query_data}   </p>
    <p>  Form Data: {self.form_data}   </p>
    <code> 
    curl -v -i 'http://127.0.0.1:8000?id=123&value=22' --data 'user=mariosky&password=clavesecreta' -H 'Cookie: session=3;eu_cookie_consent=true'
    </code>
"""


if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
