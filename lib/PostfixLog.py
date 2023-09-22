from Sql import Sql
class PostfixLog:

    @staticmethod
    def createTable():
        sql = '''
           CREATE TABLE IF NOT EXISTS postfix_logs (
                id int AUTO_INCREMENT,
                month varchar(3) DEFAULT NULL,
                day varchar(2) DEFAULT NULL,
                hour varchar(2) DEFAULT NULL,
                mail_to varchar(124) DEFAULT NULL,
                mail_to_domain varchar(124) DEFAULT NULL,
                mail_from varchar(124) DEFAULT NULL,
                mail_from_domain varchar(124) DEFAULT NULL,
                status text,
                msgid varchar(255) DEFAULT NULL,
                PRIMARY KEY  (id, mail_to, mail_to_domain, mail_from, mail_from_domain, msgid, hour, day, month))
        '''
        try:
            Sql.execute(sql)
        except Exception as e:
            #print(e)
	    #Syslog.write(e)	
            pass

