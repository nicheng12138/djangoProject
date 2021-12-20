import pymysql

from tcpServer.mysqlUtil import update, query
from tcpServer.redisUtil import get_str, del_key
from tcpServer.rsp import my_rsp
from tcpServer.var import Code


def update_user(token, nickname, picture):
    id = get_str(token)
    print id
    if id is None:
        return my_rsp(code=Code.TOKEN_INVALID, msg='token is invalid', data=None)
    else:
        sql = "update user set nickname = %s, picture = %s where id = %s"
        res = update(sql, (str(nickname), str(picture), id))
        if res == 1:
            return my_rsp(code=Code.SUC, msg='success', data=None)
        else:
            return my_rsp(code=Code.FAIL, msg='fail', data=None)


def logout(token):
    del_key(token)
    return my_rsp(code=Code.SUC, msg='success', data=None)


def get_user(token):
    id = get_str(token)
    if id is None:
        return my_rsp(code=Code.TOKEN_INVALID, msg='token is invalid', data=None)
    sql = "select * from user where id = %s"
    results = query(sql, id)
    if len(results) == 0:
        return my_rsp(code=Code.TOKEN_INVALID, msg='token is invalid', data=None)
    return my_rsp(code=Code.SUC, msg='success', data={
            'username': results[0][1],
            'nickname': results[0][3],
            'picture': results[0][4],
        })
