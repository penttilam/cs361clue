from serverPlayer import ServerPlayer
from serverCard import serverCards, createDecks, dealCards
from serverToken import ServerToken, assignTokens
from serverChat import ServerChat
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
        self.discards = []
        serverCards = createDecks()
        self.fullDeck = serverCards[2]
        self.suggestCards = None
        self.refuteCard = None


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

    def getFullDeck(self):
        return self.fullDeck 

    def changeTurn(self, player):
        if self.playerTurnOrder[0] is player:
            self.playerTurnOrder.remove(player)
            self.playerTurnOrder.append(player)
            while(self.playerTurnOrder[0].getWonLostGame() == False):
                self.changeTurn(self.playerTurnOrder[0])

    def setSuggestCards(self, suggestCards):
        self.suggestCards =suggestCards

    def getSuggestCards(self):
        return self.suggestCards

    def getRefuteCard(self):
        return self.refuteCard

    def setRefuteCard(self, refuteCard):
        self.refuteCard = refuteCard

    def getGameChat(self):
        return self.chat

    def setGameChat(self, chatIn):
        if len(self.chat) == 10:
            del(self.chat[0])
        self.chat.append(chatIn)

    def setDiscardedCards(self, player): 
        for card in player.getMyCards():
            self.discards.append(card)

    def getDiscardedCards(self): 
        return self.discards
        














