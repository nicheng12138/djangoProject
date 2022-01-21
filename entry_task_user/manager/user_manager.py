from conf.log import log
from entry_task_user.manager.rpc_manager import req_rpc
from tcpServer.common.var import Code


def update_user(uid, nickname, picture):
    result = req_rpc("update_user", (uid, nickname, picture))
    if not result:
        data = {
            "msg": "error Server"
        }
        result = {'code': Code.FAIL}
        return result['code'], data
    elif result['code'] != Code.SUC:
        log.info("rpc request error: error_code:%s|method:%s|uid:%s|nickname:%s|picture:%s" %
                 (str(result['code']), "update_user", uid, nickname, picture))
    data = {
        "msg": result['msg']
    }
    return result['code'], data

def get_user(uid):
    result = req_rpc("get_user", uid)
    if not result:
        data = {
            "msg": "error Server"
        }
        result = {'code': Code.FAIL}
    elif result['code'] != Code.SUC:
        log.info("rpc request error: error_code:%s|method:%s|uid:%s" %
                 (str(result['code']), "get_user", uid))
        data = {
            "msg": result['msg']
        }
    else:
        data = {
            'username': result['data']['username'],
            'nickname': result['data']['nickname'],
            'picture': result['data']['picture'],
        }
    return result['code'], data
