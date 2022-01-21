import redis
import tcpServer.redis
import conf.conf
import tcpServer
from tcpServer.common.var import Code


class redis_base:

    def __init__(self):
        self._pool = redis.ConnectionPool(host=conf.conf.RDS_HOST, port=conf.conf.RDS_PORT, decode_responses=True)

    def get_conn(self):
        return self._pool.get_connection()

    def str_get(self, key):
        try:
            conn = self.get_conn()
            res = conn.get(key)
        except Exception as e:
            print "RedisException: ", e
            res = -1
        return res

    def str_set(self, key, value, ex):
        try:
            conn = self.get_conn()
            res = conn.set(key, value, ex=ex)
        except Exception as e:
            print "RedisException: ", e
            res = Code.REDIS_FAIL
        return res

    def del_key(self, key):
        try:
            conn = self.get_conn()
            res = conn.delete(key)
        except Exception as e:
            print "RedisException: " , e
            res = Code.REDIS_FAIL
        return res



