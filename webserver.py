from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        books = None
        if self.query_data and 'q' in self.query_data:
            books = r.sinter(self.query_data['q'].split(' '))
        self.wfile.write(self.get_response(books).encode("utf-8"))

    def get_response(self, books):
        return f"""
    <h1> Hola Web </h1>
    <form action="/" method="get">
    	<label for="q">  Búsqueda </label>
    	<input type="text" name="q" required />
	</form>

    <p>  {self.query_data}   </p>
      <p>  {books}   </p>
"""


if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
