from serverPlayer import *
from serverCard import *
from serverToken import *
import random


class serverGame:
    def __init__(self, playerList):
        print("do we make it here")
        self.playerTurnOrder = playerList
        self.numberPlayers = len(playerList)
        self.guiltyCards = []
        print("if we made it there we'll make it here")
        print(self.playerTurnOrder)
        assignTokens(self.playerTurnOrder)
        print("but can we make it here?")
        self.assignCards()
        print("with Jesus we can")

    def getPlayerTurnOrder(self):
        return self.playerTurnOrder

    def getNumberPlayers(self):
        return self.numberPlayers

    def getGuiltyCards(self):
        return self.guiltyCards

    def getTokens(self):
        tokenList = []
        for player in self.playerTurnOrder:
            tokenList.append(player.getToken())
        return tokenList

    def rollDie():
        return random.randint(1,6)


    def assignCards(self):
        print("b4 create")
        serverCards = createDecks()
        print("after create")
        self.guiltyCards = serverCards[0]
        print("guilty?")
        dealCards(serverCards[1], self.playerTurnOrder)
        print("after deal")


















