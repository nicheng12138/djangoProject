import redis

import conf.conf
import tcpServer
from tcpServer.var import Code

pool = redis.ConnectionPool(host=conf.conf.RDS_HOST, port=conf.conf.RDS_PORT, decode_responses=True)


def get_conn():
    try:
        redis_conn = tcpServer.redis.Redis(connection_pool=pool)
    except Exception as e:
        print "RedisError: " + e.message
    return redis_conn


def get_str(key):
    try:
        res = get_conn().get(key)
    except Exception as e:
        print "RedisError: " + e.message
        res = -1
    return res


def set_str(key, value):
    try:
        conn = get_conn()
        res = conn.set(key, value, ex=1800)
    except Exception as e:
        print "RedisError: " + e.message
        res = Code.REDIS_FAIL
    return res


def del_key(key):
    try:
        conn = get_conn()
        res = conn.delete(key)
    except Exception as e:
        print "RedisError: " + e.message
        res = Code.REDIS_FAIL
    return res



