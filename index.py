#todo: Separate out the templating part for the server
#Serving Static Pages - Serving them from the disk instead of generating them 
#on the fly
#todo: Add a favicon.ico for the website
#todo: Error Handling
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess

#Base class for case handler parents
class base_class(object):
    '''Parent for case handlers.'''
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
                print("This is content from handle_file=", content)
            handler.send_content(content)
        except IOError as msg:
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented'

    def act(self, handler):
        assert False, 'Not implemented'

class case_file(base_class):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return self.handle_file(handler, handler.full_path)

class case_no_file(base_class):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return handler.handle_file(handler.full_path)  

class case_cgi_file(base_class):
    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')
    def act(self, handler):
        return self.run_cgi(handler)
    def run_cgi(self, handler):
        cmd = ['python', handler.full_path]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        response = b''
        while True:
            if process.poll() is not None:
                break
        for line in process.stdout:
            response = response + line
        handler.send_content(response)

class case_directory_index_file(base_class):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler))
    def act(self, handler):
        return handler.handle_file(self.index_path(handler))

class case_directory_no_index_file(base_class):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler))
    def act(self, handler):
        return handler.list_dir(handler.full_path)

class case_always_fail(base_class):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return handler.handle_file(handler.full_path)


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
    serverAddress = ("localhost", 9000)
    server = HTTPServer(serverAddress, RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server")
    finally:    
        server.server_close()
