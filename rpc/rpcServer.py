import json
import os
import socket
import struct


def pre_fork(n):
    for i in range(n):
        pid = os.fork()
        if pid < 0:
            return
        if pid > 0:
            continue
        if pid == 0:
            break


def receive(conn, n):
    rs = []
    while n > 0:
        r = conn.recv(n)
        if not r:  # EOF
            return rs
        rs.append(r)
        n -= len(r)
    return ''.join(rs)


class RPCServer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.funs = {}

    def connect(self, port, num=None):
        self.sock.bind(('localhost', port))
        if num is None:
            num = 1
        self.sock.listen(num)
        pre_fork(10)
        self.loop(self.sock)

    def register_method(self, function, name=None):
        if name is None:
            name = function.__name__
        self.funs[name] = function

    def loop(self, sock):
        while True:
            conn, addr = self.sock.accept()
            self.handle_conn(conn)

    def handle_conn(self, conn):
        while True:
            length_prefix = receive(conn, 4)
            if not length_prefix:
                conn.close()
                break
            length, = struct.unpack("I", length_prefix)
            body = receive(conn, length)
            request = json.loads(body, encoding='utf-8')
            name = request['name']
            args = request['args']
            kwargs = request['kwargs']
            res = self.funs[name](*args, **kwargs)
            response = json.dumps(res.__dict__).encode('utf-8')
            length_prefix = struct.pack("I", len(response))
            conn.sendall(length_prefix)
            conn.sendall(response)
