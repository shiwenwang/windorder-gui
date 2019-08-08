from mysql import connector


class MySQL_DataBase(object):
    def __init__(self, **kwargs):
        self.config = {'host': kwargs['主机:'],
                       'port': kwargs['端口:'],
                       'user': kwargs['用户:'],
                       'password': kwargs['密码:'],
                       'database': kwargs['数据库名称:']}
        self.db = connector.MySQLConnection()

    def connect(self):
        print(self.db.is_connected())
        try:
            self.db = connector.MySQLConnection(**self.config)
        except:
            return False

        return self.db.is_connected()

    def query(self):
        pass


if __name__ == "__main__":
    config = {'数据库名称:': 'farm_insight', '': '', '主机:': '10.11.42.00',
              '端口:': '3306', '用户:': '36719', '密码:': 'wsw123456'}
    db_mysql = MySQL_DataBase(**config)

    print(db_mysql.connect())
