import conf.conf
from rpc.rpc_server import rpc_server


if __name__ == '__main__':
    server = rpc_server()
    server.connect(conf.conf.RPC_SVR_PORT)




