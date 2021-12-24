from tcpServer.mysqlUtil import update, query
from tcpServer.redisUtil import get_str, del_key
from tcpServer.rsp import my_rsp
from tcpServer.var import Code


def update_user(token, nickname, picture, username):
    if token == 'tokenTest':
        sql = "update user set nickname = %s, picture = %s where username = %s limit 1 "
        res = update(sql, (str(nickname), str(picture), str(username)))
        if res == Code.MYSQL_FAIL:
            return my_rsp(code=Code.MYSQL_FAIL, msg='mysqlError', data=None)
        return my_rsp(code=Code.SUC, msg='success', data=None)
    else:
        if token is None:
            return my_rsp(code=Code.PARAM_INVALID, msg='param error', data=None)
        id = get_str(token)
        if id is None:
            return my_rsp(code=Code.TOKEN_INVALID, msg='token is invalid', data=None)
        elif id == -1:
            return my_rsp(code=Code.REDIS_FAIL, msg='redis error', data=None)
        sql = "update user set nickname = %s, picture = %s where id = %s limit 1"
        res = update(sql, (str(nickname), str(picture), int(id)))
        if res == Code.MYSQL_FAIL:
            return my_rsp(code=Code.MYSQL_FAIL, msg='mysql error', data=None)
        return my_rsp(code=Code.SUC, msg='success', data=None)


def logout(token):
    res = del_key(token)
    if res == Code.REDIS_FAIL:
        return my_rsp(code=Code.REDIS_FAIL, msg='redis error', data=None)
    return my_rsp(code=Code.SUC, msg='success', data=None)


def get_user(token, username):
    if token == 'tokenTest':
        sql = "select * from user where username = %s"
        results = query(sql, (username,))
    else:
        id = get_str(token)
        if id is None:
            return my_rsp(code=Code.TOKEN_INVALID, msg='token is invalid', data=None)
        elif id == -1:
            return my_rsp(code=Code.REDIS_FAIL, msg='redis error', data=None)
        sql = "select * from user where id = %s"
        results = query(sql, (id,))
    if len(results) == 0:
        return my_rsp(code=Code.NOT_FOUND, msg='user not found', data=None)
    elif results[0] == Code.MYSQL_FAIL:
        return my_rsp(code=Code.MYSQL_FAIL, msg='mysql error', data=None)
    return my_rsp(code=Code.SUC, msg='success', data={
        'username': results[0][1],
        'nickname': results[0][3],
        'picture': results[0][4],
    })


