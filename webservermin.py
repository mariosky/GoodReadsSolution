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
        book_list = re.findall(r'^/Book/(\d+)$', self.url.path)
        if book_list:
            if book_list[0] in books:
                self.get_book( book_list[0])
                return 
            else:
                    print("Not Found")
                    self.error_message_format = "Does not compute!"
                    self.send_error(self, 404, "Not Found") 
        else:
                print("Not Found")
                self.send_error( 404, "Not Found") 

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

    def get_response(self, book_id):
        return f"""
         {books[book_id]}
    <p>  Ruta: {self.path}         </p>
    <p>  URL: {self.url}         </p>
    <p>  HEADERS: {self.headers}      </p>
"""


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
