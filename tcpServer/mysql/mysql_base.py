import pymysql
from dbutils.pooled_db import PooledDB

import conf.conf
from tcpServer.common.var import Code


class mysql_base:

    def __init__(self):
        self._pool = PooledDB(pymysql,
                        mincached=conf.conf.DB_MINCACHE,
                        maxcached=conf.conf.DB_MAXCACHE,
                        maxconnections=conf.conf.DB_MAXCONNECT,
                        maxusage=conf.conf.DB_MAXUSEAGE,
                        host=conf.conf.DB_HOST,
                        port=conf.conf.DB_PORT,
                        user=conf.conf.DB_USER,
                        passwd=conf.conf.DB_PASS,
                        db=conf.conf.DB_DATABASE,
                        use_unicode=False,
                        blocking=False,
                        charset="utf8")

    def get_conn(self):
        return self._pool.connection()

    def update(self, sql, args):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute(sql, args)
            conn.commit()
            result = Code.SUC
        except Exception as e:
            conn.rollback()
            result = Code.MYSQL_FAIL
        finally:
            conn.close()
            cur.close()
            return result

    def get_one(self, sql, args):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            count = cur.execute(self, args)
            results = None
            if count != 0:
                results = cur.fetchone()
            return results
        except Exception as e:
            return (-1,)
        finally:
            cur.close()
            conn.close()


