from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import parse_qs
import cgi

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print (self.path)
        print (parse_qs(self.path[2:]))
        self.wfile.write(bytes("<html><body><h1>Get Request Received!</h1></body></html>\n",'utf-8'))
    def do_POST(self):
        
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        print ("VLAN is "+form.getvalue("vlan"))
        print ("IP assigned "+form.getvalue("ip"))
        print ("Customer ID "+form.getvalue("customer ID"))
        self.wfile.write(bytes("<html><body><h1>POST Request Received!</h1></body></html>\n",'utf-8'))

def run(server_class=HTTPServer, handler_class=GP, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Server running at localhost:8088...')
    httpd.serve_forever()

run()
