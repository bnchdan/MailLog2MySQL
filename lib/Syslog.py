import syslog

class Syslog:

    @staticmethod
    def write(msg):
        syslog.syslog(msg)