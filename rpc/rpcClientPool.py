import json
import struct

from socketpool.conn import TcpConnector
from socketpool.pool import ConnectionPool
from rpc.rpcServer import receive
from tcpServer.var import Code


class RPCClientPool(object):

    def __init__(self, host, port):
        self._pool = ConnectionPool(factory=TcpConnector,
                                    options={'host': host, 'port': port},
                                    max_size=100)
        self.host = host
        self.port = port

    def __initpool__(self):
        self._pool = ConnectionPool(factory=TcpConnector,
                                    options={'host': self.host, 'port': self.port},
                                    max_size=100)

    def __getattr__(self, function):
        def _func(*args, **kwargs):
            try:
                response_error = {"code": Code.FAIL, "msg": "server error", "data": None}
                with self._pool.connection() as conn:
                    d = {'name': function, 'args': args, 'kwargs': kwargs}
                    requests = json.dumps(d).encode('utf-8')
                    length = struct.pack('I', len(requests))
                    conn.send(length)
                    conn.send(requests)
                    self.conn_list[id(conn)] = 0
                    length_pre = receive(conn, 4)
                    length, = struct.unpack('I', length_pre)
                    data = receive(conn, length)
                    response = json.loads(data, encoding='utf-8')
                    return response
            except Exception as e:
                print "Exception:" + str(e)
                self._pool.release_connection(conn)
                self.conn_list.pop(id(conn))
                return response_error
        setattr(self, function, _func)
        return _func
