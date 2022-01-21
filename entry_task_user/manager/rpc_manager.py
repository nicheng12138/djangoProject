import time

from conf import conf
from conf.log import log
from rpc.rpc_client_pool import rpc_client_pool
from tcpServer.common.rsp import my_rsp
from tcpServer.common.var import Code

client_pool = rpc_client_pool(conf.RPC_SVR_IP, conf.RPC_SVR_PORT)


def req_rpc(func, *args):
    client = client_pool.get_rpc_client()
    start = time.time()
    try:
        log.debug("start request_rpc--------")
        result = client.call(func, *args)
        end = time.time()
        elapsed = int((end - start) * 1000)
        log.debug("rpc_request: elapsed=%s| func = %s|args= %s" % (str(elapsed), func, str(args)))
        return result
    except Exception as e:
        log.info("socket error:error_type = %s | func = %s|args= %s" % (e, func, str(args)))
        return my_rsp(Code.ERROR_PARAMS, "error params", None)
    finally:
        client_pool.release_rpc_client(client)
