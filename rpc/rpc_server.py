import json
import socket
import struct
import thread

from conf.log import log
from rpc.rpc_util import receive
from tcpServer.common.rsp import my_rsp
from tcpServer.common.var import Code


class rpc_server(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.funcs = {}

    def connect(self, port):
        self.sock.bind(('localhost', port))
        self.sock.listen(0xfff)
        self.loop(self.sock)

    def register_method(self, function, name=None):
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    def loop(self, sock):
        while True:
            conn, addr = self.sock.accept()
            try:
                thread.start_new_thread(self.handle_conn, conn)
            except socket.error as e:
                log.info("connect error,addr is %s" % addr)

    def handle_conn(self, conn):
        try:
            while True:
                length_prefix = conn.recv(4)
                if not length_prefix:
                    conn.close()
                    break
                length, = struct.unpack("I", length_prefix)
                body = receive(conn, length)
                request = json.loads(body, encoding='utf-8')
                name = request['name']
                args = request['args']
                res = self.funcs[name](*args)
                if res is None:
                    res = my_rsp(Code.PARAM_INVALID, "param is invalid", None)
                response = json.dumps(res.__dict__).encode('utf-8')
                length_prefix = struct.pack("I", len(response))
                conn.sendall(length_prefix)
                conn.sendall(response)
        except socket.error as e:
            print 'socket error: ' + str(e)

