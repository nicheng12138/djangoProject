import conf.conf
from rpc.rpcServer import RPCServer
from tcpServer.login import login
from tcpServer.user import update_user, logout, get_user

if __name__ == '__main__':
    s = RPCServer()
    s.register_method(login)
    s.register_method(update_user)
    s.register_method(logout)
    s.register_method(get_user)
    s.connect(conf.conf.RPC_SVR_PORT)


