from serverPlayer import *
from serverCard import *
from serverToken import *
from serverChat import *
import random


class serverGame:
    def __init__(self, playerList):
        self.playerTurnOrder = []
        for player in playerList:
            self.playerTurnOrder.append(player)

        self.numberPlayers = len(playerList)
        self.guiltyCards = []
        assignTokens(self.playerTurnOrder)
        self.assignCards()
        self.chat = None

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
        serverCards = createDecks()
        self.guiltyCards = serverCards[0]
        dealCards(serverCards[1], self.playerTurnOrder)

    def changeTurn(self, player):
        if self.playerTurnOrder[0] is player:
            self.playerTurnOrder.remove(player)
            self.playerTurnOrder.append(player)
            player.sendClientAString("game.turn:success")

    def getGameChat(self):
        return self.chat

    def setGameChat(self, chatIn):
        self.chat = chatIn














