import time
from Logs       import Logs
from Messages   import Messages

class Queue:
    q={}
    AVAILABLE   = 5*60*60   #5 hour
    LIMIT       = 1000      #maximum number of objects in Queue
    NUM_LOGS    = 0

    def __init__ (self, id, timeout, mounth, day, hour):
        self.id         = id
        self.month      = month
        self.day        = day
        self.hour       = hour
        self.timeout    = timeout
        self.To         = []
        self.ToDomain   = []
        self.From       = None
        self.FromDomain = None
        self.Status     = []
        self.msgID      = "None"
        self.Subject    = None
        self.toInsert   = False
        Queue.NUM_LOGS = Queue.NUM_LOGS + 1



    def insertTo(self, To, Status):
        self.Status.append(Status)
        loc = To.find('@')
        if (loc == -1):
            self.To.append(To[:loc])
            self.ToDomain.append("")
            return
        
        self.To.append(To[:loc])
        self.ToDomain.append(To[loc+1:])
        


    def insertFrom(self, From):
        loc = From.find('@')
        if (loc == -1):
            self.From       = From
            self.FromDomain = ""
            return
        
        self.From       = From[:loc]
        self.FromDomain = From[loc+1:]



    def insertToFrom(self, To, From, Status):
        self.insertTo(To, Status)
        self.insertFrom(From)



    def insertMsgID(self, msgID):
        if (len(msgID)> 254 ):
            msgID=msgID[:254]
        self.msgID = msgID
        


    def toList(self):
        response = []
        for i in range(0, len(self.To) ):
            response.append([
                self.month, 
                self.day,
                self.hour,            
                self.To[i],
                self.ToDomain[i],         
                self.From,
                self.FromDomain,       
                self.Status[i],     
                self.msgID,     
                ])

        return response


    @staticmethod
    def add(id, month, day, hour):
        Queue.limit()
        if (id in Queue.q):
            return 0
        
        Queue.q[id] = Queue(
                id, 
                int ( time.mktime(time.localtime() ) ) +  Queue.AVAILABLE, 
                month, 
                day, 
                hour
            )
        return 0



    @staticmethod
    def removeOld():
        time =  int ( time.mktime(time.localtime() ) ) +  Queue.AVAILABLE
        for k in Queue.q:
            if ( Queue.q[k] < time ):
                del Queue.q[k]


    @staticmethod
    def remove(id):
        try:
            Queue.q[id].toInsert = True
        except:
            pass
        return 0


    @staticmethod
    def addFrom(id, From):
        try:
            Queue.q[id].insertFrom(From)
        except Exception as e:
            pass
        return 0


    @staticmethod
    def addTo(id, To, Status):
        try:
            Queue.q[id].insertTo(To, Status)
        except Exception as e:
            pass
        return 0



    @staticmethod
    def addToFrom(id, To, From, Status):
        try:
            Queue.q[id].insertToFrom(To, From, Status)
            Queue.remove(id)
        except Exception as e:
            #print(e)
            pass
        return 0



    @staticmethod 
    def addMsgID(id, msgID):
        if (id not in Queue.q):
            return 0

        if (len(msgID)> 254 ):
            msgID=msgID[:254]

        #add and check if msgid already exists with different queue id
        if (Messages.addID(msgID) == 0):
            del Queue.q[id]
            Queue.NUM_LOGS = Queue.NUM_LOGS - 1
            return 0

        try:
            Queue.q[id].insertMsgID(msgID)
        except Exception as e:
            pass
        
        return 0
  


    @staticmethod
    def print():
        print("-----------Queue----------")
        for id in Queue.q:
            print(Queue.q[id].id)
            print(Queue.q[id].From)
            print(Queue.q[id].FromDomain)
            print(Queue.q[id].To)
            print(Queue.q[id].ToDomain)
            print(Queue.q[id].Status)
            print(Queue.q[id].msgID)
            print(Queue.q[id].timeout)
            print(Queue.q[id].toInsert)
        print("-------------------------")



    @staticmethod
    def preareToInsert(logs):
        toDelete = []
        currentTime = time.time()
        # print(" Queue size: "+str(Queue.NUM_LOGS))
        for id in Queue.q:
            if (currentTime - Queue.q[id].timeout > 0 ):
                #if expired, insert with status unknown         
                Queue.q[id].Status  = "unknown"
                Queue.q[id].toInsert= True 

            if ( Queue.q[id].toInsert != True ):
                continue

            for data in Queue.q[id].toList():
                logs.set(data, logs.TYPE_POSTFIX )

            toDelete.append(id)


        #delete from queue
        for id in toDelete:
            Messages.delete(Queue.q[id].msgID)
            del Queue.q[id]
            Queue.NUM_LOGS = Queue.NUM_LOGS - 1
         
        


    @staticmethod
    def limit():
        if ( Queue.NUM_LOGS > Queue.LIMIT ):            
            try:
                # remove first 10 elements, if queue is to large
                #print( Queue.NUM_LOGS)
                #print( Queue.LIMIT)
                for i in range(1,10) :
                    id = next(iter(Queue.q))
                    Queue.q[id].Status  = "unknown"
                    Queue.q[id].toInsert= True
                    # Queue.q.pop(next(iter(Queue.q)))

                Queue.preareToInsert()

            except Exception as e:
                pass
            return 1

        return 0


