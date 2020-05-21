##
## This class is the Player in the Server. It represents their connection and their information
##

import sys

from serverConnection import *
from clientPlayer import ClientPlayer

class ServerPlayer():
    def __init__(self, playerConnection):
        self.playerConnection = playerConnection
        self.ready = False
        self.myCards = []
        self.myToken = ("", 0, 0)
        self.myTurn = False
        self.lostGame = False

    def setReady(self, ready):
        self.ready = ready

    def getReady(self):
        return self.ready

    def setHand(self, handList):
        self.myCards = handList

    def getMyCards(self):
        return self.myCards

    def setMyTurn(self, turn):
        self.myTurn = turn 

    def getMyTurn(self):
        return self.myTurn

    def setLostGame(self):
        self.lostGame = True

    def getLostGame(self):
        return self.lostGame

    def getMyToken(self):
        return self.myToken

    def setMyToken(self, newToken):
        self.myToken = newToken


     ##private playerConnection functions
    def sendClientAString(self, serverString):
        self.playerConnection.sendClientAString(serverString)

    def sendClientAObject(self, serverObject):
        print("here" + str(serverObject))
        self.playerConnection.sendClientAObject(serverObject)

    def getClientMessage(self):
        return self.playerConnection.getClientMessage()

    def getConnectionId(self):
        return self.playerConnection.getId()

    def closeConnection(self):
        self.playerConnection.closeConnection()

        


