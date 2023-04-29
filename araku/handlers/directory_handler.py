import os
from .common import base_handler

class case_directory_index_file(base_handler):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler))
    def act(self, handler):
        return handler.handle_file(self.index_path(handler))

class case_directory_no_index_file(base_handler):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler))
    def act(self, handler):
        return handler.list_dir(handler.full_path)