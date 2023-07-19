import os

f = open("/var/log/mailogtest")


i = 0 
while (True):
    line = f.readline()
    if (not line) :
        break

    cmd = "echo '"+line.split("\n")[0]+"' >> /var/log/mail.log"
    # print(cmd)

    os.system(cmd)

#    i=i+1


 #   if ( i == 5000 ):
 #       break



