from Sql        import Sql
from Syslog     import Syslog

class AuthLog:
    month  =""
    day     =""
    hour    =""
    domain  =""
    email   =""
    ip      =""
    log     =""


    @staticmethod
    def toList(auth):
        return [
            auth.month,
            auth.day,
            auth.hour,
            auth.domain,
            auth.email,
            auth.ip,
            auth.log
        ]


    @staticmethod
    def createTable():
        sql = '''
           CREATE TABLE IF NOT EXISTS auth_logs (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `month` varchar(3) DEFAULT NULL,
                `day` varchar(2) NOT NULL,
                `hour` varchar(2) DEFAULT NULL,
                `domain` varchar(124) NOT NULL,
                `ip` varchar(64) NOT NULL,
                `email` varchar(64) NOT NULL,
                `log` text DEFAULT NULL,
                PRIMARY KEY (`id`,`domain`,`email`,`ip`,`month`,`day`, `hour`)
                )
        '''
        try:
            Sql.execute(sql)
        except:
            Syslog.write("Error to create auth_logs table")
