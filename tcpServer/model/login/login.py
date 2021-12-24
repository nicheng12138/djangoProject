import hashlib
import random
import time

from tcpServer import mysql, redis
from tcpServer.common.rsp import my_rsp
from tcpServer.common.var import Code
user_util = mysql.UserUtil()
token_util = redis.Token()


def login(username, password):
    res = user_util.get_one_by_name()
    # 用户名错误
    if res is None:
        data = my_rsp(code=Code.NOT_FOUND, msg='user not found', data=None)
    # mysql错误
    elif res[0] == -1:
        data = my_rsp(code=Code.MYSQL_FAIL, msg='mysql is fail', data=None)
    # 密码错误
    elif res[2] != code_pwd(password):
        data = my_rsp(code=Code.AUTH_FAIL, msg='username or password error', data=None)
    else:
        token = get_token()
        token_util.set_token(token, res[0], 1800)
        data = my_rsp(code=Code.SUC, msg='success', data={
            'username': username,
            'nickname': res[3],
            'picture': res[4],
            'token': token
        })
    return data


def code_pwd(password):
    return password


def check_token(token):
    return token_util.check_token(token)


def logout(token):
    res = token_util.del_key(token)
    if res == Code.REDIS_FAIL:
        return my_rsp(code=Code.REDIS_FAIL, msg='redis error', data=None)
    return my_rsp(code=Code.SUC, msg='success', data=None)


def get_token():
    token = str(time.time()) + str(results[0][0]) + str(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    md5 = hashlib.md5()
    md5.update(token.encode(encoding='utf-8'))
    return md5.hexdigest()
