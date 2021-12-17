import redis


def get_conn():
    redis_conn = redis.Redis(host='127.0.0.1', port='6379')
    return redis_conn


def get_str(key):
    return get_conn().get(key)


def set_str(key, value):
    conn = get_conn()
    conn.set(key, value)
