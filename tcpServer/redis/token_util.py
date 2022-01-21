from tcpServer.redis.redis_base import redis_base


class token_util(redis_base):

    def __init__(self):
        redis_base.__init__(self)

    def check_token(self, token, uid):
        if token is None:
            return False
        uuid = self.str_get(token)
        if uuid != uid:
            return False
        return True

    def del_token(self, token):
        res = self.del_key(token)
        if res is None:
            return True
        else:
            return False

    def set_token(self, token, id, time):
        return self.str_set(token, id, time)
