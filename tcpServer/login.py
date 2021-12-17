# -*- coding: utf-8 -*


from tcpServer.mysqlUtil import query


def login(username, password):
    sql = 'select * from user where username = %s'
    results = query(sql, username)
    if len(results) == 0:
        data = {
            'code': -1,
            'msg': '用户不存在'
        }
    elif results[0][1] != password:
        data = {
            'code': -2,
            'msg': '用户名或密码错误'
        }
    else:
        data = {
            'code': 0,
            'msg': '登陆成功',
            'data': results
        }
    return data
