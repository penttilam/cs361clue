from serverPlayer import *
from serverCard import *
from serverToken import *
from serverChat import *
import random


class ServerGame:
    def __init__(self, playerList):
        self.playerTurnOrder = []
        for player in playerList:
            self.playerTurnOrder.append(player)

        self.numberPlayers = len(playerList)
        self.guiltyCards = []
        assignTokens(self.playerTurnOrder)
        self.assignCards()
        self.chat = []

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

    def assignCards(self):
        serverCards = createDecks()
        self.guiltyCards = serverCards[0]
        dealCards(serverCards[1], self.playerTurnOrder)

    def changeTurn(self, player):
        if self.playerTurnOrder[0] is player:
            self.playerTurnOrder.remove(player)
            self.playerTurnOrder.append(player)

    def getGameChat(self):
        return self.chat

    def setGameChat(self, chatIn):
        if len(self.chat) == 10:
            del(self.chat[0])
        self.chat.append(chatIn) 














