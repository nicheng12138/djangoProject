from rpc.rpcServer import RPCServer
from tcpServer.login import login

if __name__ == '__main__':
    s = RPCServer()
    s.register_function(login)
    s.loop(5000)
