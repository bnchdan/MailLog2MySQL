from    AuthLog    import AuthLog
from    DovecotLog import DovecotLog
from    Sql        import Sql
from    Syslog     import Syslog
import  time

class Logs:
    TYPE_AUTH       = 1
    TYPE_MAIL       = 2
    TYPE_POSTFIX    = 3
    TYPE_DOVECOT    = 4

    def __init__(self):
        self.auth       = []
        self.mail       = []
        self.postfix    = []
        self.dovecot    = []
        self.num_logs   = 0 


    #set auth log
    def set(self, log, type):
        self.num_logs = self.num_logs + 1

        if ( type == Logs.TYPE_AUTH ):
            self.auth.append(AuthLog.toList(log))
            return 0

        if ( type == Logs.TYPE_MAIL ):
            self.mail.append(log)
            return 0

        if ( type == Logs.TYPE_POSTFIX ):
            self.postfix.append(log)
            return 0

        if ( type == Logs.TYPE_DOVECOT ):
            self.dovecot.append(DovecotLog.toList(log))
            
            return 0

        return 1


    def get(self):
        pass
        
    
    def insertToMySQL(self) : 
        sql = '''
            INSERT IGNORE INTO auth_logs 
            (month, day, hour, domain, email, ip, log) 
            VALUES (%s,%s,%s,%s,%s,%s,%s);'''
        try:
            if ( len(self.auth) > 0 ):
                Sql.insert(sql, self.auth)
                self.auth=[]

        except Exception as e :
            Syslog.write(e)
    
        sql = '''
            INSERT IGNORE INTO dovecot_logs 
            (month, day, hour, domain, email, msgid, log) 
            VALUES (%s,%s,%s,%s,%s,%s,%s);'''
        try:
            if ( len(self.dovecot) > 0 ):
                Sql.insert(sql, self.dovecot)
                self.dovecot=[]

        except Exception as e :
            Syslog.write(e)
        
        sql = '''
            INSERT IGNORE INTO postfix_logs 
            (month, day, hour, mail_to, mail_to_domain, 
            mail_from, mail_from_domain, status, msgid) 
            VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s);'''
        try:
            if ( len(self.postfix) > 0 ):
                Sql.insert(sql, self.postfix)
                idx=0
                self.postfix=[]

        except Exception as e :
            Syslog.write(e)
            
        
        self.num_logs=0


    def clear(self):
        self.auth.clear()
        self.num_logs = 0


    def clearAuth(self):
        pass
    