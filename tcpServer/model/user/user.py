from tcpServer import mysql
from tcpServer.common.rsp import my_rsp
from tcpServer.common.var import Code
from tcpServer.redis.token_util import Token


user = mysql.UserUtil()


def update_user(id, nickname, picture):
    res = user.update_user_by_id(id, nickname, picture)
    if res is None or res == Code.MYSQL_FAIL:
        return my_rsp(Code.MYSQL_FAIL, "mysql is error", None)
    return my_rsp(Code.SUC, "success", None)


def get_user(id):
    res = user.get_one_by_id(id)
    if res is None:
        return my_rsp(Code.MYSQL_FAIL, "mysql is error", None)
    return my_rsp(Code.SUC, "success", {
        "username": res[1],
        "nickname": res[3],
        "picture": res[4]
    })

