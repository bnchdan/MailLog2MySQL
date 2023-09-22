import os, sys, time
from ProcessLine    import ProcessLine
from Sql            import Sql
from Logs           import Logs
from AuthLog        import AuthLog
from DovecotLog     import DovecotLog
from PostfixLog     import PostfixLog
from Queue          import Queue
from Config         import Config
from Syslog         import Syslog


class ProcessLog:
    @staticmethod
    def main():
        Config.read()

        file = ProcessLog.openFile()
        inode   = os.fstat(file.fileno()).st_ino

        logs = Logs()
        
        AuthLog   .createTable()
        DovecotLog.createTable()
        PostfixLog.createTable()

        tik = time.time()
        i=0
        Syslog.write("started")
        while True:
            try:
                line = file.readline()
                line = line.split("\r")[0]
                
                if not line:
                    time.sleep(1)
                    if os.stat(Config.log_file).st_ino != inode:
                        Syslog.write("LOGROTATE")
                        file.close()
                        file = ProcessLog.openFile()
                        inode   = os.fstat(file.fileno()).st_ino

                else:
                    ProcessLine.main(line, logs) 
               
                tok = time.time()
                if ( (tok - tik) > 1 ):
                    tik=time.time()
                    Queue.preareToInsert(logs)
                    logs.insertToMySQL()
                    # print(logs.num_logs)

                if (Queue.NUM_LOGS > 4):    
                    Queue.preareToInsert(logs)

                if (logs.num_logs > 10 ):
                    logs.insertToMySQL()
                i=i+1
            except:
                pass
                
    
    @staticmethod
    def openFile():
        file=Config.log_file
        
        if ( not (os.path.exists(file) ) ):
            Syslog.write(f"File {file} not exists")
            raise Exception (f"File {file} not exists")

        f= open(file,"r")
        f.seek(0, os.SEEK_END)
        return f

