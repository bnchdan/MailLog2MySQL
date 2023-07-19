
class Messages:
    ids=[]


    @staticmethod
    def addID(id):
        if (Messages.exist(id) == 1 ):
            return 0
        Messages.ids.append(id)
        return 1


    @staticmethod
    def exist(id):
        if (id in Messages.ids):
            return 1
        return 0


    @staticmethod
    def delete(id):
        if (id not in Messages.ids):
            return
        
        Messages.ids.remove(id)
