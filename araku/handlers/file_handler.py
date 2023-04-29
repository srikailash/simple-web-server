import os
import subprocess
from .common import base_handler

class case_file(base_handler):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return self.handle_file(handler, handler.full_path)

class case_no_file(base_handler):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return handler.handle_file(handler.full_path)  

class case_cgi_file(base_handler):
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
