import json
import socket
import struct
import threading

from tcpServer.rsp import my_rsp
from tcpServer.var import Code


class TCPClient(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.num = threading.Semaphore(1)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data):
        self.sock.sendall(data)

    def recv(self, length):
        return self.sock.recv(length)

    def close(self):
        return self.sock.close()


class RPCStub(object):
    def __getattr__(self, function):
        def _func(*args, **kwargs):
            try:
                d = {'name': function, 'args': args, 'kwargs': kwargs}
                requests = json.dumps(d).encode('utf-8')
                length = struct.pack('I', len(requests))
                self.num.acquire()
                self.send(length)
                self.send(requests)
                length_pre = self.recv(4)
                length, = struct.unpack('I', length_pre)
                data = self.recv(length)
                self.num.release()
                response = json.loads(data, encoding='utf-8')
                return response
            except Exception as e:
                return my_rsp(Code.FAIL, "server error", None).__dict__

        setattr(self, function, _func)
        return _func


class RPCClient(TCPClient, RPCStub):
    pass
