import json
import socket
import struct

from conf.log import log
from tcpServer.common.rsp import my_rsp
from tcpServer.common.var import Code


class rpc_client(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data):
        self.sock.sendall(data)

    def recv(self, length):
        return self.sock.recv(length)

    def close(self):
        return self.sock.close()

    def call(self, function, *args):
        try:
            d = {'name': function, 'args': args}
            requests = json.dumps(d).encode('utf-8')
            length = struct.pack('I', len(requests))
            self.send(length)
            self.send(requests)
            log.debug("send success")
            length_pre = self.recv(4)
            length, = struct.unpack('I', length_pre)
            data = self.recv(length)
            response = json.loads(data, encoding='utf-8')
            log.debug("recv success")
            return response
        except Exception as e:
            log.debug("req_%s fail| error_type=%s" % (function, e))
            return my_rsp(Code.FAIL, "server error", None).__dict__
