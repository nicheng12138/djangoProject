import conf.conf
from rpc.rpc_server import rpc_server
from tcpServer.model.login.login import login, logout
from tcpServer.model.user.user import update_user, get_user

if __name__ == '__main__':
    server = rpc_server()
    server.register_method(login)
    server.register_method(logout)
    server.register_method(update_user)
    server.register_method(get_user)
    server.connect(conf.conf.RPC_SVR_PORT)
