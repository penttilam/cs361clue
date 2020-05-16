import sys
import pickle

class Connection():
    def __init__(self, connectionId, conn):
        self.id = connectionId     ## this is the player ID stored as a string
        self.conn = conn       ## this is the player's conn object
        self.conn.send(pickle.dumps(str(self.id) + ":connected"))


    def sendClientAString(self, message):
        self.conn.send(pickle.dumps(str(self.id) + ":" + str(message)))
        print("    Sent  --  " + str(self.id) + ":" + str(message))

    def sendClientAObject(self, clientObject):
        print("maybe here? " + str(clientObject))
        self.conn.send(pickle.dumps(clientObject))
        print("    Sent -- " + str(self.id) + ".object:" + str(type(clientObject)))

    def getClientMessage(self):
        return pickle.loads(self.conn.recv(2048))

    def getId(self):
        return self.id

    def closeConnection(self):
        self.conn.close()
