from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import re


class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    def do_GET(self):
        method = self.get_method(self.url.path)
        if method:
            method_name, dict_params = method
            method = getattr(self, method_name)
            method(**dict_params)
            return
        else:
            self.send_error(404, "Not Found")

    def get_book(self, book_id):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        response = f"""
         {books[book_id]}
    <p>  Ruta: {self.path}            </p>
    <p>  URL: {self.url}              </p>
    <p>  HEADERS: {self.headers}      </p>
"""
        self.wfile.write(response.encode("utf-8"))

    def get_index(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        response = f"""
    <h1> Welcome to Great Books </h1>
    <p>  Ruta: {self.path}            </p>
    <p>  URL: {self.url}              </p>
    <p>  HEADERS: {self.headers}      </p>
"""
        self.wfile.write(response.encode("utf-8"))

    def get_method(self, path):
        for pattern, method in mapping:
            match = re.match(pattern, path)
            if match:
                return (method, match.groupdict())


mapping = [
            (r'^/Book/(?P<book_id>\d+)$', 'get_book'),
            (r'^/$', 'get_index')
        ]

books = {
            '1':"""
            <h1> Book 1 </h1>
            """, 
            '2':"""
            <h1> Book 2 </h1>
            """, 
            '3':"""
            <h1> Book 3 </h1>
            """, 
        }

if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 80), WebRequestHandler)
    server.serve_forever()
