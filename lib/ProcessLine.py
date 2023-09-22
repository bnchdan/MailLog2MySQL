from AuthLog    import AuthLog
from DovecotLog import DovecotLog
from Logs       import Logs
from Queue      import Queue

class ProcessLine:

    @staticmethod
    def main(line, logs):
        words       = line.split(" ")
        len_words   = len(words)
       
        try:
            if ( len(words) < 5 ):
                return 1
            
            if (words[5][:11] == "auth-worker" or
                words[5][:11] == "imap-login:" or
                words[5][:11] == "pop3-login:" or
                words[5][:17] == "managesieve-login"):
                    return ProcessLine.auth_log(words, len_words, logs )

            if (words[4][:7] == "dovecot"):
                return ProcessLine.dovecot_log(words, len_words, logs )

            if (words[4][:7] == "postfix"):
                return ProcessLine.postfix_log(words, len_words, logs)
        except:
            pass
        return 1



    @staticmethod
    def auth_log(words, len_words, logs ):
        while(len_words == 13):
            if ( words[10][0:4] != "sql(" ):
                break
         
            aux_word = words[10].split(",")
            loc      = aux_word[0].find('@')

            flag1 = True
            if (len(aux_word) < 2 ):
                if ( words[10].find(")") == -1 ):
                    break
                else:
                    flag1 = False
            
            flag2 = True
            if (loc == -1 ):
                flag2 = False

            authLog = AuthLog()
            authLog.month  = words[0][:3]
            authLog.day     = words[1][:3]
            authLog.hour    = words[2].split(":")[0][:2]
            authLog.email   = aux_word[0][4:loc][:64]
            
            if (flag2 == True):
                authLog.domain  = aux_word[0][loc+1:][:124]
            
            authLog.ip = ""
            if ( flag1 == True ):
                authLog.ip      = aux_word[1].split(")")[0][:64]
                authLog.domain  = aux_word[0][loc+1:][:124]
            else:
                authLog.domain  = aux_word[0][loc+1:].split(")")[0][:124]
            
            if (words[11]=="Password" and words[12][0:8]=="mismatch" ):
                authLog.log = "Password mismatch"
                return logs.set(authLog, logs.TYPE_AUTH)

            if (words[11]=="unknown" and words[12][0:4]== "user"):
                authLog.log = "unknown user"
                return logs.set(authLog, logs.TYPE_AUTH)
            break

        while (len_words == 13):
            if (words[6]    != "Login:"):
                break
            if (words[7][:6]!= "user=<"):
                break    
            if (words[9][:4]!= "rip="):
                break    

            authLog = AuthLog()
            authLog.month  = words[0][:3]
            authLog.day     = words[1][:2]
            authLog.hour    = words[2].split(":")[0][:2]

            loc = words[7].find("@")
            if ( loc == -1 ):
                authLog.email  = words[7][6:-2][:64]
                authLog.domain = ""
            else:
                authLog.email  = words[7][    6:loc][:64]
                authLog.domain = words[7][loc+1:-2][:124]

            authLog.ip  = words[9][4:-1][:64]
            authLog.log = "logged in "+ words[5][:-1]
            return logs.set(authLog, logs.TYPE_AUTH)
        
        return 1



    @staticmethod   
    def dovecot_log(words, len_words, logs):
        while( len_words > 9 ):
            if ( words[5][:5] != "imap(" and  words[5][:5] != "pop3("):
                break
            
            if ( words[-2][:7] != "msgid=<"):
                break

            loc = words[5].find('@')
            dovecotLog = DovecotLog()
            dovecotLog.month  = words[0][:3]
            dovecotLog.day     = words[1][:2]
            dovecotLog.hour    = words[2].split(":")[0][:2]

            if ( loc == -1 ): 
                dovecotLog.email  = words[5][5:].split(")")[0][:64]
            else:
                dovecotLog.email  = words[5][5:].split("@")[0][:64]
                dovecotLog.domain = words[5][5:].split("@")[1].split(")")[0][:124]

            dovecotLog.msgid  = words[-2][7:7+64][:-2]
            dovecotLog.log = " ".join(words[6:-3])[:64][:-1]
            return logs.set(dovecotLog, logs.TYPE_DOVECOT )
        
        return 1
        


    @staticmethod   
    def postfix_log(words, len_words, logs):
        
        # if (words[6][:7] == "client="):
        #     return Queue.add(words[5][:-1], words[0], words[1], words[2].split(":")[0])
       
        if (words[6][:7] == "removed"):
            return Queue.remove(words[5][:-1])
        
        if (words[6][:12] == "message-id=<"):
            Queue.add(words[5][:-1], words[0], words[1], words[2].split(":")[0])
            return Queue.addMsgID(words[5][:-1], words[6][12:-2] )

        
        if (words[6][0:6] == "from=<"):
            return Queue.addFrom(words[5][:-1], words[6][6:-2])
        
        if (words[6][0:4] == "to=<"):
            i = 7
            while True:
                if ( i == len_words ):
                    break

                if (words[i][0:7] == "status="):
                    return Queue.addTo(words[5][:-1], words[6][4:-2], words[i][7:].split("\n")[0])

                i=i+1

        if (words[6]        == "milter-reject:" and
            words[-4][:6]   == "from=<"         and
            words[-3][:4]   == "to=<"           ):
            return Queue.addToFrom(words[5][:-1], words[-3][4:-1], words[-4][6:-1], words[14][:-1].split("\n")[0] )

        
        if (words[5]        == "NOQUEUE:"   and
            words[-4][:6]   == "from=<"     and
            words[-3][:4]   == "to=<"       ):

            loc = words[-3].find("@")
            if (loc == -1 ):
                To       = words[-3][4:-1]
                ToDomain = ""
            else:
                To       = words[-3][4:loc]
                ToDomain = words[-3][loc+1:-1]

            loc = words[-4].find("@")
            if (loc == -1 ):
                From       = words[-4][6:-1]
                FromDomain = ""
            else:
                From       = words[-4][6:loc]
                FromDomain = words[-4][loc+1:-1]
            NOQUEUE = [
                words[0],
                words[1],
                words[2].split(":")[0],
                To,
                ToDomain,
                From,
                FromDomain,
                " ".join(words[6:-4]),
                " - "
            ]   
            return logs.set(NOQUEUE, logs.TYPE_POSTFIX )
        return 1
