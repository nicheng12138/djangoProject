

class my_rsp:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    def code(self):
        return self.code

    def msg(self):
        return self.msg

    def data(self):
        return self.data
