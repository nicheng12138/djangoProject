import pymysql


def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root123456', db='test')
    return conn


def insert(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    print (result)
    conn.commit()
    cur.close()
    conn.close()


def update(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()


def query(sql, args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, args)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return results
