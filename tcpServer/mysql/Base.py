import pymysql
from dbutils.pooled_db import PooledDB

import conf.conf
from tcpServer.common.var import Code


class Base:

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

        def get_conn():
            return self._pool.connection()

        def update(sql, args):
            try:
                conn = get_conn()
                cur = conn.cursor()
                cur.execute(sql, args)
                conn.commit()
                result = Code.SUC
            except Exception as e:
                print 'mysqlException: ', e
                conn.rollback()
                result = Code.MYSQL_FAIL
            finally:
                conn.close()
                cur.close()
                return result

        def get_one(sql, args):
            try:
                conn = get_conn()
                cur = conn.cursor()
                count = cur.execute(sql, args)
                if count == 0:
                    result = None
                else:
                    results = cur.fetchone()
            except Exception as e:
                print 'mysqlException: ' + e.msg
                result = (-1,)
            finally:
                cur.close()
                conn.close()
                return results

