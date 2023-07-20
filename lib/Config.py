import os
from Syslog     import Syslog

class Config:
    mysql = {
        "host"     : None,
        "user"     : None,
        "password" : None,
        "database" : None,
        "port"     : None
    }
    log_file = None


    @staticmethod
    def read():
        file="/etc/MailLog2MySQL.conf"
        
        if ( not (os.path.exists(file) ) ):
            Syslog.write(f"File {file} not exists")
            raise Exception (f"File {file} not exists")

        conf = open(file, "r")

        while (True):
            line = conf.readline()

            if (not line):
                break
            
            line= line.split("\n")[0]
            line=line.replace(" ", "")
            splitted = line.split("=")

            # if (len(splitted) != 2 and line !=""):
            #     Syslog.write(f"error at {line} ")
            #     raise Exception (f"error at {line} ")

            if ( splitted[0] in Config.mysql ):
                Config.mysql[splitted[0]] = splitted[1]
                continue

            if ( splitted[0] == "log_file"):
                Config.log_file = splitted[1]

        return 1
        
        



