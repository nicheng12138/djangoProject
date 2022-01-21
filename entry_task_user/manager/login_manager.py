from django.shortcuts import render

from conf.log import log
from entry_task_user.manager.rpc_manager import req_rpc
from tcpServer.common.var import Code


def login(username, pwd):
    respon = req_rpc("login", (username, pwd))
    if not respon:
        myresp
    elif respon['code'] != Code.SUC:
        log.info("rpc request error: error_code:%s|method:%s|username:%s|pwd:%s" %
                 (str(result['code']), "login", username, pwd))
        data = {
            "msg": result['msg']
        }
    else:
        data = {
            'username': result['data']['username'],
            'nickname': result['data']['nickname'],
            'picture': result['data']['picture'],
            'token': result['data']['token'],
            'uid': result['data']['uid'],
        }
    return result['code'], data

def logout(token):
    result = req_rpc("logout", token)
    if not result:
        data = {
            "msg": "error Server"
        }
        result = {'code': Code.FAIL}
        return result['code'], data
    elif result['code'] != Code.SUC:
        log.info("rpc request error: error_code:%s|method:%s|token:%" %
                 (str(result['code']), "logout", token))
    data = {
        "msg": result['msg']
    }
    return result['code'], data
