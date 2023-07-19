import pymysql

from Config import Config

class Sql:
    @staticmethod
    def connect():
        Sql.conn = pymysql.connect(
            host     = Config.mysql['host'],
            user     = Config.mysql['user'], 
            password = Config.mysql['password'],
            db       = Config.mysql['database'],
            port     = int(Config.mysql['port'])
            )
        return 0


    @staticmethod
    def reconnect():
        try:
            Sql.conn.ping(reconnect=False)
        except:
            Sql.connect()



    @staticmethod
    def insert(sql, data):
        Sql.reconnect()
        cursor = Sql.conn.cursor()
        cursor.executemany(sql,(data))
        Sql.conn.commit()
        cursor.close()



    @staticmethod
    def execute(sql):
        Sql.connect()
        cursor = Sql.conn.cursor()
        cursor._defer_warnings = True
        cursor.execute(sql)
        Sql.conn.commit()

        cursor.close()
        Sql.conn.close()