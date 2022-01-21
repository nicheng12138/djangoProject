from tcpServer.mysql.mysql_base import mysql_base


class user_mysql(mysql_base):

    def __init__(self):
        mysql_base.__init__(self)

    def get_user_by_name(self, username):
        sql = "select * from entry_task_user where username = %s"
        return self.get_one(sql, username)

    def get_user_by_id(self, id):
        sql = "select * from entry_task_user where id = %s"
        return self.get_one(sql, id)

    def update_user_by_id(self, id, nickname, picture):
        sql = "update entry_task_user set nickname = %s, picture = %s where id = %s"
        return self.update(sql, (nickname, picture, id))
