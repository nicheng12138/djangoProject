import socket
import threading

from rpc.rpc_client import rpc_client

class rpc_client_pool(object):
    def __init__(self, host, port, num=20):
        self.rpc_client_list = []
        self.num = threading.Semaphore(num)
        for i in range(num):
            client = rpc_client()
            client.connect(host, port)
            self.rpc_client_list.append(client)

    def get_rpc_client(self):
        self.num.acquire()
        client = self.rpc_client_list.pop()
        return client

    def release_rpc_client(self, client):
        self.rpc_client_list.append(client)
        self.num.release()

