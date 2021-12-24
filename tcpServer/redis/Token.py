from tcpServer.redis.Base import Base


class Token(Base):

    def __init__(self):
        Base.__init__()

    def check_token(self, token, id):
        if token is None:
            return False
        uuid = self.str_get(token)
        if uuid != id:
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
