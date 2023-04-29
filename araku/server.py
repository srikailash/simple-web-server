#todo: Separate out the templating part for the server
#Serving Static Pages - Serving them from the disk instead of generating them 
#on the fly
#todo: Add a favicon.ico for the website
#todo: Error Handling
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
from sws.handlers import *

class RequestHandler(BaseHTTPRequestHandler):
    cases = [
            case_cgi_file(),
            case_directory_no_index_file(),
            case_file(),
            case_no_file()
        ]
    full_path = ""

    Listing_Page = '''\
    <html>
        <body>
            <ul>
                {0}
            </ul>
        </body>
    </html>
    '''

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            print(msg)

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = []

            for e in entries:
                if not e.startswith('.'):
                    bullets.append(self.get_href_for_full_path(e))

            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(bytes(page, 'utf-8'))
        except OSError as msg:
            print(msg)

    def get_href_for_full_path(self, full_path):
        directory_url = self.path + '/' + full_path
        return '<li><a href={0}>{1}</a></li>'.format(self.path + '/' + full_path, full_path)

    # Send actual content
    def send_content(self, content):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__== '__main__':
    health.healthClass.is_healthy()
    serverAddress = ("localhost", 9000)
    server = HTTPServer(serverAddress, RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server")
    finally:    
        server.server_close()
