import mysql.connector.pooling
import pymysql
from dbutils.pooled_db import PooledDB

import conf.conf
from tcpServer.var import Code


pool = PooledDB(pymysql,
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
    try:
        conn = pool.connection()
        return conn
    except mysql.connector.Error as e:
        print 'error: ' + e.msg


def update(sql, args):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql, args)
        conn.commit()
        result = 0
    except mysql.connector.Error as e:
        print 'MysqlError: ' + e.msg
        conn.rollback()
        result = Code.MYSQL_FAIL
    finally:
        conn.close()
        cur.close()
        return result


def query(sql, args):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql, args)
        results = cur.fetchall()
        return results
    except mysql.connector.Error as e:
        print 'MysqlError: ' + e.msg
        return (Code.MYSQL_FAIL,)
    finally:
        cur.close()
        conn.close()

