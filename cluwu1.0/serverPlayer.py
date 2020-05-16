##
## This class is the Player in the Server. It represents their connection and their information
##

import sys

from serverConnection import *
from clientPlayer import ClientPlayer

class ServerPlayer():
    def __init__(self, playerConnection):
        self.playerConnection = playerConnection

        ##Lobby Variables
        self.ready = False

        ##Game Variables
        self.myCards = []
        self.gameCharacter = " "
        self.myTurn = False
        self.lostGame = False

    ##Lobby Functions
    def setReady(self, ready):
        self.ready = ready

    def getReady(self):
        return self.ready

    ##Game Functions
    def addCard(self, newCard):
        self.myCards.append(newCard) 

    def getMyCards(self):
        return self.myCards

    def setMyCharacter(self, char):
        self.gameCharacter = char

    def getMyCharacter(self):
        return self.gameCharacter

    def setMyTurn(self, turn):
        self.myTurn = turn 

    def getMyTurn(self):
        return self.myTurn

    def setLostGame(self):
        self.lostGame = True

    def getLostGame(self):
        return self.lostGame


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

        


