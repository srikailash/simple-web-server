import os

#Base class for case handler parents
class base_handler(object):
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

class case_always_fail(base_handler):
    def test(self, handler):
        return os.path.exists(handler.full_path)
    def act(self, handler):
        return handler.handle_file(handler.full_path)