from Sql        import Sql
from Syslog     import Syslog

class DovecotLog:
    month  =""
    day     =""
    hour    =""
    domain  =""
    email   =""
    msgid   =""
    log     =""


    @staticmethod
    def toList(dovecot):
        return [
            dovecot.month,
            dovecot.day,
            dovecot.hour,
            dovecot.domain,
            dovecot.email,
            dovecot.msgid,
            dovecot.log
        ]


    @staticmethod
    def createTable():
        sql = '''
           CREATE TABLE IF NOT EXISTS dovecot_logs (
                id int AUTO_INCREMENT,
                month varchar(3),
                day varchar(2),
                hour varchar(2),
                domain varchar(124),
                email varchar(64),
                msgid varchar(64),
                log varchar(64),
                PRIMARY KEY  (id, domain, email, msgid, hour, day, month))
        '''
        try:
            Sql.execute(sql)
        except Exception as e:
            Syslog.write("Error to create dovecot_logs table")
            


    