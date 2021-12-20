import hashlib
import random
import time

from tcpServer.mysqlUtil import query
from tcpServer.redisUtil import set_str, get_str
from tcpServer.rsp import my_rsp
from tcpServer.var import Code


def login(username, password):
    sql = 'select * from user where username = %s'
    results = query(sql, username)
    if len(results) == 0:
        data = my_rsp(code=Code.NOT_FOUND, msg='user not found', data=None)
    elif results[0][2] != password:
        data = my_rsp(code=Code.AUTH_FAIL, msg='username or passwd error', data=None)
    else:
        token = str(time.time()) + str(results[0][0]) + str(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
        md5 = hashlib.md5()
        md5.update(token.encode(encoding='utf-8'))
        data = my_rsp(code=Code.SUC, msg='success', data={
            'username': username,
            'nickname': results[0][3],
            'picture': results[0][4],
            'token': md5.hexdigest()
        })
        set_str(md5.hexdigest(), results[0][0])
    return data

