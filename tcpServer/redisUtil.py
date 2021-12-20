import redis


def get_conn():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    redis_conn = redis.Redis(connection_pool=pool)
    return redis_conn


def get_str(key):
    return get_conn().get(key)


def set_str(key, value):
    conn = get_conn()
    conn.set(key, value, ex=1800)


def del_key(key):
    conn = get_conn()
    conn.delete(key)



